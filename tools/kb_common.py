from __future__ import annotations

import hashlib
import html
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

KB = Path(__file__).resolve().parent.parent
# Machine-specific paths are opt-in; never infer another maintainer's drive.
def external_root(env_name: str, key: str, fallback: Path) -> Path:
    config = KB / "tools" / "external_source_paths.json"
    settings = json.loads(config.read_text(encoding="utf-8")) if config.is_file() else {}
    value = os.environ.get(env_name) or settings.get(key)
    if not value:
        return fallback
    result = Path(value)
    return result if result.is_absolute() else KB / result

GAME = external_root("DD_GAME_ROOT", "game_root", KB / "DarkestDungeon")
LOCAL_MODS = external_root("DD_LOCAL_MODS_ROOT", "local_mods_root", GAME / "mods")
WORKSHOP_262060 = external_root("DD_WORKSHOP_262060_ROOT", "workshop_root", KB / "workshop" / "content" / "262060")
PORTABLE_INPUTS = KB / "Sources" / "portable_inputs"
def refresh_external() -> bool:
    return os.environ.get("DD_KB_REFRESH_EXTERNAL") == "1"

BUILD = KB / ".build_sources"
GENERATED_AT = datetime.now().astimezone().date().isoformat()

TEXT_EXTS = {".md", ".txt", ".json", ".xml", ".darkest", ".cs", ".py", ".xaml", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".props", ".targets"}
SKIP_PARTS = {".git", ".vs", "bin", "obj", "packages", "node_modules", "__pycache__", "build", "dist"}

IDENTITY_TERMS_MARKER = "<!-- KB_IDENTITY_TERMS_V1 -->"
IDENTITY_TERMS = """<!-- KB_IDENTITY_TERMS_V1 -->
> **身份术语（适用于本知识库全部文档）**
>
> - **当前用户**：正在与当前 Agent 对话、提出本次任务的人。当前任务的授权、设计、目标、约束和纠正只以当前用户的明确表达为准。
> - **知识库编写者**：维护本知识库并在入库时提供历史实测、解释、设计确认或修正的人。本知识库中的“用户提供”“用户明确补充”“用户实测”等未明确指向当前会话的历史措辞，一律指知识库编写者，不是当前用户的新授权或新需求。
> - **外部来源作者**：工作簿、文档、Mod、原版或官方 DLC 等来源的作者；其资料仅按记录的证据等级使用，不等同于知识库编写者或当前用户。
> - **游戏玩家**：游戏内的操作者；不等同于当前用户。
>
> Agent 在回复、证据账本和写入说明中必须显式使用“当前用户”或“知识库编写者”；不得用无修饰的“用户”混同实时指令与历史证据。
<!-- /KB_IDENTITY_TERMS_V1 -->
"""


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def apply_identity_terms(path: Path, text: str) -> str:
    """Keep identity explicit without repeating the entire glossary on every page."""
    if path.suffix.lower() != ".md":
        return text
    short = ("<!-- KB_IDENTITY_TERMS_V1 -->\n"
             "> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。"
             "外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。\n"
             "<!-- /KB_IDENTITY_TERMS_V1 -->")
    if IDENTITY_TERMS_MARKER in text:
        return re.sub(r'<!-- KB_IDENTITY_TERMS_V1 -->.*?<!-- /KB_IDENTITY_TERMS_V1 -->',
                      lambda _:short, text, flags=re.S)
    lines = text.lstrip("\n").splitlines()
    for index, line in enumerate(lines):
        if line.startswith("# "):
            lines[index + 1:index + 1] = ["", short, ""]
            return "\n".join(lines)
    return short + "\n\n" + "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    text = apply_identity_terms(path, text)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, obj: Any) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=2))


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> int:
    ensure_dir(path.parent)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
            count += 1
    return count


def load_sources() -> tuple[dict[str, Any], dict[str, Any]]:
    workbooks = json.loads((BUILD / "workbooks.json").read_text(encoding="utf-8"))["workbooks"]
    docx = json.loads((BUILD / "docx.json").read_text(encoding="utf-8"))
    return workbooks, docx


