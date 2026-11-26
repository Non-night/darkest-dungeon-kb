# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.skill_instant
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数必须为 `true` 或 `false`。
- `true` 时 `.target` 绝对不得为 `target` 或 `target_enemy_group`；该组合会使游戏立即崩溃。
- 既有资料还把 `target_group`、`target_group_other` 列为 `.skill_instant true` 的不安全目标；在其边界得到进一步确认前同样禁止使用。
- 常规用法的 `.chance` 写 `100%`；高于 `100%` 用于明确设计的点击即时执行／翻页迂回，须检查点击记忆丢失和首次点击重复。
- 默认 `bsrc_instantSkill` 来源的 Buff 会在 Update 时清除；若设计要求长效存在，可用 `.buff_source_type` 覆盖为非该来源，例如 `.skill_instant true .buff_source_type bsrc_skill`，但必须核对残留、重复施加和清理。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- `true`：启用两次施加。第一次从点击技能图标开始；第二次从该 Effect 实际被引用的具体时序开始。
- `false`：不启用 skill_instant 的即时执行；该 Effect 仍可按普通引用时序执行。
- 当前用户补充：自定义文本有时使用 `skill_instant` 来避免自动渲染“增益自身”等通用目标描述，使界面主要显示自定义文本；这是文本演出技巧，不是通用条件开关。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.skill_instant true` 第一次从点击技能图标开始，第二次从 Effect 的实际引用时序开始；第二次不固定为 AWR。
- 引出的 Buff 默认属于 `bsrc_instantSkill` 源，并在游戏 Update 时消失；下次 Update 清除的根本原因是该 Buff 源，而不是 `.skill_instant true` 本身。可用 `.buff_source_type` 覆盖默认来源，例如 `.skill_instant true .buff_source_type bsrc_skill`，从而保留即时获得窗口并使 Buff 不因 `bsrc_instantSkill` Update 清除。
- AOE 中若它反复修饰同一施术者或同一次技能结果，未写 `.apply_once true` 时可能按技能目标数重复叠加；是否去重取决于设计，未说明且会明显改变强度时必须询问用户。详见 Mechanics/02-target与群攻重复.md。
- 详见：[Mechanics/35-Effect条件简写与目标最小化.md](../../Mechanics/35-Effect条件简写与目标最小化.md)
- 无动画翻页若写在官方移动技能中，不会出现上述心控卡死问题，因为官方 AI 不可能调用官方移动技能，不会满足“AI 实际调用该类技能”的触发条件。当前用户于2026-11-03明确补充；非本轮新增实机测试。本项针对官方 AI 与官方移动技能，不据此扩展到自定义 AI；脱战返回等系统流程另按对应调用处理。
- 无动画翻页技能在英雄被心控或发生自主行动时，若 AI 实际调用了该类技能，会导致回合永久卡死；不能省略“AI 实际调用”这一条件。针对心控，可将迂回中的切换模式代码改写为调用虚拟道具执行，以规避该卡死；代价是出现一次 item 越界黑屏，原表记载该次黑屏没有其他副作用。黑屏说明仅限此流程，不推广任意 item 黑屏；该方案不适用于自主行动。证据：迂回表第38条 P944/X1102–P946/X1104，当前用户于2026-11-03确认；非本轮新增实机测试。
- 无动画翻页的本质是点击技能图标时触发即时效果，根本没有释放技能。因此绝对不会触发任何以释放该技能为前提的相关特效，包括技能释放类饰品特效、友方技能特效及相关 ActorDot；反复点击翻页也不会因释放技能而反复触发它们。这一结论不限于“友方技能”分类，而是根本没有技能释放事件。无动画翻页本身的即时效果仍按点击执行；其他保留点击记忆并随后实际释放技能的 skill_instant 用法，须按其实际释放处理。证据：迂回表第38条 P943/X1101，当前用户于2026-11-03补充本质及绝对不触发的结论；非本轮新增实机测试。
- 迂回表第38条 P937/X1095 的“己方全体”具体指 `.target performer_group`：在该条所述 `.skill_instant true` 无动画切换流程中可指向己方全体，原表观察为会报错但不会崩溃。当前用户于2026-11-03明确该目标枚举；非本轮新增实机测试。此观察不解禁 `target_group`、`target_group_other`，也不改变 `target`、`target_enemy_group` 的已确认致命组合；不能仅按“群体”或“己方”字面互换参数。
- `.chance` 低于 `100%` 时会产生红字并强制按 `100%`；高于 `100%` 时进入无动画翻页特殊行为。
- 致命组合：`.skill_instant true` 与 `.target "target"` 或 `.target "target_enemy_group"` 位于同一条 Effect 时，游戏必定立即崩溃。
- 第一次施加窗口从点击技能图标开始，到直伤面板第一次结算为止。第二次施加不固定在 AWR；它从该 Effect 的实际引用时序开始，并按常规 Effect 的 AWR、`queue false`、`queue true` 等时序执行。
- `.skill_instant true` 引出的 Buff 默认属于 `bsrc_instantSkill` 源；该源 Buff 会在游戏 Update 时消失，例如其他单位回合开始或玩家切换当前选择的技能。
- 若用 `.buff_source_type` 覆盖为非 `bsrc_instantSkill` 来源，例如 `.skill_instant true .buff_source_type bsrc_skill`，首次点击可能因原因尚不明确的双重施加而使 Buff 错误堆叠；这是需要注意的风险，不是绝对禁用规则。
- 该机制只适合需要覆盖当前技能处理期间的 Buff，高度不建议用于只应存在于某一步结算窗口的瞬时效果；需要瞬时窗口时应使用明确施加与及时善后的实现。
- `bsrc_instantSkill` 的 Update 清除优先于长期持续时间设计；若覆盖为非该来源则不适用这条默认清除，但仍需核对首次点击双重施加、长期残留和清理。
- 使用该字段隐藏自动目标描述时，仍须遵守目标崩溃、两次施加、AOE 重复和生命周期限制；不能为了文本表现把长期 Buff 强行改成 skill-instant。
- AOE 会按每个技能目标调用 Effect。若 `.skill_instant true` 用于修饰同一个施术者或同一次技能结果，而未写 `.apply_once true`，该 Effect 可能随每个 AOE 目标重复施加，使目标越多、当前技能获得的修正越强。
- 上述风险并不表示 AOE 中的 `.skill_instant` 一律必须写 `.apply_once true`：若设计明确要求随目标数叠加，可以保留重复；若要求整次技能只修饰一次，通常应考虑 `.apply_once true`；设计未说明且会明显改变强度时必须先询问用户。
# 常见错误
- 将 `.skill_instant true` 与 `.target "target"` 或 `.target "target_enemy_group"` 写在同一条 Effect。
- 把第二次施加固定解释为 AWR，或用 `.skill_instant true` 实现只应影响某一步结算的瞬时效果。
- 给需要存在超过 1 回合的 Buff 使用默认 `bsrc_instantSkill` 来源的 `.skill_instant true`；若有明确设计需求，可用 `.buff_source_type` 覆盖为非 `bsrc_instantSkill` 来源，但必须单独核对残留、重复施加、首次点击双重施加风险和清理。
- 在 AOE 中用 `.skill_instant true` 修饰同一施术者或同一次技能结果，却未检查各目标调用是否会重复叠加，也未在设计不明确时询问是否需要 `.apply_once true`。
# 代码案例
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:56`
```darkest
effect: .name "RW Ransack ACC Stealthed" .target "performer" .skill_instant true .chance 100% .buff_ids rw_acc_stealthed .on_hit true .on_miss false
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:451`
```darkest
effect: .name "Stake Vampire Damage 1" .target "performer" .skill_instant true .buff_ids fanatic_crit_chance_buff .on_hit true .on_miss false .queue false
```
- 官方 DLC `702540_shieldbreaker`：`DarkestDungeon\dlc\702540_shieldbreaker\effects\shieldbreaker.effects.darkest:29`
```darkest
effect: .name "SB Crit Guarded 1" .target "performer" .skill_instant true .chance 100% .buff_ids "sb_kill_guarded_buff_crit_1" .on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
