using System.Text.RegularExpressions;
using For_the_Darkest_Dungeon.DefinitionDarkest;

namespace LocalModSyntaxChecker;

internal static class InfoSyntax
{
    private static readonly HashSet<string> SkillHeaders = new(StringComparer.Ordinal)
    { "skill:", "riposte_skill:", "combat_skill:", "combat_move_skill:" };
    private static readonly Regex DynamicEffects = new(@"^\.(?<body>[^\s.]+)_effects$", RegexOptions.Compiled);
    private static readonly HashSet<string> EffectReferenceFields = new(StringComparer.Ordinal)
    {
        "mode:|.battle_start_effect_ids",
        "hp_reaction:|.effects", "death_reaction:|.effects", "crit:|.effects",
        "captor_empty:|.capture_effects", "captor_full:|.release_effects",
        "death_class:|.change_class_effects", "controller:|.uncontrol_effects",
        "skill_reaction:|.was_hit_performer_effects", "skill_reaction:|.was_hit_target_effects",
        "skill_reaction:|.was_killed_other_monsters_effects", "skill_reaction:|.was_killed_by_hero_effects",
        "skill_reaction:|.was_killed_all_heroes_effects", "skill_reaction:|.was_killed_effects",
        "spawn:|.effects", "spawn:|.wave_effects", "deaths_door:|.enter_effects"
    };

    public static IEnumerable<string> IndexModeIds(string text)
    {
        var doc = Parse(text, report: false, string.Empty, (_,_,_,_,_,_,_) => { });
        return doc.Fields.Where(f => f.Token.Header == "mode:" && f.Token.Keyword == ".id")
            .SelectMany(f => f.Arguments).Select(a => a.Value).Where(v => !string.IsNullOrWhiteSpace(v)).Distinct(StringComparer.Ordinal).ToArray();
    }

    public static void Validate(string file, string text, IReadOnlySet<string> modeIds, IReadOnlySet<string> effectIds,
        bool strictReferences, Action<string,int,int,string,string,string,string> add)
    {
        var doc = Parse(text, report: true, file, add);
        foreach (var field in doc.Fields)
        {
            var token = field.Token;
            string header = token.Header;
            if (!DarkestInfoData.AllHeaders.Contains(header)) continue;
            bool defined = DarkestInfoData.InfoContextMap.TryGetValue(header, out var allowed) && allowed.Contains(token.Keyword);
            bool knownElsewhere = DarkestInfoData.InfoContextMap.Values.Any(list => list.Contains(token.Keyword));
            bool dynamic = !defined && token.Keyword.EndsWith("_effects", StringComparison.Ordinal);

            if (!defined && !dynamic)
            {
                string message = knownElsewhere
                    ? $"关键字 '{token.Keyword}' 不属于 Header '{header}'。"
                    : $"无效的关键字：{token.Keyword}";
                add(file, token.Line, token.Column, "error", "VSIX-INFO-INVALID-KEYWORD", message, "VSIX/Error/InfoBaseErrorTagger.cs");
                continue;
            }

            if (dynamic)
            {
                ValidateDynamic(file, doc, field, modeIds, effectIds, strictReferences, add);
                continue;
            }

            if (token.Keyword == ".was_killed_effects")
                add(file, token.Line, token.Column, "error", "VSIX-INFO-WAS-KILLED-EFFECTS",
                    "VSIX 明确报错：请勿使用 .was_killed_effects，避免击杀 Trigger 导致游戏崩溃。",
                    "VSIX/Error/InfoBaseErrorTagger.cs");

            ValidateArguments(file, field, add);
            if (SkillHeaders.Contains(header) && token.Keyword == ".valid_modes")
                foreach (var arg in field.Arguments) CheckMode(file, arg.Line, arg.Column, arg.Value, ".valid_modes", modeIds, strictReferences, currentUserRequest:false, add);

            bool effectReference = SkillHeaders.Contains(header) && token.Keyword == ".effect" ||
                EffectReferenceFields.Contains(header + "|" + token.Keyword);
            if (effectReference)
                foreach (var arg in field.Arguments) CheckEffect(file, arg.Line, arg.Column, arg.Value, token.Keyword, effectIds, strictReferences,
                    currentUserRequest: SkillHeaders.Contains(header) && token.Keyword == ".effect", add);
        }

        var deathFields = doc.Fields.Where(f => f.Token.Header == "death_class:" &&
            (f.Token.Keyword == ".monster_class_id" || f.Token.Keyword == ".random_monster_class_ids")).ToList();
        var fixedId = deathFields.FirstOrDefault(f => f.Token.Keyword == ".monster_class_id");
        var randomIds = deathFields.FirstOrDefault(f => f.Token.Keyword == ".random_monster_class_ids");
        if (fixedId is not null && randomIds is not null)
        {
            const string message = "death_class: 下不能同时使用 .monster_class_id 与 .random_monster_class_ids。";
            add(file, fixedId.Token.Line, fixedId.Token.Column, "error", "VSIX-INFO-DEATH-CLASS-CONFLICT", message, "VSIX/Error/InfoBaseErrorTagger.cs");
            add(file, randomIds.Token.Line, randomIds.Token.Column, "error", "VSIX-INFO-DEATH-CLASS-CONFLICT", message, "VSIX/Error/InfoBaseErrorTagger.cs");
        }
    }

