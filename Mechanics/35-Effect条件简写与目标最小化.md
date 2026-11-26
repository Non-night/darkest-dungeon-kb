# Effect 条件简写与目标最小化

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 条件简写不是普通目标条件
`.keyStatus`、`.skill_instant true`、`.monsterType` 都会引出临时简写 Buff。它们不是把任意 Effect 变成“若目标满足条件则正常施加”的通用开关。

- `.keyStatus` 属于 `.combat_stat_buff` 系列的条件简写，按本次攻击目标状态启用简写战斗属性 Buff，常见目标是 `performer`。
- `.monsterType` 与 `.keyStatus` 类似，也属于 `.combat_stat_buff` 系列的条件简写；它按本次攻击目标的怪物 type 启用简写战斗属性 Buff。
- `.skill_instant true` 使相关 Buff 在技能选择阶段提前施加，并在 Effect 实际引用时再次施加。
- 当同一条 Effect 使用 `.buff_ids` 引出外部 Buff 时，`.keyStatus` 与 `.monsterType` 会被按等同于 `.skill_instant true` 的机制处理；引用外部 Buff 定义不能绕开 instant-skill 的施加和清除规则。

此处 `Update` 与模型、真光环等章节所称 Update 为同一机制，见 [Update 的统一含义](01-effect执行模型.md#update-的统一含义)；不应另造一个独立的“Buff Update”。

三者引出的 Buff 默认属于 `bsrc_instantSkill` 源。该来源的 Buff 会在游戏发生 Update 时消失，例如：

- 其他单位回合开始；
- 玩家切换当前选择的技能；
- 其他会触发游戏状态刷新的 Update。

因此不能把其生命周期简化成“只在点击下一个技能时清除”。

## 两次施加与 `.buff_ids` 等同处理
高于 100% 的 `.chance` 配合 `.skill_instant true` 时，另有点击记忆丢失及首次点击可能重复施加的特殊边界，见[无动画翻页与点击状态](76-无动画友方技能与skill-instant限制.md)。首次点击可能重复与下列两个施加窗口不能直接视为同一机制。

当前已确认 `.keyStatus` 与 `.skill_instant true` 均存在两次施加：

1. **第一次施加**：从玩家点击技能图标开始，持续到直伤面板第一次结算为止。
2. **第二次施加**：从该 Effect 实际被引用的具体时序开始，时序与常规 Effect 相同。

第二次施加不固定为 AWR。若 Effect 属于 AWR，则从 AWR 时序开始；若属于普通 `queue false` 或 `queue true`，则分别从对应时序开始。还必须结合技能、饰品 Trigger、附魔 Buff 等调用来源的整体顺序判断。

对于 `.monsterType`，当前明确确认的是：当它通过 `.buff_ids` 引出 Buff 时，会被视为等同于 `.skill_instant true`，因此这些 Buff 同样按两次施加和 `bsrc_instantSkill` 的 Update 清除规则处理。不要把这一结论无条件扩展为所有未使用 `.buff_ids` 的未知组合均具有完全相同的内部流程。

## 自定义文本中的 `skill_instant` 用法

当前用户补充：在制作自定义文本时，很多 Effect 会使用 `skill_instant`，因为这种写法可以避免游戏自动渲染类似“增益自身”之类的通用 Buff/目标描述，让界面主要显示自定义文本本身。这个用法属于文本演出技巧，不应被误解成 `skill_instant` 的普通条件开关。

使用该技巧时仍必须同时检查：

- `.skill_instant true` 的目标限制和致命组合；
- 两次施加窗口及 `bsrc_instantSkill` 的 Update 清除；
- Buff 是否实际需要超过 1 回合；
- AOE 中是否会重复修饰同一施术者或同一次技能结果；
- 自定义文本是否仍需要精确的 `.target`、清理或其他善后。

若 Buff 需要精确作用于 `target`，不能为了隐藏目标描述强行使用 `skill_instant` 的致命目标组合。长期存在的 Buff 则须核对下文显式改源例外；仅要文本时也可评估 Effect 自身 `.description_tooltip_id`，不必引入即时施加机制。

## 禁用增益/减益技能与自定义文本的误伤风险

当前用户明确补充（2026-09-24）：在绝大多数情况下，都不应该设计或使用 `disable_combat_skill_attribute` 的 `buff` 或 `debuff` 副类型，也就是禁用增益技能/禁用减益技能。它们极其容易误伤自定义文本。

这是一条设计安全建议，不是语法非法结论：只有确有必要，并且已经逐项检查所有相关技能、Effect/Buff 描述和自定义文本的影响范围时，才考虑使用例外。该警告只针对 `buff` 与 `debuff` 两个副类型，不自动推广到 `heal`、`bleed`、`poison`、`stun`、`tag`、`stress`、`move`、`guard` 或 `daze`。

## Buff 承载的技能自定义文本须保留描述显示

知识库编写者补充（2026-09-20）：如果某条 Effect 是为了让技能描述显示自定义文本，不能在该 Effect 或其引出的 Buff 上写 `.has_description false`／`"has_description": false`。这样会使这条自定义文本不出现在技能描述中。

只有实际挂载出去、无需作为技能描述文本显示的 Buff（例如长期状态、纯辅助逻辑 Buff、寄存器或清理 Buff），才可以按其用途考虑 `has_description: false`。这与“Rule 不能直接控制文本显示”是两条不同边界：Rule 本身不能动态控制显示，而 `has_description false` 会静态关闭这条自定义描述的技能描述显示。

以上限于 **Buff 承载**的描述方案。新版 **Effect 自身**的 `.description_tooltip_id` 是另一条描述路径，即使 Effect 的 `.has_description false` 仍显示；不能套用本节的 Buff 隐藏规则。见[自定义描述方案](16-loc与loc2本地化覆盖优先级.md)。

因此审查 Buff 承载的自定义文本时先区分：

- `skill_instant` 或其他技能描述型自定义文本：必须保留 `has_description: true` 或省略为当前可见默认，不能写 `false`；
- 实际挂载出去且不需要进入技能描述的 Buff：才可按辅助用途写 `has_description: false`，同时仍须核对 `description_tooltip_id`、Rule、来源和生命周期。

## 默认来源的适用范围与瞬时效果限制
使用默认 `bsrc_instantSkill` 来源时，这些机制适合需要在当前技能处理期间保持生效的简写战斗属性 Buff，例如按目标状态或怪物类型修正施术者本次技能的伤害、精准或暴击。

它们**高度不建议用于瞬时效果**。如果设计要求某个 Buff 只影响当前某一步结算，而后立即消失，应使用准确指向实际对象的普通 Effect/Buff，并配合顺序、ID 定向驱散、二段驱散等已确认的善后方式。不能因为 `bsrc_instantSkill` 最终会在 Update 时清除，就把它视为足够短暂；在清除前，它仍可能干扰：

- 同一技能的后续 Effect；
- 饰品 Trigger；
- `attack_additional_effect_ids` 带出的附魔 Effect；
- 反击；
- 其他发生在下一次 Update 前的流程。

### 超过 1 回合的 Buff 与来源覆盖
如果某个 Buff 需要实际存在超过 1 回合，通常不应直接使用默认来源的 `.skill_instant true`、`.keyStatus` 或 `.monsterType` 引出，因为它们默认使用 `bsrc_instantSkill`，会在 Update 时清除。

这不是“`.skill_instant true` 布尔字段在任何情况下都绝对禁用长效 Buff”：若在同一 Effect 中用 `.buff_source_type` 明确覆盖为非 `bsrc_instantSkill` 的来源，例如 `.skill_instant true .buff_source_type bsrc_skill`，则可以保留即时获得窗口，并使 Buff 按新来源的生命周期处理。该方案并非通常设计，但有实际用途；必须继续核对两次施加、重复点击、AOE 重复、Buff 残留以及是否需要在其他技能中专门清理。

`.buff_ids` 只改变 Buff 的引用方式，不能自动覆盖来源；`.keyStatus` 或 `.monsterType` 与 `.buff_ids` 同用时，仍按等同于 `.skill_instant true` 处理，除非调用路径确实提供了明确的来源覆盖。反过来，Buff 只计划存在 1 回合或更短，也不代表这些机制必然合适。

## 目标最小化原则
没有绝对必要时，任何 Effect 都不得作用于设计范围之外的目标。

- `.target` 必须与设计要求的实际对象一致。
- 单体效果不得为了绕开崩溃、迁就某种简写或减少代码量而扩大为群体效果。
- `target_group` 不是 `target` 的通用替代品。
- 若某种简写无法在正确目标范围内安全实现设计，应更换机制，而不是扩大受术者范围。
- 对设计之外目标产生“数值为 0”“随后会清除”或“通常看不出影响”的 Effect，仍然属于错误目标扩张；不能以暂时看似无害为理由保留。

反例：某设计只要求给当前单体攻击目标施加临时易伤。`.keyStatus + target` 会立即崩溃，但不能因此改成 `target_group` 给整组目标施加易伤。正确方向是放弃该简写，使用精确指向当前目标的普通 Buff Effect，并在本次结算后及时清除。

## 致命目标组合
同一条 Effect 中，只要存在以下任一有效字段：

- `.keyStatus <status>`；
- `.skill_instant true`；
- `.monsterType <monster_type>`；

则 `.target` 绝对不得为 `target` 或 `target_enemy_group`，否则游戏必定立即崩溃。既有资料还把 `target_group`、`target_group_other` 列为 `.skill_instant true` 的不安全目标；在边界确认前同样禁止。

这条致命限制与目标最小化原则必须同时遵守：不能通过把目标换成设计之外的群体来“规避”致命组合。

## Agent 实现检查
写 Mod 前逐项确认：

1. 设计需要的是整个技能期间的简写 Buff，还是只影响某一步结算的瞬时 Buff？
2. 若使用 `.keyStatus` 或 `.monsterType`，是否确实在同一条 Effect 中提供了需要的简写战斗属性字段，或者明确通过 `.buff_ids` 引出了 Buff？
3. 若使用 `.buff_ids`，是否错误地以为外部 Buff 定义可以绕开 `.keyStatus`、`.monsterType` 的 skill-instant 等同处理？
4. 该 Buff 是否需要存在超过 1 回合？若是，不可保留默认 `bsrc_instantSkill` 来源；通常改用其他施加方式，明确采用 `.buff_source_type` 覆盖时则按新源核对生命周期、两次施加与清理。
5. 是否错误地把第二次施加固定理解成 AWR，而没有读取 Effect 的实际时序？
6. 是否考虑了 `bsrc_instantSkill` 在下一次游戏 Update 前仍可能干扰其他流程？
7. Effect 的最终受术者集合是否严格等于设计要求，是否为了绕开限制而扩大目标？
8. 是否触发已确认的致命目标组合或 `.skill_instant true` 的其他不安全群体目标？
