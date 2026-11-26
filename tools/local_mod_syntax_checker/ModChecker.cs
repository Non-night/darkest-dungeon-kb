using System.Text;
using System.Text.Json;
using BuffGrammarChecker.Core;

namespace LocalModSyntaxChecker;

internal sealed class ModChecker
{
    private static readonly UTF8Encoding StrictUtf8 = new(false, true);
    private static readonly HashSet<string> SkippedDirectories = new(StringComparer.OrdinalIgnoreCase)
    {
        "bin", "obj", "node_modules", "packages", "__pycache__"
    };
    private readonly Options _options;
    private readonly List<Diagnostic> _diagnostics = new();
    private readonly Dictionary<string, string?> _textCache = new(StringComparer.OrdinalIgnoreCase);
    private readonly HashSet<string> _effectIds = new(StringComparer.Ordinal);
    private readonly HashSet<string> _modeIds = new(StringComparer.Ordinal);
    private readonly HashSet<string> _buffIds = new(StringComparer.Ordinal);
    private readonly HashSet<string> _colourIds = new(StringComparer.Ordinal);
    private List<string> _rootFiles = new();
    private List<string> _referenceFiles = new();
    private int _filesScanned;

    public ModChecker(Options options) => _options = options;

    public CheckerResult Run()
    {
        _rootFiles = EnumerateFiles(_options.Root).ToList();
        _referenceFiles = _options.ReferenceRoots.SelectMany(EnumerateFiles).ToList();
        // 先检查目标 Mod 的编码，再建立 ID 索引，避免索引阶段缓存跳过 BOM 诊断。
        foreach (var file in _rootFiles)
            if (Path.GetFileName(file).EndsWith(".darkest", StringComparison.OrdinalIgnoreCase) || Path.GetFileName(file).EndsWith(".json", StringComparison.OrdinalIgnoreCase))
                ReadUtf8(file, reportEncoding: true);
        BuildReferenceIndexes();

        foreach (string file in _rootFiles)
        {
            string name = Path.GetFileName(file);
            bool darkest = name.EndsWith(".darkest", StringComparison.OrdinalIgnoreCase);
            bool json = name.EndsWith(".json", StringComparison.OrdinalIgnoreCase);
            bool localization = name.EndsWith(".string_table.xml", StringComparison.OrdinalIgnoreCase);
            if (localization)
            {
                _filesScanned++;
                LocalizationSyntax.Validate(file, _options.Root, _colourIds, _options.StrictReferences, Add);
                continue;
            }
            if (!darkest && !json) continue;
            _filesScanned++;
            string? text = ReadUtf8(file, reportEncoding: false);
            if (text is null) continue;

            UpdateRules.ReportPartialCoverage(file, text, Add);

            if (Ends(name, ".colours.darkest"))
            {
                if (!IsColourScanPath(file))
                    Add(file, 1, 1, "warning", "KB-COLOUR-WRONG-DIRECTORY", "localization.exe 已确认扫描项目根目录 colours/*.colours.darkest；此颜色文件路径可能不在扫描范围。", "Mechanics/16-loc与loc2本地化覆盖优先级.md");
            }
            else if (Ends(name, ".info.darkest", ".art.darkest", ".override.darkest"))
            {
                if (Ends(name, ".info.darkest"))
                    foreach (var line in SyntaxUtils.BuildLines(text))
                        if (line.Code.Length >= 511)
                            Add(file, line.Number, 511, "error", "KB-INFO-LINE-OVERFLOW", "Info 非注释行长度达到或超过 511 个字符，可能被引擎截断。", "Info/README.md; RAG/mechanic-card:info-line-length-overflow");
                InfoSyntax.Validate(file, text, _modeIds, _effectIds, _options.StrictReferences, Add);
            }
            else if (Ends(name, ".effects.darkest"))
            {
                ValidateEffectFilePath(file, name);
                EffectSyntax.Validate(file, text, _buffIds, _modeIds, _effectIds, _options.StrictReferences, Add);
            }
            if (!_options.SkipBuffs && IsBuffCandidate(file)) ValidateBuff(file);
        }

        var diagnostics = _diagnostics
            .OrderBy(d => d.File, StringComparer.OrdinalIgnoreCase)
            .ThenBy(d => d.Line)
            .ThenBy(d => d.Column)
            .ThenBy(d => Diagnostics.Order(d.Severity))
            .ThenBy(d => d.Code, StringComparer.Ordinal)
            .ToArray();
        return new CheckerResult(_options.Root, _filesScanned,
            diagnostics.Count(d => d.Severity == "error"),
            diagnostics.Count(d => d.Severity == "warning"),
            diagnostics.Count(d => d.Severity == "info"), diagnostics);
    }

