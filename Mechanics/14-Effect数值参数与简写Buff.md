# Effect 数值参数与简写 Buff

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 2026-11-05 新版更新

新版ignore_stealth支持Rule；选择技能后改变条件时可能保留选择快照，但道具使用会打断技能选中。新增effect_chance、crit_dmg_add/multiply、heal_crit_chance_add/multiply、hp_heal_amount_received、disable_combat_skill见新版专题。

详见[新版字段与修复](96-新版Modding更新Buff技能地牢饰品怪癖.md)及`Sources/modding_update_20261105_remaining.json`。

## 术语范围
“Effect 简写 Buff”是总称，不能只理解为 `.buff_type` 系列。当前至少包括：

1. `.buff_type` / `.buff_amount` 系列，部分主类型还使用 `.buff_sub_type`；
2. `.combat_stat_buff 1` 与战斗属性改变量字段组成的系列。

两类写法的配套字段不同，不得混用规则。完整简写形式范围尚未穷举。

## 简写 Buff 的空 ID
- 所有由 Effect 简写形式生成的 Buff，其 Buff ID 均为空字符串，即 `""`。
- 这意味着它们不能像 `*.buffs.json` 中有独立非空 ID 的 Buff 一样，通过各自名称被 ID 定向区分。
- 如果某个常规 Buff 的 `clear_buffs_on_rule_active` 列表中包含空字符串 `""`，那么该清理 Buff 的持有者身上所有 ID 为空的 Effect 简写 Buff 都会被一并驱散。
- 这种写法不是“只清除某一种简写 Buff”，而是对持有者全部简写 Buff 的宽泛清除，极易误伤同一单位身上来自技能、饰品、反击或其他机制的简写 Buff，因此通常不建议使用 `""` 作为 ID 定向驱散项。
- ID 定向驱散只检查清理 Buff **持有者自身**的 Buff，不会借由 `""` 清除场上其他单位的简写 Buff。

## 通用数值写法
`.buff_amount`、`.attack_rating_add`、`.attack_rating_multiply`、`.defense_rating_add`、`.defense_rating_multiply`、`.crit_chance_add` 与 `.crit_chance_multiply` 都可写整数、小数或带 `%` 的数值。

- `_add` 表示加法／固定量修正，`_multiply` 表示比例／倍率修正；二者即使参数字面相同，结果也不相同。
- 精准与闪避都使用内部比例单位：游戏内显示的 1 点精准或 1 点闪避，在文件中均对应 `0.01`，不是 `1`；因此 10 点对应 `0.10`，文件值 `1` 对应 100 点。这也是 Info 中精准、闪避数值后经常带 `%` 的原因。
- 上述 `0.01 = 游戏内 1 点` 的换算目前明确适用于精准与闪避；不得无证据推广到其他战斗属性。
- 除数字型布尔外，其他 Effect 数值参数是否都接受这三种形式仍是未完全确认的推测，不能代替逐字段证据。

## 科学计数法与极大数值的描述边界

知识库编写者于2026-11-08提供Cathelia与无夜22:50–22:51的聊天及三张截图，并确认入库；证据见 `Sources/scientific_notation_20261108.json`，截图已随知识库保存相对路径副本及字节数、SHA-256。这是社区实测转述，不是本轮Agent实机测试。

- **直接实例**：截图中的抗性参数片段为 `.death_blow 3.4e38`，说明游戏存在可解析科学计数法的数值写法。截图未包含完整行首、Header或文件路径，不能将其补写成已验证的完整Info、Effect或Buff定义。
- **社区概括**：Cathelia说明“没溢出float就行”。保留其为社区说明；本次没有逐字段验证所有浮点参数，也没有提供精确浮点端点或超界实验。不能无条件扩展到整数、数字布尔、带百分号的指数形式或所有其他数值字段。
- **解析与描述分开**：同组截图中的基础提示出现 `inf% 基础`，Cathelia反馈描述异常，但该次没有崩溃。不得仅据此认定输入或内部实际抗性已成为无穷大，不推断描述异常的底层成因，也不推荐直接输入 `inf`。
- **实际有效范围不变**：同组另一张抗性面板仍显示死亡抗性 `87%`；这不是突破英雄死抗 `0%～87%` 有效范围的证据。参数可解析、描述能否正常格式化、最终有效值的上下限，是三个不同问题。
- **安全边界**：该次未崩溃不代表极大数值在所有后续运算、文本或调用路径均安全；不能把“未超出float”写成普遍安全保证，也不能据此改变既有逐字段参数约束。

