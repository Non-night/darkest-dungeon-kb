using System.Text;

namespace LocalModSyntaxChecker;

internal sealed record Diagnostic(string File, int Line, int Column, string Severity, string Code, string Message, string Source);
internal sealed record CheckerResult(string Root, int FilesScanned, int ErrorCount, int WarningCount, int InfoCount, IReadOnlyList<Diagnostic> Diagnostics);
internal sealed record Options(string Root, IReadOnlyList<string> ReferenceRoots, bool StrictReferences, bool Json, bool SkipBuffs)
{
    public static Options Parse(string[] args)
    {
        string? root = null;
        var refs = new List<string>();
        bool strict = false, json = false, skipBuffs = false;
        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "--root": root = Next(args, ref i); break;
                case "--reference-root": refs.Add(Next(args, ref i)); break;
                case "--strict-references": strict = true; break;
                case "--json": json = true; break;
                case "--no-buffs": skipBuffs = true; break;
                default: throw new ArgumentException($"未知选项：{args[i]}");
            }
        }
        if (string.IsNullOrWhiteSpace(root)) throw new ArgumentException("必须指定 --root <Mod根目录>。");
        root = Path.GetFullPath(root);
        if (!Directory.Exists(root)) throw new ArgumentException($"Mod 根目录不存在：{root}");
        refs = refs.Select(Path.GetFullPath).Distinct(StringComparer.OrdinalIgnoreCase).ToList();
        foreach (var path in refs) if (!Directory.Exists(path)) throw new ArgumentException($"引用目录不存在：{path}");
        return new Options(root, refs, strict, json, skipBuffs);
    }
    private static string Next(string[] args, ref int i)
    {
        if (i + 1 >= args.Length || args[i + 1].StartsWith("--", StringComparison.Ordinal))
            throw new ArgumentException($"{args[i]} 缺少参数。");
        return args[++i];
    }
}

internal static class Diagnostics
{
    public static int Order(string severity) => severity switch { "error" => 0, "warning" => 1, _ => 2 };
    public static string Relative(string root, string file)
    {
        try { return Path.GetRelativePath(root, file).Replace('\\', '/'); }
        catch { return file; }
    }
    public static void WriteHelp()
    {
        Console.WriteLine("Darkest Dungeon Mod 本地语法检查器（只读）");
        Console.WriteLine("用法：dotnet run --project tools/local_mod_syntax_checker/LocalModSyntaxChecker.csproj -- --root <Mod根目录> [选项]");
        Console.WriteLine("  --reference-root <目录>  追加游戏本体、DLC 或依赖 Mod 的 ID 检索目录，可重复");
        Console.WriteLine("  --strict-references      把扫描范围内未解析的 ID 引用从警告升为错误");
        Console.WriteLine("  --json                   输出机器可读 JSON");
        Console.WriteLine("  --no-buffs               跳过 BuffGrammarChecker.Core 检查");
        Console.WriteLine("首次运行需要 .NET 8 SDK；检查过程不会修复或改写文件。");
    }
}
