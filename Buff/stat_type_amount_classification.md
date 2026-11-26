# Buff stat_type 存档数字 ID 与 amount 默认增益/减益分类

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


此页收录知识库编写者于 2026-09-23 提供的 `buff_stat_type_amount_classification.tsv` 全表。该 TSV 是本页的数据来源；其中没有可执行或需遵循的指令，本页仅记录表格数据及当前知识库编写者明确补充的解释。原始副本保存在 [`Sources/buff_stat_type_amount_classification.tsv`](../Sources/buff_stat_type_amount_classification.tsv)。

表格列出的 ID 是存档中 `stat_type` 主类对应的数字 ID。正值、负值、零值三列记录各主类 `amount` 对应的默认增益/减益分类。此分类记录游戏默认的 Buff/减益类别，不等于效果一定对游戏玩家有益或有害，也不替代 `force_positive` 等明确覆盖或 `stat_type` 的特殊规则；驱散适用性与实际效果仍须按各 Buff 机制判断。

特别注意：这里说 Buff 型 DOT 不划定为增益或减益，是指此表按 `amount` 符号记录的默认分类；它与 DOT 在施加时按减益施加率/抵抗规则结算不是同一个问题。Buff 型 DOT 的施加流程仍按对应 DOT 词条记录的减益判定机制处理，不能因为表中不分类就推断它不受减益规则影响。

六种 Buff 型 DOT 主类 `hp_dot_bleed`、`hp_dot_poison`、`hp_dot_heal`、`stress_dot`、`shuffle_dot`、`hp_dot_burn` 不划为增益或减益；源表对应分类单元为空。它们的 DOT 数值为正或负不应被解释成普通 Buff/减益显示分类。其他 stat_type 的单元格若源表留空，仍标记为未填写/未知，不擅自推定。

