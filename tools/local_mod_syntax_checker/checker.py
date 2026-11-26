#!/usr/bin/env python3
"""Darkest Dungeon Mod 的只读、可供 Agent 调用的本地静态检查器。"""
from __future__ import annotations
import argparse, json, math, os, re, sys, xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

KB = Path(__file__).resolve().parents[2]
INFO_SCHEMA = KB / "tools" / "info_schema_data.json"
RAG = KB / "RAG"

@dataclass
class Diagnostic:
    file: str; line: int; column: int; severity: str; code: str; message: str; source: str

class Checker:
    def __init__(self, root: Path, refs: list[Path], strict: bool = False, default_game: Path | None = None):
        self.root=root.resolve()
        # 游戏本体、DLC 和依赖 Mod 只来自本次显式传入的 reference-root。
        self.default_game=(default_game.resolve() if default_game else None)
        self.explicit_ref_roots=[]
        for candidate in (p.resolve() for p in refs):
            if candidate.is_dir() and candidate != self.root and candidate not in self.explicit_ref_roots:
                self.explicit_ref_roots.append(candidate)
        if self.default_game is None:
            for candidate in self.explicit_ref_roots:
                if candidate.name.lower()=="darkestdungeon":
                    self.default_game=candidate
                    break
        self.ref_roots=[]
        for candidate in [self.default_game,*self.explicit_ref_roots]:
            if candidate and candidate.is_dir() and candidate != self.root and candidate not in self.ref_roots:
                self.ref_roots.append(candidate)
        self.strict=strict; self.diagnostics=[]
        self.effect_ids=set(); self.mode_ids=set(); self.buff_ids=set(); self.colour_ids=set(); self.trinket_ids=set(); self.rarity_ids=set()
        self.schema=json.loads(INFO_SCHEMA.read_text(encoding="utf-8"))
        self.headers=set(self.schema["plugin"]["headers"]); self.contexts=self.schema["plugin"]["contexts"]
        self.values=self.schema["plugin"]["resolved_keyword_values"]
        effect_records=[json.loads(x) for x in (RAG/"effect_keywords.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        self.effect_keywords={d["keyword"] for d in effect_records}
        self.effect_values={d["keyword"]:set(d.get("allowed_values") or d.get("accepted_values") or []) for d in effect_records}
        self.effect_numeric_bool={d["keyword"] for d in effect_records if d.get("argument_kind")=="numeric_boolean"}
        self.effect_string_bool={d["keyword"] for d in effect_records if d.get("argument_kind")=="boolean_string"}
        self.buff_subtypes={}
        self.buff_required_subtypes=set()
        self.buff_free_subtypes={'upgrade_discount','riposte','quirk_tag_evolution_duration'}
        self._load_vsix_effect_rules()
        self.update_rules=json.loads(Path(__file__).with_name("update_rules.json").read_text(encoding="utf-8"))
        for header,fields in self.update_rules["info_boolean_fields"].items():
            self.contexts[header]=list(dict.fromkeys([*self.contexts.get(header,[]),*fields]))
            for field in fields:self.values[f"{header}|{field}"]=["true","false"]
        self.effect_keywords.update(self.update_rules["effect_arguments"])
        self.effect_values.setdefault(".target",set()).update(self.update_rules["effect_targets"])
        for field in self.update_rules["effect_arguments"]:
            self.effect_values.pop(field,None)
            self.effect_numeric_bool.discard(field)
            self.effect_string_bool.discard(field)
        buff_source=Path(__file__).parent/"vendor"/"BuffGrammarChecker.Core"
        self.buff_fields=dict(re.findall(r'\["([^"]+)"\]\s*=\s*ExpectedValueType\.(\w+)',
            (buff_source/"BuffFileValidator.cs").read_text(encoding="utf-8-sig").split("RequiredBuffFields")[0]))
        rule_source=(buff_source/"BuffRuleTypeRules.cs").read_text(encoding="utf-8-sig")
        self.buff_rules=set(re.findall(r'"([^"]+)"',rule_source.split("AllowedValues",1)[1].split("];",1)[0]))
        self.files=list(self.walk(self.root))
        self.ref_files=[]
        for ref_root in self.ref_roots:
            for file_path in self.walk(ref_root):
                # 默认游戏根只贡献本体/DLC；游戏安装目录下的 Workshop Mod
                # 必须通过 --reference-root <具体Mod目录> 显式加入。
                if self.default_game and ref_root == self.default_game and self._is_default_game_workshop_file(file_path) and not self._is_explicit_reference_file(file_path):
                    continue
                self.ref_files.append(file_path)
    def _load_vsix_effect_rules(self):
        """从 VSIX 的 DarkestData.cs 补齐固定 Effect 值域，避免 RAG 与插件数据漂移。"""
        source=KB / "tools" / "local_mod_syntax_checker" / "vendor" / "vsix" / "DarkestData.cs"
        if not source.is_file(): return
        try:text=source.read_text(encoding="utf-8-sig")
        except OSError:return
        lists={}
        for m in re.finditer(r'public static readonly (?:List<string>|HashSet<string>)\s+(\w+)\s*=.*?\{(.*?)\};',text,re.S):
            lists[m.group(1)]=set(re.findall(r'"([^"]+)"',m.group(2)))
        lists["StealBuffStatTypeValues"]=lists.get("BuffTypeValues",set())-{
            "effect_chance","crit_dmg_multiply","crit_dmg_add","heal_crit_chance_add",
            "heal_crit_chance_multiply","hp_heal_amount_received","disable_combat_skill"
        }
        block_match=re.search(r'KeywordToValuesMap\s*=\s*new Dictionary<string, List<string>>\s*\{(.*?)\n\s*\};',text,re.S)
        if not block_match:return
        for key,name in re.findall(r'\{\s*"([^"]+)"\s*,\s*(\w+)\s*\}',block_match.group(1)):
            if name in lists:
                self.effect_values.setdefault(key,set()).update(lists[name])
                if name=="NumBoolValues":self.effect_numeric_bool.add(key)
                if name=="StrBoolValues":self.effect_string_bool.add(key)
        map_match=re.search(r'BuffTypeToSubTypesMap\s*=.*?\{(.*?)\n\s*\};',text,re.S)
        if map_match:
            for bm in re.finditer(r'\{\s*"([^"]+)"\s*,\s*new HashSet<string>\s*\{(.*?)\}\s*\}',map_match.group(1),re.S):
                self.buff_subtypes[bm.group(1)]=set(re.findall(r'"([^"]+)"',bm.group(2)))
        required_match=re.search(r'MustHaveSubBuffTypes\s*=.*?\{(.*?)\};',text,re.S)
        if required_match:self.buff_required_subtypes.update(re.findall(r'"([^"]+)"',required_match.group(1)))
        self.buff_free_subtypes.update(lists.get("SubFreeBuffTypes",set()))
        # 插件允许的双布尔关键字同时接受 0/1 与 true/false。
        double_match=re.search(r'DoubleBoolKeywords\s*=.*?\{(.*?)\};',text,re.S)
        if double_match:
            doubles=re.findall(r'"([^"]+)"',double_match.group(1))
            self.effect_numeric_bool.update(doubles)
            for key in doubles:self.effect_values.setdefault(key,set()).update({"0","1","true","false","True","False","TRUE","FALSE"})
        for key in list(self.effect_string_bool):
            self.effect_values.setdefault(key,set()).update({"true","false","True","False","TRUE","FALSE"})
    def rel(self,p:Path)->str:
        try:return p.relative_to(self.root).as_posix()
        except ValueError:return str(p)
    def add(self,p,line,col,severity,code,msg,source): self.diagnostics.append(Diagnostic(self.rel(p),max(1,line),max(1,col),severity,code,msg,source))
    def read(self,p:Path, check=True):
        try:
            b=p.read_bytes()
            if check and b.startswith(b"\xef\xbb\xbf") and p.suffix.lower() in {".json",".darkest",".xml"}: self.add(p,1,1,"error","KB-ENC-UTF8-BOM","配置文件必须使用 UTF-8 无 BOM。","Mechanics/42-JSON与Darkest文件的UTF-8无BOM硬性要求.md")
            return b.decode("utf-8-sig" if b.startswith(b"\xef\xbb\xbf") else "utf-8")
        except UnicodeDecodeError as e:
            if check:self.add(p,1,1,"error","KB-ENC-NOT-UTF8",f"文件不是有效 UTF-8：{e}","Mechanics/42-JSON与Darkest文件的UTF-8无BOM硬性要求.md")
            return None
        except OSError as e:
            if check:self.add(p,1,1,"error","IO-READ",str(e),"本地读取")
            return None
    @staticmethod
    def walk(root:Path):
        skipped_directories = {"bin", "obj", "node_modules", "__pycache__"}
        if root.name.startswith("."):
            return
        for directory, subdirectories, files in os.walk(root):
            subdirectories[:] = [name for name in subdirectories
                                 if not name.startswith(".") and name not in skipped_directories]
            for name in files:
                if not name.startswith("."):
                    path = Path(directory) / name
                    if path.is_file():
                        yield path
    @staticmethod
    def lines(text):
        return text.replace("\r\n","\n").replace("\r","\n").splitlines()
    @staticmethod
    def args(s):
        return [m.group(2) if m.group(2) is not None else m.group(1) for m in re.finditer(r'"([^"]*)"|(\S+)',s)]
    @staticmethod
    def _content_parts(parts, preserve_case=False):
        """剥离原版 DLC 的真实包装层，保留功能目录层级。"""
        parts=list(parts) if preserve_case else [x.lower() for x in parts]
        if len(parts)>=2 and parts[0].lower()=="dlc": parts=parts[2:]
        changed=True
        while changed:
            changed=False
            for marker in ("features","modes"):
                if len(parts)>=2 and parts[0].lower()==marker:
                    parts=parts[2:]; changed=True; break
        return parts
    @staticmethod
    def _under_root(p,root):
        try: p.resolve().relative_to(root.resolve()); return True
        except ValueError: return False
    def _is_explicit_reference_file(self,p):
        return any(self._under_root(p, root) for root in self.explicit_ref_roots)
    def _is_default_game_workshop_file(self,p):
        """默认游戏索引只包含本体/DLC，不隐式加载安装目录下的其他 Mod。"""
        try:
            if not self.default_game: return False
            rel=p.resolve().relative_to(self.default_game)
        except ValueError:
            return False
        return len(rel.parts)>=2 and rel.parts[0].lower()=="mods"
    def _path_parts(self,p):
        """以 Mod 或参考根为基准；显式 reference-root 可指定任意依赖 Mod。"""
        roots=[self.root,*self.ref_roots]
        matches=[]
        for root in roots:
            try: matches.append((len(root.parts),root,list(p.relative_to(root).parts)))
            except ValueError: pass
        if not matches: return list(p.parts)
        _,root,parts=max(matches,key=lambda x:x[0])
        # 如果文件属于显式引用的子 Mod，优先使用该 Mod 根的相对路径，
        # 不把游戏安装树的 mods/<id> 包装带入功能目录判断。
        for explicit in self.explicit_ref_roots:
            try:
                parts=list(p.relative_to(explicit).parts)
                break
            except ValueError:
                continue
        return parts
    def path_kind(self,p:Path):
        """按原版及官方 DLC 的功能路径判断文件是否位于可扫描位置。"""
        name=p.name.lower()
        if self.default_game and self._is_default_game_workshop_file(p) and not self._is_explicit_reference_file(p): return None, False
        parts=self._content_parts(self._path_parts(p)); parent=p.parent.name.lower()
        if name.endswith(".effects.darkest"): return "effects", len(parts)>=2 and parts[-2]=="effects"
        if name.endswith((".entries.trinkets.json",".rarities.trinkets.json")): return "trinket", len(parts)>=2 and parts[-2]=="trinkets"
        if name.endswith(".buffs.json"): return "buff", len(parts)>=3 and parts[-3:-1]==["shared","buffs"]
        if name.endswith(".string_table.xml"): return "localization", len(parts)>=2 and parts[-2]=="localization"
        if name.endswith(".colours.darkest"): return "colours", len(parts)>=2 and parts[-2]=="colours"
        if name.endswith((".info.darkest",".art.darkest",".override.darkest")):
            if "heroes" in parts:
                i=parts.index("heroes")
                return "info", len(parts)==i+3
            if "monsters" in parts:
                i=parts.index("monsters")
                return "info", len(parts)==i+4
            return "info", False
        return None,True
    def unreadable_path_info(self,p,kind):
        self.add(p,1,1,"info","KB-FILE-UNREADABLE-PATH",f"该 {kind} 文件不位于游戏可扫描的标准目录，因此不会被游戏读取；已跳过内容检查。","Mechanics/24-Mod识别与职业Mod目录结构.md; anchor:path-layout")
    def run(self):
        self.index()
        for p in self.files:
            n=p.name.lower(); kind,loadable=self.path_kind(p)
            if kind=="info" and "monsters" in [part.lower() for part in self._content_parts(self._path_parts(p))] and n.endswith((".info.darkest", ".art.darkest")):
                self.monster_path(p)
            if kind is not None and not loadable:
                self.unreadable_path_info(p,kind); continue
            if n.endswith(".json"):
                domains=self.update_rules["partial_domains"]
                parts=self._content_parts(self._path_parts(p))
                for domain,message in domains.items():
                    if domain in parts:
                        self.add(p,1,1,"info","KB-COVERAGE-PARTIAL",message,"tools/local_mod_syntax_checker/update_rules.json")
                        self.update_json(p,domain)
                        break
            if n.endswith(".string_table.xml"): self.localization(p)
            elif n.endswith((".info.darkest",".art.darkest",".override.darkest")): self.info(p)
            elif n.endswith(".effects.darkest"): self.effects(p)
            elif n.endswith((".entries.trinkets.json",".rarities.trinkets.json")): self.trinkets(p)
            elif n.endswith(".buffs.json") or (n.endswith(".json") and "shared" in p.parts and "buffs" in p.parts): self.buffs(p)
            elif n=="project.xml": self.project(p)
            if p.suffix.lower() in {".json",".darkest"} and n not in {"project.xml"}: self.encoding_semantics(p)
        return sorted(self.diagnostics,key=lambda x:(x.file,x.line,x.column,x.severity,x.code))
    def index(self):
        for p in self.files+self.ref_files:
            n=p.name.lower()
            kind,loadable=self.path_kind(p)
            if kind is None or not loadable: continue
            if not n.endswith((".effects.darkest",".info.darkest",".colours.darkest",".entries.trinkets.json",".rarities.trinkets.json",".buffs.json")):continue
            text=self.read(p,False)
            if text is None: continue
            if n.endswith(".effects.darkest"):
                for m in re.finditer(r'\.name\s+(?:"([^"]+)"|(\S+))',text): self.effect_ids.add(m.group(1) or m.group(2))
            elif n.endswith(".info.darkest"):
                current=None
                for line in self.lines(text):
                    h=re.match(r'^\s*([\w]+:)',line)
                    if h: current=h.group(1)
                    if current=="mode:":
                        m=re.search(r'\.id\s+(?:"([^"]+)"|(\S+))',line)
                        if m:self.mode_ids.add(m.group(1) or m.group(2))
            elif n.endswith(".colours.darkest") and "/colours/" in p.as_posix().lower():
                for m in re.finditer(r'\.id\s+(?:"([^"]+)"|(\S+))',text): self.colour_ids.add(m.group(1) or m.group(2))
            elif n.endswith(".entries.trinkets.json"):
                try:
                    d=json.loads(text)
                    for e in d.get("entries",[]):
                        if isinstance(e,dict) and isinstance(e.get("id"),str): self.trinket_ids.add(e["id"])
                except Exception: pass
            elif n.endswith(".rarities.trinkets.json"):
                try:
                    d=json.loads(text)
                    for e in d.get("rarities",[]):
                        if isinstance(e,dict) and isinstance(e.get("id"),str): self.rarity_ids.add(e["id"])
                except Exception: pass
            elif n.endswith(".buffs.json"):
                try:
                    d=json.loads(text)
                    for b in d.get("buffs",[]):
                        if isinstance(b,dict) and isinstance(b.get("id"),str):self.buff_ids.add(b["id"])
                except Exception: pass
    def encoding_semantics(self,p):
        text=self.read(p,False)
        if text is None:return
        if p.name.lower().endswith(".info.darkest"):
            for i,line in enumerate(self.lines(text),1):
                code=line.split("//",1)[0]
                if len(code)>=511:self.add(p,i,511,"error","KB-INFO-LINE-OVERFLOW","Info 非注释行达到 511 字符，可能发生引擎截断。","Info/README.md")
    def refs(self,p,ids,kind,line,col,context):
        for x in ids:
            if x in (self.effect_ids if kind=="effect" else self.mode_ids if kind=="mode" else self.buff_ids):continue
            # 本体/DLC及显式依赖目录均未找到时，属于无法解析的空引用，按错误报告。
            sev="error"; code=f"KB-REF-{kind.upper()}-NOT-FOUND"
            self.add(p,line,col,sev,code,f"{context} 引用的 ID '{x}' 未在扫描范围找到定义；外部依赖请追加 --reference-root。","当前用户明确要求的本地引用检查")
    def _lexical(self,p,i,code,kind):
        source="VSIX/Error/EffectErrorTagger.cs" if kind=="effect" else "VSIX/Error/InfoBaseErrorTagger.cs"
        if "//" in self.lines(self.read(p,False) or "")[i-1] and code.strip():
            self.add(p,i,self.lines(self.read(p,False) or "")[i-1].find("//")+1,"warning" if kind=="effect" else "error",
                     "VSIX-%s-INLINE-COMMENT" % kind.upper(),"请避免行内注释，以防游戏识别错误。",source)
        if code.count('"')%2:
            self.add(p,i,max(1,code.rfind('"')+1),"error","VSIX-%s-UNPAIRED-QUOTE"%kind.upper(),"单行内引号不成对。",source)
        # 插件在代码区禁止中文字符和中文标点。
        if re.search(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff01-\uff65]',code):
            self.add(p,i,1,"error","VSIX-%s-NON-ASCII-CJK"%kind.upper(),"代码区不允许中文字符或中文标点。",source)
        in_quote=False
        for q in re.finditer(r'"',code):
            before=code[q.start()-1] if q.start() else " "
            if not in_quote:
                if before and not before.isspace():
                    self.add(p,i,q.start()+1,"error","VSIX-%s-QUOTE-LEFT-ADJACENT"%kind.upper(),"引号前紧贴普通字符，请使用空格分隔。",source)
                in_quote=True
            else:
                nxt=code[q.end():]
                if nxt and not nxt[0].isspace():
                    self.add(p,i,q.start()+1,"warning" if nxt[0]=='.' else "error","VSIX-%s-QUOTE-RIGHT-ADJACENT"%kind.upper(),"引号后应使用空格分隔。",source)
                in_quote=False
    def _info_argument_checks(self,p,i,header,kw,args,col):
        """移植 InfoBaseErrorTagger 的参数检查，保留告警级别的例外。"""
        if not args:return
        source="VSIX/Error/InfoBaseErrorTagger.cs"
        def report(level,code,message):
            self.add(p,i,col,level,code,message,source)
        skills={"skill:","riposte_skill:","combat_skill:","combat_move_skill:"}
        key=f"{header}|{kw}"
        if kw in self.update_rules["info_boolean_fields"].get(header,[]):
            if len(args)!=1 or args[0].lower() not in {"true","false"}:
                report("error","KB-UPDATE-INFO-ARGUMENT",f"{kw} 必须有且只有一个 true/false 参数。")
            return
        rule=self.schema["plugin"].get("string_argument_rules",{}).get(key)
        maxargs=self.schema["plugin"].get("max_argument_count_rules",{}).get(key)
        mode_name=(header=="mode:" and kw==".id") or (header in skills and kw==".valid_modes")
        if rule is None and header in skills and kw.endswith("_effects"):
            rule={"max_args":6,"max_length":64}
        if rule:
            limit=rule["max_args"]
            if len(args)>limit:
                level="warning" if kw in {".damage_heal_base_class_ids",".incompatible_class_ids"} else "error"
                code="VSIX-INFO-SINGLE-ARG-COUNT" if limit==1 else "VSIX-INFO-TOO-MANY-ARGS"
                report(level,code,f"{kw} 参数数量超过 {limit}。")
            if header=="spawn:" and kw==".effects" and len(args)>limit//2:
                report("warning","VSIX-INFO-SPAWN-EFFECTS-LONG",f"spawn: .effects 参数数量不建议超过 {limit//2}。")
            for value in (args[:1] if limit==1 else args):
                # VSIX 使用 .NET UTF-16 长度并排除空白，而非 UTF-8 字节数。
                size=len(''.join(ch for ch in value if not ch.isspace()).encode("utf-16-le",errors="surrogatepass"))//2
                if mode_name:
                    if size>64:report("error","VSIX-INFO-STRING-TOO-LONG",f"{kw} 模式名超过 64 个字符。")
                    elif size>32:report("warning","VSIX-INFO-STRING-LONG",f"{kw} 模式名超过 32 个字符，建议缩短。")
                elif size>rule["max_length"]:
                    report("error","VSIX-INFO-STRING-TOO-LONG",f"{kw} 参数长度超过 {rule['max_length']}。")
                elif size==rule["max_length"]:
                    report("warning","VSIX-INFO-STRING-AT-LIMIT",f"{kw} 参数长度已达到 {rule['max_length']}。")
        if maxargs is not None and len(args)>maxargs:
            report("error","VSIX-INFO-TOO-MANY-ARGS",f"{kw} 参数数量不能超过 {maxargs}。")
        allowed=self.values.get(key)
        if allowed is None:return
        boolean=set(allowed)=={"true","false"}
        special=kw in {".disabled_popup_text_types",".disabled_act_out_combat_start_turn_types"}
        if special:
            limit=len(allowed) if kw==".disabled_popup_text_types" else 4
            if len(args)>limit:report("error","VSIX-INFO-TOO-MANY-ARGS",f"{kw} 参数数量不能超过 {limit}。")
        if boolean and len(args)>1:
            report("error","VSIX-INFO-BOOLEAN-MULTI-ARG","布尔型关键字不应填写多个参数。")
        seen=set()
        for value in args:
            if any(ch.isspace() for ch in value):
                report("error","VSIX-INFO-ARG-WHITESPACE",f"{kw} 参数 '{value}' 不能包含空白。")
                continue
            valid=value in ({"true","false","True","False","TRUE","FALSE"} if boolean else set(allowed))
            if not valid:
                if header in skills and kw==".type":
                    report("info","VSIX-INFO-CUSTOM-SKILL-TYPE","自定义技能类型可能无法享受近战/远程增益或触发相关 Trigger。")
                else:report("error","VSIX-INFO-INVALID-VALUE",f"参数 '{value}' 对关键字 '{kw}' 无效。")
            elif special:
                if value in seen:report("error","VSIX-INFO-DUPLICATE-ARG",f"{kw} 出现重复参数 '{value}'。")
                seen.add(value)
    def _effect_block_checks(self,p,block):
        """按实际关键字检查同一 Effect，同行规则不扩展到整个块。"""
        source="VSIX/Error/EffectErrorTagger.cs"
        fields=[]
        for line,text,col in block:
            for token in self._keywords(text):
                fields.append((token.group(),self._keyword_args(text,token),line,token.start()+1,text,token))
        def first(key):
            row=next((r for r in fields if r[0]==key),None)
            return row[1][0] if row and row[1] else None
        def report(row,level,code,message):
            self.add(p,row[2],row[3],level,code,message,source)
        names={r[0] for r in fields}
        if ".name" not in names:
            self.add(p,block[0][0],1,"error","KB-EFFECT-MISSING-NAME","每条 Effect 定义必须包含 .name。","Effect/keyword/Effect.name.md")
        targets=[r[1][0] for r in fields if r[0]==".target" and r[1]]
        forbidden=any(t in {"target","target_enemy_group"} for t in targets)
        other=any(t not in {"target","target_enemy_group"} for t in targets)
        dots={".dotBleed",".dotPoison",".dotStress",".dotHpHeal",".dotShuffle",".dotBurn"}
        for line,text,col in block:
            seen=set()
            for row in (r for r in fields if r[2]==line and r[0] in dots):
                if seen-{row[0]}:report(row,"error","VSIX-EFFECT-DOT-CONFLICT","同行 Effect 存在互斥 DOT/延迟扰乱关键字。")
                seen.add(row[0])
        for row in fields:
            kw,args,line,col,text,token=row
            if kw==".name":
                if not args or not args[0]:
                    self.add(p,line,col,"error","KB-EFFECT-EMPTY-NAME",".name 必须非空。","Effect/keyword/Effect.name.md")
                else:
                    if len(args)>1 and not text[token.end():].lstrip().startswith('"'):
                        report(row,"error","VSIX-EFFECT-NAME-WHITESPACE",".name 无引号时不能含空白。")
                    else:
                        length=len(''.join(c for c in args[0] if not c.isspace()).encode('utf-16-le'))//2
                        if length>64:report(row,"error","VSIX-EFFECT-NAME-TOO-LONG",".name 名称超过 64 字符。")
                        elif length==64:report(row,"warning","VSIX-EFFECT-NAME-AT-LIMIT",".name 名称达到 64 字符，建议缩短。")
            elif kw==".use_item_id" and ".use_item_type" not in names:
                report(row,"error","VSIX-EFFECT-USE-ITEM-TYPE-REQUIRED",".use_item_id 要求同一 Effect 存在 .use_item_type。")
            elif kw in {".keyStatus",".monsterType"} and forbidden:
                report(row,"error","VSIX-EFFECT-UNSAFE-TARGET","该效果不能使用 target/target_enemy_group。")
            elif kw==".skill_instant" and args and args[0]=="true" and not other:
                report(row,"error","VSIX-EFFECT-UNSAFE-TARGET","skill_instant true 需要非 target/target_enemy_group 目标。")
            elif kw==".spawn_target_actor_base_class_id":
                if any(r[0]==".target" and r[2]==line and r[3]<col for r in fields):
                    report(row,"error","VSIX-EFFECT-SPAWN-TARGET-ORDER","spawn 定向必须写在同行 .target 前。")
            elif kw in {".guard",".clearguarded",".clearguarding"} and args and args[0]=="1" and ".force_resist_type" not in names:
                active=any((first(k) or '').lower()=='true' for k in ('.on_hit','.on_miss'))
                for chance in (r[1][0] for r in fields if r[0]=='.chance' and r[1]):
                    try:below=float(chance[:-1])<100 if chance.endswith('%') else float(chance)<1
                    except ValueError:continue
                    if active and below:
                        report(row,"warning","VSIX-EFFECT-GUARD-CHANCE","守护及移除守护不能被 .chance 制约。")
                        break
            elif kw==".buff_type" and first('.buff_type') is not None:
                bt=first('.buff_type');bs=first('.buff_sub_type')
                if first('.buff_amount') is None:report(row,"error","VSIX-EFFECT-BUFF-AMOUNT-REQUIRED","简写 Buff 必须有数值。")
                if bt in self.buff_required_subtypes:
                    if bs is None or (bt in self.buff_free_subtypes and not bs.strip()):report(row,"error","VSIX-EFFECT-BUFF-SUBTYPE-REQUIRED",f"{bt} 必须声明非空 buff_sub_type。")
                elif bt in self.buff_subtypes:
                    if bs is not None and bs not in self.buff_subtypes[bt]:report(row,"error","VSIX-EFFECT-BUFF-SUBTYPE-INVALID",f"{bs} 不属于 {bt}。")
                elif bt not in self.buff_free_subtypes and bs is not None:
                    report(row,"error","VSIX-EFFECT-BUFF-SUBTYPE-UNEXPECTED",f"{bt} 没有 buff_sub_type。")
            elif kw=='.daze':report(row,"info","VSIX-EFFECT-DAZE-SUGGESTION","谨慎使用 daze，注意崩溃或无效风险。")
            elif kw=='.affliction_blockable_chance':report(row,"info","VSIX-EFFECT-AFFLICTION-CHANCE","不建议使用 affliction_blockable_chance。")
    def info(self,p):
        text=self.read(p); 
        if text is None:return
        current=None; mode_ids=[]
        source_lines=self.lines(text)
        for i,raw in enumerate(source_lines,1):
            code=raw.split("//",1)[0]
            self._lexical(p,i,code,"info")
            h=re.match(r'^\s*([\w]+:)',code)
            if h:
                current=h.group(1)
                if current not in self.headers:self.add(p,i,1,"error","VSIX-INFO-UNKNOWN-HEADER",f"未知 Header：{current}","VSIX/Error/InfoBaseErrorTagger.cs");continue
            if not code.strip():continue
            for m in self._keywords(code):
                kw=m.group(); before=code[:m.start()]
                if before.endswith(".") or (m.start() and code[m.start()-1].isdigit()):continue
                if current is None:self.add(p,i,m.start()+1,"error","VSIX-INFO-MISSING-HEADER","关键字前没有合法 Header。","VSIX/Error/InfoBaseErrorTagger.cs");continue
                dynamic=kw.endswith("_effects") and not any(kw in values for values in self.contexts.values())
                if dynamic:
                    if current not in {"skill:","combat_skill:","combat_move_skill:","riposte_skill:"}:
                        self.add(p,i,m.start()+1,"error","VSIX-INFO-DYNAMIC-EFFECT-CONTEXT","动态 _effects 关键字只能用于技能类 Header。","VSIX/Error/InfoBaseErrorTagger.cs")
                    body=kw[1:-8]
                    known_prefixes={x.lstrip('.') for h,vals in self.contexts.items() if h in {'skill:','combat_skill:','combat_move_skill:','riposte_skill:'} for x in vals}
                    if any(body.lower().startswith(prefix.lower()) for prefix in known_prefixes):
                        self.add(p,i,m.start()+1,"error","VSIX-INFO-DYNAMIC-EFFECT-PREFIX","模式差分 Effect 关键字不能以技能已有关键字作为前缀。","VSIX/Error/InfoBaseErrorTagger.cs")
                    prev=code[:m.start()]
                    if any(ch.isdigit() for ch in body) and re.search(r'\.target\s+[^.]*$',prev):
                        self.add(p,i,m.start()+1,"error","VSIX-INFO-DYNAMIC-EFFECT-DIGIT-AFTER-TARGET","模式名含数字且动态 Effect 紧跟 .target，可能造成识别错误。","VSIX/Error/InfoBaseErrorTagger.cs")
                if kw not in self.contexts.get(current,[]) and not dynamic:
                    self.add(p,i,m.start()+1,"error","VSIX-INFO-INVALID-KEYWORD",f"关键字 {kw} 不属于 Header {current}。","VSIX/Error/InfoBaseErrorTagger.cs");continue
                if kw==".was_killed_effects":
                    self.add(p,i,m.start()+1,"error","VSIX-INFO-WAS-KILLED-EFFECTS","请勿使用 .was_killed_effects，以防击杀路径导致游戏崩溃。","VSIX/Error/InfoBaseErrorTagger.cs")
                args=self._info_args(source_lines,i-1,m)
                if dynamic and current in {"skill:","combat_skill:","combat_move_skill:","riposte_skill:"}:
                    mode_body=kw[1:-8]
                    same_line_valid=[]
                    vm=re.search(r"\.valid_modes\s+(.+?)(?=\s+\.|$)",code)
                    if vm: same_line_valid=self.args(vm.group(1))
                    if mode_body not in same_line_valid:
                        self.add(p,i,m.start()+1,"error","KB-INFO-MODE-EFFECT-NOT-VALID","模式差分 Effect 必须在同一技能行由 .valid_modes 明确包含对应模式；否则该模式差分视为未写入。","Mechanics/37-技能同ID分行与无等级共用分行.md; anchor:skill-valid-modes-shared-line")
                if dynamic:
                    if len(args)>6:self.add(p,i,m.start()+1,"error","VSIX-INFO-DYNAMIC-EFFECT-TOO-MANY","动态 _effects 参数数量超过 6。","VSIX/Error/InfoBaseErrorTagger.cs")
                    for value in args:
                        if len(value)>64:self.add(p,i,m.start()+1,"error","VSIX-INFO-DYNAMIC-EFFECT-ARG-LONG","动态 _effects 单个 Effect ID 长度超过 64。","VSIX/Error/InfoBaseErrorTagger.cs")
                self._info_argument_checks(p,i,current,kw,args,m.start()+1)
                if current=="spawn:" and kw==".effects":
                    for arg in args:
                        if len(arg)>31:self.add(p,i,m.start()+1,"warning","KB-SPAWN-EFFECT-ID-LENGTH-CONSERVATIVE","spawn .effects 的 Effect ID 按知识库保守限制不得超过 31 个字符；底层精确计数边界仍未知。","RAG/info_fields.jsonl; Info/headers/Info.spawn.md")
                if kw==".valid_modes": self.refs(p,args,"mode",i,m.start()+1,".valid_modes")
                if current in {"skill:","combat_skill:","combat_move_skill:","riposte_skill:"} and kw==".effect": self.refs(p,args,"effect",i,m.start()+1,".effect")
                if dynamic:
                    body=kw[1:-8]; self.refs(p,[body],"mode",i,m.start()+1,"动态 _effects 模式名")
                    self.refs(p,args,"effect",i,m.start()+1,kw)
                if current=="death_class:" and kw in {".monster_class_id",".random_monster_class_ids"}: mode_ids.append(kw)
        if len(set(mode_ids))==2:
            self.add(p,1,1,"error","VSIX-INFO-DEATH-CLASS-CONFLICT","death_class: 不能同时使用 .monster_class_id 与 .random_monster_class_ids。","VSIX/Error/InfoBaseErrorTagger.cs")
    @staticmethod
    def _keywords(code):
        """与 VSIX 一样，忽略成对引号中的关键字和数字后的小数伪关键字。"""
        strings=[(m.start(),m.end()) for m in re.finditer(r'"[^"\r\n]*"',code)]
        return [m for m in re.finditer(r'\.[A-Za-z_][A-Za-z0-9_]*',code)
                if not any(a<=m.start()<b for a,b in strings)
                and not (m.start()>0 and code[m.start()-1].isdigit())]
    def _keyword_args(self,code,match):
        end=next((m.start() for m in self._keywords(code) if m.start()>=match.end()),len(code))
        return self.args(code[match.end():end])
    def _info_args(self,lines,line_index,match):
        """逐行读取参数；下个关键字前的参数仍计入，遇到新 Header 即结束。"""
        result=[]
        for index in range(line_index,len(lines)):
            code=lines[index].split("//",1)[0]
            if index!=line_index and re.match(r'^[ \t]*[A-Za-z0-9_]+:',code):
                break
            start=match.end() if index==line_index else 0
            next_kw=next((m for m in self._keywords(code) if m.start()>=start),None)
            result.extend(self.args(code[start:next_kw.start() if next_kw else len(code)]))
            if next_kw is not None:break
        return result
    def _effect_arg_checks(self,p,line,code):
        for m in self._keywords(code):
            kw=m.group(); args=self._keyword_args(code,m)
            kind=self.update_rules["effect_arguments"].get(kw)
            if kind:
                valid=len(args)==1
                if valid:
                    value=args[0]
                    if kind=="boolean":valid=value.lower() in {"true","false"}
                    elif kind=="numeric_boolean":valid=value in {"0","1"}
                    elif kind=="integer":valid=re.fullmatch(r"[+-]?[0-9]+",value) is not None
                    elif kind=="number":
                        try:valid=math.isfinite(float(value))
                        except ValueError:valid=False
                    elif kind=="string":valid=bool(value.strip())
                if not valid:self.add(p,line,m.start()+1,"error","KB-UPDATE-EFFECT-ARGUMENT",f"{kw} 必须有且只有一个 {kind} 参数。","tools/local_mod_syntax_checker/update_rules.json")
                elif kind=="numeric_boolean" and code[m.end():].lstrip().startswith('"'):
                    self.add(p,line,m.start()+1,"error","VSIX-EFFECT-QUOTED-NUMERIC-BOOL",f"{kw} 的数值布尔参数不应带引号。","VSIX/Error/EffectErrorTagger.cs")
                continue
            if not args: continue
            if kw in self.effect_values and self.effect_values[kw] and args[0] not in self.effect_values[kw] and kw not in {".buff_source_type",".dotSource",".steal_buff_source_type",".buff_sub_type"}:
                self.add(p,line,m.start()+1,"error","VSIX-EFFECT-INVALID-VALUE",f"值 '{args[0]}' 对关键字 '{kw}' 无效。","VSIX/Error/EffectErrorTagger.cs")
            if kw in self.effect_numeric_bool and args[0] in {"0","1"} and re.search(re.escape(kw)+r'\s+"',code):
                self.add(p,line,m.start()+1,"error","VSIX-EFFECT-QUOTED-NUMERIC-BOOL",f"值 '{args[0]}' 不应带引号。","VSIX/Error/EffectErrorTagger.cs")
            if kw==".buff_duration_type" and args[0]=="none":
                self.add(p,line,m.start()+1,"warning","VSIX-EFFECT-DURATION-NONE","在 Effect 中，none 持续类型会被视为 round。","VSIX/Error/EffectErrorTagger.cs")
            if kw==".steal_buff_source_type":
                if args[0] in {"bsrc_district","bsrc_skill"}:
                    msg="建筑源 Buff 不可再生，请谨慎偷取/驱散。" if args[0]=="bsrc_district" else "谨慎偷取/驱散技能源，以防破坏其他机制。"
                    self.add(p,line,m.start()+1,"warning","VSIX-EFFECT-STEAL-SOURCE-RISK",msg,"VSIX/Error/EffectErrorTagger.cs")
                elif args[0] not in self.effect_values.get(kw,set()):
                    self.add(p,line,m.start()+1,"warning","VSIX-EFFECT-CUSTOM-SOURCE","自定义 Buff 源会被视为 combat_end 源。","VSIX/Error/EffectErrorTagger.cs")
            if kw==".steal_buff_stat_type" and args[0] not in {"hp_dot_bleed","hp_dot_poison","hp_dot_heal","stress_dot","shuffle_dot","tag","stealth"}:
                self.add(p,line,m.start()+1,"warning","VSIX-EFFECT-STEAL-STAT-RISK","慎用超级真驱散，以免破坏其他机制。","VSIX/Error/EffectErrorTagger.cs")
            if kw in {".dotSource",".buff_source_type",".steal_buff_source_type"} and self.effect_values.get(kw) and args[0] not in self.effect_values[kw]:
                self.add(p,line,m.start()+1,"warning","VSIX-EFFECT-CUSTOM-SOURCE","自定义 Buff 源会被视为 combat_end 源。","VSIX/Error/EffectErrorTagger.cs")
            if kw in {".buff_ids",".set_monster_class_ids"}:
                if any(" " in value or "\t" in value for value in args):
                    self.add(p,line,m.start()+1,"warning" if kw==".buff_ids" else "error","VSIX-EFFECT-QUOTED-LIST-WHITESPACE",f"{kw} 引号参数不应包含空格或制表符。","VSIX/Error/EffectErrorTagger.cs")
                if len(args)>8:self.add(p,line,m.start()+1,"error","VSIX-EFFECT-TOO-MANY-LIST-ARGS",f"{kw} 参数数量不能超过 8 个。","VSIX/Error/EffectErrorTagger.cs")
                elif len(args)==8:self.add(p,line,m.start()+1,"info","VSIX-EFFECT-LIST-ARGS-AT-LIMIT",f"{kw} 参数数量已达到 8 个。","VSIX/Error/EffectErrorTagger.cs")
                for value in args:
                    if len(value)>64:self.add(p,line,m.start()+1,"error","VSIX-EFFECT-ARG-TOO-LONG",f"{kw} 参数长度超过 64。","VSIX/Error/EffectErrorTagger.cs")
                    elif len(value)==64:self.add(p,line,m.start()+1,"warning","VSIX-EFFECT-ARG-AT-LIMIT",f"{kw} 参数长度达到 64。","VSIX/Error/EffectErrorTagger.cs")
    def _effect_order_checks(self,p,line,code):
        names=[m.group() for m in self._keywords(code)]
        def has_later(first,second):
            return any(second in names[i+1:] for i,n in enumerate(names) if n==first)
        source="VSIX/Error/EffectErrorTagger.cs"
        if has_later(".cure",".cure_burn") or has_later(".cure_burn",".cure"):
            self.add(p,line,1,"error","VSIX-EFFECT-CURE-CONFLICT",".cure 与 .cure_burn 同行时只有后写关键字生效。",source)
        if has_later(".heal",".healstress"):
            self.add(p,line,1,"error","VSIX-EFFECT-HEAL-ORDER",".heal 写在 .healstress 前时不生效。",source)
        if has_later(".cure",".cure_disease") and not has_later(".cure",".cure_burn"):
            self.add(p,line,1,"error","VSIX-EFFECT-CURE-DISEASE-ORDER",".cure 写在 .cure_disease 前时不生效。",source)
        if ".cure" in names and not has_later(".cure",".cure_burn"):
            self.add(p,line,1,"info","VSIX-EFFECT-CURE-SUGGESTION","建议换用 .cure_bleed 与 .cure_poison。",source)
    def _trinket_target_check(self,p,line,code):
        fields={m.group():self._keyword_args(code,m) for m in self._keywords(code)}
        target=next(iter(fields.get(".target",[])),None)
        for kw in (".trigger_limit_minimum_increase",".trigger_limit_maximum_increase",".gain_random_trinket",".gain_trinket",".destroy_trinket"):
            if kw not in fields:continue
            value=next(iter(fields[kw]),None)
            if (kw!=".destroy_trinket" or str(value).lower()=="true") and target not in {"this_trinket","other_trinket"}:
                self.add(p,line,1,"warning","VSIX-EFFECT-TRINKET-TARGET",f"{kw} 要求同一 Effect 行的 .target 为 this_trinket/other_trinket。","VSIX/Error/EffectErrorTagger.cs")
    def effects(self,p):
        text=self.read(p)
        if text is None:return
        if not str(p.relative_to(self.root)).replace('\\','/').lower().startswith("effects/"):self.add(p,1,1,"warning","KB-EFFECT-WRONG-DIRECTORY","Effect 文件通常应位于 effects/。","RAG/effect_basics.jsonl")
        block=[]
        for i,line in enumerate(self.lines(text),1):
            code=line.split("//",1)[0]
            if not code.strip():continue
            self._lexical(p,i,code,"effect")
            self._effect_arg_checks(p,i,code)
            self._effect_order_checks(p,i,code)
            self._trinket_target_check(p,i,code)
            unquoted=re.sub(r'"[^"\r\n]*"',lambda m: " "*len(m.group()),code)
            colon=unquoted.find(":")
            is_header=colon>=0 and code[:colon+1].strip().lower()=="effect:"
            if colon>=0 and not is_header:
                self.add(p,i,1,"error","VSIX-EFFECT-INVALID-HEADER","Effect 文件只能使用 effect: Header。","VSIX/Error/EffectErrorTagger.cs")
            if is_header:
                if block:self._effect_block_checks(p,block)
                header=code.strip().split(None,1)[0]
                if not header.lower().startswith("effect:"):
                    self.add(p,i,1,"error","VSIX-EFFECT-INVALID-HEADER",f"无效 Header '{header}'；Effect 文件必须使用 effect:。","VSIX/Error/EffectErrorTagger.cs")
                block=[(i,code,1)]
            elif not block:
                self.add(p,i,1,"error","VSIX-EFFECT-OUTSIDE-BLOCK","此行不属于任何 effect:。","VSIX/Error/EffectErrorTagger.cs"); continue
            else:
                block.append((i,code,1))
                if self._keywords(code):self.add(p,i,1,"warning","VSIX-EFFECT-MULTILINE","建议单条 Effect 不在块内换行，优先同名分行。","VSIX/Error/EffectErrorTagger.cs")
                if "." not in code:self.add(p,i,1,"error","VSIX-EFFECT-INVALID-CONTENT","Effect 续行没有可识别关键字。","VSIX/Error/EffectErrorTagger.cs")
            for m in self._keywords(code):
                kw=m.group()
                if kw not in self.effect_keywords:self.add(p,i,m.start()+1,"error","VSIX-EFFECT-INVALID-KEYWORD",f"无效 Effect 关键字：{kw}","VSIX/Error/EffectErrorTagger.cs")
            for token in self._keywords(code):
                kind={".set_mode":"mode",".buff_ids":"buff"}.get(token.group())
                if kind:self.refs(p,self._keyword_args(code,token),kind,i,token.start()+1,token.group())
        if block:self._effect_block_checks(p,block)
    def update_json(self,p,domain):
        text=self.read(p,False)
        if text is None:return
        try:data=json.loads(text)
        except json.JSONDecodeError as error:
            self.add(p,error.lineno,error.colno,"error","JSON-INVALID",str(error),"JSON")
            return
        def valid(kind,value):
            if kind=="boolean":return type(value) is bool
            if kind=="string":return isinstance(value,str) and bool(value.strip())
            if kind=="integer":return type(value) in {int,float} and math.isfinite(value) and value==int(value)
            if kind=="string_array":return isinstance(value,list) and all(isinstance(item,str) for item in value)
            return value in self.update_rules["json_enums"].get(kind,[]) if isinstance(value,str) else False
        def visit(node,path):
            if isinstance(node,dict):
                fields=dict(self.update_rules["json_fields"][domain])
                type_name=node.get("type")
                required=self.update_rules["json_required_by_type"].get(domain,{}).get(type_name,{}) if isinstance(type_name,str) else {}
                fields.update(required)
                for field,kind in fields.items():
                    if field not in node and field not in required:continue
                    if field not in node or not valid(kind,node[field]):
                        self.add(p,1,1,"error","KB-UPDATE-JSON-ARGUMENT",f"{path}.{field} 要求 {kind}。","tools/local_mod_syntax_checker/update_rules.json")
                for key,value in node.items():visit(value,f"{path}.{key}")
            elif isinstance(node,list):
                for index,value in enumerate(node):visit(value,f"{path}[{index}]")
        visit(data,"$")
    def trinkets(self,p):
        text=self.read(p)
        if text is None:return
        if p.name.lower().endswith(".entries.trinkets.json"):
            if p.parent.name.lower()!="trinkets":
                self.add(p,1,1,"warning","KB-TRINKET-WRONG-DIRECTORY","饰品条目文件应位于 Mod 根目录 trinkets/。","Mechanics/47-饰品条目定义与装备Buff.md")
            try:d=json.loads(text)
            except json.JSONDecodeError as e:self.add(p,e.lineno,e.colno,"error","TRINKET-INVALID-JSON",str(e),"Mechanics/47-饰品条目定义与装备Buff.md");return
            entries=d.get("entries") if isinstance(d,dict) else None
            if not isinstance(entries,list):self.add(p,1,1,"error","TRINKET-MISSING-ENTRIES","饰品文件顶层必须包含 entries 数组。","Mechanics/47-饰品条目定义与装备Buff.md");return
            for i,e in enumerate(entries):
                if not isinstance(e,dict):self.add(p,1,1,"error","TRINKET-ENTRY-NOT-OBJECT",f"entries[{i}] 必须是对象。","Mechanics/47-饰品条目定义与装备Buff.md");continue
                tid=e.get("id")
                if not isinstance(tid,str) or not tid:self.add(p,1,1,"error","TRINKET-ID-MISSING",f"entries[{i}] 缺少非空 id。","Mechanics/47-饰品条目定义与装备Buff.md")
                buffs=e.get("buffs",[])
                if buffs is not None:
                    if not isinstance(buffs,list):self.add(p,1,1,"error","TRINKET-BUFFS-NOT-ARRAY","饰品 buffs 必须是 Buff ID 数组。","Mechanics/47-饰品条目定义与装备Buff.md")
                    else:
                        for b in buffs:
                            if not isinstance(b,str):self.add(p,1,1,"error","TRINKET-BUFF-ID-NOT-STRING","饰品 buffs 中每项必须是字符串 Buff ID。","Mechanics/47-饰品条目定义与装备Buff.md")
                            elif b not in self.buff_ids:self.add(p,1,1,"error","KB-REF-BUFF-NOT-FOUND",f"饰品 buffs 引用的 Buff ID '{b}' 未找到定义。","Mechanics/47-饰品条目定义与装备Buff.md")
                rarity=e.get("rarity")
                if isinstance(rarity,str) and rarity and rarity not in self.rarity_ids:self.add(p,1,1,"error","KB-REF-RARITY-NOT-FOUND",f"饰品 rarity '{rarity}' 未在 *.rarities.trinkets.json 中找到。","Mechanics/47-饰品条目定义与装备Buff.md")
                visual=e.get("visual_rarity")
                if visual is not None and visual==rarity:self.add(p,1,1,"warning","TRINKET-VISUAL-RARITY-SAME","visual_rarity 不应与 rarity 使用同一 ID。","Mechanics/47-饰品条目定义与装备Buff.md")
                if isinstance(visual,str) and visual and visual not in self.rarity_ids:self.add(p,1,1,"error","KB-REF-VISUAL-RARITY-NOT-FOUND",f"饰品 visual_rarity '{visual}' 未找到稀有度定义。","Mechanics/47-饰品条目定义与装备Buff.md")
        else:
            if p.parent.name.lower()!="trinkets":self.add(p,1,1,"warning","KB-TRINKET-RARITY-WRONG-DIRECTORY","饰品稀有度文件应位于 trinkets/。","Mechanics/47-饰品条目定义与装备Buff.md")
            try:d=json.loads(text)
            except json.JSONDecodeError as e:self.add(p,e.lineno,e.colno,"error","TRINKET-RARITY-INVALID-JSON",str(e),"Mechanics/47-饰品条目定义与装备Buff.md");return
            rs=d.get("rarities") if isinstance(d,dict) else None
            if not isinstance(rs,list):self.add(p,1,1,"error","TRINKET-RARITY-MISSING-ARRAY","稀有度文件顶层必须包含 rarities 数组。","Mechanics/47-饰品条目定义与装备Buff.md");return
            allowed={"dd","trophy","battle","universal","quest","kickstarter"}
            for i,r in enumerate(rs):
                if not isinstance(r,dict):continue
                if not isinstance(r.get("id"),str) or not r.get("id"):self.add(p,1,1,"error","TRINKET-RARITY-ID-MISSING",f"rarities[{i}] 缺少非空 id。","Mechanics/47-饰品条目定义与装备Buff.md")
                if "award_category" in r and r["award_category"] not in allowed:self.add(p,1,1,"error","TRINKET-RARITY-AWARD-CATEGORY",f"未知 award_category：{r['award_category']}。","Mechanics/47-饰品条目定义与装备Buff.md")
    def monster_path(self,p):
        parts=self._content_parts(self._path_parts(p), preserve_case=True)
        low=[x.lower() for x in parts]
        try:i=low.index("monsters")
        except ValueError:return
        if len(parts)<=i+3:return
        base=parts[i+1]; subclass=parts[i+2]
        if len(parts)>i+4:
            self.add(p,1,1,"error","KB-MONSTER-EXTRA-DIRECTORY","怪物大类/小类目录下不允许继续嵌套包含 info/art 的目录；文件必须直接位于 <大类>_<单字符差分>/ 下。","Mechanics/24-Mod识别与职业Mod目录结构.md; AGENT_USAGE.md")
        if subclass.lower()=="anim":return
        base_len=len(base); subclass_len=len(subclass)
        if base_len>30:
            self.add(p,1,1,"error","KB-MONSTER-BASE-NAME-TOO-LONG",f"怪物大类名长度为 {base_len}，不得超过 30 个字符。","Mechanics/24-Mod识别与职业Mod目录结构.md")
        if subclass_len>32:
            self.add(p,1,1,"error","KB-MONSTER-SUBCLASS-NAME-TOO-LONG",f"怪物完整小类名长度为 {subclass_len}，不得超过 32 个字符。","Mechanics/24-Mod识别与职业Mod目录结构.md")
        expected=re.escape(base)+r"_[A-Za-z0-9]"
        if not re.fullmatch(expected,subclass):
            self.add(p,1,1,"error","KB-MONSTER-SUBCLASS-NAME","怪物小类目录必须为 <怪物大类ID>_<单字符差分>；大写 A-Z 和数字 0-9 已确认可用。","Mechanics/24-Mod识别与职业Mod目录结构.md; anchor:monster-base-class-diff-reuse")
        stem=p.name
        for suffix in (".info.darkest",".art.darkest"):
            if stem.lower().endswith(suffix):
                stem=stem[:-len(suffix)]
                break
        if stem!=subclass:
            self.add(p,1,1,"error","KB-MONSTER-FILENAME-MISMATCH",f"怪物文件名前缀必须与小类目录完全一致（包括大小写，允许大写）：期望 {subclass}，实际 {stem}。","Mechanics/24-Mod识别与职业Mod目录结构.md")
    def buffs(self,p):
        text=self.read(p); 
        if text is None:return
        try:d=json.loads(text)
        except json.JSONDecodeError as e:self.add(p,e.lineno,e.colno,"error","BUFF-INVALID_JSON",str(e),"tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core");return
        if not isinstance(d,dict) or not isinstance(d.get("buffs"),list):
            self.add(p,1,1,"error","BUFF-MISSING-BUFFS","根对象必须包含 buffs 数组。","tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core")
            return
        self.add(p,1,1,"info","KB-COVERAGE-BUFF-PARTIAL","Python 已检查 Buff 字段类型、主副类型、rule_type 与基础结构；完整 Rule 联动/特殊 ID 语义请另运行内置 C# 入口。","tools/local_mod_syntax_checker/README.md")
        for idx,b in enumerate(d.get("buffs",[]) if isinstance(d,dict) else []):
            if not isinstance(b,dict):self.add(p,1,1,"error","BUFF-ITEM-NOT-OBJECT",f"buffs[{idx}] 必须是对象。","tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core");continue
            for k in ("id","stat_type","stat_sub_type","amount","rule_type","is_false_rule","rule_data"):
                if k not in b:self.add(p,1,1,"error","BUFF-MISSING-REQUIRED-FIELD",f"buffs[{idx}] 缺少 {k}。","tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core")
            def report(code,message,severity="error"):
                self.add(p,1,1,severity,code,f"buffs[{idx}]: {message}","tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core")
            checks={"String":lambda value:isinstance(value,str),
                    "Number":lambda value:type(value) in {int,float} and math.isfinite(value),
                    "Boolean":lambda value:type(value) is bool,
                    "Object":lambda value:isinstance(value,dict),
                    "StringArray":lambda value:isinstance(value,list) and all(isinstance(item,str) for item in value)}
            for field,value in b.items():
                expected=self.buff_fields.get(field)
                if expected is None:report("BUFF-UNKNOWN_FIELD",f"未知字段 {field}。","warning")
                elif not checks[expected](value):report("BUFF-INVALID_VALUE_TYPE",f"{field} 必须是 {expected}。")
            rule_data=b.get("rule_data")
            if isinstance(rule_data,dict):
                for field,value in rule_data.items():
                    expected={"float":"Number","string":"String"}.get(field)
                    if expected is None:report("BUFF-UNKNOWN_FIELD",f"未知 rule_data 字段 {field}。","warning")
                    elif not checks[expected](value):report("BUFF-INVALID_VALUE_TYPE",f"rule_data.{field} 必须是 {expected}。")
            stat=b.get("stat_type"); subtype=b.get("stat_sub_type")
            if isinstance(stat,str):
                if stat not in self.effect_values.get(".buff_type",set()):report("BUFF-UNKNOWN_STAT_TYPE",f"未知 stat_type {stat}。")
                if isinstance(subtype,str):
                    if stat in self.buff_required_subtypes and not subtype.strip():report("BUFF-MISSING_STAT_SUB_TYPE_VALUE",f"{stat} 要求非空 stat_sub_type。")
                    elif subtype and stat in self.buff_subtypes and subtype not in self.buff_subtypes[stat]:report("BUFF-INVALID_STAT_SUB_TYPE",f"{subtype} 不属于 {stat}。")
                    elif subtype and stat not in self.buff_subtypes and stat not in self.buff_free_subtypes:report("BUFF-UNEXPECTED_STAT_SUB_TYPE",f"{stat} 不接受 stat_sub_type。")
            if isinstance(b.get("rule_type"),str) and b["rule_type"] not in self.buff_rules:report("BUFF-INVALID_RULE_TYPE",f"未知 rule_type {b['rule_type']}。")
            if isinstance(b.get("rule_data"),dict) and not any(k in b["rule_data"] for k in ("float","string")):self.add(p,1,1,"error","BUFF-RULE-DATA-EMPTY","rule_data 必须包含 float 或 string。","tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core")
            if b.get("rule_type")=="always" and b.get("is_false_rule") is True:self.add(p,1,1,"warning","BUFF-INVERTED-ALWAYS","always + is_false_rule=true 会使 Buff 始终无效。","tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core")
    def localization(self,p):
        try:root=ET.parse(p).getroot()
        except ET.ParseError as e:self.add(p,e.position[0],e.position[1],"error","LOC-XML-MALFORMED",str(e),"Mechanics/16-loc与loc2本地化覆盖优先级.md");return
        langs={x.get("id"):x for x in root.iter("language")}
        if "english" not in langs:self.add(p,1,1,"error","LOC-ENGLISH-BASELINE-MISSING","缺少 english 基准节点。","Mechanics/16-loc与loc2本地化覆盖优先级.md")
        for lid,lang in langs.items():
            for e in lang.iter("entry"):
                if not (e.get("id") or "").strip():self.add(p,1,1,"error","LOC-ENTRY-ID-MISSING","entry 缺少非空 id。","Mechanics/16-loc与loc2本地化覆盖优先级.md")
                for c in re.findall(r'\{colour_start\|([^{}|]+)\}',e.text or ""):
                    if c not in self.colour_ids:self.add(p,1,1,"error","LOC-COLOR-NOT-FOUND",f"颜色 {c} 未找到定义。","Mechanics/16-loc与loc2本地化覆盖优先级.md")
        if "english" in langs:
            base={e.get("id"):(e.text or "") for e in langs["english"].iter("entry")}
            for lid,lang in langs.items():
                if lid=="english":continue
                for e in lang.iter("entry"):
                    if e.get("id") in base and self.format_sig(base[e.get("id")])!=self.format_sig(e.text or ""):self.add(p,1,1,"warning","LOC-PLACEHOLDER-MISMATCH",f"Entry {e.get('id')} 在 {lid} 中格式参数与 english 不一致。","Mechanics/16-loc与loc2本地化覆盖优先级.md")
    @staticmethod
    def format_sig(s):return sorted(re.findall(r'%(?:[+\-#0 .0-9]*)([dfuisc])',s.replace('%%','')))
    def project(self,p):
        if "error" in p.parent.name.lower():self.add(p,1,1,"error","KB-MOD-ROOT-ERROR-FRAGMENT","Mod 根目录名称包含 error，可能导致游戏无法识别。","Mechanics/24-Mod识别与职业Mod目录结构.md")
        try:r=ET.parse(p).getroot()
        except ET.ParseError as e:self.add(p,e.position[0],e.position[1],"error","PROJECT-XML-MALFORMED",str(e),"Mechanics/24-Mod识别与职业Mod目录结构.md");return
        # PublishedFileId 由首次工坊发布回写；自用或尚未发布的 Mod 可省略或留空。
        for tag in ("Title","VersionMajor","VersionMinor","TargetBuild"):
            if r.find(f".//{tag}") is None:self.add(p,1,1,"warning","PROJECT-FIELD-MISSING",f"project.xml 缺少常用字段 {tag}。","Mechanics/24-Mod识别与职业Mod目录结构.md")

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--root",required=True,type=Path);ap.add_argument("--reference-root",action="append",default=[],type=Path);ap.add_argument("--strict-references",action="store_true");ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    try:
        c=Checker(a.root,a.reference_root,a.strict_references)
    except ValueError as e:
        print(f"无法开始检查：{e}", file=sys.stderr)
        return 2
    # 没有显式 --reference-root 时只使用知识库内置规则和目标 Mod 自身。
    # 游戏本体、DLC 或依赖 Mod 必须由当前调用者在本次运行中显式提供。
    ds=c.run(); result={"root":str(c.root),"files_scanned":len(c.files),"error_count":sum(x.severity=="error" for x in ds),"warning_count":sum(x.severity=="warning" for x in ds),"info_count":sum(x.severity=="info" for x in ds),"diagnostics":[asdict(x) for x in ds]}
    if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for x in ds:print(f"{x.file}:{x.line}:{x.column}: {x.severity.upper()} {x.code}: {x.message} [{x.source}]")
        print(f"检查完成：文件 {result['files_scanned']}，错误 {result['error_count']}，警告 {result['warning_count']}，提示 {result['info_count']}。")
    return 1 if result["error_count"] else 0
if __name__=="__main__":sys.exit(main())








