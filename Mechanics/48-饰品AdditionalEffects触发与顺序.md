# 饰品 Additional Effects 触发与顺序

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 2026-11-05 新版更新

新增move_skill_additional_effects、quest_start_additional_effects、combat_start_additional_effects、turn_start_additional_effects；所有饰品Trigger不再强制Buff来源。既有顺序表不自动代表新增四项相对排序，新增项排序未提供。

详见[新版字段与修复](96-新版Modding更新Buff技能地牢饰品怪癖.md)及`Sources/modding_update_20261105_remaining.json`。

## 当前剩余次数、初始上限与减少次数

`.set_trigger_limit N` 把目标饰品**当前剩余次数设为N**，不是设置以后不可超过N的永久上限。知识库编写者2026-11-05明确：至少此次更新前即如此；`trigger_limit`的语义是初始状态下的上限，不是后续能获得的次数上限。可以获得超过初始值的次数；“不封顶”不代表底层整数没有边界。

- 设置针对饰品；新版有`other_trinket`，不能固定只允许`this_trinket`。不是技能次数或饰品持有数量`limit`。
- `.trigger_limit_minimum_decrease`／`.trigger_limit_maximum_decrease`为对应increase的减少版；minimum与maximum是本次减少量的区间边界，不是剩余总次数上下限。
- **最低可能降到0、行为应与增加类似，均为知识库编写者推测**。具体随机抽取、单边缺省、超过剩余次数、负值、重置／存档行为未确认。
- 原有increase的最小／最大值描述的是本次增加量，不能当作后续可用总次数的封顶。
- 补录前插件已有set_trigger_limit，知识库有目标说明引用及increase词条，但缺少独立set词条；本次补齐，不宣称旧版没有此功能。

来源：文档B047–B050；当前用户2026-11-05补充“当前剩余／初始上限”语义及减少可能最低0；Sources/modding_update_20261105_effects.json；无本轮实机测试。

## 饰品目标不等于饰品静态附魔上下文

知识库编写者2026-11-11实测：技能直接引用及饰品静态Buff附魔中，目标为 `this_trinket`／`other_trinket` 的Effect内一切效果均不生效。不能因为Buff来自饰品，就把其附魔当成饰品Trigger的调用上下文。其他非饰品Trigger入口大概率也无效，但仍为推测。`this_trinket` 不额外渲染目标描述，`other_trinket` 会；描述不证明生效。饰品Trigger内已有字段支持不变。来源：`Sources/trinket_target_effect_scope_20261111.json`；详见[目标专题](02-target与群攻重复.md)。

饰品条目可以通过多种 `*_additional_effects` 数组，在相应行为发生时额外调用 Effect。

## 英雄 effect_chance 对 this_trinket 概率的影响

**英雄身上持有的 `effect_chance` 不能修饰饰品 Trigger 引出的、目标为 `this_trinket` 的 Effect 的 `.chance`。本条为已确认结论。**

本条限定英雄持有修饰 Buff、调用方为饰品 Trigger、目标为 `this_trinket` 的组合。不由此判定 `other_trinket`、常规单位目标或其他调用入口，也不表示该 Effect 自身的 `.chance` 无效。它与“在技能／饰品静态附魔中饰品目标不生效”的既有测试分别记录；本条不解释引擎内部原因。

来源：YuriRoseHime于2026-11-17 13:03:07提问，13:14:05反馈“看起来不能”；知识库编写者同日明确说明“这个看起来不能就是不能，记录一下吧”。据此撤销先前“初步观察，未确认”的标注，按已确认结论记录。原始聊天与确认保留于 `Sources/trinket_effect_chance_20261117.json`；具体测试代码及构建等元数据未提供，Agent未新增游戏实测。

### 静态 Buff 的补充测试反馈（暂行）

YuriRoseHime于2026-11-17 13:21:52补充：“就连静态buff里的effect_chance也不能修饰目标为this_trinket的effect”。本次按**社区补充测试反馈，暂行、非绝对结论**记录：改用静态 Buff 承载 `effect_chance`，在所述测试中仍未能修饰目标为 `this_trinket` 的 Effect 的概率。