    private static void ValidateDynamic(string file, InfoDocument doc, SyntaxField field,
        IReadOnlySet<string> modeIds, IReadOnlySet<string> effectIds, bool strictReferences,
        Action<string,int,int,string,string,string,string> add)
    {
        var token = field.Token;
        var match = DynamicEffects.Match(token.Keyword);
        if (!match.Success)
        {
            add(file, token.Line, token.Column, "error", "VSIX-INFO-DYNAMIC-EFFECT-FORMAT", $"动态效果关键字 '{token.Keyword}' 格式错误。", "VSIX/Error/InfoBaseErrorTagger.cs");
            return;
        }
        if (!SkillHeaders.Contains(token.Header))
        {
            add(file, token.Line, token.Column, "error", "VSIX-INFO-DYNAMIC-EFFECT-CONTEXT", "模式差分 _effects 关键字只能用于技能类 Header。", "VSIX/Error/InfoBaseErrorTagger.cs");
            return;
        }
        string body = match.Groups["body"].Value;
        string? prefix = DarkestInfoData.InfoContextMap
            .Where(pair => SkillHeaders.Contains(pair.Key))
            .SelectMany(pair => pair.Value)
            .OrderByDescending(value => value.Length)
            .FirstOrDefault(value => body.StartsWith(value.TrimStart('.'), StringComparison.OrdinalIgnoreCase));
        if (prefix is not null)
            add(file, token.Line, token.Column, "error", "VSIX-INFO-DYNAMIC-EFFECT-PREFIX", "模式差分 Effect 关键字不能以技能本身已有关键字作为前缀（例如 .critxxx_effects）。", "VSIX/Error/InfoBaseErrorTagger.cs");

        var previous = doc.Fields.Where(f => f.Token.Start < token.Start).OrderByDescending(f => f.Token.Start).FirstOrDefault();
        if (body.Any(char.IsDigit) && previous?.Token.Keyword == ".target")
            add(file, token.Line, token.Column, "error", "VSIX-INFO-DYNAMIC-EFFECT-DIGIT-AFTER-TARGET", "模式名含数字且动态 Effect 紧跟 .target，可能造成识别错误。", "VSIX/Error/InfoBaseErrorTagger.cs");

        CheckMode(file, token.Line, token.Column, body, "模式专用字段中的 mode ID", modeIds, strictReferences, currentUserRequest:true, add);
        // VSIX Info 多字符串规则的 _effects 后备限制：最多 6 个 ID，每个最多 64 字符。
        foreach (var arg in field.Arguments)
        {
            int length=arg.Value.Count(c=>!char.IsWhiteSpace(c));
            if(length>64) add(file,arg.Line,arg.Column,"error","VSIX-INFO-DYNAMIC-EFFECT-ARG-LONG","动态 _effects 字段单个 Effect ID 长度超过 64 个字符。","VSIX/Error/InfoBaseErrorTagger.cs");
            else if(length==64) add(file,arg.Line,arg.Column,"warning","VSIX-INFO-DYNAMIC-EFFECT-ARG-AT-LIMIT","动态 _effects 字段单个 Effect ID 已达到 64 个字符。","VSIX/Error/InfoBaseErrorTagger.cs");
        }
        if(field.Arguments.Count>6) add(file,field.Arguments[6].Line,field.Arguments[6].Column,"error","VSIX-INFO-DYNAMIC-EFFECT-TOO-MANY","动态 _effects 字段 Effect ID 参数数量超过 6 个。","VSIX/Error/InfoBaseErrorTagger.cs");
        foreach (var arg in field.Arguments) CheckEffect(file, arg.Line, arg.Column, arg.Value, token.Keyword, effectIds, strictReferences, currentUserRequest:true, add);
    }

