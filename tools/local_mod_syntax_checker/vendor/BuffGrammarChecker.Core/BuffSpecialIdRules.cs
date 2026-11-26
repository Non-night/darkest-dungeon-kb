namespace BuffGrammarChecker.Core;

/// <summary>
/// 由 buff ID 前缀触发、且不直接体现在普通字段语法中的特殊游戏行为。
/// </summary>
internal static class BuffSpecialIdRules
{
    internal const string ClearOnDodgePrefix = "DUELIST_TOUCHE_DODGE_";
    internal const string AttacksAnyLaunchRankPrefix = "ATTACKS_ANY_LAUNCH_RANK";
    internal const string AttacksAnyTargetRankPrefix = "ATTACKS_ANY_TARGET_RANK";

    internal static bool IgnoresRule(string buffId) =>
        buffId.StartsWith(AttacksAnyLaunchRankPrefix, StringComparison.Ordinal) ||
        buffId.StartsWith(AttacksAnyTargetRankPrefix, StringComparison.Ordinal);
}
