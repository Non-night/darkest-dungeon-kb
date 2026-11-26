using For_the_Darkest_Dungeon.DefinitionDarkest;

namespace LocalModSyntaxChecker;

internal static class EffectSyntax
{
    private static readonly HashSet<string> DotKeywords = new(StringComparer.Ordinal)
    { ".dotBleed", ".dotPoison", ".dotStress", ".dotHpHeal", ".dotShuffle", ".dotBurn" };
    private static readonly HashSet<string> TrinketKeywords = new(StringComparer.Ordinal)
    { ".trigger_limit_minimum_increase", ".trigger_limit_maximum_increase", ".gain_random_trinket", ".gain_trinket", ".destroy_trinket" };
    private static readonly System.Text.RegularExpressions.Regex NameValueRegex = new(@"^\s*(?:""(?<quoted>[^""]*)""|(?<plain>[^\s]+))",System.Text.RegularExpressions.RegexOptions.Compiled);
    private sealed class Block
    {
        public required int StartLine { get; init; }
        public List<SyntaxToken> Tokens { get; } = new();
    }

    public static IEnumerable<string> IndexNames(string text)
    {
        var (lines,blocks) = ParseStructure(text,string.Empty,false,(_,_,_,_,_,_,_)=>{});
        foreach (var block in blocks)
        foreach (var token in block.Tokens.Where(t=>t.Keyword==".name"))
        {
            var line=lines[token.LineIndex];
            int start=token.Start-line.ParserOffset+token.Keyword.Length;
            if(start<0 || start>line.Code.Length) continue;
            var match=NameValueRegex.Match(line.Code[start..]);
            if(!match.Success) continue;
            string id=match.Groups["quoted"].Success?match.Groups["quoted"].Value:match.Groups["plain"].Value;
            if(!string.IsNullOrWhiteSpace(id)) yield return id;
        }
    }

    public static void Validate(string file, string text, IReadOnlySet<string> buffIds, IReadOnlySet<string> modeIds,
        IReadOnlySet<string> effectIds, bool strictReferences, Action<string,int,int,string,string,string,string> add)
    {
        var (lines, blocks) = ParseStructure(text, file, true, add);
        foreach (var block in blocks) ValidateBlock(file, block, lines, buffIds, modeIds, effectIds, strictReferences, add);
    }

    private static (List<SyntaxLine> Lines, List<Block> Blocks) ParseStructure(string text, string file, bool report,
        Action<string,int,int,string,string,string,string> add)
    {
        var lines = SyntaxUtils.BuildLines(text);
        var blocks = new List<Block>();
        Block? current = null;
        for (int i = 0; i < lines.Count; i++)
        {
            var line = lines[i];
            if (report) SyntaxUtils.CheckLexical(file,line,"effect",add);
            if (string.IsNullOrWhiteSpace(line.Code)) continue;
            int colon = FirstLogicalColon(line.Code);
            if (colon >= 0)
            {
                string header = line.Code[..(colon + 1)].Trim();
                if (header.Equals("effect:",StringComparison.OrdinalIgnoreCase))
                {
                    current = new Block { StartLine = line.Number };
                    blocks.Add(current);
                }
                else if (report)
                    add(file,line.Number,Math.Max(1,colon+1),"error","VSIX-EFFECT-INVALID-HEADER",$"无效 Header '{header}'；Effect 文件必须使用 effect:。","VSIX/Error/EffectErrorTagger.cs");
            }
            else if (current is null)
            {
                if (report) add(file,line.Number,1,"error","VSIX-EFFECT-OUTSIDE-BLOCK","此行不属于任何 effect: 块。","VSIX/Error/EffectErrorTagger.cs");
            }
            else if (report)
            {
                bool hasKeyword = SyntaxUtils.FindKeywords(line,i,"effect:").Count > 0;
                add(file,line.Number,1,hasKeyword ? "warning" : "error",hasKeyword ? "VSIX-EFFECT-MULTILINE" : "VSIX-EFFECT-INVALID-CONTENT",
                    hasKeyword ? "VSIX 建议单条 Effect 不在块内换行；如有需求请使用同名分行。" : "Effect 块续行中没有可识别关键字。",
                    "VSIX/Error/EffectErrorTagger.cs");
            }
            var tokens = SyntaxUtils.FindKeywords(line,i,"effect:");
            if (current is not null) current.Tokens.AddRange(tokens);
            if (report)
                foreach (var token in tokens)
                    if (!DarkestEffectsData.AllKeywords.Contains(token.Keyword))
                        add(file,token.Line,token.Column,"error","VSIX-EFFECT-INVALID-KEYWORD",$"无效关键字：{token.Keyword}","VSIX/Error/EffectErrorTagger.cs");
        }
        if (report)
            foreach (var block in blocks)
                if (!block.Tokens.Any(t => t.Keyword == ".name"))
                    add(file,block.StartLine,1,"error","KB-EFFECT-MISSING-NAME","每条 Effect 定义都必须包含非空 .name。","Effect/keyword/Effect.name.md");
        return (lines,blocks);
    }

