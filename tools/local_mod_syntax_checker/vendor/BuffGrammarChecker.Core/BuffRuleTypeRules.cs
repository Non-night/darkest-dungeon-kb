namespace BuffGrammarChecker.Core;

/// <summary>
/// rule_type 的作用对象分类。
/// </summary>
public enum BuffRuleCategory
{
    /// <summary>进攻型，也称施术型。</summary>
    Offensive,

    /// <summary>防御型，也称受术型。</summary>
    Defensive,

    /// <summary>通用型，也称条件型。</summary>
    General
}

/// <summary>
/// buffs.json 中 rule_type 字段允许使用的固定值及其分类。
/// </summary>
public static class BuffRuleTypeRules
{
    public static readonly IReadOnlyList<string> AllowedValues =
    [
        "always",
        "skill",
        "riposte",
        "rangedonly",
        "meleeonly",
        "actorStatus",
        "monsterSize",
        "firstroundonly",
        "in_camp",
        "in_dungeon",
        "in_activity",
        "in_room",
        "in_corridor",
        "at_deaths_door",
        "in_rank",
        "hpbelow",
        "hpabove",
        "lightbelow",
        "lightabove",
        "torch_setting",
        "stress_below",
        "stress_above",
        "virtued",
        "afflicted",
        "monsterType",
        "attacking_monster_type",
        "monster_type_count_min",
        "is_vampire",
        "target_is_vampire",
        "has_quirk",
        "walking_backwards",
        "actor_base_class",
        "in_mode",
        "is_guarded",
        "target_is_guarded",
        "is_guarding",
        "target_is_guarding",
        "is_stealthed",
        "target_is_stealthed",
        "has_item_id",
        "has_item_type",
        "is_actor_status",
        "no_trinkets",
        "target_hpabove",
        "target_hpbelow",
        "activated_last",
        "activated_first",
        "ondeathsdoorenter",
        "target_in_rank",
        "is_target_corpse",
        "any_is_burning",
        "negative_quirk_above",
        "quest_uses_remaining_above",
        "has_buff",
        "target_is_burning"
    ];

    public static readonly HashSet<string> AllowedValueSet = new(AllowedValues, StringComparer.Ordinal);

    /// <summary>进攻型，也称施术型。</summary>
    public static readonly IReadOnlySet<string> OffensiveRules =
        new HashSet<string>(StringComparer.Ordinal)
        {
            "riposte",
            "rangedonly",
            "meleeonly",
            "actorStatus",
            "monsterSize",
            "monsterType",
            "target_is_vampire",
            "actor_base_class",
            "target_is_guarded",
            "target_is_guarding",
            "target_is_stealthed",
            "target_hpabove",
            "target_hpbelow",
            "target_in_rank",
            "is_target_corpse",
            "target_is_burning"
        };

    /// <summary>防御型，也称受术型。</summary>
    public static readonly IReadOnlySet<string> DefensiveRules =
        new HashSet<string>(StringComparer.Ordinal)
        {
            "attacking_monster_type"
        };

    /// <summary>通用型，也称条件型；包含全部未归入进攻型或防御型的 rule_type。</summary>
    public static readonly IReadOnlySet<string> GeneralRules =
        new HashSet<string>(
            AllowedValues.Where(ruleType =>
                !OffensiveRules.Contains(ruleType) &&
                !DefensiveRules.Contains(ruleType)),
            StringComparer.Ordinal);

    public static readonly IReadOnlyDictionary<string, BuffRuleCategory> CategoryByRuleType =
        AllowedValues.ToDictionary(
            ruleType => ruleType,
            ruleType => OffensiveRules.Contains(ruleType)
                ? BuffRuleCategory.Offensive
                : DefensiveRules.Contains(ruleType)
                    ? BuffRuleCategory.Defensive
                    : BuffRuleCategory.General,
            StringComparer.Ordinal);

    public static bool TryGetCategory(string ruleType, out BuffRuleCategory category) =>
        CategoryByRuleType.TryGetValue(ruleType, out category);

    public static string GetCategoryDisplayName(BuffRuleCategory category) => category switch
    {
        BuffRuleCategory.Offensive => "进攻型（施术）",
        BuffRuleCategory.Defensive => "防御型（受术）",
        BuffRuleCategory.General => "通用型（条件型）",
        _ => throw new ArgumentOutOfRangeException(nameof(category), category, null)
    };
}