原话未提供该静态 Buff 的具体载体、完整代码及调用参数，不补定其来源；不扩展为所有静态 Buff 均失效，也不据此判定 `other_trinket` 或常规单位目标。此前上节已确认的英雄持有修饰／饰品 Trigger／`this_trinket` 组合保留原有证据状态；本次新增反馈单独暂行记录。两条都不表示该 Effect 自身的 `.chance` 无效。

来源及原话：`Sources/trinket_effect_chance_20261117.json` 的 `supplements`。知识库编写者本次要求先记录、暂不作为绝对结论；Agent未新增游戏实测。

## 与技能 Effect 的关系

以攻击技能触发为例：

```json
"attack_skill_additional_effects": [
  "example_effect_a",
  "example_effect_b"
]
```

可将其理解为：当相应饰品 Trigger 成立时，数组中的 Effect 被拼接到本次技能自身的 Effect 之后执行。

- 数组元素填写 Effect 名称。
- 同一数组内的多个 Effect 按引用顺序参与执行，使用方式与技能 `.effect` 列表相近。
- 在相同大时序下，由饰品 Trigger **直接发起**的 Effect **永远晚于技能自身同一时序的 Effect**。
- 这条“晚于技能 Effect”的结论只用于同时序比较；仍需先检查 AWR、普通 `queue false`、`queue true` 等大时序，不能用 Trigger 分类顺序覆盖 Effect 自身的大时序。

## 饰品 Trigger 直发 Effect 与附魔/Size-0 链的时序边界

当前用户补充（2026-09-25）：上面的“饰品 Trigger 晚于同层技能时序”只适用于**严格由饰品 Trigger 直接发起的 Effect**，不能继续套用到下游调用链。以下几类都不属于饰品 Trigger 直发 Effect：

- 饰品 Trigger 直接带出的附魔，随后由附魔上的 `attack_additional_effect_ids` 等机制调用的 Effect；
- 饰品 Trigger 召唤的 size-0 的 `spawn` 或生命反馈（`hp_reaction`）中带出的 Effect；
- 饰品附魔召唤的 size-0 的 `spawn` 或生命反馈中带出的 Effect。

在 size-0 的 `spawn` 和生命反馈中继续带出的 Effect，其自身定义行所写的时序不能用来独立决定它处于哪一层；这些 Effect 应视为紧随真正触发它们的上游 Effect。对大多数情况而言，它们所处的时序层取决于召唤该 size-0 的召唤 Effect 所处的时序层，而不是下游 Effect 自己写出的时序字段。

若 size-0 会长期存在，则其生命反馈的时序取决于**真正引发生命变化并触发生命反馈的那个 Effect**；不能一律按最初的召唤 Effect 或饰品 Trigger 的时序固定处理。上述边界仍须结合实际调用方、是否发生附魔、size-0 是否已入场、生命变化来源以及死亡/清理时序逐项核对。

## AOE 与重复调用

饰品 Trigger 引出的 Effect 在 AOE 中具有与技能调用 Effect 相同的重复风险：

- AOE 命中多个目标时，触发链可能随每个技能目标分别执行；
- 若引出的 Effect 最终反复指向同一个单位或同一个群体，同一单位可能因技能目标数量而被执行多次；
- 不能默认“饰品 Trigger 对整次技能只触发一次”；
- 若设计要求整次技能只生效一次，应检查对应 Effect 是否需要 `.apply_once true`；
- 若用户没有说明是否允许随目标数叠加，必须询问设计意图，不得自行决定。

典型风险包括：AOE 技能触发一个以施术者、施术者全队或其他重叠目标集为目标的饰品 Effect，导致四个技能目标时同一受术者被执行四次。

## 多种饰品 Trigger 同时成立时的分类顺序

同一个英雄身上的饰品在同一技能或行为中同时触发多种 `additional_effects` 时，Trigger 分类按下列顺序从前到后执行：

