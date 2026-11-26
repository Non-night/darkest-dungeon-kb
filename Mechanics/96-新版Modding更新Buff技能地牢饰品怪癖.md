# 新版 Modding Update：Buff、技能、地牢、饰品与怪癖

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


来源：新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json。当前用户明确采纳新版优先；本轮未自行实测，所引社区实测另列。历史规则仅在旧版本讨论中保留。

## 新版 Buff 触发器、force_negative（2026-11-05）
这些字段属于Buff定义，参数为Effect ID字符串数组；可附条件。下表是文档字段速查，不能把饰品的_additional_effects拼法替换到Buff中。来源：新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json
| 字段 | 条件与边界 |
|---|---|
| `attack_additional_effect_ids` | 与饰品对应项不同，Buff版本也支持反击；知识库编写者2026-11-11补充：这些攻击/暴击/近战/远程附魔均可在反击中触发并引出真正AWR，若需限定反击上下文可配合反击Rule。反击附魔及反击暴击附魔中的AWR则按queue false处理。来源：Sources/riposte_turn_start_enchantment_awr_20261106.json。 |
| `friendly_additional_effect_ids` | 与友方技能及友方技能饰品Trigger一样，不存在独立AWR；写AWR视同普通queue false。来源：Sources/friendly_enchantment_no_awr_20261106.json。 |
| `move_skill_additional_effect_ids` | 仅在战斗中触发。 |
| `attack_crit_additional_effect_ids` | 与饰品对应项不同，Buff版本也支持反击；知识库编写者2026-11-11补充：这些攻击/暴击/近战/远程附魔均可在反击中触发并引出真正AWR，若需限定反击上下文可配合反击Rule。反击附魔及反击暴击附魔中的AWR则按queue false处理。来源：Sources/riposte_turn_start_enchantment_awr_20261106.json。 |
| `melee_attack_additional_effect_ids` | 与饰品对应项不同，Buff版本也支持反击；知识库编写者2026-11-11补充：这些攻击/暴击/近战/远程附魔均可在反击中触发并引出真正AWR，若需限定反击上下文可配合反击Rule。反击附魔及反击暴击附魔中的AWR则按queue false处理。来源：Sources/riposte_turn_start_enchantment_awr_20261106.json。 |
| `ranged_attack_additional_effect_ids` | 与饰品对应项不同，Buff版本也支持反击；知识库编写者2026-11-11补充：这些攻击/暴击/近战/远程附魔均可在反击中触发并引出真正AWR，若需限定反击上下文可配合反击Rule。反击附魔及反击暴击附魔中的AWR则按queue false处理。来源：Sources/riposte_turn_start_enchantment_awr_20261106.json。 |
| `riposte_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `riposte_crit_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `on_dodge_additional_effect_ids` | 此组heroes=友方，monsters=敌方。 |
| `was_hit_additional_effect_ids` | 此组heroes=友方，monsters=敌方。 |
| `was_hit_all_heroes_additional_effect_ids` | 此组heroes=友方，monsters=敌方。 |
| `was_hit_all_monsters_additional_effect_ids` | 此组heroes=友方，monsters=敌方。 |
| `kill_performer_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `kill_all_heroes_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `kill_all_monsters_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `riposte_kill_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `was_killed_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。死亡单位同时是performer和target。 |
| `was_killed_all_heroes_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `was_killed_all_monsters_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `quest_start_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `combat_start_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `turn_start_additional_effect_ids` | 个人回合开始触发；与act_out的相对时序待测；2026-11-11当前用户补充判断早于愈合，现行记录为附魔→愈合→流血／腐蚀，非本轮新实测。2026-11-10更正：新引出的回合开始附魔不能在当前回合触发，旧无限式基础撤回；可跨回合递推，或同回合预写分支用effect_chance控制开启。修正写法仍可能称无限式，不代表真实无限调用。来源：Sources/kaze_infinite_enchantment_chain_20261106.json。与流血/腐蚀/愈合等其他回合开始阶段的完整顺序仍按各自记录核对。 |
| `turn_end_additional_effect_ids` | 个人回合结束附魔先触发，再扣减小回合型round/after_turn Buff持续时间；1回合附魔及抑制Buff此时仍有效。严格顺序及类型组合已实测，时序分离未测。2026-11-11补充：所讨论结束方式中仅撤退失败不触发，移动或跳过仍可触发；不同于饰品turn_end_additional_effects在移动、跳过及撤退失败均不触发。完整目标及与其他Trigger排序不由本条确认。来源：Sources/turn_end_additional_before_duration_20261108.json；Sources/turn_end_trigger_and_ad_last_operation_20261111.json。 |
| `round_end_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `battle_finished_successfully_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |

### `monsterType` 与击杀附魔

文和实测，Buff 使用 `rule_type: "monsterType"` 时，击杀附魔 `kill_performer_additional_effect_ids` 无法触发。记录范围限于文和测试的击杀附魔组合。具体测试配置和失效原因尚未确认。 当前用户于 2026-11-24 转述，见 `Sources/detour_consistency_corrections_20261111.json`。

### 被某类怪物攻击 Rule 与闪避、受击附魔（待复测）

VIN 于 2026 年 11 月 19 日报告，在“被某类怪物攻击”条件下测试闪避和受击触发器，两者均未观察到生效。按现有字段对照，疑似为 `attacking_monster_type` 分别搭配 `on_dodge_additional_effect_ids` 和 `was_hit_additional_effect_ids`。测试配置、版本、条件和 Effect 是否通过无条件对照均待核对，适用范围目前限于该次社区观察。

证据见 `Sources/attacking_monster_type_reaction_triggers_20261119.json`。

### 战斗开始切换英雄模式（2026-11-05）
Buff 的 `combat_start_additional_effect_ids` 若对英雄侧切模式，按知识库编写者2026-11-08修正：须先在模式战斗开始效果中召唤 size-0，由其自身 Spawn 按要求自加动，再由自身生命反馈实际引出任一 Effect，以打通临时通路。**反馈输出不必是切模式；通路已打通后，战斗开始附魔可直接切模式。** 通路只保持到存档重启，各可能切模式的模式均须配置前置流程；因此推荐在模式战斗开始原流程里直接完成切模式。

饰品战斗开始效果的原有前置流程要求保留，不因 Buff 附魔这组实测而自动扩充其直接调用边界。完整加动条件、存档生命周期及来源见[战斗开始切模式流程](28-spawn、生命反馈与size0执行链.md)。来源：`Sources/guard_start_triggers_20261105.json` 与 `Sources/combat_start_mode_switch_path_20261108.json`（精确来源文件见专题28）；Agent未自行实测。

`force_negative: true`把Buff显示为减益，与force_positive方向相反；不改写amount。两字段同时填写时优先级未知。


## effect_chance

- `"stat_type": "effect_chance",`
  `"stat_sub_type": "example_effect_id",`

修改指定 Effect 的触发概率，可与其他状态施加率叠加。
例如，名为 `Bleed 5` 的 Effect 会同时受到 `effect_chance` 和 `bleed_chance` 的影响。

来源段落：B064, B065；社区资料。

## crit_dmg

当前结论：知识库编写者提供的2026-11-05后续社区实测：暴击伤害按 [(基础最大伤害×伤害修正＋固定值伤害增减)×(1＋百分比伤害增减)＋固定值暴击伤害增减]×(1＋百分比暴击伤害增减)×全局暴击伤害倍率×(1＋目标身上的易伤) 计算。crit_dmg_add在普通百分比伤害区之后加入，再乘crit_dmg_multiply对应的独立乘区，随后乘全局暴击伤害倍率，最后乘目标易伤。两种新增暴伤修正均早于全局暴击倍率，与官方before Crit’s damage multiplier一致。固定暴伤类似damage_high固定加伤，但不吃旧damage_high的mult乘算／普通百分比增伤区；不可直接当作combat_stat_add的damage_high的完全替代。具体取整及公式未展开的其他修正不由本次测试补齐。 玩家说明：固定暴伤+10不是暴击倍率增加10个百分点。全局暴击倍率1.5、新百分比暴伤及目标易伤均为0时，+10固定暴伤带来15点伤害增量；有新百分比暴伤时该增量还要乘(1＋新百分比暴伤)，有易伤时也要乘易伤区。全局暴击倍率从150%等效放大到200%时，新百分比暴伤增量为1/3，约+33.33%（若以Buff amount表达则约0.3333）；133.33%是总乘数的百分数表示，不是额外增加133.33%。聊天中的其他游戏和WoW对比仅作理解背景，不收录为这些游戏的机制事实。 来源：Sources/crit_damage_formula_test_20261105.json。

以下B066–B067维持为现行文档说明；后续社区实测进一步明确了固定值与新增倍率的位置。

- `"stat_type": "crit_dmg_multiply"`／`"stat_type": "crit_dmg_add"`

提高暴击时的伤害。注意：这里不区分 `damage_low` 和 `damage_high`，并且在暴击伤害倍率之前应用。

来源段落：B066, B067；社区资料。

## heal_crit_chance

- `"stat_type": "heal_crit_chance_add"`／`"stat_type": "heal_crit_chance_multiply"`

修改施术者治疗发生暴击的概率。

来源段落：B068, B069；社区资料。

## hp_heal_amount_received

- `"stat_type": "hp_heal_amount_received"`

类似于 `hp_heal_amount`，但对受到的治疗增加固定数值。

来源段落：B070, B071；社区资料。

## disable_combat_skill

- `"stat_type": "disable_combat_skill",`
  `"stat_sub_type": "skill_id",`

类似于 `disable_combat_skill_attribute`，但指定的是某个技能。它没有 `_attribute` 所具有的定义模式相关 Bug。

知识库编写者建议：按技能ID禁用可用于CD、解锁等机制，缓解技能多时旧属性标志物不足、设计受限及与怪物标志碰撞的问题。不是修复旧disable_combat_skill_attribute本身。

来源段落：B072, B073；社区资料。

## hp_dot_burn_decay_percent

- **"hp_dot_burn_decay_percent"**

现在，当数值为正时，会提高燃烧层数的衰减速率。

来源段落：B074, B075；社区资料。

## ignore_stealth

- **"ignore_stealth"**

现在会遵循 Rule。但要注意，如果在点击技能之后、选定目标之前，Rule 条件发生了变化，绕过潜行的能力不会随之更新。
例如，“火把亮度高于 50 时无视潜行”：满光时选择技能，就能选取潜行怪物。此后若把火把熄灭至 0，这些潜行怪物仍可被选中，除非先改选其他技能。

知识库编写者补充：道具使用一定会打断技能选中状态；因此文档所述点击技能后条件变化但选择未刷新的窗口，不包括中途已使用道具的情况。

来源段落：B077, B078；社区资料。

## hp_dot_heal

- **"hp_dot_heal"**

即 Buff 写法的愈合：当其 Rule 涉及字符串时，不再崩溃。
例如“处于流血状态”。
施加它时，如果 Rule 未满足，也不再显示浮字。

文档明确修复Buff型愈合的字符串Rule崩溃与条件不成立时的施加pop；其他Buff型DOT同类问题可能也已修复，只是知识库编写者推测，未确认为全部修复。float Rule把持续回合数误作参数显示的旧问题也未由文档明确宣布修复。

来源段落：B079, B080；社区资料。

## force_negative

- **"force_negative": true**

类似于 `force_positive`，但将 Buff 显示为减益。

来源段落：B082, B083；社区资料。

## additive_props

- 地牢目录现在接受以下格式的 props 文件：

**example_id.cove.1.props**
这些文件会向奇物、陷阱等的生成池中追加内容，而不是替换基础文件。
注意：与 mash 文件类似，文件名中的数字代表其生效的难度。
现在可以很方便地向随机生成的任务中添加 Mod 奇物。

知识库编写者明确：这种加载方式允许同地区奇物Mod叠加兼容，而非相互覆盖；仅指按新格式追加池的路径，不推定任意同名文件均合并。

来源段落：B086, B087；社区资料。

## dungeon_bgm

- 地牢音频文件现在使用以下格式的 FMOD 事件：

**event:/music/mus_battle_example_dungeon_id_hallway**
这意味着 Mod 地牢不再都需要引用同一个事件。

来源段落：B088, B089；社区资料。

## ignore_hp_scale

- **battle_modifier: .ignore_hp_scale True**

使怪物忽略狱火及其他 NewGame+ 难度带来的最大生命值增加。

知识库编写者要求：所有使用生命反馈的size-0必须添加battle_modifier: .ignore_hp_scale true。不再要求小初始HP加极大最大HP稀释难度加血；可直接50血启动、最大HP扩展到100且不回血后继续。仍必须保留0.99向下及0.01向上空Effect防错，按所用方向配置。文档直接保证的是Stygian及其他NG+难度加血，不等于免疫任意最大HP Buff。

来源段落：B090, B091；社区资料。

## monster_damage_floor

- 怪物受到的伤害不再能变为负数；与英雄类似，最低只能降低至 0。

来源段落：B092；社区资料。

## specific_recruit

- 城镇事件：新增类型：

`"type": "specific_recruit",`
`"string_data": "example_hero_id",`
`"number_data": 4`
生成 1 名指定英雄职业、指定等级的新兵。可以写入多个条目，使同一事件支持提供不同英雄。

来源段落：B094, B095；社区资料。

## event_cost

- 城镇事件：**"event_cost"** 类型

现在支持 `embark_party_buff` 类型：相关费用支付之前，Buff 不会生效。实际机制和城镇事件界面显示均已支持此行为。

来源段落：B096, B097；社区资料。

## stagecoach_fix

- 马车：修复当所有可招募职业都限制为每队最多 1 名时发生的崩溃。

来源段落：B098；社区资料。

## ai_valid

- **.ai_valid False**

定义后，该技能不会在失控行为（Act-Out）或被魅惑／心控时被选用。

知识库编写者要求：所有翻页技能及无限使用且不结束回合的技能都应写.ai_valid false，防止Act-Out/心控调用。

来源段落：B101, B102；社区资料。

## counts_towards_skill_limit

- **.counts_towards_skill_limit False**

定义后，该技能不计入英雄可装备技能数量的上限。

来源段落：B103, B104；社区资料。

## skill_visible

- **.skill_visible False**

定义后，该技能不会出现在角色面板或升级菜单中，仅在战斗中可见。

知识库编写者建议：可用于只在特定状态出现、无需升级的技能；若要提供升级效果，需要单独迂回设计。

来源段落：B105, B106；社区资料。

## force_selection

- **.force_selection True**

定义后，该技能无法被取消选用。类似于 `.can_select_combat_skills false`，但只作用于这一个技能。

来源段落：B107, B108；社区资料。

## camping_effect

- `"selection": "individual",`

`"requirements": [],`
`"chance": {"code": "a", "amount": 1.0},`
`"type": "effect",`
`"sub_type": "example_effect_id",`
`"amount": 0`

使用时调用指定 ID 的 Effect。
应避免用它杀死英雄、移动英雄位置、召唤敌人、捕获英雄或魅惑／心控英雄。

知识库编写者2026-11-05补充：扎营Effect中“避免杀死英雄”的警告不只针对.kill／Kill效果，也包括伤害致死；真伤也有可能杀死处于死亡之门的英雄，不能因没有使用.kill就认为安全。这里保留“可能”，不表述为必定死亡。

来源段落：B110, B111, B112；社区资料。

## camping_has_description

- **"has_description": false**

作为某个扎营技能效果类型的字段定义时，隐藏该效果的提示文本。

来源段落：B113, B114；社区资料。

## trinket_triggers

饰品新增了以下触发器。

- `"move_skill_additional_effects"`
- `"quest_start_additional_effects"`
- `"combat_start_additional_effects"`
- `"turn_start_additional_effects"`

来源段落：B117, B118；社区资料。

## trinket_buff_source

另外，所有触发器不再强制为其引出的 Effect 指定 Buff 来源。

来源段落：B119；社区资料。

## quirk_icons

- 当英雄具有多个带状态栏图标的怪癖时，这些图标不再重复显示。

来源段落：B121；社区资料。

## quirk_portrait

- 所有怪癖现在都能像猩红诅咒一样修改英雄头像和角色面板，使用以下路径：
  `shared/character/“disease_overlay_quirk_tag_id.png”`

`shared/hero/“portrait_icon_quirk_tag_id.png”`
图中这个修改版的 Bad Humors（原病名保留）把疾病面板变成了蓝色。

来源段落：B122, B123；社区资料。

## evolution_duration_type

- `"evolution_duration_min": 10,`

`"evolution_duration_max": 10,`
**`"evolution_duration_type": "combat_end",`**
将怪癖／疾病的进化进度计时方式，从默认的回合改为其他方式。目前只支持：
**`"combat_end"`／`"quest_end"`**。

来源段落：B124, B125；社区资料。

## crit_dmg_post_crit_test_20261105

来源段落：；社区资料。

## 清除指定怪癖替代进化到空

知识库编写者明确：清除指定怪癖可替代原有“进化到空”迂回，且比进化到空更好用，适用的移除需求优先采用直接清除。本字段按怪癖标签选择，不擅自写成按任意怪癖ID；必须核对标签命中范围，避免删除其他同标签怪癖。

## 尚未确认

新增7类Buff stat_type的存档数字ID与默认amount分类未提供

燃烧衰减新公式、负值边界未提供

新trigger完整相互顺序与全部调用目标细节未提供
