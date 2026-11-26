namespace BuffGrammarChecker.Core;

public sealed record BuffBatchValidationOptions(
    string FolderPath,
    string? FileNamePattern = null,
    bool SearchSubdirectories = false);

public sealed record BuffBatchFileResult(
    string FilePath,
    ValidationResult ValidationResult)
{
    public string FileName => Path.GetFileName(FilePath);
}
public sealed record BuffBatchProgress(
    int CompletedFileCount,
    int TotalFileCount,
    string? CurrentFilePath);

public sealed class BuffBatchValidationResult
{
    public BuffBatchValidationResult(
        string folderPath,
        IReadOnlyList<string> patterns,
        bool searchSubdirectories,
        IReadOnlyList<BuffBatchFileResult> files)
    {
        FolderPath = folderPath;
        Patterns = patterns;
        SearchSubdirectories = searchSubdirectories;
        Files = files;
    }

    public string FolderPath { get; }
    public IReadOnlyList<string> Patterns { get; }
    public bool SearchSubdirectories { get; }
    public IReadOnlyList<BuffBatchFileResult> Files { get; }
    public int FileCount => Files.Count;
    public int ErrorCount => Files.Sum(file => file.ValidationResult.ErrorCount);
    public int WarningCount => Files.Sum(file => file.ValidationResult.WarningCount);
    public int FailedFileCount => Files.Count(file => !file.ValidationResult.IsSuccess);
    public int WarningFileCount => Files.Count(file => file.ValidationResult.IsSuccess && file.ValidationResult.WarningCount > 0);
    public int PassedFileCount => Files.Count(file => file.ValidationResult.IsSuccess && file.ValidationResult.WarningCount == 0);
}

/// <summary>
/// 在指定目录中按文件名通配符寻找文件，并逐个使用 BuffFileValidator 检查。
/// </summary>
public sealed class BuffBatchValidator
{
    public const string DefaultFileNamePattern = "*.buffs.json";

    private readonly BuffFileValidator _fileValidator;

    public BuffBatchValidator(BuffFileValidator? fileValidator = null)
    {
        _fileValidator = fileValidator ?? new BuffFileValidator();
    }

    public IReadOnlyList<string> FindFiles(BuffBatchValidationOptions options)
    {
        ArgumentNullException.ThrowIfNull(options);

        if (string.IsNullOrWhiteSpace(options.FolderPath))
        {
            throw new ArgumentException("必须选择要检查的文件夹。", nameof(options));
        }

        var folderPath = Path.GetFullPath(options.FolderPath);
        if (!Directory.Exists(folderPath))
        {
            throw new DirectoryNotFoundException($"找不到文件夹：{folderPath}");
        }

        var patterns = ParsePatterns(options.FileNamePattern);
        var enumerationOptions = new EnumerationOptions
        {
            RecurseSubdirectories = options.SearchSubdirectories,
            IgnoreInaccessible = true,
            MatchCasing = MatchCasing.CaseInsensitive,
            MatchType = MatchType.Simple,
            ReturnSpecialDirectories = false,
            AttributesToSkip = 0
        };

        var files = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var pattern in patterns)
        {
            foreach (var filePath in Directory.EnumerateFiles(folderPath, pattern, enumerationOptions))
            {
                files.Add(Path.GetFullPath(filePath));
            }
        }

        return files.OrderBy(path => path, StringComparer.OrdinalIgnoreCase).ToArray();
    }

    public BuffBatchValidationResult ValidateFolder(BuffBatchValidationOptions options) =>
        ValidateFolder(options, null);

    public BuffBatchValidationResult ValidateFolder(
        BuffBatchValidationOptions options,
        IProgress<BuffBatchProgress>? progress)
    {
        var files = FindFiles(options);
        var folderPath = Path.GetFullPath(options.FolderPath);
        var patterns = ParsePatterns(options.FileNamePattern);
        var results = new List<BuffBatchFileResult>(files.Count);
        progress?.Report(new BuffBatchProgress(0, files.Count, null));

        for (var index = 0; index < files.Count; index++)
        {
            var filePath = files[index];
            results.Add(new BuffBatchFileResult(filePath, _fileValidator.ValidateFile(filePath)));
            progress?.Report(new BuffBatchProgress(index + 1, files.Count, filePath));
        }

        return new BuffBatchValidationResult(
            folderPath,
            patterns,
            options.SearchSubdirectories,
            results);
    }

    public static IReadOnlyList<string> ParsePatterns(string? fileNamePattern)
    {
        if (string.IsNullOrWhiteSpace(fileNamePattern))
        {
            return [DefaultFileNamePattern];
        }

        var patterns = fileNamePattern
            .Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToArray();

        if (patterns.Length == 0)
        {
            return [DefaultFileNamePattern];
        }

        foreach (var pattern in patterns)
        {
            if (pattern.IndexOfAny([Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar]) >= 0)
            {
                throw new ArgumentException($"文件名形式“{pattern}”不能包含文件夹路径。请只填写文件名或通配符，例如 *.buffs.json。", nameof(fileNamePattern));
            }

            if (pattern.Contains('\0'))
            {
                throw new ArgumentException("文件名形式中不能包含空字符。", nameof(fileNamePattern));
            }
        }

        return patterns;
    }
}
