namespace BuffGrammarChecker.Core;

internal static class BuffRuleSemantics
{
    internal static readonly IReadOnlySet<string> ActorStatuses =
        new HashSet<string>(StringComparer.Ordinal)
        {
            "tagged",
            "poisoned",
            "bleeding",
            "stunned",
            "virtued",
            "afflicted",
            "burning"
        };

    internal static readonly IReadOnlySet<string> Activities =
        new HashSet<string>(StringComparer.Ordinal)
        {
            "meditation",
            "prayer",
            "flagellation",
            "bar",
            "gambling",
            "brothel",
            "treatment",
            "disease_treatment"
        };

    internal static readonly IReadOnlySet<float> Ranks =
        new HashSet<float> { -1f, 0f, 1f, 2f, 3f };

    internal static readonly IReadOnlySet<string> RulesWithUnreachableAdditionalEffects =
        new HashSet<string>(StringComparer.Ordinal)
        {
            "activated_first",
            "activated_last",
            "target_in_rank",
            "is_target_corpse",
            "target_is_burning",
            "actorStatus",
            "monsterSize",
            "in_camp",
            "in_activity",
            "monsterType",
            "target_is_vampire",
            "walking_backwards",
            "actor_base_class",
            "target_is_guarded",
            "target_is_guarding",
            "target_is_stealthed",
            "target_hpabove",
            "target_hpbelow",
            "ondeathsdoorenter"
        };

    internal static readonly IReadOnlySet<string> GeneralRuleOnlyStatTypes =
        new HashSet<string>(StringComparer.Ordinal)
        {
            "party_surprise_chance",
            "monsters_surprise_chance",
            "ambush_chance",
            "scouting_chance",
            "starving_damage_percent",
            "food_consumption_percent",
            "resolve_xp_bonus_percent",
            "vampire_evolution_duration",
            "quirk_evolution_death_immune",
            "disable_combat_skill_attribute",
            "torchlight_burn_percent",
            "stress_from_idle_in_town",
            "shard_reward_percent",
            "shard_consume_percent"
        };
}


