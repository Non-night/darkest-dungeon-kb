namespace BuffGrammarChecker.Core;

public sealed class ValidationResult
{
    public ValidationResult(string fileName, IReadOnlyList<ValidationIssue> issues, bool fileNameValid, bool jsonValid)
    {
        FileName = fileName;
        Issues = issues;
        FileNameValid = fileNameValid;
        JsonValid = jsonValid;
    }

    public string FileName { get; }
    public IReadOnlyList<ValidationIssue> Issues { get; }
    public bool FileNameValid { get; }
    public bool JsonValid { get; }
    public int ErrorCount => Issues.Count(issue => issue.Severity == ValidationSeverity.Error);
    public int WarningCount => Issues.Count(issue => issue.Severity == ValidationSeverity.Warning);
    public bool IsSuccess => FileNameValid && JsonValid && ErrorCount == 0;
}