    private static void ValidateArguments(string file, SyntaxField field, Action<string,int,int,string,string,string,string> add)
    {
        var t = field.Token;
        var args = field.Arguments;
        if (UpdateRules.IsInfoBoolean(t.Header, t.Keyword))
        {
            if (args.Count != 1 || !UpdateRules.IsValidArgument("boolean", args[0].Value))
                add(file, t.Line, t.Column, "error", "KB-UPDATE-INFO-ARGUMENT", $"{t.Keyword} 必须有且只有一个 true/false 参数。", "tools/local_mod_syntax_checker/update_rules.json");
            return;
        }
        if (args.Count == 0) return;

        bool modeId = t.Header == "mode:" && t.Keyword == ".id";
        bool modeList = SkillHeaders.Contains(t.Header) && t.Keyword == ".valid_modes";
        bool modeNames = modeId || modeList;
        int? singleMax = null;
        if (DarkestInfoData.SingleString32.Contains((t.Header,t.Keyword))) singleMax = 32;
        else if (DarkestInfoData.SingleString64.Contains((t.Header,t.Keyword))) singleMax = 64;
        else if (DarkestInfoData.SingleString128.Contains((t.Header,t.Keyword))) singleMax = 128;
        else if (DarkestInfoData.SingleString512.Contains((t.Header,t.Keyword))) singleMax = 512;
        if (singleMax.HasValue && args.Count > 1)
            add(file,args[1].Line,args[1].Column,"error","VSIX-INFO-SINGLE-ARG-COUNT",$"{t.Header} 的 {t.Keyword} 理论上只允许一个参数。","VSIX/Error/InfoBaseErrorTagger.cs");
        if (modeNames)
        {
            var checkedArgs = modeId ? args.Take(1) : args;
            foreach (var arg in checkedArgs)
            {
                int length = arg.Value.Count(c => !char.IsWhiteSpace(c));
                if (length > 64) add(file,arg.Line,arg.Column,"error","VSIX-INFO-STRING-TOO-LONG",$"{t.Keyword} mode 名长度不能超过 64 个字符（当前 {length}）。","VSIX/Error/InfoBaseErrorTagger.cs");
                else if (length > 32) add(file,arg.Line,arg.Column,"warning","VSIX-INFO-STRING-LONG",$"{t.Keyword} mode 名长度超过 32 个字符，建议缩短。","VSIX/Error/InfoBaseErrorTagger.cs");
            }
        }
        else if (singleMax.HasValue)
        {
            var arg = args[0];
            int length = arg.Value.Count(c => !char.IsWhiteSpace(c));
            if (length > singleMax.Value) add(file,arg.Line,arg.Column,"error","VSIX-INFO-STRING-TOO-LONG",$"{t.Keyword} 参数长度不能超过 {singleMax.Value}（当前 {length}）。","VSIX/Error/InfoBaseErrorTagger.cs");
            else if (length == singleMax.Value) add(file,arg.Line,arg.Column,"warning","VSIX-INFO-STRING-AT-LIMIT",$"{t.Keyword} 参数已达到 {singleMax.Value} 个字符，建议缩短。","VSIX/Error/InfoBaseErrorTagger.cs");
        }

        if (DarkestInfoData.MultiStringLengthRules.TryGetValue((t.Header,t.Keyword), out var multi))
        {
            bool canExceed = t.Keyword is ".damage_heal_base_class_ids" or ".incompatible_class_ids";
            bool suggestFewer = t.Header == "spawn:" && t.Keyword == ".effects";
            if (args.Count > multi.MaxArgs)
            {
                var severity = canExceed ? "warning" : "error";
                add(file,args[multi.MaxArgs].Line,args[multi.MaxArgs].Column,severity,"VSIX-INFO-TOO-MANY-STRINGS",$"{t.Keyword} 参数数量超过建议/允许值 {multi.MaxArgs}。", "VSIX/Error/InfoBaseErrorTagger.cs");
            }
            if (suggestFewer && args.Count > multi.MaxArgs / 2)
                add(file,args[multi.MaxArgs / 2].Line,args[multi.MaxArgs / 2].Column,"warning","VSIX-INFO-SPAWN-EFFECTS-LONG",$"spawn: 的 .effects 参数数量不建议超过 {multi.MaxArgs / 2}。", "VSIX/Error/InfoBaseErrorTagger.cs");
            if (!modeNames)
            {
                foreach (var arg in args)
                {
                    int length = arg.Value.Count(c => !char.IsWhiteSpace(c));
                    if (length > multi.MaxLength) add(file,arg.Line,arg.Column,"error","VSIX-INFO-STRING-TOO-LONG",$"{t.Keyword} 单个参数长度超过 {multi.MaxLength}（当前 {length}）。","VSIX/Error/InfoBaseErrorTagger.cs");
                    else if (length == multi.MaxLength) add(file,arg.Line,arg.Column,"warning","VSIX-INFO-STRING-AT-LIMIT",$"{t.Keyword} 单个参数已达到 {multi.MaxLength} 个字符，建议缩短。","VSIX/Error/InfoBaseErrorTagger.cs");
                }
            }
            // 独立的 KB 安全边界：spawn:.effects 的 ID 内部空格计入保守 31 字符上限；该证据注明引擎底层精确计数边界仍未知。
            if (t.Header == "spawn:" && t.Keyword == ".effects")
                foreach (var arg in args)
                    if (arg.Value.Length > 31)
                        add(file,arg.Line,arg.Column,"warning","KB-SPAWN-EFFECT-ID-LENGTH-CONSERVATIVE","KB 保守安全检查：spawn .effects 的 Effect ID 按含内部空格长度不得超过 31；外层引号不计，底层精确计数边界仍未知。","RAG/info_fields.jsonl; Info/headers/Info.spawn.md");
        }
        else if (!modeNames && SkillHeaders.Contains(t.Header) && t.Keyword.EndsWith("_effects",StringComparison.Ordinal))
        {
            // VSIX 的通用多字符串后备规则：技能类 Header 下、无静态表项的 *_effects 关键字按 6×64 检查。
            if (args.Count > 6) add(file,args[6].Line,args[6].Column,"error","VSIX-INFO-TOO-MANY-STRINGS",$"{t.Keyword} 参数数量超过 6。","VSIX/Error/InfoBaseErrorTagger.cs");
            foreach (var arg in args)
            {
                int length=arg.Value.Count(c=>!char.IsWhiteSpace(c));
                if(length>64) add(file,arg.Line,arg.Column,"error","VSIX-INFO-STRING-TOO-LONG",$"{t.Keyword} 单个参数长度超过 64。","VSIX/Error/InfoBaseErrorTagger.cs");
                else if(length==64) add(file,arg.Line,arg.Column,"warning","VSIX-INFO-STRING-AT-LIMIT",$"{t.Keyword} 单个参数已达到 64 个字符，建议缩短。","VSIX/Error/InfoBaseErrorTagger.cs");
            }
        }
        if (DarkestInfoData.MaxArgumentCountRules.TryGetValue((t.Header,t.Keyword), out int maxArgs) && args.Count > maxArgs)
            add(file,args[maxArgs].Line,args[maxArgs].Column,"error","VSIX-INFO-TOO-MANY-ARGS",$"{t.Keyword} 参数数量超过 {maxArgs}。","VSIX/Error/InfoBaseErrorTagger.cs");

        var valid = DarkestInfoData.GetValuesForKeyword(t.Header,t.Keyword);
        if (valid is null) return;
        if (t.Keyword is ".disabled_popup_text_types" or ".disabled_act_out_combat_start_turn_types")
        {
            int limit = t.Keyword == ".disabled_popup_text_types" ? valid.Count : 4;
            var seen = new HashSet<string>(StringComparer.Ordinal);
            foreach (var arg in args)
            {
                if (arg.Value.Any(char.IsWhiteSpace)) add(file,arg.Line,arg.Column,"error","VSIX-INFO-ARG-WHITESPACE",$"{t.Keyword} 参数不能包含空格或制表符。","VSIX/Error/InfoBaseErrorTagger.cs");
                if (!valid.Contains(arg.Value)) add(file,arg.Line,arg.Column,"error","VSIX-INFO-INVALID-VALUE",$"{t.Keyword} 不存在参数 '{arg.Value}'。","VSIX/Error/InfoBaseErrorTagger.cs");
                if (!seen.Add(arg.Value)) add(file,arg.Line,arg.Column,"error","VSIX-INFO-DUPLICATE-ARG",$"{t.Keyword} 出现重复参数 '{arg.Value}'。","VSIX/Error/InfoBaseErrorTagger.cs");
            }
            if (args.Count > limit) add(file,args[limit].Line,args[limit].Column,"error","VSIX-INFO-TOO-MANY-ARGS",$"{t.Keyword} 参数数量不能超过 {limit}。","VSIX/Error/InfoBaseErrorTagger.cs");
            return;
        }
        bool boolean = valid.Count == 2 && valid.Contains("true") && valid.Contains("false");
        if (boolean && args.Count > 1) add(file,args[1].Line,args[1].Column,"error","VSIX-INFO-BOOLEAN-MULTI-ARG","布尔型关键字不应写多个参数。","VSIX/Error/InfoBaseErrorTagger.cs");
        foreach (var arg in args)
        {
            if (arg.Value.Any(char.IsWhiteSpace)) { add(file,arg.Line,arg.Column,"error","VSIX-INFO-ARG-WHITESPACE",$"参数 '{arg.Value}' 不能包含空格或制表符。","VSIX/Error/InfoBaseErrorTagger.cs"); continue; }
            bool accepted = boolean
                ? new[] { "true","false","True","False","TRUE","FALSE" }.Contains(arg.Value,StringComparer.Ordinal)
                : valid.Contains(arg.Value);
            if (accepted) continue;
            if (SkillHeaders.Contains(t.Header) && t.Keyword == ".type")
                add(file,arg.Line,arg.Column,"info","VSIX-INFO-CUSTOM-SKILL-TYPE","若这是自定义技能类型，它可能无法享受近战/远程增益或触发相关 Trigger。","VSIX/Error/InfoBaseErrorTagger.cs");
            else add(file,arg.Line,arg.Column,"error","VSIX-INFO-INVALID-VALUE",$"参数 '{arg.Value}' 对关键字 '{t.Keyword}' 无效。","VSIX/Error/InfoBaseErrorTagger.cs");
        }
    }

