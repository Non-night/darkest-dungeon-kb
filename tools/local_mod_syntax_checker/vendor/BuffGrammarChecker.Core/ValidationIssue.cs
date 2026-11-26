namespace BuffGrammarChecker.Core;

public sealed record ValidationIssue(
    ValidationSeverity Severity,
    string Code,
    string Message,
    string JsonPath = "$",
    int? LineNumber = null,
    int? ColumnNumber = null,
    string? BuffId = null,
    int? BuffIndex = null)
{
    public string SeverityText => Severity switch
    {
        ValidationSeverity.Error => "错误",
        ValidationSeverity.Warning => "警告",
        _ => "提示"
    };

    public string LocationText => LineNumber.HasValue
        ? $"第 {LineNumber} 行，第 {ColumnNumber ?? 1} 列"
        : JsonPath;
}
