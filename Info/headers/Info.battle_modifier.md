# `battle_modifier:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物特有。
- **用途**：定义怪物在战斗目标、拖延、突袭、召唤站位和常驻 Buff 等方面的规则。
- **官方实例分布**：怪物 2517 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.disable_stall_penalty` | 布尔值：`true` 或 `false` | 怪物特有。 | 怪物侧阻止增援开关。true：只要该怪物仍在场便阻止增援发生；false：该怪物不通过此字段阻止增援。现有认识倾向于认为它与原版 Size 2 及以上怪物、Boss 的阻止增援逻辑处于同一层，但这一对应关系尚未专项验证，特殊怪物仍须结合 Size、Boss 身份与完整 battle_modifier 配置判断。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.does_count_towards_stall_penalty` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.accelerate_stall_penalty` | 布尔值：`true` 或 `false` | 怪物特有。 | 怪物侧常规拖延增援加速标记。true 标记加速，false 不加速。清丽静《地牢大学习》系列的原版观察是混编取较慢一档，禁用优先；不能仅因场上存在一只加速怪就断定全场加速。技能次数及压力、召怪阈值还需查全局规则。见专题 38 与原版副本数据速查表。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_surprise` | 布尔值：`true` 或 `false` | 怪物特有。 | 控制怪物方在战斗开始时是否允许令英雄方惊慌。true 只表示该怪物不禁止这一过程，不代表必定惊慌；现有高可信认识是，只要初始怪物队伍中任意一个怪物写 false，英雄方就不会被惊慌，但这一队伍级行为尚未专项验证。若没有该禁止项，夜袭时英雄方必定惊慌。中途召唤的怪物不参与，因为惊慌判定只发生在战斗开始。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_be_surprised` | 布尔值：`true` 或 `false` | 怪物特有。 | 控制怪物方是否允许在战斗开始时陷入惊慌。true 只表示该怪物不禁止这一过程，不代表怪物方必定惊慌；当前高可信认识是，只要初始怪物队伍中任意一个怪物写 false，整支怪物队伍便不会惊慌，但这一队伍级行为尚未专项验证。无 Mod 的原版常规环境中，英雄方与怪物方似乎只会有一方惊慌；该互斥关系同样尚未专项验证。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.always_surprise` | 布尔值：`true` 或 `false` | 怪物特有。 | true：怪物方在战斗开始时必定令英雄方惊慌，不依赖常规惊慌概率；false：不提供这种强制效果。若与同队怪物的 .can_surprise false 同时存在，二者优先级目前未知；不得猜测结果，创作时应避免冲突配置。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.always_be_surprised` | 布尔值：`true` 或 `false` | 怪物特有。 | true：怪物方在战斗开始时必定惊慌，不依赖常规惊慌概率；false：不提供这种强制效果。若与 .can_be_surprised false 同时存在，二者优先级目前未知；不得猜测结果，创作时应避免冲突配置。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_relieve_stress_from_crit` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_relieve_stress_from_killing_blow` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_be_summon_rank` | 布尔值：`true` 或 `false` | 怪物特有。 | true：可被视为召唤可占据站位；false：不可。Size-0 必须显式写 false，否则存在 rank 溢出崩溃风险。迂回表第 3 条 P369/X392 经当前用户于 2026-11-02 确认该风险边界；不表示每次省略均必定立即崩溃，非本轮新增实机测试。针对迂回表第 9 条 P444/X492，当前用户于 2026-11-02 进一步确认：尤其在连锁 spawn 与自灭流程中，未显式写 false 存在 rank 溢出崩溃并进一步导致存档循环卡死、无法正常继续的风险。不将其写成每次必现，也不推断存档永久损坏或具体恢复方法；非本轮新增实机测试。详见 Mechanics/05-size0召唤物.md。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.does_count_as_monster_size_for_monster_brain` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.does_count_as_guardable_for_monster_brain` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_be_missed` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_be_hit` | 布尔值：`true` 或 `false` | 怪物特有。 | false：禁止该怪物被命中。怪物 battle_modifier 中，`.can_be_hit false` 禁止被命中；`.can_be_damaged_directly false` 至少可以阻止直伤和 DOT。真伤的全类型覆盖尚未完全确认，但当前判断为大概率也会被阻止；原表‘包括真伤’保留为历史观察，不升级为当前版本对所有真伤调用均已确认。两者都是怪物预设开关，难以在战斗中灵活添加或取消，不能直接当作普通 Buff 随时开关的临时免疫方案。证据：迂回表第27条 P643/X726，当前用户于2026-11-02及2026-11-06补充；非本轮新增实机测试。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.is_valid_friendly_target` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_be_damaged_directly` | 布尔值：`true` 或 `false` | 怪物特有。 | false：至少阻止直伤和 DOT；真伤的全类型覆盖尚未完全确认，但当前判断为大概率也会被阻止。原表‘包括真伤’保留为历史观察，不升级为当前版本对所有真伤调用均已确认。该字段是怪物预设开关，难以在战斗中灵活添加或取消，不能直接当作普通 Buff 随时开关的临时免疫方案。证据：迂回表第27条 P643/X726，当前用户于2026-11-02及2026-11-06补充；非本轮新增实机测试。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_be_random_target` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_be_guarded` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.remove_on_retreat` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表 |
| `.living_other_enemy_buffs` | 后跟最多8个buff id，每个不超过64个字符；字符串参数至多 8 个；每个至多 64 字符 | 怪物特有。 | 怪物真光环所用的 Buff ID 列表字段。真光环机制随游戏 `Update` 刷新；迂回表第78条 P1329–P1330/X1580–X1581 记录任意敌我单位个人回合结束为其中一种 `Update` 时点。在下一次 `Update` 前瞬间生成并自灭的 Size-0 不会实际获得该机制施加的 Buff。此处不等同于单独声明 `bsrc_battle_modifier` 来源的 Buff，也不推定主动施加路径或所有版本。当前用户于2026-11-03确认并澄清刷新时点；非本轮新增实机测试。Cathelia 的 Abigail Williams 案例确认同一怪物 Info 可用多条 `battle_modifier:` 分行追加 `.living_other_enemy_buffs`。 | 静态合法字段表、Cathelia 的 Abigail Williams 案例、截图与知识库编写者于 2026-11-25 的实测确认；Sources/captor_release_effects_20261125.json、游戏本体/官方 DLC 实例 |
| `.living_hero_buff_instance_ids` | 后跟最多8个buff id，每个不超过64个字符；字符串参数至多 8 个；每个至多 64 字符 | 怪物特有。 | 怪物真光环所用的 Buff ID 列表字段。真光环机制随游戏 `Update` 刷新；迂回表第78条 P1329–P1330/X1580–X1581 记录任意敌我单位个人回合结束为其中一种 `Update` 时点。在下一次 `Update` 前瞬间生成并自灭的 Size-0 不会实际获得该机制施加的 Buff。此处不等同于单独声明 `bsrc_battle_modifier` 来源的 Buff，也不推定主动施加路径或所有版本。当前用户于2026-11-03确认并澄清刷新时点；非本轮新增实机测试。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.disabled_act_out_combat_start_turn_types` | 固定候选：`nothing`、`bark_stress`、`change_pos`、`ignore_command`、`random_command`、`retreat_from_combat`、`attack_friendly`、`attack_self`、`mark_self`、`stress_heal_self`、`stress_heal_party`、`buff_random_party_member`、`buff_party`、`heal_self`、`consume_item`；后跟最多4个CombatStartTurnType | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.ignore_hp_scale` | 布尔值：true 或 false；文档未说明省略默认值 | 怪物特有。 | true使怪物忽略Stygian及其他NG+难度带来的最大HP增加。所有生命反馈size-0必须添加；可50血启动、最大HP升至100不回血后继续，不再强制极小HP加极大倍率稀释。0.99向下/0.01向上空Effect sentinel仍必需。不是免疫任意生命Buff。 | 新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json；新增字段，不冒称旧插件或官方实例已有 |

## 怪物侧真光环与负数 DOT 例外

知识库编写者确认（2026-09-21）：怪物侧 `battle_modifier` 内的真光环机制可以带出并维持 Buff 型负数 DOT；这类 Buff 型负数 DOT 可以存在且生效。真光环机制不能写 Effect 型 DOT；该例外也不是把 Buff 改用单独的真光环源类型就能获得的通用效果。详见[负数 DOT 当前边界](../../Mechanics/66-负数DOT与不可治愈边界.md)。

迂回表第78条 P1329–P1330/X1580–X1581 的历史观察：这类真光环随游戏 `Update` 刷新；任意敌我单位的个人回合结束是原表记录的 `Update` 时点之一。因此，若 Size-0 在下一次 `Update` 前瞬间生成并自灭，它不会实际获得该真光环所施的 Buff。该边界只适用于这一路径，不外推到主动施加的 Buff、单独声明 `bsrc_battle_modifier` 的 Buff 或所有版本。当前用户于2026-11-03确认原表边界，并澄清刷新属于统一的 `Update` 机制；非本轮新增实机测试。

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\modes\bloodmoon\monsters\brigand_sapper\brigand_sapper_D\brigand_sapper_D.info.darkest:14`

