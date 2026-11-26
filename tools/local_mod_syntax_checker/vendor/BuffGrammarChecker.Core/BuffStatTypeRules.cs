namespace BuffGrammarChecker.Core;

/// <summary>
/// 来自 For_the_Darkest_Dungeon effect 校验器的 buff 主类型与副类型规则。
/// .buff_type 对应 buffs.json 的 stat_type，.buff_sub_type 对应 stat_sub_type。
/// </summary>
public static class BuffStatTypeRules
{
    public static readonly HashSet<string> ValidStatTypes = new(StringComparer.Ordinal)
    {
        "hp_heal_amount", "hp_heal_percent", "hp_heal_received_percent", "combat_stat_multiply",
        "combat_stat_add", "resistance", "poison_chance", "bleed_chance", "stress_dmg_percent",
        "stress_dmg_received_percent", "stress_heal_percent", "stress_heal_received_percent",
        "party_surprise_chance", "monsters_surprise_chance", "ambush_chance", "scouting_chance",
        "starving_damage_percent", "upgrade_discount", "damage_received_percent", "debuff_chance",
        "resolve_check_percent", "stun_chance", "move_chance", "remove_negative_quirk_chance",
        "food_consumption_percent", "resolve_xp_bonus_percent", "activity_side_effect_chance",
        "vampire_evolution_duration", "quirk_evolution_death_immune", "disable_combat_skill_attribute",
        "guard_blocked", "tag_blocked", "ignore_protection", "ignore_stealth", "crit_received_chance",
        "riposte", "tag", "guarded", "vampire", "stealth", "hp_dot_bleed", "hp_dot_poison",
        "hp_dot_heal", "stress_dot", "shuffle_dot", "torch_increase_percent", "torch_decrease_percent",
        "torchlight_burn_percent", "stress_on_miss", "stress_from_idle_in_town", "shard_reward_percent",
        "shard_consume_percent", "damage_reflect_percent", "hp_dot_bleed_duration_received_percent",
        "hp_dot_bleed_duration_percent", "hp_dot_bleed_amount_received_percent", "hp_dot_bleed_amount_percent",
        "hp_dot_poison_duration_received_percent", "hp_dot_poison_duration_percent",
        "hp_dot_poison_amount_received_percent", "hp_dot_poison_amount_percent",
        "stress_dot_duration_received_percent", "stress_dot_duration_percent",
        "stress_dot_amount_received_percent", "stress_dot_amount_percent",
        "hp_heal_dot_duration_received_percent", "hp_heal_dot_duration_percent",
        "hp_heal_dot_amount_received_percent", "hp_heal_dot_amount_percent",
        "shuffle_dot_duration_received_percent", "shuffle_dot_duration_percent",
        "guard_duration_received_percent", "guard_duration_percent", "cure_bleed_received_chance",
        "cure_poison_received_chance", "cure_bleed_chance", "cure_poison_chance",
        "random_target_friendly_chance", "random_target_attack_chance",
        "transfer_debuff_from_attacker_chance", "transfer_buff_from_attacker_chance",
        "quirk_tag_evolution_duration", "deathblow_chance", "heartattack_stress_heal_percent",
        "ignore_guard", "buff_duration_percent", "riposte_duration_percent",
        "hp_dot_burn", "hp_dot_burn_decay_percent", "hp_dot_burn_amount_percent",
        "hp_dot_burn_amount_received_percent", "wildfire_apply_adjacent_targets",
        "cure_burn_chance", "cure_burn_received_chance", "effect_chance",
        "crit_dmg_multiply", "crit_dmg_add", "heal_crit_chance_add",
        "heal_crit_chance_multiply", "hp_heal_amount_received", "disable_combat_skill"
    };