    private static void CheckMode(string file, int line, int column, string id, string context,
        IReadOnlySet<string> ids, bool strict, bool currentUserRequest,
        Action<string,int,int,string,string,string,string> add)
    {
        if (string.IsNullOrWhiteSpace(id) || ids.Contains(id)) return;
        string source = currentUserRequest
            ? "当前用户要求的本地引用检查；Info/headers/Info.mode.md; RAG/info_fields.jsonl"
            : "知识库字段约束的静态引用检查；Info/headers/Info.mode.md; RAG/info_fields.jsonl";
        add(file,line,column,strict ? "error" : "warning","KB-REF-MODE-NOT-FOUND",
            $"{context} 引用的 ID '{id}' 未在 Mod/引用目录中找到 mode: .id 定义；外部模式请追加 --reference-root。",source);
    }
    private static void CheckEffect(string file, int line, int column, string id, string keyword,
        IReadOnlySet<string> ids, bool strict, bool currentUserRequest,
        Action<string,int,int,string,string,string,string> add)
    {
        if (string.IsNullOrWhiteSpace(id) || ids.Contains(id)) return;
        string source = currentUserRequest
            ? "当前用户要求的本地引用检查；Effect/keyword/Effect.name.md; RAG/info_fields.jsonl"
            : "知识库字段约束的静态引用检查；Info/README.md; RAG/info_fields.jsonl; Effect/keyword/Effect.name.md";
        add(file,line,column,strict ? "error" : "warning","KB-REF-EFFECT-NOT-FOUND",
            $"{keyword} 引用的 Effect ID '{id}' 未在扫描范围的 .effects.darkest 定义中找到；原版/DLC/依赖 Mod 的内容请追加 --reference-root。",source);
    }