def main_workbook(workbooks: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    for name, value in workbooks.items():
        if "代码（基于Oni术语表）" in name or "代码（基于" in name:
            return name, value
    raise KeyError("未找到主术语表工作簿")


def cell_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip()


def flat_row(row: list[Any]) -> str:
    return " | ".join(x for x in (cell_text(v) for v in row) if x)


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\r", "").replace("\n", "<br>")


def quoted_strings(text: str) -> list[str]:
    return re.findall(r'"((?:\\.|[^"\\])*)"', text)


def initializer_block(text: str, name: str) -> str:
    start = text.find(name)
    if start < 0:
        return ""
    brace = text.find("{", start)
    bracket = text.find("[", start)
    if brace < 0 or (0 <= bracket < brace and "=" in text[start:bracket]):
        opener, closer, begin = "[", "]", bracket
    else:
        opener, closer, begin = "{", "}", brace
    if begin < 0:
        return ""
    depth = 0
    in_string = False
    escaped = False
    for i in range(begin, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[begin : i + 1]
    return ""


def named_strings(text: str, name: str) -> list[str]:
    return quoted_strings(initializer_block(text, name))


def parse_keyword_value_map(text: str) -> dict[str, list[str]]:
    list_names = [
        "TargetValues", "CurioResultValues", "KeyStatusValues", "BuffTypeValues",
        "BuffSubTypeValues", "BuffDurationTypeValues", "BuffSourceValues",
        "HealSourceValues", "DamageTypeValues", "DamageSourceValues",
        "NumBoolValues", "StrBoolValues", "DoubleBoolValuesForError",
    ]
    lists = {name: named_strings(text, name) for name in list_names}
    block = initializer_block(text, "KeywordToValuesMap")
    result: dict[str, list[str]] = {}
    for keyword, list_name in re.findall(r'\{\s*"(\.[^"]+)"\s*,\s*(\w+)\s*\}', block):
        result[keyword] = lists.get(list_name, [])
    doubles = set(named_strings(text, "DoubleBoolKeywords"))
    for keyword in doubles:
        result[keyword] = ["0", "1", "true", "false", "True", "False", "TRUE", "FALSE"]
    return result


def parse_effect_blocks(rows: list[list[Any]]) -> dict[str, list[list[Any]]]:
    blocks: dict[str, list[list[Any]]] = {}
    current = ""
    for row in rows:
        first = cell_text(row[0] if row else None)
        match = re.search(r"\.[A-Za-z_][A-Za-z0-9_]*", first)
        if match:
            current = match.group(0)
            blocks.setdefault(current, []).append(row)
        elif current and any(cell_text(v) for v in row):
            blocks[current].append(row)
    return blocks


def parse_rule_blocks(rows: list[list[Any]], allowed: set[str]) -> dict[str, list[list[Any]]]:
    blocks: dict[str, list[list[Any]]] = {}
    current = ""
    for row in rows:
        raw = cell_text(row[1] if len(row) > 1 else None)
        token = re.match(r"[A-Za-z_]+", raw)
        if token and token.group(0) in allowed:
            current = token.group(0)
            blocks.setdefault(current, []).append(row)
        elif current and any(cell_text(v) for v in row):
            blocks[current].append(row)
    return blocks


def parse_stat_rows(rows: list[list[Any]], allowed: set[str]) -> dict[str, list[Any]]:
    result: dict[str, list[Any]] = {}
    for row in rows:
        key = cell_text(row[0] if row else None)
        if key in allowed:
            result[key] = row
    return result


def rel(path: Path, base: Path) -> str:
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return str(path)


def win_rel(path: Path, base: Path) -> str:
    return rel(path, base).replace("/", "\\")


def portable_game_path(path: Path) -> str:
    return "DarkestDungeon\\" + win_rel(path, GAME)


def project_title(mod_root: Path) -> str:
    project = mod_root / "project.xml"
    if not project.is_file():
        matches = list(mod_root.glob("**/project.xml"))
        project = matches[0] if matches else project
    if project.is_file():
        try:
            match = re.search(r"<Title>(.*?)</Title>", read_text_guess(project), re.S | re.I)
            if match:
                return html.unescape(re.sub(r"\s+", " ", match.group(1)).strip())
        except OSError:
            pass
    return mod_root.name


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def text_files(root: Path, extensions: set[str] | None = None) -> Iterable[Path]:
    extensions = extensions or TEXT_EXTS
    if not root.exists():
        return []
    return (p for p in root.rglob("*") if p.is_file() and not is_skipped(p) and p.suffix.lower() in extensions)


def read_text_guess(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "gb18030", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: Path, kind: str, base: Path | None = None) -> dict[str, Any]:
    stat = path.stat()
    portable = win_rel(path, base) if base else path.name
    return {
        "kind": kind,
        "path": portable,
        "relative_path": portable,
        "size": stat.st_size,
        "sha256": sha256(path),
    }


def chunk_text(text: str, max_chars: int = 1600) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.replace("\r", "")) if p.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            for i in range(0, len(paragraph), max_chars):
                chunks.append(paragraph[i : i + max_chars])
        elif not current:
            current = paragraph
        elif len(current) + len(paragraph) + 2 <= max_chars:
            current += "\n\n" + paragraph
        else:
            chunks.append(current)
            current = paragraph
    if current:
        chunks.append(current)
    return chunks


def first_nonempty(values: Iterable[Any]) -> str:
    for value in values:
        text = cell_text(value)
        if text:
            return text
    return ""