| 顺序 | 字段 |
|---:|---|
| 1 | `friendly_skill_additional_effects` |
| 2 | `attack_skill_additional_effects` |
| 3 | `melee_attack_skill_additional_effects` |
| 4 | `ranged_attack_skill_additional_effects` |
| 5 | `attack_crit_additional_effects` |
| 6 | `riposte_skill_additional_effects` |
| 7 | `kill_performer_additional_effects` |
| 8 | `kill_all_heroes_additional_effects` |
| 9 | `kill_all_monsters_additional_effects` |
| 10 | `was_killed_all_heroes_additional_effects` |
| 11 | `was_killed_all_monsters_additional_effects` |
| 12 | `was_hit_additional_effects` |
| 13 | `was_hit_all_heroes_additional_effects` |
| 14 | `was_hit_all_monsters_additional_effects` |

该表确认的是 **Trigger 分类之间**的优先顺序。不能仅凭字段英文名继续补造每个 Trigger 的完整成立条件、击杀归属边界、尸体处理或目标集合；这些语义仍需结合原版实例与专项测试逐项整理。

**没有出现在上述表格中的其他 Trigger，其相对时序一律视为未知。** 不得根据字段名称、文件排列、饰品装备槽或原版常见写法将其擅自插入该顺序表。

`.battle_complete_combat_skill_id` 脱战自动调用官方移动时，会触发饰品的 `friendly_skill_additional_effects`。同一调用的友方技能附魔待测。见[脱战自动技能专题](72-skill-rule时效与全场范围.md)。

## `melee_attack_skill_additional_effects`：近战攻击技能 Trigger

```json
"melee_attack_skill_additional_effects": [
  "example_effect"
]
```

该字段在饰品佩戴者使用 `.type "melee"` 的**攻击技能**时进入触发链：

- 只有技能类型属于近战攻击时，才满足该 Trigger 的分类条件；
- 攻击未命中时仍会进入 Trigger 调用链，数组中各 Effect 最终是否执行由其自身的 `.on_hit`、`.on_miss` 等条件决定；
- 不能把 Trigger 名称理解为“只有命中后才开始调用”；
- AOE 技能按每个技能目标分别触发，因此仍然存在同一最终受术者被重复执行的风险；
- 若 Trigger Effect 指向佩戴者、施术者队伍或其他重叠目标，应检查 `.apply_once true`，并在用户未说明能否随目标数叠加时先确认设计意图。

正常反击不会正常触发该 Trigger；但反击可能错误触发其中处于 AWR 时序的 Effect，见后文异常边界。

## `was_hit_additional_effects`：被命中 Trigger

```json
"was_hit_additional_effects": ["When hit Self heal trigger effect"]
```

- 该 Trigger 对应**饰品佩戴者被来袭攻击成功命中**，不是佩戴者攻击别人成功命中；佩戴者成功闪避该次攻击时不触发。此处只确定该攻击命中条件，不由字段名称推定 DOT、真伤或其他受击路径。迂回表第70条 P1245–P1248/X1462–X1465 及官方 Fire's Edge 实例支持该方向；当前用户于2026-11-03确认纠正旧反向表述。
- 将被调用 Effect 的 `.on_miss` 写为 `false` 或 `true`，都不能把 `was_hit_additional_effects` 改造成“佩戴者闪避时触发”；Trigger 的成立条件在调用 Effect 之前已经决定。
- 命中判定与 Effect 自身 `.chance`、抗性和 `.on_hit`／`.on_miss` 是不同门；Trigger 成立不代表数组中的每条 Effect 必定成功。

上面的引用来自官方 Fire's Edge 的 `rw_charcoal_effigy`，位于 `DarkestDungeon/dlc/4964110_fires_edge/features/runaway/trinkets/runaway.entries.trinkets.json:63-66`；其 Effect 位于同一 DLC 的 `effects/runaway.effects.darkest:110`，含 `.target "performer" .heal 3 .on_hit true .on_miss false`。它是受击后自疗的官方配置实例，不是此处新增的实机版本兼容性测试。