## `.buff_type` / `.buff_amount` 系列
两者必须配套建立这一系列的 Effect 简写 Buff：

```darkest
.buff_type hp_heal_received_percent .buff_amount 20%
```

- `.buff_type` 选择主类型。
- `.buff_amount` 提供数值。
- 缺少任一字段时的引擎结果当前未确认；创作时必须成对填写。

## 同类 Buff 的数值加算
- 所有 Buff 类型在汇总同类数值贡献时都采用加算；不存在仅因某个 Buff `stat_type` 的固有性质，就令同类数值天然不可叠加的情况。
- 这里的“同类加算”描述的是已经同时有效的 Buff 如何汇总数值，不表示每次重复施加都必然新建一层。相同 ID、Buff 源、持续时间、刷新／覆盖规则、Rule 是否成立及调用次数仍可能决定实际能同时存在多少条 Buff。
- 各类型完成加算后，仍按自身机制处理上下限、取整、先加后乘或概率判定。例如 DOT 持续时间可能需要四舍五入；不能把“加算”扩展成所有类型具有相同的最终结算公式。侦查实际概率疑似存在大于0的下限，不能再用“固定截断至0%–100%”作为已确认示例，见专题50的水月测试记录。

原版实例：`DarkestDungeon\effects\base.effects.darkest:324`。

```darkest
effect: .name "Stacking Heal 1" .target "target" .curio_result_type "positive" .chance 100% .buff_type hp_heal_received_percent .buff_amount 20% .on_hit true .on_miss true .queue true
```

## `.buff_sub_type`
以下主类型必须同时填写副类型：

| `.buff_type` | 可用 `.buff_sub_type` |
|---|---|
| `combat_stat_multiply`、`combat_stat_add` | `max_hp`、`damage_low`、`damage_high`、`attack_rating`、`crit_chance`、`defense_rating`、`protection_rating`、`speed_rating`、`riposte_on_hit_chance`、`riposte_on_miss_chance` |
| `resistance` | `stun`、`move`、`poison`、`bleed`、`disease`、`debuff`、`death_blow`、`trap` |
| `activity_side_effect_chance` | `add_currency`、`remove_currency`、`add_trinket`、`remove_trinket`、`activity_lock`、`apply_buff`、`go_missing` |
| `disable_combat_skill_attribute` | `heal`、`buff`、`debuff`、`bleed`、`poison`、`stun`、`tag`、`stress`、`move`、`guard`、`daze` |

- 漏写必需副类型的结果当前未确认。
- 没有明确主副类型关系时，不要自行添加 `.buff_sub_type`。
- `unkown` 是已收录副类型的原拼写，不得擅自改为 `unknown`。

### `activity_side_effect_chance` 的设施活动副作用

城镇减压／治疗建筑中的常规活动通常持续一周；正常过周后，英雄结束活动并返回名册。但活动可能产生副作用，使英雄不能按通常流程立即恢复可用。`activity_side_effect_chance` 用于修正这类设施活动副作用的发生概率；当前只确认其用途，严格概率公式尚未明确，不得直接断言极端负值或合值小于等于 `0` 必定完全阻止副作用。

已确认的五个副类型含义如下：

| `stat_sub_type` | 已知含义 |
|---|---|
| `add_currency` | 提高设施活动产生“获得货币”这一正面附加结果的发生倾向／概率；只影响该结果是否发生，不影响获得的货币种类或数量。 |
| `add_trinket` | 提高设施活动产生“获得饰品”这一正面附加结果的发生倾向／概率；只影响该结果是否发生，不影响饰品数量、品质、稀有度或奖励池。 |
| `activity_lock` | 英雄被继续锁在当前设施中，即额外进行一周活动；发生后能否由玩家主动取消活动、令英雄提前返回名册，目前未知。 |
| `apply_buff` | 活动结束时给英雄施加 Buff；酒馆产生的此类 Buff 大概率是降低精准等负面效果，但具体结果仍由相应活动配置决定。 |
| `go_missing` | 英雄失踪一周；已知只能等待一周，不能通过其他常规操作使其提前返回。 |

`amount` 确认只修正对应结果的发生概率／权重，不修改结果内容；但其严格数学语义尚未确认。因此 `amount: 0.2` 不得直接断言为“最终概率增加 20 个百分点”或“乘以 20%”，也可能参与权重或其他概率公式。



