using System.Text;
using System.Text.RegularExpressions;

namespace LocalModSyntaxChecker;

internal sealed record SyntaxLine(int Number, int ParserOffset, string Raw, string Code, int CommentIndex);
internal sealed record SyntaxToken(string Keyword, string Header, int LineIndex, int Line, int Column, int Start, int End);
internal sealed record SyntaxArgument(string Value, bool Quoted, int Line, int Column);
internal sealed record SyntaxField(SyntaxToken Token, IReadOnlyList<SyntaxArgument> Arguments, string RawArguments);

internal static class SyntaxUtils
{
    public static readonly Regex KeywordRegex = new(@"\.[a-zA-Z_][a-zA-Z0-9_]*", RegexOptions.Compiled);
    public static readonly Regex HeaderRegex = new(@"^[ \t]*(?<header>[a-zA-Z0-9_]+:)", RegexOptions.Compiled);
    private static readonly Regex StringsRegex = new(@"""[^""]*""", RegexOptions.Compiled);

    public static List<SyntaxLine> BuildLines(string text)
    {
        string normalized = text.Replace("\r\n", "\n", StringComparison.Ordinal).Replace('\r', '\n');
        var rawLines = normalized.Split('\n');
        var result = new List<SyntaxLine>(rawLines.Length);
        int offset = 0;
        for (int i = 0; i < rawLines.Length; i++)
        {
            string raw = rawLines[i];
            int comment = raw.IndexOf("//", StringComparison.Ordinal);
            string code = comment >= 0 ? raw[..comment] : raw;
            result.Add(new SyntaxLine(i + 1, offset, raw, code, comment));
            offset += code.Length + 1;
        }
        return result;
    }

    public static List<SyntaxToken> FindKeywords(SyntaxLine line, int lineIndex, string? header)
    {
        var result = new List<SyntaxToken>();
        var spans = StringsRegex.Matches(line.Code).Cast<Match>().Select(m => (m.Index, m.Index + m.Length)).ToArray();
        foreach (Match match in KeywordRegex.Matches(line.Code))
        {
            if (spans.Any(s => match.Index >= s.Index && match.Index < s.Item2)) continue;
            if (match.Index > 0 && char.IsDigit(line.Code[match.Index - 1])) continue;
            result.Add(new SyntaxToken(match.Value, header ?? string.Empty, lineIndex, line.Number,
                match.Index + 1, line.ParserOffset + match.Index, line.ParserOffset + match.Index + match.Length));
        }
        return result;
    }

    public static List<SyntaxField> MakeFields(string parserText, IReadOnlyList<SyntaxLine> lines,
        IReadOnlyList<SyntaxToken> tokens, IReadOnlyList<int> headerBoundaries)
    {
        var ordered = tokens.OrderBy(t => t.Start).ToArray();
        var fields = new List<SyntaxField>(ordered.Length);
        for (int i = 0; i < ordered.Length; i++)
        {
            var token = ordered[i];
            int end = i + 1 < ordered.Length ? ordered[i + 1].Start : parserText.Length;
            int headerBoundary = headerBoundaries.Where(h => h > token.Start).DefaultIfEmpty(int.MaxValue).Min();
            end = Math.Min(end, headerBoundary);
            end = Math.Max(token.End, end);
            string raw = parserText.Substring(token.End, end - token.End);
            fields.Add(new SyntaxField(token, ParseArguments(raw, token.End, lines), raw));
        }
        return fields;
    }

    public static List<SyntaxArgument> ParseArguments(string raw, int absoluteStart, IReadOnlyList<SyntaxLine> lines)
    {
        var result = new List<SyntaxArgument>();
        int i = 0;
        while (i < raw.Length)
        {
            while (i < raw.Length && char.IsWhiteSpace(raw[i])) i++;
            if (i >= raw.Length) break;
            int start = i;
            bool quoted = raw[i] == '"';
            string value;
            if (quoted)
            {
                int contentStart = ++i;
                while (i < raw.Length && raw[i] != '"') i++;
                value = raw.Substring(contentStart, i - contentStart);
                if (i < raw.Length) i++;
            }
            else
            {
                while (i < raw.Length && !char.IsWhiteSpace(raw[i])) i++;
                value = raw.Substring(start, i - start);
            }
            var location = Locate(absoluteStart + start, lines);
            result.Add(new SyntaxArgument(value, quoted, location.Line, location.Column));
        }
        return result;
    }

    public static List<SyntaxArgument> ParseLineArguments(SyntaxLine line, SyntaxToken token, IReadOnlyList<SyntaxToken> tokens)
    {
        int start = token.Start - line.ParserOffset + token.Keyword.Length;
        int end = line.Code.Length;
        foreach (var next in tokens.Where(t => t.LineIndex == token.LineIndex && t.Start > token.Start))
            end = Math.Min(end, next.Start - line.ParserOffset);
        start = Math.Clamp(start, 0, line.Code.Length);
        end = Math.Clamp(end, start, line.Code.Length);
        return ParseArguments(line.Code[start..end], line.ParserOffset + start, new[] { line });
    }