    private sealed record InfoDocument(string ParserText, IReadOnlyList<SyntaxLine> Lines, IReadOnlyList<SyntaxField> Fields);
    private static InfoDocument Parse(string text, bool report, string file, Action<string,int,int,string,string,string,string> add)
    {
        var lines = SyntaxUtils.BuildLines(text);
        string parserText = string.Join("\n", lines.Select(l => l.Code)) + "\n";
        var tokens = new List<SyntaxToken>();
        var boundaries = new List<int>();
        string? current = null;
        for (int i = 0; i < lines.Count; i++)
        {
            var line = lines[i];
            if (report) SyntaxUtils.CheckLexical(file,line,"info",add);
            var match = SyntaxUtils.HeaderRegex.Match(line.Code);
            bool headerLine = match.Success;
            if (headerLine)
            {
                current = match.Groups["header"].Value;
                boundaries.Add(line.ParserOffset);
                if (report && !DarkestInfoData.AllHeaders.Contains(current))
                {
                    add(file,line.Number,1,"error","VSIX-INFO-UNKNOWN-HEADER",$"未知的 Header：{current}","VSIX/Error/InfoBaseErrorTagger.cs");
                    continue;
                }
            }
            var found = SyntaxUtils.FindKeywords(line,i,current);
            if (!headerLine && current is null && found.Count > 0 && report)
                add(file,line.Number,found[0].Column,"error","VSIX-INFO-MISSING-HEADER","缺少 Header：该关键字前没有合法 Header 定义。","VSIX/Error/InfoBaseErrorTagger.cs");
            tokens.AddRange(found);
        }
        return new InfoDocument(parserText,lines,SyntaxUtils.MakeFields(parserText,lines,tokens,boundaries));
    }
}