    private static int FirstLogicalColon(string code)
    {
        foreach (var span in System.Text.RegularExpressions.Regex.Matches(code,@"""[^""]*""").Cast<System.Text.RegularExpressions.Match>())
            code = code.Remove(span.Index, span.Length).Insert(span.Index, new string(' ',span.Length));
        return code.IndexOf(':');
    }

    private static void ValidateBlock(string file, Block block, IReadOnlyList<SyntaxLine> lines,
        IReadOnlySet<string> buffIds, IReadOnlySet<string> modeIds, IReadOnlySet<string> effectIds,
        bool strictReferences, Action<string,int,int,string,string,string,string> add)
    {
        foreach (var token in block.Tokens)
        {
            var line = lines[token.LineIndex];
            var args = SyntaxUtils.ParseLineArguments(line,token,block.Tokens);
            if (token.Keyword == ".name") ValidateName(file,line,token,block.Tokens,args,add);
            ValidateKeywordValue(file,token,args,add);
            if (token.Keyword is ".buff_ids" or ".set_monster_class_ids") ValidateLimitedList(file,token,args,add);
        }

        foreach (var lineGroup in block.Tokens.GroupBy(t => t.LineIndex))
        {
            var tokens = lineGroup.OrderBy(t => t.Start).ToList();
            var line = lines[lineGroup.Key];
            for (int i = 0; i < tokens.Count; i++)
            {
                var token = tokens[i];
                var later = tokens.Skip(i + 1).Select(t => t.Keyword).ToList();
                if ((token.Keyword == ".cure" && later.Contains(".cure_burn")) || (token.Keyword == ".cure_burn" && later.Contains(".cure")))
                    add(file,token.Line,token.Column,"error","VSIX-EFFECT-CURE-CONFLICT",".cure 与 .cure_burn 同行时，只有后写的关键字生效。","VSIX/Error/EffectErrorTagger.cs");
                if (token.Keyword == ".heal" && later.Contains(".healstress"))
                    add(file,token.Line,token.Column,"error","VSIX-EFFECT-HEAL-ORDER",".heal 写在 .healstress 前时不生效。","VSIX/Error/EffectErrorTagger.cs");
                if (token.Keyword == ".cure" && later.Contains(".cure_disease"))
                    add(file,token.Line,token.Column,"error","VSIX-EFFECT-CURE-DISEASE-ORDER",".cure 写在 .cure_disease 前时不生效。","VSIX/Error/EffectErrorTagger.cs");
                if (token.Keyword == ".cure")
                    add(file,token.Line,token.Column,"info","VSIX-EFFECT-CURE-SUGGESTION","VSIX 建议优先使用 .cure_bleed 与 .cure_poison。","VSIX/Error/EffectErrorTagger.cs");
                if (token.Keyword == ".daze")
                    add(file,token.Line,token.Column,"info","VSIX-EFFECT-DAZE-SUGGESTION","VSIX 建议谨慎使用 daze，并确认其效果与崩溃风险。","VSIX/Error/EffectErrorTagger.cs");
                if (token.Keyword == ".affliction_blockable_chance")
                    add(file,token.Line,token.Column,"info","VSIX-EFFECT-AFFLICTION-CHANCE","VSIX 对该关键字显示崩溃风险建议。","VSIX/Error/EffectErrorTagger.cs");
            }
            var dots = tokens.Where(t => DotKeywords.Contains(t.Keyword)).ToList();
            if (dots.Select(t => t.Keyword).Distinct(StringComparer.Ordinal).Count() > 1)
                foreach (var token in dots.Skip(1))
                    add(file,token.Line,token.Column,"error","VSIX-EFFECT-DOT-CONFLICT","同一 Effect 行中出现多个 VSIX 判定互斥的 DOT/延迟扰乱关键字。","VSIX/Error/EffectErrorTagger.cs");

            foreach (var token in tokens)
            {
                var args = SyntaxUtils.ParseLineArguments(line,token,block.Tokens);
                if (TrinketKeywords.Contains(token.Keyword))
                {
                    bool requires = token.Keyword != ".destroy_trinket" || args.FirstOrDefault()?.Value.Equals("true",StringComparison.OrdinalIgnoreCase) == true;
                    var target = tokens.FirstOrDefault(t => t.Keyword == ".target");
                    string? targetValue = target is null ? null : SyntaxUtils.ParseLineArguments(line,target,block.Tokens).FirstOrDefault()?.Value;
                    if (requires && targetValue is not ("this_trinket" or "other_trinket"))
                        add(file,token.Line,token.Column,"warning","VSIX-EFFECT-TRINKET-TARGET",$"{token.Keyword} 要求同一行 .target 为 this_trinket/other_trinket。","VSIX/Error/EffectErrorTagger.cs");
                }
                if (token.Keyword == ".spawn_target_actor_base_class_id")
                {
                    var target = tokens.FirstOrDefault(t => t.Keyword == ".target");
                    if (target is not null && target.Start < token.Start)
                        add(file,token.Line,token.Column,"error","VSIX-EFFECT-SPAWN-TARGET-ORDER",".spawn_target_actor_base_class_id 必须写在 .target 前。","VSIX/Error/EffectErrorTagger.cs");
                }
            }
        }

        string First(string keyword)
        {
            var token = block.Tokens.FirstOrDefault(t => t.Keyword == keyword);
            return token is null ? string.Empty : SyntaxUtils.ParseLineArguments(lines[token.LineIndex],token,block.Tokens).FirstOrDefault()?.Value ?? string.Empty;
        }
        bool Has(string keyword) => block.Tokens.Any(t => t.Keyword == keyword && SyntaxUtils.ParseLineArguments(lines[t.LineIndex],t,block.Tokens).Count > 0);
        if (block.Tokens.Any(t => t.Keyword == ".use_item_id") && !block.Tokens.Any(t => t.Keyword == ".use_item_type"))
        {
            var t = block.Tokens.First(x => x.Keyword == ".use_item_id");
            add(file,t.Line,t.Column,"error","VSIX-EFFECT-USE-ITEM-TYPE-REQUIRED",".use_item_id 要求同一 Effect 内存在 .use_item_type。","VSIX/Error/EffectErrorTagger.cs");
        }
        ValidateBuffShorthand(file,block,lines,Has,First,add);
        ValidateUnsafeTargets(file,block,lines,Has,First,add);
        ValidateGuardChance(file,block,lines,First,add);

        foreach (var token in block.Tokens)
        {
            var line = lines[token.LineIndex];
            if (token.Keyword == ".set_mode")
            {
                var arg = SyntaxUtils.ParseLineArguments(line,token,block.Tokens).FirstOrDefault();
                if (arg is not null) CheckReference(file,arg.Line,arg.Column,arg.Value,modeIds,"KB-REF-MODE-NOT-FOUND", ".set_mode",strictReferences,
                    "知识库静态引用检查；Effect/keyword/Effect.set_mode.md; Info/headers/Info.mode.md",add);
            }
            if (token.Keyword == ".buff_ids")
                foreach (var arg in SyntaxUtils.ParseLineArguments(line,token,block.Tokens))
                    CheckReference(file,arg.Line,arg.Column,arg.Value,buffIds,"KB-REF-BUFF-NOT-FOUND",".buff_ids",strictReferences,
                        "知识库静态引用检查；Effect/keyword/Effect.buff_ids.md; Buff/buff_schema.md",add);
        }
    }