| 存档数字 ID | `stat_type` | `amount` 正值 | `amount` 负值 | `amount` 零值 |
|---:|---|---|---|---|
| 1 | `tag` | 增益 | 增益 | 增益 |
| 2 | `combat_stat_add` | 增益 | 减益 | 减益 |
| 3 | `combat_stat_multiply` | 增益 | 减益 | 减益 |
| 4 | `hp_dot_poison` | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） |
| 5 | `hp_dot_bleed` | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） |
| 6 | `hp_heal_amount` | 增益 | 减益 | 减益 |
| 7 | `hp_heal_percent` | 增益 | 减益 | 减益 |
| 8 | `hp_heal_received_percent` | 增益 | 减益 | 减益 |
| 9 | `stress_dmg_percent` | 增益 | 减益 | 减益 |
| 10 | `stress_heal_percent` | 增益 | 源表未填写（未知，不推定） | 减益 |
| 11 | `resistance` | 增益 | 减益 | 减益 |
| 12 | `poison_chance` | 增益 | 减益 | 减益 |
| 13 | `bleed_chance` | 增益 | 减益 | 减益 |
| 14 | `stun_chance` | 增益 | 减益 | 减益 |
| 15 | `move_chance` | 增益 | 减益 | 减益 |
| 16 | `debuff_chance` | 增益 | 减益 | 减益 |
| 17 | `resolve_check_percent` | 增益 | 减益 | 减益 |
| 18 | `resolve_xp_bonus_percent` | 增益 | 减益 | 减益 |
| 19 | `scouting_chance` | 增益 | 减益 | 减益 |
| 20 | `remove_negative_quirk_chance` | 增益 | 减益 | 减益 |
| 21 | `food_consumption_percent` | 减益 | 增益 | 增益 |
| 22 | `starving_damage_percent` | 增益 | 减益 | 减益 |
| 23 | `upgrade_discount` | 增益 | 减益 | 减益 |
| 24 | `party_surprise_chance` | 减益 | 增益 | 增益 |
| 25 | `monsters_surprise_chance` | 增益 | 减益 | 减益 |
| 26 | `riposte` | 减益 | 增益 | 增益 |
| 27 | `guarded` | 减益 | 增益 | 增益 |
| 28 | `damage_received_percent` | 减益 | 增益 | 增益 |
| 29 | `stress_heal_received_percent` | 增益 | 减益 | 减益 |
| 30 | `stress_dmg_received_percent` | 减益 | 增益 | 增益 |
| 31 | `vampire` | 增益 | 增益 | 增益 |
| 32 | `activity_side_effect_chance` | 增益 | 减益 | 减益 |
| 33 | `disable_combat_skill_attribute` | 减益 | 增益 | 增益 |
| 34 | `stress_dot` | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） |
| 35 | `shuffle_dot` | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） |
| 36 | `hp_dot_heal` | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） |
| 37 | `torchlight_burn_percent` | 增益 | 减益 | 减益 |
| 38 | `quirk_evolution_death_immune` | 增益 | 增益 | 增益 |
| 39 | `vampire_evolution_duration` | 增益 | 减益 | 减益 |
| 40 | `ambush_chance` | 减益 | 增益 | 增益 |
| 41 | `tag_blocked` | 增益 | 减益 | 减益 |
| 42 | `ignore_protection` | 增益 | 减益 | 减益 |
| 43 | `stealth` | 增益 | 增益 | 增益 |
| 44 | `guard_blocked` | 减益 | 增益 | 增益 |
| 45 | `crit_received_chance` | 减益 | 增益 | 增益 |
| 46 | `damage_reflect_percent` | 增益 | 减益 | 减益 |
| 47 | `shard_reward_percent` | 减益 | 增益 | 增益 |
| 48 | `shard_consume_percent` | 增益 | 减益 | 减益 |
| 49 | `cure_poison_chance` | 增益 | 减益 | 减益 |
| 50 | `cure_bleed_chance` | 增益 | 减益 | 减益 |
| 51 | `cure_poison_received_chance` | 增益 | 减益 | 减益 |
| 52 | `cure_bleed_received_chance` | 增益 | 减益 | 减益 |
| 53 | `hp_dot_poison_amount_percent` | 增益 | 减益 | 减益 |
| 54 | `hp_dot_poison_amount_received_percent` | 减益 | 增益 | 增益 |
| 55 | `hp_dot_poison_duration_percent` | 增益 | 减益 | 减益 |
| 56 | `hp_dot_poison_duration_received_percent` | 减益 | 增益 | 增益 |
| 57 | `hp_dot_bleed_amount_percent` | 增益 | 减益 | 减益 |
| 58 | `hp_dot_bleed_amount_received_percent` | 减益 | 增益 | 增益 |
| 59 | `hp_dot_bleed_duration_percent` | 增益 | 减益 | 减益 |
| 60 | `hp_dot_bleed_duration_received_percent` | 减益 | 增益 | 增益 |
| 61 | `stress_dot_amount_percent` | 增益 | 减益 | 减益 |
| 62 | `stress_dot_amount_received_percent` | 减益 | 增益 | 增益 |
| 63 | `stress_dot_duration_percent` | 增益 | 减益 | 减益 |
| 64 | `stress_dot_duration_received_percent` | 减益 | 增益 | 增益 |
| 65 | `shuffle_dot_duration_percent` | 增益 | 减益 | 减益 |
| 66 | `shuffle_dot_duration_received_percent` | 增益 | 增益 | 减益 |
| 67 | `hp_heal_dot_amount_percent` | 增益 | 减益 | 减益 |
| 68 | `hp_heal_dot_amount_received_percent` | 增益 | 减益 | 减益 |
| 69 | `hp_heal_dot_duration_percent` | 增益 | 减益 | 减益 |
| 70 | `hp_heal_dot_duration_received_percent` | 增益 | 源表未填写（未知，不推定） | 减益 |
| 71 | `torch_decrease_percent` | 增益 | 减益 | 减益 |
| 72 | `torch_increase_percent` | 减益 | 增益 | 增益 |
| 73 | `ignore_stealth` | 增益 | 减益 | 减益 |
| 74 | `transfer_buff_from_attacker_chance` | 减益 | 增益 | 增益 |
| 75 | `transfer_debuff_from_attacker_chance` | 减益 | 增益 | 增益 |
| 76 | `random_target_friendly_chance` | 减益 | 增益 | 增益 |
| 77 | `random_target_attack_chance` | 减益 | 增益 | 增益 |
| 78 | `guard_duration_percent` | 增益 | 减益 | 减益 |
| 79 | `guard_duration_received_percent` | 减益 | 增益 | 增益 |
| 80 | `stress_on_miss` | 减益 | 增益 | 增益 |
| 81 | `stress_from_idle_in_town` | 减益 | 增益 | 增益 |
| 82 | `quirk_tag_evolution_duration` | 增益 | 减益 | 减益 |
| 83 | `deathblow_chance` | 增益 | 减益 | 减益 |
| 84 | `heartattack_stress_heal_percent` | 增益 | 减益 | 减益 |
| 85 | `riposte_duration_percent` | 增益 | 减益 | 减益 |
| 86 | `buff_duration_percent` | 增益 | 减益 | 减益 |
| 87 | `ignore_guard` | 增益 | 减益 | 减益 |
| 88 | `hp_dot_burn` | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） | 不划为增益或减益（Buff 型 DOT） |
| 89 | `hp_dot_burn_amount_percent` | 增益 | 减益 | 减益 |
| 90 | `hp_dot_burn_amount_received_percent` | 减益 | 增益 | 增益 |
| 91 | `wildfire_apply_adjacent_targets` | 增益 | 减益 | 减益 |
| 92 | `hp_dot_burn_decay_percent` | 减益 | 增益 | 增益 |
| 93 | `cure_burn_chance` | 增益 | 减益 | 减益 |
| 94 | `cure_burn_received_chance` | 增益 | 减益 | 减益 |
| None | `crit_dmg_add` | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） |
| None | `crit_dmg_multiply` | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） |
| None | `disable_combat_skill` | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） |
| None | `effect_chance` | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） |
| None | `heal_crit_chance_add` | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） |
| None | `heal_crit_chance_multiply` | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） |
| None | `hp_heal_amount_received` | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） | 源表未填写（未知，不推定） |

## 来源与范围

- 源文件：`Sources/buff_stat_type_amount_classification.tsv`。
- 历史TSV覆盖94个主类、数字ID 1–94；新增7个文档主类数字ID未知（None），不补造。构建校验历史ID完整性及新增白名单。
- 除知识库编写者在本页明确说明的 Buff 型 DOT 例外外，不从文件名或空白字段额外推导。