### 生命比例 Rule 的闭区间阈值

以下四种 Buff Rule 的阈值都包含等号，`rule_data.float` 使用生命比例：

| `rule_type` | 满足条件 |
|---|---|
| `hpabove` | Buff 持有者当前生命比例大于等于阈值。 |
| `hpbelow` | Buff 持有者当前生命比例小于等于阈值。 |
| `target_hpabove` | 当前技能／Effect 的判定目标生命比例大于等于阈值。 |
| `target_hpbelow` | 当前技能／Effect 的判定目标生命比例小于等于阈值。 |

例如 `hpabove` 配合 `rule_data.float: 0.5` 时，持有者生命值恰好为 `50%` 也满足条件；不能按名称或本地化中的“高于”误解成严格大于。目标型 Rule 只改变被检查的单位，阈值边界与自身型完全相同。

四种 Rule 取反后都改为不包含临界值的开区间：`hpabove`／`target_hpabove` 取反后为严格小于阈值，`hpbelow`／`target_hpbelow` 取反后为严格大于阈值。不能把取反后的条件写成小于等于或大于等于。

### 亮度 Rule 的开区间与整数状态

当前用户本次补充明确：`lightbelow` 与 `lightabove` 的正向判定都是开区间，亮度临界值不成立；`is_false_rule: true` 取反后才包含临界值，变为闭区间。亮度状态本身只会取整数，因此不能把亮度当成可连续取小数的状态。

| `rule_type` | `is_false_rule: false`（正向） | `is_false_rule: true`（取反） |
|---|---|---|
| `lightbelow` | `current_light < rule_data.float` | `current_light >= rule_data.float` |
| `lightabove` | `current_light > rule_data.float` | `current_light <= rule_data.float` |

`rule_data.float` 虽然沿用数值槽位，亮度边界应按整数亮度点设计和复核；不要用小数亮度假设出游戏中不存在的中间状态。这个开／闭区间结论只针对亮度 Rule，不要套用到上面的生命比例 Rule。

### 目标类 Rule 的鼠标悬停判定

凡是检测当前目标状态、类型、生命比例等内容的 Rule，均可称为目标类 Rule。已明确验证的是 `actorStatus`：战斗中玩家鼠标碰到任一怪物的碰撞箱时，它会进行一次生效性判定。该行为可能用于刷新当前英雄攻击技能面板，但这一引擎目的只是推测。

其他目标类 Rule 应该也会在相同的鼠标悬停时机重新判定，但尚未逐项验证。审查时可以把这种行为作为高可信推测，用于解释悬停目标后技能面板变化；不能把它提升为所有目标类 Rule 均已实测的确定结论，也不能据此断言悬停判定就是最终施法结算。

### `random_target_attack_chance` 的单体攻击目标随机化

`random_target_attack_chance` 只干涉单体攻击技能，AOE 技能不受该 Buff 影响。随机化不会突破技能原本的合法目标集合，也不会把技能导向非法站位或非法阵营：

- 如果技能当前只有敌方 1 号位属于合法目标，那么即使触发随机化，最终仍只能攻击敌方 1 号位，实际目标不会改变。
- 如果技能存在多个常规合法单体目标，触发后只会从这些合法目标中随机选择。


随机化判定应发生在技能正式释放、接近伤害面板首次结算的阶段，而不是 AWR Effect 执行阶段。因而在 AWR 时序内才取得 `random_target_attack_chance` Buff，通常已经来不及干涉本次技能，应视为对本次目标随机化无意义。其与首次伤害面板结算的严格先后位置尚未逐帧确认，所以知识库只记录为“接近首次面板结算、早于 AWR 临时修改能够介入的窗口”，不得推断更细的内部调用顺序。



### `resolve_xp_bonus_percent` 的历练值奖励

- 英雄正常成功完成任务时获得历练值奖励；`resolve_xp_bonus_percent` 修正 Buff 持有者取得的该奖励。
- 多个同类 Buff 数值相互加算。例如 `amount: 0.1` 与 `amount: 0.2` 合计为历练值获取 `+30%`。
- 不同任务、难度对应的基础奖励值，以及非整数历练值如何取整，目前未知。
- 低于 `-100%` 的负向修正可能导致英雄降级，甚至从 0 级溢出为满级；这是异常边界，不得作为正常升级方案。

### 负值 Buff 型潜行抵消 Effect 型潜行