    public static (int Line, int Column) Locate(int parserOffset, IReadOnlyList<SyntaxLine> lines)
    {
        for (int i = lines.Count - 1; i >= 0; i--)
        {
            var line = lines[i];
            int end = line.ParserOffset + line.Code.Length;
            if (parserOffset >= line.ParserOffset && parserOffset <= end)
                return (line.Number, parserOffset - line.ParserOffset + 1);
        }
        return (lines.Count > 0 ? lines[^1].Number : 1, 1);
    }

    public static void CheckLexical(string file, SyntaxLine line, string type,
        Action<string, int, int, string, string, string, string> add)
    {
        if (string.IsNullOrWhiteSpace(line.Code)) return;
        string source = type == "effect" ? "VSIX/Error/EffectErrorTagger.cs" : "VSIX/Error/InfoBaseErrorTagger.cs";
        if (line.CommentIndex >= 0)
            add(file, line.Number, line.CommentIndex + 1, type == "effect" ? "warning" : "error",
                type == "effect" ? "VSIX-EFFECT-INLINE-COMMENT" : "VSIX-INFO-INLINE-COMMENT",
                type == "effect" ? "请尽可能避免行内注释，以防游戏识别错误。" : "Info/Art/Override 行内注释可能造成识别错误，请避免。", source);
        CheckChinese(file, line, type, add, source);
        int quotes = line.Code.Count(c => c == '"');
        if (quotes % 2 != 0)
            add(file, line.Number, Math.Max(1, line.Code.LastIndexOf('"') + 1), "error",
                $"VSIX-{type.ToUpperInvariant()}-UNPAIRED-QUOTE", "单行内引号不成对。", source);
        bool inString = false;
        for (int i = 0; i < line.Code.Length; i++)
        {
            if (line.Code[i] != '"') continue;
            if (!inString)
            {
                if (i > 0 && !char.IsWhiteSpace(line.Code[i - 1]))
                    add(file, line.Number, i + 1, "error", $"VSIX-{type.ToUpperInvariant()}-QUOTE-LEFT-ADJACENT",
                        "引号前紧贴普通字符；请用空格分隔或把整个参数放入引号。", source);
                inString = true;
            }
            else
            {
                if (i + 1 < line.Code.Length && !char.IsWhiteSpace(line.Code[i + 1]))
                {
                    bool nextKeyword = line.Code[i + 1] == '.';
                    add(file, line.Number, i + 1, nextKeyword ? "warning" : "error",
                        $"VSIX-{type.ToUpperInvariant()}-QUOTE-RIGHT-ADJACENT",
                        nextKeyword ? "引号后紧接下一个关键字，建议用空格分隔。" : "引号后紧贴普通字符；请用空格分隔。", source);
                }
                inString = false;
            }
        }
    }

    private static void CheckChinese(string file, SyntaxLine line, string type,
        Action<string, int, int, string, string, string, string> add, string source)
    {
        int runStart = -1, runEnd = -1;
        for (int i = 0; i <= line.Code.Length;)
        {
            bool end = i >= line.Code.Length;
            int cp = 0, width = 1;
            if (!end)
            {
                if (char.IsHighSurrogate(line.Code[i]) && i + 1 < line.Code.Length && char.IsLowSurrogate(line.Code[i + 1]))
                { cp = char.ConvertToUtf32(line.Code[i], line.Code[i + 1]); width = 2; }
                else cp = line.Code[i];
            }
            bool bad = !end && IsChineseOrPunctuation(cp);
            if (bad)
            {
                if (runStart < 0) runStart = i;
                runEnd = i + width;
                i += width;
            }
            else
            {
                if (runStart >= 0)
                {
                    string value = line.Code.Substring(runStart, runEnd - runStart);
                    add(file, line.Number, runStart + 1, "error", $"VSIX-{type.ToUpperInvariant()}-NON-ASCII-CJK",
                        $"代码区不允许中文字符或中文标点：{value}", source);
                    runStart = -1;
                }
                i += width;
            }
        }
    }

    private static bool IsChineseOrPunctuation(int c) =>
        c is >= 0x3400 and <= 0x4DBF or >= 0x4E00 and <= 0x9FFF or >= 0xF900 and <= 0xFAFF or
        >= 0x20000 and <= 0x2A6DF or >= 0x2A700 and <= 0x2B73F or >= 0x2B740 and <= 0x2B81F or
        >= 0x2B820 and <= 0x2CEAF or >= 0x2CEB0 and <= 0x2EBEF or >= 0x30000 and <= 0x3134F or
        >= 0x31350 and <= 0x323AF or >= 0x3000 and <= 0x303F or >= 0xFE10 and <= 0xFE1F or
        >= 0xFE30 and <= 0xFE4F or >= 0xFF01 and <= 0xFF0F or >= 0xFF1A and <= 0xFF20 or
        >= 0xFF3B and <= 0xFF40 or >= 0xFF5B and <= 0xFF65;
}