    private static void ValidateName(string file,SyntaxLine line,SyntaxToken token,IReadOnlyList<SyntaxToken> tokens,
        IReadOnlyList<SyntaxArgument> args,Action<string,int,int,string,string,string,string> add)
    {
        int start = token.Start - line.ParserOffset + token.Keyword.Length;
        int end = line.Code.Length;
        var next = tokens.Where(t => t.LineIndex == token.LineIndex && t.Start > token.Start).OrderBy(t => t.Start).FirstOrDefault();
        if (next is not null) end = next.Start - line.ParserOffset;
        string raw = line.Code[Math.Clamp(start,0,line.Code.Length)..Math.Clamp(end,start,line.Code.Length)].Trim();
        bool quoted = raw.StartsWith('"');
        string value = raw;
        if (quoted && raw.Length >= 1)
        {
            int close = raw.IndexOf('"',1);
            value = close >= 0 ? raw.Substring(1,close-1) : raw[1..];
        }
        value = value.Trim();
        if (string.IsNullOrEmpty(value)) add(file,token.Line,token.Column,"error","KB-EFFECT-EMPTY-NAME",".name 必须为非空 ID。","Effect/keyword/Effect.name.md");
        if (!quoted && value.Any(char.IsWhiteSpace)) add(file,token.Line,token.Column,"error","VSIX-EFFECT-NAME-WHITESPACE",".name 无引号时不能包含空格或制表符。","VSIX/Error/EffectErrorTagger.cs");
        int length = value.Count(c => !char.IsWhiteSpace(c));
        if (length > 64) add(file,token.Line,token.Column,"error","VSIX-EFFECT-NAME-TOO-LONG",$".name 长度不能超过 64 个字符（当前 {length}）。","VSIX/Error/EffectErrorTagger.cs");
        else if (length == 64) add(file,token.Line,token.Column,"warning","VSIX-EFFECT-NAME-AT-LIMIT",".name 长度已达到 64 个字符，建议缩短。","VSIX/Error/EffectErrorTagger.cs");
    }