知识库编写者2026-11-08确认：负值的 Buff 型潜行（`stat_type: stealth`）可以抵消 Effect 型潜行。所需 `amount` 阈值推测为 `-1` 或更低，尚未确认，不能据此断言任意负值都能抵消。此处记录抵消表现，不等同于已证明删除或驱散原潜行 Buff，也不是 `ignore_stealth` 的目标选取豁免。

来源：`Sources/negative_stealth_skill_hover_20261108.json`；Agent未自行执行游戏测试。

### `ignore_stealth`：允许选择潜行目标

`ignore_stealth` 只干涉潜行带来的目标选择限制：

- 合计／最终 `amount > 0` 时，无视潜行有效，Buff 持有者的攻击技能可以选择正在潜行的敌人；
- `amount <= 0` 时，无视潜行无效；
- 它不会驱散、清除或改变目标身上的潜行状态；
- 它不会扩展技能原本的合法目标集合。潜行敌人在不考虑潜行时，仍必须是该技能依照阵营、站位及其他常规条件可以正常选中的目标；
- 因此它只解除“该合法敌人当前处于潜行，所以不能被选择”这一层限制，不能让技能攻击原本非法的站位、阵营或其他目标。

新版该Buff支持条件Rule；旧只能always的限制已退休。选择技能后改变条件可能不刷新目标选择快照，改选技能刷新；使用道具会打断技能选中，故不属于该未刷新窗口。它在作用方式上可理解为给持有者的攻击技能提供全局的潜行选取豁免，但不能据此把它解释成驱散潜行或无视所有目标限制。

## `combat_stat_add` 与 `combat_stat_multiply`

这两个值是 `.buff_type` 系列的主类型，都必须搭配 `.buff_sub_type` 与 `.buff_amount`，但语义不同：

- `combat_stat_add`：对指定战斗属性进行**固定量／加法修改**，不是根据当前属性值按比例缩放。
- `combat_stat_multiply`：对指定战斗属性进行**比例／倍率修改**，不是直接增加相同数值的显示属性点数。
- 二者填写相同的 `.buff_amount` 也不会得到相同结果，不能因为字段名称相近而互换。
- 所有 `combat_stat_*` 系战斗属性 Buff 都遵循**先加后乘**：先把固定值／`add` 修正计入基础属性，再对加法结算后的结果计算百分比／`multiply` 修正。不能先乘基础值再补固定值。

可按以下顺序理解单个属性的结算：

```text
加法结算值 = 基础属性 + 固定值加成
最终属性 = 加法结算值 × (1 + 百分比加成)
```

例如，基础闪避为 100 点，先获得固定 `+1` 点闪避，再获得 `+100%` 闪避，最终结果为 `(100 + 1) × (1 + 100%) = 202` 点闪避，而不是 201 点。

这里的“先加后乘”只是在说明 `combat_stat_*` 系战斗属性 Buff。**治疗量是明确的反例**：治疗先结算治疗造成量／所受量等百分比修正，最后再结算固定治疗量；详见[治疗源与真吸血](27-治疗源与真吸血.md)。

精准 `attack_rating` 与闪避 `defense_rating` 都使用内部比例单位：

| 游戏内显示变化 | 文件中的固定增加值 |
|---|---:|
| 1 点精准 / 1 点闪避 | `0.01` |
| 10 点精准 / 10 点闪避 | `0.10` |
| 100 点精准 / 100 点闪避 | `1` |

因此，设计稿中的“精准 +10%”或“闪避 +10%”都具有真实歧义：既可能表示“固定增加 10 点／10 个百分点”，也可能表示“按当前属性提高 10%”。Info 或 UI 使用百分号不能消除这种歧义。**遇到这类存在合理争议的描述，必须先向用户确认其意图，不能自行选择 `combat_stat_add` 或 `combat_stat_multiply` 后直接写代码。**建议让用户明确写成“精准／闪避增加 N 点”或“当前精准／闪避按比例提高 N%”。

在 `.buff_type combat_stat_add .buff_sub_type attack_rating/defense_rating` 的固定增加语义下，`.buff_amount 0.01` 对应游戏内增加 1 点精准／闪避；若写 `.buff_amount 1`，则对应增加 100 点。此固定点数换算不得套用于 `combat_stat_multiply`。

这里讨论的是 `.buff_type combat_stat_add/combat_stat_multiply` 配合 `.buff_amount`、`.buff_sub_type` 的体系。`.combat_stat_buff 1` 配合 `.attack_rating_add/.attack_rating_multiply` 是另一套 Effect 简写字段；两套体系遵循同样的“加法与倍率不同”原则，但字段结构不得混用。