## `on_dodge_additional_effects`：闪避时 Trigger

官方 Fire's Edge 的 `rw_warm_scarf` 在 `features/runaway/trinkets/runaway.entries.trinkets.json:21-24` 使用 `on_dodge_additional_effects`，引用 `On dodge attacker shuffle single trigger effect`；同一 DLC 的 `effects/runaway.effects.darkest:113` 为该 Effect 写有 `.on_hit false .on_miss true`。这是**佩戴者成功闪避时**的独立触发字段，不必借 `was_hit_additional_effects` 修改 Effect 命中门来模拟。其相对其他 Trigger 的分类顺序不在上表，当前不据此确定。

迂回表第70条 P1249/X1466 以“仅闪避时反击”引出特效，并指出会占用反击机制；保留为原表的历史替代方案，不能再称“仅闪避时触发一般只能借反击”。当前用户补充：这种迂回通常把反击做成**不实际造成伤害、只引出特效的虚假反击**，也可以设计成真正造成伤害的反击；两种设计都占用反击机制。这里不补造虚假反击的具体字段配置。当前用户于2026-11-03确认补入官方闪避 Trigger 实例；该实例证明该 DLC 中存在该写法，尚未逐版实测，不能对其他程序环境作跨版本保证。

受击和闪避 Trigger 已分别限定佩戴者被命中和成功闪避。两者引用的 Effect 通常直接写 `.on_hit true .on_miss true`，让 Trigger 本身决定走哪条分支。Effect 的 `.chance`、抗性等条件仍照常判断。

## `attack_crit_additional_effects`：攻击暴击 Trigger

```json
"attack_crit_additional_effects": [
  "example_effect"
]
```

该字段在饰品佩戴者的**攻击发生暴击**时调用数组中的 Effect。当前已确认的核心条件是“攻击暴击”；不能把治疗暴击或其他非攻击型暴击自动纳入该 Trigger。

AOE 攻击中，每个目标分别进行暴击判定。当前判断是：如果多个目标分别被暴击，则应按每个暴击目标分别触发一次 `attack_crit_additional_effects`。不过该多目标触发次数仍带有“应该”的测试边界，尚未完成严格专项验证：

- 在要求整次 AOE 只执行一次的设计中，不得直接假定该 Trigger 天然只触发一次；
- 应检查 Effect 的最终目标是否重叠，以及是否需要 `.apply_once true`；
- 默认 `target` 是否一定指向各自发生暴击的目标，目前没有得到确认，必须保留为未知，不能从“逐目标触发”继续外推目标语义。

反击与该 Trigger 的异常关系见下节：正常反击不会正常触发攻击暴击 Trigger，但可能错误触发其中的 AWR Effect。
## 反击与攻击类 Trigger 的异常边界

正常情况下，英雄发动反击时：

- 会进入 `riposte_skill_additional_effects`；
- 不会正常触发 `attack_skill_additional_effects`；
- 不会正常触发 `melee_attack_skill_additional_effects`；
- 不会正常触发 `ranged_attack_skill_additional_effects`；
- 不会正常触发 `attack_crit_additional_effects`。

但是存在一项引擎异常：反击会错误触发上述攻击、近战、远程、暴击四类 Trigger 中处于 **AWR 时序**的 Effect。因此不能仅凭“反击不会触发普通攻击 Trigger”就认定这四个数组中的 AWR Effect 在反击时绝对安全。

这里确认的是 AWR 异常，不得扩展成这四类 Trigger 的 `queue false` 或 `queue true` 也会被反击触发。

## `on_quest_complete_additional_effects`：任务成功 Trigger

```json
"on_quest_complete_additional_effects": [
  "example_effect"
]
```

该字段在任务**成功完成**时触发饰品数组中的 Effect：