    private void BuildReferenceIndexes()
    {
        foreach (var file in _rootFiles.Concat(_referenceFiles).Distinct(StringComparer.OrdinalIgnoreCase))
        {
            string name = Path.GetFileName(file);
            bool effectFile = Ends(name, ".effects.darkest");
            bool infoFile = Ends(name, ".info.darkest");
            bool colourFile = Ends(name, ".colours.darkest") && IsColourScanPath(file);
            bool buffFile = IsBuffCandidate(file);
            if (!effectFile && !infoFile && !colourFile && !buffFile) continue;
            string? text = ReadUtf8(file, reportEncoding: false);
            if (text is null) continue;
            if (effectFile)
                foreach (string id in EffectSyntax.IndexNames(text)) _effectIds.Add(id);
            else if (infoFile)
                foreach (string id in InfoSyntax.IndexModeIds(text)) _modeIds.Add(id);
            else if (colourFile)
                foreach (string id in IndexColourIds(text)) _colourIds.Add(id);
            else if (buffFile)
                foreach (string id in IndexBuffIds(text)) _buffIds.Add(id);
        }
    }

    private bool IsColourScanPath(string file)
    {
        foreach (var root in new[] { _options.Root }.Concat(_options.ReferenceRoots))
        {
            string relative = Path.GetRelativePath(root, file).Replace('\\', '/');
            const string prefix = "colours/";
            if (!relative.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)) continue;
            if (!relative[prefix.Length..].Contains('/')) return true;
        }
        return false;
    }

    private void ValidateEffectFilePath(string file, string fileName)
    {
        const string suffix = ".effects.darkest";
        string relative = Path.GetRelativePath(_options.Root, file).Replace('\\', '/');
        if (!relative.StartsWith("effects/", StringComparison.OrdinalIgnoreCase))
            Add(file, 1, 1, "warning", "KB-EFFECT-WRONG-DIRECTORY", "Effect 定义文件通常应放在 Mod 根目录的 effects/ 下；仅语法正确不能证明游戏会扫描该路径。", "RAG/effect_basics.jsonl; Mechanics/24-Mod识别与职业Mod目录结构.md");
        string prefix = fileName.EndsWith(suffix, StringComparison.OrdinalIgnoreCase) ? fileName[..^suffix.Length] : string.Empty;
        if (prefix.Length == 0)
            Add(file, 1, 1, "error", "KB-EFFECT-FILE-PREFIX-EMPTY", "Effect 文件名必须包含非空自定义前缀并以 .effects.darkest 结尾。", "RAG/effect_basics.jsonl");
    }

    private void ValidateBuff(string file)
    {
        try
        {
            var result = new BuffFileValidator().ValidateFile(file);
            foreach (var issue in result.Issues)
            {
                string severity = issue.Severity switch
                {
                    ValidationSeverity.Error => "error",
                    ValidationSeverity.Warning => "warning",
                    _ => "info"
                };
                Add(file, issue.LineNumber ?? 1, issue.ColumnNumber ?? 1, severity,
                    "BUFF-" + issue.Code, issue.Message, "tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core");
            }
        }
        catch (Exception e)
        {
            Add(file, 1, 1, "error", "BUFF-CHECKER-FAILED", $"调用 BuffGrammarChecker.Core 失败：{e.Message}", "tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core");
        }
    }

    private static IReadOnlyList<string> IndexBuffIds(string text)
    {
        var ids = new List<string>();
        try
        {
            using var doc = JsonDocument.Parse(text);
            if (!doc.RootElement.TryGetProperty("buffs", out var buffs) || buffs.ValueKind != JsonValueKind.Array) return ids;
            foreach (var buff in buffs.EnumerateArray())
                if (buff.ValueKind == JsonValueKind.Object && buff.TryGetProperty("id", out var id) && id.ValueKind == JsonValueKind.String && !string.IsNullOrWhiteSpace(id.GetString()))
                    ids.Add(id.GetString()!);
        }
        catch (JsonException) { }
        return ids;
    }

    private static IEnumerable<string> IndexColourIds(string text)
    {
        string? header = null;
        var idRegex = new System.Text.RegularExpressions.Regex(@"\.id\s+(?:""(?<q>[^""]*)""|(?<p>[^\s]+))",System.Text.RegularExpressions.RegexOptions.Compiled);
        foreach (var line in SyntaxUtils.BuildLines(text))
        {
            var match = SyntaxUtils.HeaderRegex.Match(line.Code);
            if (match.Success) header = match.Groups["header"].Value;
            if (header != "colour:") continue;
            foreach (System.Text.RegularExpressions.Match id in idRegex.Matches(line.Code))
            {
                var value = id.Groups["q"].Success ? id.Groups["q"].Value : id.Groups["p"].Value;
                if (!string.IsNullOrWhiteSpace(value)) yield return value;
            }
        }
    }

    private bool IsBuffCandidate(string file)
    {
        string name = Path.GetFileName(file);
        if (name.EndsWith(".buffs.json", StringComparison.OrdinalIgnoreCase)) return true;
        if (!name.EndsWith(".json", StringComparison.OrdinalIgnoreCase)) return false;
        foreach (var root in new[] { _options.Root }.Concat(_options.ReferenceRoots))
        {
            string relative = Path.GetRelativePath(root, file).Replace('\\', '/');
            if (relative.StartsWith("shared/buffs/", StringComparison.OrdinalIgnoreCase)) return true;
        }
        return false;
    }

    private string? ReadUtf8(string file, bool reportEncoding)
    {
        if (_textCache.TryGetValue(file, out var cached)) return cached;
        try
        {
            byte[] bytes = File.ReadAllBytes(file);
            bool bom = bytes.Length >= 3 && bytes[0] == 0xEF && bytes[1] == 0xBB && bytes[2] == 0xBF;
            if (bom && reportEncoding)
                Add(file, 1, 1, "error", "KB-ENC-UTF8-BOM", "*.darkest 与 *.json 必须保存为 UTF-8 无 BOM。", "Mechanics/42-JSON与Darkest文件的UTF-8无BOM硬性要求.md");
            string text = StrictUtf8.GetString(bytes, bom ? 3 : 0, bytes.Length - (bom ? 3 : 0));
            _textCache[file] = text;
            return text;
        }
        catch (DecoderFallbackException e)
        {
            if (reportEncoding) Add(file, 1, 1, "error", "KB-ENC-NOT-UTF8", $"文本不是有效 UTF-8：{e.Message}", "Mechanics/42-JSON与Darkest文件的UTF-8无BOM硬性要求.md");
            _textCache[file] = null;
            return null;
        }
        catch (IOException e)
        {
            if (reportEncoding) Add(file, 1, 1, "error", "IO-READ", $"无法读取：{e.Message}", "本地文件读取");
            _textCache[file] = null;
            return null;
        }
    }

    private void Add(string file, int line, int column, string severity, string code, string message, string source)
        => _diagnostics.Add(new Diagnostic(Diagnostics.Relative(_options.Root, file), Math.Max(1, line), Math.Max(1, column), severity, code, message, source));

    private static bool Ends(string value, params string[] suffixes)
        => suffixes.Any(s => value.EndsWith(s, StringComparison.OrdinalIgnoreCase));

    private static IEnumerable<string> EnumerateFiles(string root)
    {
        if (Path.GetFileName(Path.TrimEndingDirectorySeparator(root)).StartsWith('.')) yield break;
        var pending = new Stack<string>(); pending.Push(root);
        while (pending.Count > 0)
        {
            string current = pending.Pop();
            string[] files, dirs;
            try { files = Directory.GetFiles(current); dirs = Directory.GetDirectories(current); }
            catch { continue; }
            foreach (var file in files)
            {
                if (!Path.GetFileName(file).StartsWith('.')) yield return file;
            }
            foreach (var dir in dirs)
            {
                string name = Path.GetFileName(dir);
                if (name.StartsWith('.') || SkippedDirectories.Contains(name)) continue;
                try { if ((File.GetAttributes(dir) & FileAttributes.ReparsePoint) != 0) continue; }
                catch { continue; }
                pending.Push(dir);
            }
        }
    }
}