### 已知红字行为
- 当 `.buff_type` 为 `riposte` 时，可以填写 `.buff_sub_type`。
- 该组合有可能产生红字报错，但并非必然报错；具体触发范围尚未明确。
- 如果产生红字，已知表现是 Buff 仍会出现并生效。
- 当前尚未确认还有哪些主类型存在同类情况。

## `.combat_stat_buff` 系列
`.combat_stat_buff 1` 与具体战斗属性改变量字段配套，形成另一类 Effect 简写 Buff，不使用 `.buff_type` 或 `.buff_amount`。原版配套实例包括 `.speed_rating_add`、`.attack_rating_add`、`.defense_rating_add`、`.crit_chance_add`、`.damage_low_add`、`.damage_high_add`、`.damage_low_multiply`、`.damage_high_multiply` 等字段；`.crit_chance_multiply` 也属于该系列。

伤害字段中，`low` 与 `high` 分别对应最低伤害和最高伤害；`_add` 表示加法修正，`_multiply` 表示倍率修正。四个字段的参数性质与其他数值型战斗属性简写字段相同：可写整数、小数或带 `%` 的数字。

```darkest
.combat_stat_buff 1 .attack_rating_add 5
```

形成普通/通用精准 Buff；“普通/通用”不表示 Buff 源类型。

`.attack_rating_multiply` 使用相同的配套判断原则，但原版与官方 DLC 中未找到直接 Effect 实例。

## `.riposte` 相关简写

### 开启反击不要求反击技能定义

获得反击 Buff（也即开启反击）无需拥有反击技能定义，但没有 `riposte_skill:` 反击技能定义的角色不会实际触发反击。开启状态与存在可执行的反击技能是两个条件，不能把缺少定义当成无法获得反击 Buff，也不能把获得状态当成已具备实际反击能力。

这是现行行为规则，不应仅因旧版“缺少定义时触发会崩溃”的说法而禁止通用反击饰品或技能赋予反击。该规则不保证其他反击配置错误也安全，不补造没有反击定义时反击附带 Effect／Trigger 的调用表现。

证据：当前用户于2026-11-03明确要求按上述现行规则表述；迂回表第52条 P1126/X1311记录删除英雄反击定义后赋予反击、挨打不再崩溃的历史对照测试，P1127/X1312转述 MLD 对旧问题修复的结论。具体修复版本及年份未知，原表估计的年份不写成确定日期；非本轮新增实机测试。

### 反击技能定义与持续回合

`riposte_skill:` 只定义反击实际触发时使用的技能数据。反击技能定义本身无需、也不能写反击持续回合；不要把普通 Buff 的 `.duration` 写到 `riposte_skill:` 行中。

有限时长的反击通常由开启反击的 Effect 声明持续时间，例如在包含 `.riposte 1` 的 Effect 上写 `.duration N`。这本质上是在声明该 Effect 生成的反击 Buff 持续多少回合，而不是声明反击技能本身持续多少回合。

如果饰品提供的是永久反击，则不需要为反击技能或相关饰品 Buff 另写持续回合数；应按饰品 Buff 的生命周期处理。

```darkest
.riposte 1 .attack_rating_add 0.01
```

形成反击源精准 Buff。

原版普通/通用实例：`DarkestDungeon\effects\base.effects.darkest:242`。

```darkest
effect: .name "ACC Debuff 1" .target "target" .curio_result_type "negative" .chance 75% .combat_stat_buff 1 .attack_rating_add -10% .on_hit true .on_miss false
```

原版反击源实例：`DarkestDungeon\effects\base.effects.darkest:19`。

```darkest
effect: .name "Riposte Example" .target "performer" .curio_result_type "positive" .chance 100% .riposte 1 .riposte_on_hit_chance_add 100% .riposte_on_miss_chance_add 100% .on_hit true .on_miss true .duration 2 .damage_low_add 0.01 .damage_high_add 0.01 .attack_rating_add 0.01 .crit_chance_add 5% .riposte_effect "Wyrd Bleed 5"
```

## Buff 源边界
- 所有 Buff 都具有来源，来源可由施加方式决定或由专门字段声明。
- 推理 Buff 的清除、叠加或触发行为时必须同时检查来源。
- 不得从“普通/通用精准 Buff”直接推断具体 `.buff_source_type`。