- 任务失败不触发；
- 主动撤退不触发；
- 饰品留在城镇饰品仓库中时不触发；
- 同一英雄装备多个带有该 Trigger 的饰品时，任务成功后这些饰品的对应效果都会触发，不能只执行其中一件；
- Effect 在这一 Trigger 中的默认 `target` 究竟指向佩戴者、任务队伍还是其他对象，尚未确认，不能凭字段名猜测；需要明确目标时应在 Effect 中使用已验证的显式目标，并进行实测。

饰品位于副本背包时能否触发尚未实测；当前倾向认为不能。即使 Effect 写有 `.is_in_inventory true`，也疑似仍不能使副本背包中的饰品获得任务成功 Trigger，但该组合尚未严格确认，因此只能作为警告，不能提升为完全确定的引擎规则。
## `turn_end_additional_effects`：个人回合结束 Trigger

```json
"turn_end_additional_effects": [
  "example_effect"
]
```

该字段在轮到饰品佩戴者行动、并且该英雄的这次个人回合结束时调用数组中的 Effect：

- 它检测的是英雄的**个人回合结束**，不是整轮 `round` 结束；
- 与反击无关，反击不会被视为一次个人回合结束；
- 与 DOT 是否造成伤害本身无关，不能把 DOT 结算误当作独立的 `turn_end` 行为；
- 游戏没有一类在机制性质上独立于普通回合的“额外行动”。英雄再次获得行动机会时，那次行动仍按普通个人回合处理，其结束也属于个人回合结束；
- 眩晕导致英雄跳过行动时，当前判断是其回合仍会正常开始和结束，因而该 Trigger 应正常触发；但该点尚未做严格专项测试，应保留“应该”的不确定性；
- “错误结束回合”等异常结束方式能否触发，尚不明确。
- 知识库编写者于2026-11-11补充：回合结束 Trigger 在使用移动技能、跳过回合、撤退失败时均不触发。若先使用不结束回合的友方／进攻技能，再使用跳过回合或移动技能结算回合，回合结束 Trigger 也不会触发；该 Trigger 具有与 AD 类似的“前序操作由最终结算操作覆盖”边界。撤退失败不等于撤退成功，不能把本条推广到成功撤退。
- 当前用户补充（2026-09-30）：饰品 `turn_end_additional_effects` 的 Trigger 生效晚于该回合的燃烧伤害结算。因此，至少在该 Trigger 直接调用的 Effect 上，`queue` 与 `AWR` 对“赶在燃烧伤害前执行”没有帮助；可推测该 Trigger 直接引用的 Effect 在这个入口中的 `queue`/`AWR` 不具有可用于调整相对时序的意义。这里的“无时序意义”不是说 Trigger 完全没有时间概念，而是说它仍然固定晚于燃烧结算，不能用 Effect 的 `queue` 或 `AWR` 把它提前。
- 该结论只针对饰品个人回合结束 Trigger 的直接 Effect；饰品附魔、Trigger 召唤的 size-0、size-0 的 spawn/hp_reaction 下游 Effect 仍须按各自调用链与真正触发它们的上游 Effect 分析。

### DOT 的实际结算时间

不要把通常的 DOT 笼统称为“发生在英雄回合外”：

- 除燃烧外，DOT 在持有者的个人回合**开始时**结算；
- 燃烧在持有者的个人回合**结束时**结算。

这描述的是 DOT 结算时点，不等于 DOT 自身创建了一次新的行动或 Trigger 回合。

