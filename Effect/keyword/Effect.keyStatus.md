# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.keyStatus
# 分类
扩展/专项字段
# 参数类型
枚举/固定候选值
# 参数约束
- 参数必须来自固定候选表。
- 常规条件 Effect 的 `.chance` 使用 `100%`；非无动画翻页设计不得使用其他概率。
- 同一条 Effect 中存在有效 `.keyStatus` 时，`.target` 绝对不得写为 `target` 或 `target_enemy_group`；该组合会使游戏立即崩溃。
- 本字段属于 `.combat_stat_buff` 系列的条件简写，通常与该系列的简写战斗属性字段搭配使用；不要把它当成给目标施加任意普通 Buff 的通用条件字段。
- 需要长效Buff时不可保留默认bsrc_instantSkill来源；显式.buff_source_type覆盖后须按新源核对生命周期、重复和清理。
# 固定值 / 参数候选
- `tagged`
- `poisoned`
- `bleeding`
- `stunned`
- `dazed`
- `burning`
# 语义
- `.keyStatus` 是 Effect 的条件简写机制：按本次攻击目标的状态启用同一条 Effect 中的简写战斗属性 Buff；常规写法通常把该简写 Buff 施加给 `performer`。
- `tagged`：目标被标记。
- `poisoned`：目标具有腐蚀。
- `bleeding`：目标具有流血。
- `stunned`：目标处于眩晕。
- `dazed`：目标处于迷乱。
- `burning`：目标正在燃烧。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.keyStatus` 属于 `.combat_stat_buff` 系列条件简写；它与 `.skill_instant true` 均有两次施加。
- 与 `.buff_ids` 同用时，引用 Buff 按 `.skill_instant true` 处理；引出的 Buff 默认属于 `bsrc_instantSkill` 源并在游戏 Update 时消失。
- 需要存在超过 1 回合的 Buff 不应使用默认 `bsrc_instantSkill` 来源；若用 `.buff_source_type` 明确覆盖为非该来源，则可以保留 `.skill_instant true` 的即时获得窗口，但必须核对生命周期与清理。
- 详见：[Mechanics/35-Effect条件简写与目标最小化.md](../../Mechanics/35-Effect条件简写与目标最小化.md)
- `.chance` 低于 `100%` 时会产生红字并强制按 `100%`；高于 `100%` 时进入无动画翻页特殊行为。
- 知识库编写者确认（2026-09-20）：高概率 skill_instant 点击流程中，切换模式或调用虚拟道具必定清除技能选择／按下状态，获得禁用类 Buff 可能清除；模式翻页因点击即取消选择而无法正常释放。其他保留选择状态的即时效果仍可正常释放技能。
- 保留选择状态的即时效果，首次点击可能施加两次，原因和具体条件未知。不能与选择阶段／实际引用两个施加窗口混同，也不保证 apply_once 可修复。上 Buff 等可累积操作必须考虑该重复。详见 Mechanics/76-无动画友方技能与skill-instant限制.md。
- 致命组合：有效 `.keyStatus` 与 `.target "target"` 或 `.target "target_enemy_group"` 位于同一条 Effect 时，游戏必定立即崩溃。
- `.keyStatus` 存在两次施加：第一次从点击技能图标开始，持续到直伤面板第一次结算；第二次从该 Effect 实际被引用的具体时序开始，并按常规 Effect 的 AWR、`queue false`、`queue true` 等时序执行。
- `.keyStatus` 引出的简写 Buff 默认属于 `bsrc_instantSkill` 源；该源 Buff 会在游戏 Update 时消失，例如其他单位回合开始或玩家切换当前选择的技能。
- 同一条 Effect 使用 `.buff_ids` 引出外部 Buff 时，`.keyStatus` 会使这些 Buff 按 `.skill_instant true` 的机制处理，默认来源不会自动获得其定义中的长期存续能力；显式.buff_source_type覆盖时另按新源生命周期核对。
- 默认来源适合当前技能期间的简写Buff，高度不建议用于只应影响某一步的瞬时效果；长效用途须显式.buff_source_type覆盖并检查两次施加及残留。
# 常见错误
- 将有效 `.keyStatus` 与 `.target "target"` 或 `.target "target_enemy_group"` 写在同一条 Effect。
- 为实现单次结算中的临时效果而优先使用 `.keyStatus`，或为了规避致命目标组合而把单体目标扩大为群体目标。
- 试图用 `.buff_ids` 绕开 `bsrc_instantSkill` 的 Update 清除，让 `.keyStatus` 引出的 Buff 存续超过 1 回合。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:294`
```darkest
effect: .name "WebKiller"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:300`
```darkest
effect: .name "BleedKiller"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "bleeding"	.combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:710`
```darkest
effect: .name "BH Dmg Marked"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 90%	.damage_high_multiply 90%	.on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
