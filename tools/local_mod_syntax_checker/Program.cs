using System.Text;
using System.Text.Json;

namespace LocalModSyntaxChecker;

internal static class Program
{
    private static int Main(string[] args)
    {
        if (args.Length == 0 || args.Contains("--help", StringComparer.Ordinal) || args.Contains("-h", StringComparer.Ordinal))
        {
            Diagnostics.WriteHelp();
            return args.Length == 0 ? 2 : 0;
        }
        try
        {
            UpdateRules.Apply();
            var options = Options.Parse(args);
            var result = new ModChecker(options).Run();
            if (options.Json)
            {
                Console.OutputEncoding = new UTF8Encoding(false);
                Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions
                {
                    WriteIndented = true,
                    Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
                }));
            }
            else
            {
                foreach (var issue in result.Diagnostics)
                {
                    string location = issue.Line > 0 ? $":{issue.Line}:{Math.Max(1, issue.Column)}" : string.Empty;
                    Console.WriteLine($"{issue.File}{location}: {issue.Severity.ToUpperInvariant()} {issue.Code}: {issue.Message} [{issue.Source}]");
                }
                Console.WriteLine($"检查完成：文件 {result.FilesScanned}，错误 {result.ErrorCount}，警告 {result.WarningCount}，提示 {result.InfoCount}。");
            }
            return result.ErrorCount > 0 ? 1 : 0;
        }
        catch (ArgumentException e)
        {
            Console.Error.WriteLine($"参数错误：{e.Message}");
            Diagnostics.WriteHelp();
            return 2;
        }
        catch (Exception e)
        {
            Console.Error.WriteLine($"检查器失败：{e.Message}");
            return 2;
        }
    }
}