    public static readonly IReadOnlyDictionary<string, HashSet<string>> StatTypeToSubTypes =
        new Dictionary<string, HashSet<string>>(StringComparer.Ordinal)
        {
            ["hp_heal_amount"] = CreateSet(
                "hero_skill", "hero_skill_multi_target", "monster_skill", "monster_skill_multi_target",
                "camp_skill", "camp_skill_multi_target", "companion", "eat", "act_out", "damage_heal",
                "effect", "flashback", "dot", "curio"),
            ["hp_heal_percent"] = CreateSet(
                "hero_skill", "hero_skill_multi_target", "monster_skill", "monster_skill_multi_target",
                "camp_skill", "camp_skill_multi_target", "companion", "eat", "act_out", "damage_heal",
                "effect", "flashback", "dot", "curio"),
            ["hp_heal_received_percent"] = CreateSet(
                "hero_skill", "hero_skill_multi_target", "monster_skill", "monster_skill_multi_target",
                "camp_skill", "camp_skill_multi_target", "companion", "eat", "act_out", "damage_heal",
                "effect", "flashback", "dot", "curio"),
            ["combat_stat_multiply"] = CreateSet(
                "max_hp", "damage_low", "damage_high", "attack_rating", "crit_chance", "defense_rating",
                "protection_rating", "speed_rating", "riposte_on_hit_chance", "riposte_on_miss_chance"),
            ["combat_stat_add"] = CreateSet(
                "max_hp", "damage_low", "damage_high", "attack_rating", "crit_chance", "defense_rating",
                "protection_rating", "speed_rating", "riposte_on_hit_chance", "riposte_on_miss_chance"),
            ["resistance"] = CreateSet("stun", "move", "poison", "bleed", "disease", "debuff", "death_blow", "trap"),
            ["stress_dmg_percent"] = CreateSet(
                "hunger", "death_blow", "hero_crit", "hero_killing_blow", "mode", "control", "unkown",
                "town_idle", "quest_fail", "pass", "camping_relieve_stress", "camping_eat", "tile",
                "retreat", "effect", "capture", "monster_crit"),
            ["stress_dmg_received_percent"] = CreateSet(
                "hunger", "death_blow", "hero_crit", "hero_killing_blow", "mode", "control", "unkown",
                "town_idle", "quest_fail", "pass", "camping_relieve_stress", "camping_eat", "tile",
                "retreat", "effect", "capture", "monster_crit"),
            ["stress_heal_percent"] = CreateSet(
                "hunger", "death_blow", "hero_crit", "hero_killing_blow", "mode", "control", "unkown",
                "town_idle", "quest_fail", "pass", "camping_relieve_stress", "camping_eat", "tile",
                "retreat", "effect", "capture", "monster_crit"),
            ["stress_heal_received_percent"] = CreateSet(
                "hunger", "death_blow", "hero_crit", "hero_killing_blow", "mode", "control", "unkown",
                "town_idle", "quest_fail", "pass", "camping_relieve_stress", "camping_eat", "tile",
                "retreat", "effect", "capture", "monster_crit"),
            ["activity_side_effect_chance"] = CreateSet(
                "add_currency", "remove_currency", "add_trinket", "remove_trinket", "activity_lock",
                "apply_buff", "go_missing"),
            ["disable_combat_skill_attribute"] = CreateSet(
                "heal", "buff", "debuff", "bleed", "poison", "stun", "tag", "stress", "move", "guard", "daze")
        };

    public static readonly HashSet<string> MustHaveSubType = new(StringComparer.Ordinal)
    {
        "combat_stat_multiply", "combat_stat_add", "resistance", "activity_side_effect_chance",
        "disable_combat_skill_attribute"
    };

    public static readonly HashSet<string> FreeFormSubType = new(StringComparer.Ordinal)
    {
        "upgrade_discount", "riposte", "quirk_tag_evolution_duration", "effect_chance", "disable_combat_skill"
    };

    public static readonly HashSet<string> RequiredFreeFormSubType = new(StringComparer.Ordinal)
    {
        "effect_chance", "disable_combat_skill"
    };

    public static bool CanSpecifySubType(string statType) =>
        StatTypeToSubTypes.ContainsKey(statType) || FreeFormSubType.Contains(statType);

    private static HashSet<string> CreateSet(params string[] values) => new(values, StringComparer.Ordinal);
}
