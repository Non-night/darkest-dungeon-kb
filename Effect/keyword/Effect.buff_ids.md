# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.buff_ids
# 分类
Buff/战斗属性
# 参数类型
多个字符串（最多 8 个）
# 参数约束
- 参数为一个或多个 Buff ID 字符串；解析后的最终参数数量最多 `8` 个。
- 每个 Buff ID 的长度不得超过 `64`；超过数量或单项长度限制都可能发生截断。
- 必须按引号外空白完成最终参数计数；不是按视觉行数或代码排版计数。超过 `8` 个时，改用合法分行拆分，或直接拆成两个不同 Effect；每个实际 `.buff_ids` 参数串都必须不超过 `8` 个。
- 多个参数由引号外的空白分隔；带引号的字符串内部可以包含空格，并仍按一个参数处理。
- 当前不确定包围字符串的引号是否计入 64 长度限制，也不确定引号内的空格是否计入。需要规避边界时，应让 ID 明显短于 64。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.buff_ids`：引用并向目标施加一个或多个已定义的 Buff，后续每个参数都是一个 Buff ID。
- 同一 `.buff_ids` 列表内部按书写顺序逐个施加：先写的 Buff 先施加，后写的 Buff 后施加。这个结论仅描述列表内部顺序，不等于所有 Effect 或所有外层时序都遵循同一规则。
- 若 Buff A 的清理逻辑会清除自身和 Buff B，则写 `.buff_ids A B` 可在能够引用 Effect 的场景中实现‘不可叠加、重复施加只刷新持续时间’：旧的 A/B 先按 A 的清理行为移除，随后 B 再被施加。该写法依赖 A 的清理配置、两次施加均成功以及持续时间覆盖关系正确。
- 同名 Effect 分行也可以实现同样结果：将同名 `aaa` 分别写成 `.buff_ids A` 与 `.buff_ids B` 两行，仍按同一逻辑 Effect 的引用顺序先施加 A、后施加 B。这里的‘分行’是同名 Effect 的多 Header 定义，不是任意两个不同名称的 Effect；跨 Mod 的同名 Effect 文件仍参与叠加。
# 作用范围
- 用于 Effect 定义行；每个参数对应一个 Buff ID。
- Effect 自身的 `.duration` 与 `.buff_duration_type` 会覆盖被引用 Buff 中的对应定义。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 详见：[Mechanics/17-Buff持续时间类型与实际清除.md](../../Mechanics/17-Buff持续时间类型与实际清除.md)
- 参数分割发生在引号外的空白处；例如 `"A crit" "B dmgl"` 是两个参数，而不是四个。
- 超过 8 个最终解析参数或单项长度超过 64 时可能截断，截断后的具体结果不应作为可依赖行为。需要更多 Buff 时使用分行或两个 Effect；不要把超过 8 个 ID 继续塞在同一条实际调用中。
# 常见错误
- 在同一 `.buff_ids` 中填写超过 8 个最终解析参数；需要更多 Buff 却没有拆成分行或两个 Effect。
- 使用长度超过 64 的 Buff ID，或依赖临界长度的未确认计数方式。
- 把带引号字符串内部的空格误认为参数分隔符。
- 同时在 Effect 与 Buff 中定义持续时间，却误以为 Buff 定义优先。
- 把 `.buff_ids A B` 的内部顺序误读为通用的跨 Effect、跨来源或跨 AWR/queue 时序结论。
- 未确认 A 确实清除自身和 B，或未确认清理后 B 仍会重新施加，就把该写法当作无条件的刷新机制。
- 忽略同名逻辑 Effect 的实际引用顺序和其他字段合并规则，或误以为跨 Mod 同名 Effect 文件会整文件覆盖。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:133`
```darkest
effect: .name "Bleed Debuff 1" .target "target" .chance 100% .buff_ids bleed_debuff_1 .on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:134`
```darkest
effect: .name "Bleed Debuff 2" .target "target" .chance 110% .buff_ids bleed_debuff_2 .on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:135`
```darkest
effect: .name "Bleed Debuff 3" .target "target" .chance 120% .buff_ids bleed_debuff_3 .on_hit true .on_miss false
```
# 参数分割案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:519`
```darkest
effect: .name "Vomit Debuff 1" .target "target" .chance 100% .buff_ids "Vomit BlightResist Debuff 1" .on_hit true .on_miss false
```
`"Vomit BlightResist Debuff 1"` 内含空格，但整体是一个参数。
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:614`
```darkest
effect: .name "Fortify Resists 1" .target "target" .curio_result_type "positive" .chance 100% .duration 3 .buff_ids "BLEEDRESIST10" "BLIGHTRESIST10" .on_hit true .on_miss true .queue true
```
两个带引号的 Buff ID 由引号外空格分隔，因此是两个参数。
## 列表内部施加顺序与刷新写法
同一 `.buff_ids` 列表按书写顺序逐个施加，先写的先处理，后写的后处理。若 Buff A 的 `clear_buffs_on_rule_active` 会清除自身和 Buff B：
```darkest
.buff_ids "A" "B"
```
可在能够引用 Effect 的场景中构成“不可叠加、重复施加只刷新持续时间”的写法：再次施加时，A 先清理旧的 A/B，随后 B 再施加。这里的“刷新”是清理旧实例后重新施加的结果，不是引擎对所有同 ID Buff 的普遍合并规则；必须确认 A 的清理配置、施加成功，以及 Effect 对 `duration` / `buff_duration_type` 的覆盖关系。
该结论只涉及同一个 `.buff_ids` 数组的内部顺序，不能直接外推到不同 Effect、不同调用来源或 AWR、`queue false`、`queue true` 之间的整体时序。
## `.buff_ids` 列表、同名分行与跨 Mod 施加顺序（2026-10-27社区实测）

证据来源：知识库编写者于2026-10-27提供的截图及聊天转录；外部来源作者无夜、Cathelia。不是本次Agent实机复测，不是反编译结论。截图标题为“由clear_buffs_on_rule_active参数反推buff_ids在同一行施加多个buff的顺序”。

### A/B测试与同文件分行
A具有 `clear_buffs_on_rule_active`，生效时清除A自身和B；B为常规Buff。截图所录无夜测试：

| `.buff_ids`参数顺序 | 观测结果 | 对顺序的解释 |
|---|---|---|
| A → B | B留存，A未清除随后施加的B | 先A后B |
| B → A | B不留存，被A清除 | 先B后A |

无夜于10-27 11:42:31、11:42:47、11:42:52补充：同名Effect分行也满足该顺序，观测与书写／阅读顺序一致；当时跨文件顺序未知。此处按同文件多Header的同名Effect分行记录，不是两个不同名称Effect的普遍时序。11:43:19提出跨文件可能按加载顺序，仅为当时推测。

### 跨Mod双向测试
Cathelia于10-27 11:45:54提出用两个Mod验证，18:03:36报告结果：两个Mod分别用同名Effect引出A/B；A为0防御的定向清理Buff，清除自身和B；B为+50%防御Buff，均有可见描述。

| 高优先级Mod | 低优先级Mod | 观测结果 | 支持的施加顺序 |
|---|---|---|---|
| A | B | 看不到B防御Buff，定向清除成功 | 低优先级B → 高优先级A |
| B | A | 能看到B防御Buff，A未清除后来施加的B | 低优先级A → 高优先级B |

已测结论：两份定义均实际保留、参与同名Effect分行时，`.buff_ids`的跨Mod施加顺序为**低优先级Mod先、高优先级Mod后**。这里的高低指聊天所述Mod优先级，不自行换算成未记录的数值或文件名字母顺序。报告作者据此解释为加载顺序；双向结果直接支持的是该同名分行Buff链的实际先后，不能据此证明所有游戏文件的内部加载算法。

### 同一Mod跨文件A/B双向测试补充（2026-10-27）
知识库编写者随后提供测试转述及截图 `codex-clipboard-51efe327-3e43-4641-bffb-54beb466dc4d.png`；本条按该次会话补充记录，不把上一轮无夜／Cathelia的署名自动套用于这次未署名的报告。截图中红框文件为 `AbigailWilliams.effects.darkest`（文件A）与 `BbigailWilliams.effects.darkest`（文件B），同目录另可见若干AbigailWilliams前缀文件；截图只用于辨认文件名，不证明其他文件参与测试或全部文件遍历顺序。

沿用同名Effect分行、定向清除与待清除Buff的测试语境，交换两份文件内的职责，得到：

| 文件A：AbigailWilliams.effects.darkest | 文件B：BbigailWilliams.effects.darkest | 观测结果 | 支持顺序 |
|---|---|---|---|
| 定向清除Buff | 待清除Buff | 待清除Buff留存，未被前者清除 | 先文件A、后文件B |
| 待清除Buff | 定向清除Buff | 待清除Buff不留存，被清除 | 先文件A、后文件B |

此处A/B是**文件标签**，不是上一轮固定指清理者A与普通Buff B；本次通过交换内容确认结果随文件先后变化，而不是清理Buff总在某个固定时点。

知识库编写者修正并补充（2026-11-04）：知识库编写者强调（2026-11-04）：文件名大小的排序规则仅适用于同一Mod／DLC内部；同目录下文件名小的先加载、大的后加载，按首字母排序理解，具体比较规则不明。不同Mod／DLC之间应按对应Mod／DLC优先级判断，不能跨来源比较文件名决定先后；低优先级先加载、高优先级后加载。同名Effect分行的重复单参数后加载覆盖先加载，buff_ids等多参数按实际加载顺序补充。跨子目录的内部顺序仍未确认。 在同一Mod／DLC、同目录、两定义均保留参与同名Effect分行时，文件名小的靠前、先加载，文件名大的靠后、后加载；这里的大小按首字母排序理解，具体采用哪种比较规则不明。原A/B双向测试支持A开头文件先于B开头文件。同名Effect分行的单参数覆盖也遵循相同加载顺序：后加载的覆盖先加载的，因此文件名大的文件中的重复单参数覆盖文件名小的文件中的值。这不同于.buff_ids等多参数内容按加载顺序补充。本次没有覆盖大小写、数字、标点、中文、共同前缀后的比较、子目录以及其他文件类型；不能升级成所有文件的通用加载或覆盖规则。原先“同一Mod跨文件未测”的空白已由此补充为“已测本组A/B先后，完整排序规则未知”。

### 适用边界
- 同列表按参数书写顺序，同文件同名Effect分行按定义书写顺序；跨Mod按上述低优先级到高优先级。不能再把同文件分行写成未知；无夜较早的跨文件未知被Cathelia后续跨Mod测试在该范围内补充，而非通用撤销。
- 同一Mod跨文件已由后续A/B双向测试补充：文件名小的先加载、文件名大的后加载（按首字母排序）；重复单参数后加载覆盖先加载；完整文件名比较规则、其他字符与子目录顺序仍未确认，见上节。
- **分行合并后的施加先后不等于整条或整文件覆盖**：跨 Mod 的同名 Effect 文件仍参与叠加，不能假定低优先级定义已整体丢失。多参数内容继续补充；重复单参数后加载覆盖前者，详见机制18。
- 聊天中“从低到高读、后读覆盖先读”的解释不升级为所有字段和所有文件类型的通则；来源作者也提示特殊文件例外。
- 不跨越AWR、普通queue false、queue true及调用来源层级推导任意Effect顺序；其他字段合并、8个最终Buff参数限制、定向清除条件仍分别按既有规则核对。

同名 Effect 分行也可采用等价写法；跨 Mod 的同名 Effect 文件仍参与叠加：
```darkest
effect: .name "aaa" .target "target" .buff_ids "A"
effect: .name "aaa" .target "target" .buff_ids "B"
```
同文件中，这两行属于同一个逻辑 Effect，仍能按 A 后 B 的顺序实现上述清理—重新施加效果。不要把它误读为两个不同名称的 Effect 分行；不同名称、不同来源或实际引用顺序不成立时，不能据此保证刷新。

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 参数数量、单项长度、截断风险和引号分组规则属于已整理的使用约束；64 长度限制的具体计数口径尚未确认。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