    private static void ValidateKeywordValue(string file,SyntaxToken token,IReadOnlyList<SyntaxArgument> args,
        Action<string,int,int,string,string,string,string> add)
    {
        if (token.Keyword == ".buff_sub_type") return;
        if (UpdateRules.Data.GetProperty("effect_arguments").TryGetProperty(token.Keyword, out var kind))
        {
            if (args.Count != 1 || !UpdateRules.IsValidArgument(kind.GetString()!, args[0].Value))
                add(file, token.Line, token.Column, "error", "KB-UPDATE-EFFECT-ARGUMENT", $"{token.Keyword} 必须有且只有一个 {kind.GetString()} 参数。", "tools/local_mod_syntax_checker/update_rules.json");
            else if (kind.GetString() == "numeric_boolean" && args[0].Quoted)
                add(file, token.Line, token.Column, "error", "VSIX-EFFECT-QUOTED-NUMERIC-BOOL", $"{token.Keyword} 的数值布尔参数不应带引号。", "VSIX/Error/EffectErrorTagger.cs");
            return;
        }
        if (!DarkestEffectsData.KeywordToValuesMap.TryGetValue(token.Keyword,out var baseValues) || args.Count == 0) return;
        var values = baseValues;
        if (DarkestEffectsData.DoubleBoolKeywords.Contains(token.Keyword)) values = DarkestEffectsData.DoubleBoolValuesForError;
        else if (ReferenceEquals(baseValues,DarkestEffectsData.StrBoolValues)) values = DarkestEffectsData.StrBoolValuesForError;
        string value = args[0].Value;
        bool valid = values.Contains(value), allowedCustom = false;
        if (token.Keyword == ".steal_buff_source_type")
        {
            if (value == "bsrc_district") add(file,token.Line,token.Column,"warning","VSIX-EFFECT-STEAL-SOURCE-RISK","建筑源 Buff 不可再生，请谨慎偷取/驱散。","VSIX/Error/EffectErrorTagger.cs");
            else if (value == "bsrc_skill") add(file,token.Line,token.Column,"warning","VSIX-EFFECT-STEAL-SOURCE-RISK","谨慎偷取/驱散技能源，以防破坏其他机制。","VSIX/Error/EffectErrorTagger.cs");
            else if (!valid) { allowedCustom = true; add(file,token.Line,token.Column,"warning","VSIX-EFFECT-CUSTOM-SOURCE","自定义 Buff 源会被视为 combat_end 源。","VSIX/Error/EffectErrorTagger.cs"); }
        }
        else if (token.Keyword == ".steal_buff_stat_type")
        {
            var cautious = new[] { "hp_dot_bleed","hp_dot_poison","hp_dot_heal","stress_dot","shuffle_dot","tag","stealth" };
            if (!cautious.Contains(value,StringComparer.Ordinal)) add(file,token.Line,token.Column,"warning","VSIX-EFFECT-STEAL-STAT-RISK","慎用超级真驱散，以免破坏其他机制。","VSIX/Error/EffectErrorTagger.cs");
        }
        else if (token.Keyword == ".buff_duration_type" && value == "none")
            add(file,args[0].Line,args[0].Column,"warning","VSIX-EFFECT-DURATION-NONE","Effect 中的 none 持续类型会被视为 round。","VSIX/Error/EffectErrorTagger.cs");
        else if ((token.Keyword is ".dotSource" or ".buff_source_type") && !valid)
        { allowedCustom = true; add(file,token.Line,token.Column,"warning","VSIX-EFFECT-CUSTOM-SOURCE","自定义 Buff 源会被视为 combat_end 源。","VSIX/Error/EffectErrorTagger.cs"); }
        if (!valid && !allowedCustom)
            add(file,args[0].Line,args[0].Column,"error","VSIX-EFFECT-INVALID-VALUE",$"值 '{value}' 对关键字 '{token.Keyword}' 无效。","VSIX/Error/EffectErrorTagger.cs");
        else if (args[0].Quoted && DarkestEffectsData.NumBoolValues.Contains(value))
            add(file,args[0].Line,args[0].Column,"error","VSIX-EFFECT-QUOTED-NUMERIC-BOOL",$"值 '{value}' 不应带引号。","VSIX/Error/EffectErrorTagger.cs");
    }

