# 原版副本数据速查表

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

数值来自本体和官方 DLC 游戏文件，清丽静《地牢大学习》系列的运行观察另行标注。文件定位、哈希和截图见[证据账本](../Sources/vanilla_raid_and_town_20261122.json)。字段用法见[副本机制专题](../Mechanics/101-原版副本探索、扎营夜袭与出本结算.md)。

## 四个常规地区的随机任务生成门槛

| 地区 | `id` | `required_number_of_quests_finished` |
|---|---|---:|
| 遗迹 | `crypts` | 1 |
| 旷野 | `weald` | 3 |
| 兽窟 | `warrens` | 4 |
| 海湾 | `cove` | 4 |

原版遗迹教学本 `plot_tutorial_crypts` 是固定剧情任务，使用地图 `tutorial_crypts`。文件路径与格式见[随机任务生成机制](../Mechanics/99-原版随机副本等级分布与刷新.md#新档地区开放与随机任务生成门槛)。默认值与教学本定义均来自[原版文件核对记录](../Sources/random_quest_region_gates_20261124.json)。

## 地区任务刷新上限与全图数量表

本体 `generated_quests_max_threshold` 默认 **4**，是常规地区共用的单区任务额度。Boss 本、固定本与事件本优先占额。字段路径和占额规则见[随机任务刷新机制](../Mechanics/99-原版随机副本等级分布与刷新.md#单地区任务刷新上限与占额优先级)。

| 配置来源 | 数量表 | 数量修正表 |
|---|---|---|
| 本体 | `[2, 6, 8, 9, 10, 11, 12, 13]` | — |
| 猩红庭院 DLC | `[2, 6, 9, 10, 11, 12, 13, 14]` | `[0, 0, 1, 1, 1, 1, 1, 1]` |
| 疯狂之色 DLC | — | `[1, 1, 2, 2, 3, 3, 3, 3]` |

以上为文件原值。DLC 数量表与修正表的实际合并顺序待核实。[原版与 DLC 文件核对记录](../Sources/region_quest_capacity_20261125.json)。

## 四地区走廊陷阱与障碍数量

本体 `scripts/map_generator.darkest` 中四地区的 `explore` 与 `cleanse` 在同大小下采用相同的 `.hallway_trap` 和 `.hallway_obstacle` 区间。下表按短／中／长排列，与证据图 03 对应列逐项一致。

| 地区 | 走廊陷阱数量 | 障碍数量 | 陷阱种类 | 障碍种类 |
|---|---|---|---|---|
| 遗迹 `crypts` | 2–3／3–5／4–6 | 0–2／0–3／0–4 | `spikes` | `rubble` |
| 海湾 `cove` | 2–3／3–5／4–6 | 0–2／0–3／0–4 | `lurker` | `shipwreck` |
| 旷野 `weald` | 1–2／2–4／3–5 | 1–3／1–4／1–5 | `poison_cloud` | `thorny_thicket` |
| 兽窟 `warrens` | 3–4／4–6／5–7 | 0–2／0–2／0–3 | `blade_wheel` | `rubble` |

同一文件中，本体四地区已有的 `kill_boss`、`gather`、`activate`、`inventory_activate` 地图段也与同地区同大小的这两列一致。种类列来自各地区的 `.props.darkest`。

## 四地区探索本与战斗本的其他地图参数

下表按短／中／长排列。房间目标数、走廊战、饥饿、奇物和密门的表值与证据图 03 一致。房间战同时保留配置值和视频列出的结果区间，两者差异的原因待查。

| 项目 | 探索本 `explore` | 战斗本 `cleanse` |
|---|---|---|
| 房间目标数 `.goal_room_number` | 9／14／19 | 7／11／14 |
| 房间战 `.total_room_battles` | 1–3／3–4／7 | 2–4／4–5／8 |
| 房间战（视频结果区间） | 1–3／2–4／5–7 | 1–4／3–6／7–8 |
| 走廊战 `.hallway_battle` | 2–4／3–4／7 | 2–4／4–5／8 |
| 走廊饥饿 `.hallway_hunger` | 1–3／2–5／2–6 | 1–3／2–5／2–6 |
| 走廊奇物 `.hallway_curio` | 9／14／19 | 9／14／19 |
| 密门 `.secret_rooms` | 0／0–1／0–1 | 0／0–1／0–1 |

原版四地区探索本与战斗本的 `.spacing` 在同一地区的短／中／长三档相同。遗迹、旷野、海湾为 `4`，兽窟为 `3`。基础走廊条数 `.base_corridor_number` 按短／中／长排列，探索本为 `10／15／20`，战斗本为 `8／11／15`。基础房间数与上表的目标房间数在这组配置中相同。[字段说明](../Mechanics/101-原版副本探索、扎营夜袭与出本结算.md#随机地图的走廊长度房间内容与战斗落点) · [文件核对记录](../Sources/random_map_layout_20261125.json)

## 随机地图的秘门生成量

| 地图大小 | `.secret_rooms` 原版写法 | 生成数量 |
|---|---|---|
| 短本 `short` | `.secret_rooms 0 0` | 0 个 |
| 中本 `medium` | `.secret_rooms 0 1` | 0–1 个 |
| 长本 `long` | `.secret_rooms 0 1` | 0–1 个 |

本体、猩红庭院和疯狂之色的 `scripts/map_generator.darkest` 中，已写 `.secret_rooms` 的随机地图配置块均符合上表。中本与长本的字段值相同。知识库编写者印象中两者各有 50% 概率生成 1 个秘门，待核实。适用范围为随机地图。[文件与行号](../Sources/secret_room_generation_20261125.json) · [字段与侦查机制](../Mechanics/101-原版副本探索、扎营夜袭与出本结算.md#侦查暴击密门与走廊格)

## 地区随机本的任务完成奖励

遗迹、海湾、旷野和兽窟的常规随机任务按下表配置。每格按短／中／长（`length` 1／2／3）排列。

| 难度 | 金币 | 雕像或画像数量 | 地契或纹章数量 | 饰品稀有度 | 砺炼值 |
|---|---:|---:|---:|---|---:|
| 学徒（1） | 3,000／4,500／7,500 | 2／2／4 | 3／5／9 | 普通／优良／稀有 | 2／3／4 |
| 精英（3） | 4,500／6,750／11,250 | 2／3／6 | 4／6／12 | 优良／稀有／非常稀有 | 4／6／8 |
| 冠军（5） | 6,000／9,000／15,000 | 3／5／9 | 6／9／18 | 稀有／非常稀有／先祖 | 8／12／16 |

- 四地区的传家宝候选顺序相同，均为 `bust`（雕像）、`portrait`（画像）、`deed`（地契）、`crest`（纹章）。九种常规难度和长度组合各只有表中对应的稀有度为 `1`。稀有度 ID 依次为 `common`、`uncommon`、`rare`、`very_rare`、`ancestral`。
- `item_table` 的难度 6 行金币表值为 9,000／13,500／22,500。
- 猩红庭院的随机任务传家宝候选只列 `crest`，带 `dungeon` 为 `courtyard` 的 `crimson_court` 稀有度行组在难度 5 和 6、长度 2 和 3 的四格写 `100000`，其余为 `0`。
- 冠军死灵法师固定任务在 `quest.plot_quests.json:363` 写了 15,000 金币、30 纹章及 `boss_necromancer` 饰品。

## 四地区 Boss 本与特殊任务砺炼值

清丽静视频列出的四地区 Boss 本砺炼值按学徒／精英／冠军分别为 4／8／16。

证据图 63 的原版额外任务表列出老路 2，尖叫魔按难度 1／2／4，头狼 16，DD1–4 各 16，血酿本按难度 2／4／8，CC1–4 分别 4／8／12／16，花园守卫 12，学徒／精英农庄 2／6。无尽农庄任务定义按波次里程碑配置 8／12／16／20。

老路的 2 点历练值见原版 `scripts/starting_save/persist.raid.json:15`，字段为 `data.raid_instance.completion_reward.resolve_xp`。

## 英雄历练值升级阈值

下表是原版 `resolve_level_thresholds` 在英雄等级 0–6 各档的累计历练值。

| 配置 | 0 级 | 1 级 | 2 级 | 3 级 | 4 级 | 5 级 | 6 级 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 基础 | 0 | 2 | 8 | 14 | 24 | 36 | 48 |
| 明耀 | 0 | 2 | 7 | 13 | 21 | 29 | 40 |

原版配置见 `campaign/roster/roster.variables.json:4` 和 `modes/radiant/campaign/roster/roster.variables.json:4`，详见[英雄等级阈值的配置入口](../Mechanics/26-英雄升级树、初始补给与名册容量.md#英雄历练值升级阈值)。

## 低等级英雄进本的一次性压力惩罚

进本时按每名英雄各自的等级差加压。下表的等级差为副本难度等级减去英雄决心等级，数值单位为压力点。

| 难度 | 差 0 | 差 1 | 差 2 | 差 3 | 差 4 | 差 5 | 差 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 明耀／极暗 | 0 | 20 | 30 | 40 | 50 | 60 | 70 |
| 血月／狱火 | 0 | 25 | 35 | 45 | 55 | 65 | 75 |

例如 1 级英雄进入 3 级精英本，极暗进本加 30 点压力，血月／狱火加 35 点。表中各档是原版配置值，实际能否形成某一等级差取决于可用任务和准入条件。

**等级差带来的一次性进本压力不会触发美德／折磨判定。** 即使进本后正好是 100 压力，也要等到下一次实际加压才触发判定。修改全局规则后，加压或减压的最终量被压到 0 时是否会触发判定，分别待测。[证据记录](../Sources/starting_stress_affliction_check_20261125.json)

折磨英雄因这项进本压力达到 200 时，也不会触发心衰。详见[心衰判定](../Mechanics/21-美德与压力机制.md#折磨达到-200-压力时的心力衰竭)。

字段为 `effectiveDifficultyDungeonStartingStress`，见本体 `shared/rules.json:55`、明耀 `modes/radiant/shared/rules.json:55`、血月／狱火 `modes/new_game_plus/shared/rules.json:55`，等级差对应关系见《全局规则整理》“全局规则”第 36 行。进本后的受压倍率另由 `effectiveDifficultyStressDmgModifiers` 配置，见[压力伤害机制](../Mechanics/52-压力伤害计算与精准加压.md#等级差的全局修正与旧数值更正)。

## 黑暗之心转阶段进场血量

极暗地牢第四关由 `ancestor_pod_D` 转为黑暗之心 `ancestor_heart_D` 时，前一阶段的 `death_class:` 写有 `.carry_over_hp_min_percent 0.75`，因此黑暗之心进场时的血量至少为其最大生命的 75%。原版黑暗之心定义的基础最大生命为 252，按此最大生命计算，下限为 189 HP。

原版配置见 `monsters/ancestor_pod/ancestor_pod_D/ancestor_pod_D.info.darkest:12` 和 `monsters/ancestor_heart/ancestor_heart_D/ancestor_heart_D.info.darkest:3`。换算出现小数时的取整规则未知。知识库编写者推测为四舍五入，待实测。

## 出本疾病判定与圣水

出本前给英雄喝圣水，若疾病抗性 Buff 在出本结算判定时仍生效，可降低该英雄获得疾病的概率。原版 `holy_water` Effect（`effects/base.effects.darkest` 第 1938 行）写 `.duration 3`，其中 `holy_water_disease_resist`（`shared/buffs/base.buffs.json` 第 8383 行）使疾病抗性增加 33 个百分点。

| `shared/rules.json` 字段 | 原版表值 |
|---|---:|
| `disease_after_quest_min_chance` | `0.05` |
| `disease_max_chance` | `0.32` |
| `disease_hero_disease_resist_weight` | `0.33` |

明耀、极暗、狱火和血月的对应表值一致。见[出本疾病判定机制](../Mechanics/101-原版副本探索、扎营夜袭与出本结算.md#出本疾病判定读取当前疾病抗性)。

## 疗养院医疗室治病

在疗养院医疗室选择一种疾病治疗时，有概率一次治愈该英雄所有可由医疗室治疗的疾病。原版 `disease_quirk_cure_all_chance_upgrades` 的三档如下。

| 医疗室升级进度 | 一次治愈全部可治疗疾病的概率 |
|---|---:|
| 初始 | 33% |
| 解锁节点 `b` | 67% |
| 解锁节点 `d` | 100% |

数值见 `campaign/town/buildings/sanitarium/sanitarium.building.json:57,67–70`。节点见 `upgrades/building/sanitarium.upgrades.json:67` 下的 `sanitarium.disease_quirk_cost` 升级树。原版中文升级提示见 `localization/miscellaneous.string_table.xml:44763`。血病四种状态的 `can_modify_in_activity` 均为 `false`。[配置与适用范围](../Mechanics/46-怪癖描述显示与奇物手贱提示.md#疗养院医疗室一次治愈全部疾病的配置)

## 常规拖延与增援

仅原版及官方 DLC。以下实战时序来自清丽静《地牢大学习》系列 。可改字段及作用域见[增援判定专题](../Mechanics/38-友方技能目标与增援判定.md#增援的基础时间条件与加速)。

**怎么防增援（图 01–07、18）：** 在常见的 Size 1 阵容里，敌方存活单位少于 3 时开始计时；英雄少于 3 时不再触发拖延压力或召怪。都是原版门槛，英雄「人数」不等同于所有阵容的存活体积。同一整轮内全队使用两次合格技能即可重置计时；打尸体、打空，或英雄因血病／折磨自行放出合格技能，也可以计数。原版例子：小丑「独奏」`solo` 无伤害但能计入，未确认是唯一例外；学者 `disruptive_curse` 有伤害但不计入。不能以命中、造成伤害或伤害修正来判断技能是否计入。

| 视频称谓 | 从开始计时后的常规流程 | 视频中的原版例子（图 09–13） |
|---|---|---|
| 二回合增援 | 第 1 轮可刷状态，第 2 轮需防增援，否则第 3 轮召怪 | 骷髅弩手、鱿鱼哥、投矛猪 |
| 三回合增援 | 前 2 轮可刷状态，第 3 轮需防增援，否则第 4 轮压力惩罚、第 5 轮召怪 | 盾牌骷髅、蘑菇人、狂喜教众 |
| 无增援 | 没有常规拖延压力或召怪 | 二体型怪物、Boss、威尔伯、小爬、死疽真菌、蛇梦 |

混编取较慢的一档：无增援优先于三回合，三回合优先于二回合。这里的「二回合／三回合」指防增援的时机，不是实际召怪轮，也不是从任意战斗开场算起的绝对轮号。常见压力警告意味着下一轮可能召怪，不能视同已经召怪（图 02）。

- **致死 DOT 延时（图 14–17）：** 视频说明怪物下次行动的 DOT 足以致死时，可避免拖延压力或召怪。单怪演示在第 4 轮出现英雄警告、只有瘟疫打了一次，第 5 轮未按原计划召怪。不能外推成多怪场景中只要有一只会死就能阻止整场增援。
- **开场就只有两怪（图 19–20）：** 庭院双结网蛛、DD1 双狂喜的首次增援计时提前一轮，之后恢复通常时序。
- **教学关（图 21）：** 原版老路与遗迹教学本均无拖延压力或召怪。遗迹教学本有明确任务开关；老路默认两名英雄，低于原版门槛，尚未定位任务专属开关或实测改法。

本体及原版难度规则的对应配置值一致。下表是**配置值**，不能直接当作上表的战斗轮号：

| 字段 | 默认值 |
|---|---:|
| `stall_party_size_threshold` / `stall_enemy_size_threshold` | `3` / `2` |
| `stall_number_of_invalidating_skills_threshold` | `2` |
| `stall_round_stress_effect_threshold` / `stall_round_summon_effect_threshold` | `3` / `4` |
| `stall_round_reset_threshold` | `4` |
| `stall_extra_round_size_threshold` / `stall_extra_round_size_amount` | `2` / `1` |
| `stall_round_accelerated_only_consecutive_increment` / `stall_round_accelerated_only_increment` | `5` / `1` |
| `stall_stress_effect_name` | `stall_stress` |