Effect 型燃烧不使用普通持续回合数；Buff 型燃烧保留自身持续时间。燃烧在持有者行动结束时结算后，默认减少燃烧前层数的 50%，剩余层数向下取整；这发生在 `round` / `after_turn` 类型 Buff 持续时间扣减之前。带燃烧单位因燃烧或其他原因死亡时，会触发野火蔓延，通常由左侧或右侧相邻目标随机一个获得死亡单位一半的燃烧层数并向下取整；`hp_dot_burn_decay_percent` 是否影响这次死亡蔓延，尚未确认。Effect 型与 Buff 型燃烧的合并、持续时间与低于 1 层行为见[燃烧生命周期](17-Buff持续时间类型与实际清除.md#effect-型燃烧的持续时间与两类燃烧的结算)。`wildfire_apply_adjacent_targets` 会把传播目标机制改为两个相邻目标。

## `kill_performer_additional_effects`：施术者击杀 Trigger

```json
"kill_performer_additional_effects": [
  "example_effect"
]
```

当饰品佩戴者是对应行为的施术者，并由该施术者完成击杀时，会调用数组中的 Effect。这里的“击杀 Trigger”不是只在英雄自己的常规行动回合内检测：

- 反击造成的击杀可以触发；
- 非燃烧 DOT 造成的击杀可以触发，因此它能够在英雄回合外触发；
- **击杀尸体可以触发饰品的 `kill_performer_additional_effects`。** 知识库编写者于 2026-11-24 再次确认。击杀尸体是否触发 Buff 击杀附魔（`kill_performer_additional_effect_ids`）尚未测试。
- **燃烧造成目标死亡时，确定不会触发击杀 Trigger。**
- 当前用户于 2026-10-08 确认：因真伤死亡的怪物不会触发英雄击杀 Trigger。

### 真伤死亡与 DOT 击杀归属的排除

因真伤而死的怪物不进入“因 DOT 而死”的击杀归属判定，也不会触发英雄身上的击杀 Trigger。即使该目标此前曾被英雄成功施加流血或腐蚀，也不能因为最后施加者规则而触发该英雄的击杀 Trigger。

这里的 DOT 特指流血和腐蚀；燃烧致死同样不会触发击杀 Trigger。此处是饰品击杀 Trigger，不能套用[击杀型 ActorDot 可识别部分非直伤击杀](10-最后一杀与非直伤击杀.md)的结论。不要把“真伤具有声明的 DOT 类型性质”与“英雄击杀 Trigger 一定会触发”混为一谈。

### 非燃烧 DOT 击杀的归属

非燃烧 DOT 致死时，击杀归属于**最后一个在该死亡目标身上成功施加 DOT 的英雄**。只触发该英雄身上的击杀 Trigger，而不是触发所有曾向目标施加过 DOT 的英雄的 Trigger。

例如：英雄 A 先成功对怪物 C 施加流血，英雄 B 随后也成功对 C 施加流血；C 在自己的回合开始时因流血死亡，则只触发英雄 B 身上的击杀 Trigger。这里要求“成功施加”：被抵抗、未实际挂上的 DOT 不取得最后施加者归属。

下列边界仍未确认：

- AOE 或其他一次行为同时击杀多个目标时，是整次行为只触发一次，还是按被击杀目标数量触发多次；
- `.kill` 等尚未单独核实的非伤害击杀是否触发；不作“大概率可以”的实现保证。`.health_damage` 真伤击杀已在上文确认为不触发英雄击杀 Trigger，不再列为未知；
- 其他特殊死亡来源如何归属施术者。

因此，不能把 `kill_performer_additional_effects` 简化为“仅在佩戴者正常回合用直伤击杀敌人时触发”，也不能在未测试的情况下依赖 AOE 多杀的具体触发次数。

新版所有饰品触发器不再强制Buff来源；`kill_performer_additional_effects`也可按Effect指定来源。迂回表第101条P1589/X1977的强制bsrc_trinket_additional_effect结果为旧版历史，不再要求仅为改源而转接size-0。原不结束回合时size-0挡鼠标风险独立存在。

## `riposte_skill_additional_effects` 的 AWR 无效 Effect

在饰品的 `riposte_skill_additional_effects` 中，部分写在 AWR 时序的 Effect 即使被调用也不会产生实际效果。当前已确认的无效内容包括：

```darkest
.kill 1
.kill_enemy_types ...
.health_damage ...
```

具体表现：

- `.kill 1`：目标怪物不会死亡，无事发生，等效于该 Effect 没有生效；
- `.kill_enemy_types`：目标怪物不会死亡，无事发生；
- `.health_damage`：目标怪物不会承受该真伤，无事发生。

将 `.kill 1` 或 `.kill_enemy_types` 改为普通 `queue false` 时，可以正常生效。`.health_damage` 在其他时序中的完整对照结果，本条不额外推断。

只能将“反击饰品 Trigger 的 AWR 对上述三类效果无效”视为已确认结论，不能泛化为 `riposte_skill_additional_effects` 中所有 AWR Effect 都无效。

## 尚未确认的边界

- 同一英雄装备多个饰品，且多个饰品使用同一种 Trigger 字段时，各饰品之间按装备槽、饰品条目顺序还是其他顺序执行，尚未在本页确认。
- 未列入顺序表的 Trigger 与已列 Trigger 之间的相对时序未知。
- Trigger 引出 Effect 时，仍须分别检查 `.on_hit`、`.on_miss`、概率、目标、`.apply_once` 与具体时序字段；数组存在不代表其中每条 Effect 必定实际生效。
- 不得把分类表误读成所有 Effect 无视 AWR/queue 的绝对总顺序。

## Agent 审查要求

1. 是否先执行技能自身的同时序 Effect，再执行饰品 Trigger 引出的同时序 Effect？
2. 同一行为触发多种 Trigger 时，是否按本页分类表从前到后分析？
3. AOE 中是否检查了每目标重复调用，以及最终受术者是否重叠？
4. 需要整次技能只生效一次时，是否评估 `.apply_once true`？
5. 用户未说明是否允许随目标数叠加时，是否先确认设计意图？
6. 是否避免用 Trigger 分类顺序覆盖 Effect 自身的 AWR、`queue false`、`queue true` 大时序？
7. 是否只对表内 Trigger 使用已知相对顺序，并将未列 Trigger 的相对时序保留为未知？
8. 反击时是否考虑攻击／近战／远程／暴击 Trigger 的 AWR Effect 可能被错误触发？
9. 分析 `melee_attack_skill_additional_effects` 时，是否要求佩戴者使用 `.type "melee"` 的攻击技能？未命中时是否仍进入触发链，并交由 Effect 自身 `.on_hit`／`.on_miss` 决定？AOE 是否按每目标触发并检查重叠目标与 `.apply_once`？
10. 分析 `attack_crit_additional_effects` 时，是否只按攻击暴击理解而没有纳入治疗暴击？AOE 多目标暴击时是否检查疑似逐暴击目标触发、最终目标重叠和 `.apply_once` 风险？是否避免猜测尚未确认的默认 `target`？
11. 分析 `on_quest_complete_additional_effects` 时，是否只在任务成功时触发，并排除失败、撤退和城镇仓库饰品？同一英雄装备多件此类饰品时是否全部触发？是否把副本背包与 `.is_in_inventory true` 的组合保留为疑似不触发，而没有当作定论？是否避免猜测尚未确认的默认 `target`？
12. 分析 `turn_end_additional_effects` 时，是否按英雄个人回合结束理解，而没有误写成整轮结束、反击结束或 DOT 的独立行动？是否把再次获得的行动按普通个人回合处理，并对眩晕跳过行动和错误结束回合保留已记录的不确定边界？是否记得该 Trigger 晚于燃烧伤害结算，且不能依靠直接引用 Effect 的 `queue`/`AWR` 提前到燃烧前？是否把“queue/AWR 对该相对时序无用”误写成“该 Trigger 没有时间概念”？
13. 分析 `kill_performer_additional_effects` 时，是否允许反击、非燃烧 DOT 与击杀尸体触发，并认识到它可在英雄回合外触发？是否明确燃烧致死确定不触发？非燃烧 DOT 致死时是否只归属于最后成功施加 DOT 的英雄？是否避免擅自确定 AOE 多杀的触发次数，或把 `.kill`／`.health_damage` 击杀的推测当作定论？
14. 是否避免在 `riposte_skill_additional_effects` 的 AWR 时序依赖 `.kill 1`、`.kill_enemy_types` 或 `.health_damage`？