    private static void ValidateLimitedList(string file,SyntaxToken token,IReadOnlyList<SyntaxArgument> args,
        Action<string,int,int,string,string,string,string> add)
    {
        foreach (var arg in args)
        {
            int length = arg.Value.Count(c => !char.IsWhiteSpace(c));
            if (length > 64) add(file,arg.Line,arg.Column,"error","VSIX-EFFECT-ARG-TOO-LONG",$"{token.Keyword} 参数长度超过 64 个字符。","VSIX/Error/EffectErrorTagger.cs");
            else if (length == 64) add(file,arg.Line,arg.Column,"warning","VSIX-EFFECT-ARG-AT-LIMIT",$"{token.Keyword} 参数已达到 64 个字符，建议缩短。","VSIX/Error/EffectErrorTagger.cs");
            if (arg.Quoted && arg.Value.Any(char.IsWhiteSpace))
                add(file,arg.Line,arg.Column,token.Keyword == ".buff_ids" ? "warning" : "error","VSIX-EFFECT-QUOTED-LIST-WHITESPACE",$"{token.Keyword} 引号内参数不建议包含空格或制表符。","VSIX/Error/EffectErrorTagger.cs");
        }
        if (args.Count > 8) add(file,token.Line,token.Column,"error","VSIX-EFFECT-TOO-MANY-LIST-ARGS",$"{token.Keyword} 参数数量超过 8 个。","VSIX/Error/EffectErrorTagger.cs");
        else if (args.Count == 8) add(file,token.Line,token.Column,"info","VSIX-EFFECT-LIST-ARGS-AT-LIMIT",$"{token.Keyword} 参数数量已达到 8 个。","VSIX/Error/EffectErrorTagger.cs");
    }

    private static void ValidateBuffShorthand(string file,Block block,IReadOnlyList<SyntaxLine> lines,
        Func<string,bool> has,Func<string,string> first,Action<string,int,int,string,string,string,string> add)
    {
        foreach (var token in block.Tokens.Where(t => t.Keyword == ".buff_type"))
        {
            string type = first(".buff_type"), subtype = first(".buff_sub_type");
            if (string.IsNullOrEmpty(type)) continue;
            if (!has(".buff_amount")) add(file,token.Line,token.Column,"error","VSIX-EFFECT-BUFF-AMOUNT-REQUIRED","简写 Buff 必须包含 .buff_amount。","VSIX/Error/EffectErrorTagger.cs");
            if (DarkestEffectsData.MustHaveSubBuffTypes.Contains(type) &&
                (!has(".buff_sub_type") || (DarkestEffectsData.SubFreeBuffTypes.Contains(type) && string.IsNullOrWhiteSpace(subtype))))
                add(file,token.Line,token.Column,"error","VSIX-EFFECT-BUFF-SUBTYPE-REQUIRED",$"{type} 类型必须声明 .buff_sub_type。","VSIX/Error/EffectErrorTagger.cs");
            else if (DarkestEffectsData.BuffTypeToSubTypesMap.TryGetValue(type,out var allowed) && has(".buff_sub_type") && !allowed.Contains(subtype))
                add(file,token.Line,token.Column,"error","VSIX-EFFECT-BUFF-SUBTYPE-INVALID",$"{subtype} 不属于 {type}。","VSIX/Error/EffectErrorTagger.cs");
            else if (!DarkestEffectsData.SubFreeBuffTypes.Contains(type) && !DarkestEffectsData.BuffTypeToSubTypesMap.ContainsKey(type) && has(".buff_sub_type"))
                add(file,token.Line,token.Column,"error","VSIX-EFFECT-BUFF-SUBTYPE-UNEXPECTED",$"{type} 类型不接受 .buff_sub_type。","VSIX/Error/EffectErrorTagger.cs");
        }
    }