```darkest
battle_modifier: .accelerate_stall_penalty False .disable_stall_penalty True .can_surprise False .can_be_surprised False .always_surprise False .always_be_surprised False .disabled_act_out_combat_start_turn_types retreat_from_combat
```

`DarkestDungeon\dlc\735730_color_of_madness\monsters\corpse_crystal\corpse_crystal_A\corpse_crystal_A.info.darkest:10`

```darkest
battle_modifier: .disable_stall_penalty False .can_surprise True .can_be_surprised True .always_surprise False .always_be_surprised False .is_valid_friendly_target False .can_relieve_stress_from_killing_blow False .can_be_summon_rank False .does_count_as_monster_size_for_monster_brain True .does_count_towards_stall_penalty False .can_relieve_stress_from_crit False
```

`DarkestDungeon\monsters\corpse\corpse_A\corpse_A.info.darkest:8`

```darkest
battle_modifier: .accelerate_stall_penalty True .disable_stall_penalty False .can_surprise True .can_be_surprised True .always_surprise False .always_be_surprised False .can_be_random_target False .is_valid_friendly_target False .can_relieve_stress_from_killing_blow False .can_be_summon_rank True .does_count_as_monster_size_for_monster_brain False .does_count_as_guardable_for_monster_brain False .does_count_towards_stall_penalty False .can_relieve_stress_from_crit False  .can_be_missed False .can_be_guarded False
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