    private static void ValidateUnsafeTargets(string file,Block block,IReadOnlyList<SyntaxLine> lines,
        Func<string,bool> has,Func<string,string> first,Action<string,int,int,string,string,string,string> add)
    {
        bool hasForbidden = block.Tokens.Where(t => t.Keyword == ".target").Any(t =>
        {
            string value = SyntaxUtils.ParseLineArguments(lines[t.LineIndex],t,block.Tokens).FirstOrDefault()?.Value ?? string.Empty;
            return value is "target" or "target_enemy_group";
        });
        bool hasPerformerTarget = block.Tokens.Where(t => t.Keyword == ".target").Any(t =>
        {
            string value = SyntaxUtils.ParseLineArguments(lines[t.LineIndex],t,block.Tokens).FirstOrDefault()?.Value ?? string.Empty;
            return value.Length > 0 && value is not ("target" or "target_enemy_group");
        });
        foreach (var token in block.Tokens.Where(t => t.Keyword is ".keyStatus" or ".monsterType" or ".skill_instant"))
        {
            bool active = token.Keyword is ".keyStatus" or ".monsterType" || first(".skill_instant") == "true";
            bool issue = token.Keyword is ".keyStatus" or ".monsterType" ? hasForbidden : !hasPerformerTarget;
            if (active && issue)
                add(file,token.Line,token.Column,"error","VSIX-EFFECT-UNSAFE-TARGET",".keyStatus/.monsterType/.skill_instant 组合要求避免危险的 target/target_enemy_group 目标，并提供安全目标。","VSIX/Error/EffectErrorTagger.cs");
        }
    }

    private static void ValidateGuardChance(string file,Block block,IReadOnlyList<SyntaxLine> lines,Func<string,string> first,
        Action<string,int,int,string,string,string,string> add)
    {
        var chances = block.Tokens.Where(t => t.Keyword == ".chance").ToList();
        bool active = first(".on_hit").Equals("true",StringComparison.OrdinalIgnoreCase) || first(".on_miss").Equals("true",StringComparison.OrdinalIgnoreCase);
        if (!active || chances.Count == 0 || block.Tokens.Any(token => token.Keyword == ".force_resist_type")) return;
        foreach (var guard in block.Tokens.Where(t => t.Keyword is ".guard" or ".clearguarded" or ".clearguarding"))
        {
            string guardValue = SyntaxUtils.ParseLineArguments(lines[guard.LineIndex],guard,block.Tokens).FirstOrDefault()?.Value ?? string.Empty;
            if (guardValue != "1") continue;
            bool below = chances.Any(chance =>
            {
                string value = SyntaxUtils.ParseLineArguments(lines[chance.LineIndex],chance,block.Tokens).FirstOrDefault()?.Value ?? string.Empty;
                return value.EndsWith('%')
                    ? double.TryParse(value[..^1],System.Globalization.NumberStyles.Float,System.Globalization.CultureInfo.InvariantCulture,out var pct) && pct < 100
                    : double.TryParse(value,System.Globalization.NumberStyles.Float,System.Globalization.CultureInfo.InvariantCulture,out var n) && n < 1;
            });
            if (below) add(file,guard.Line,guard.Column,"warning","VSIX-EFFECT-GUARD-CHANCE","守护和移除守护无法被 .chance 制约。","VSIX/Error/EffectErrorTagger.cs");
        }
    }

    private static void CheckReference(string file,int line,int column,string id,IReadOnlySet<string> ids,string code,
        string keyword,bool strict,string source,Action<string,int,int,string,string,string,string> add)
    {
        if (string.IsNullOrWhiteSpace(id) || ids.Contains(id)) return;
        add(file,line,column,strict ? "error" : "warning",code,
            $"{keyword} 引用的 ID '{id}' 未在 Mod/引用目录找到定义；原版、DLC 或依赖 Mod 的 ID 请追加 --reference-root。",
            "当前用户要求的本地引用检查；"+source);
    }
}
