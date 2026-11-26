# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.apply_once
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数使用 `true` 或 `false`；省略时默认为 `false`。
- `true` 只抑制同一次技能或同一调用流程内的重复，不是跨技能、跨回合或全局锁。
- 去重疑似按 Effect 的 `.name` 判断；同名 Effect 在同一流程中通常最多实际生效一次，但该判定模型尚未完全确认。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- `.apply_once true`：抑制同一次技能或调用流程中同名 Effect 的后续重复生效；作用不限于群攻按目标重复调用。
- `.apply_once false`：不启用该重复抑制。
# 作用范围
- 可影响群攻技能、单体技能内的同名 Effect 重复引用，以及饰品 Trigger 等非技能调用。
- 非技能系统中何时算作同一个调用流程尚未完整确认。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 会抑制同一次技能或调用流程内同名 Effect 的重复生效，不限于群攻；单体技能重复引用和饰品 Trigger 也可能受影响。
- 命中顺序观察提示它可能在首次实际生效时才被消耗，但该模型尚未完全确认。
- 详见：[Mechanics/02-target与群攻重复.md](../../Mechanics/02-target与群攻重复.md)
- 群攻逐目标调用时，`true` 会阻止同名 Effect 在同一技能内反复生效。
- AOE 重复风险不只发生在 `performer_group` 等群体目标。检查重点是各次调用的最终受术者集合是否重叠；只要同一单位在多个调用轮次中再次成为受术者，就可能按 AOE 目标数重复承受 Effect。
- 若 AOE 有 N 个调用目标，而该 Effect 的最终目标为 `performer_group` 等群体，`.apply_once false` 会使整组单位各承受 N 次该 Effect；例如 4 个 AOE 目标会对全队执行 4 次，3 个目标会执行 3 次。
- `.target performer`、重叠群体映射，以及用于修饰同一施术者或同一次技能结果的 `.skill_instant true`，也可能让同一最终单位被每个 AOE 目标重复施加；典型表现是未写 `.apply_once true` 时，技能目标越多，当前技能获得的修正越强。
- 当这种重复会明显叠加，而用户没有明确说明是否应随 AOE 目标数增加时，必须先确认设计要求是整次技能一次还是每个目标一次，不能自行添加或省略 `.apply_once true`。
- 即使是单体技能，同名 Effect 被重复调用时，`true` 也会限制其生效次数；已观察到只生效一个。
- 饰品 Trigger 等非技能来源重复调用同名 Effect 时，也会受到 `apply_once true` 的去重干涉。
- 对 `.on_hit true .on_miss false` 的群攻 Effect，若第一个目标未命中而第二个目标命中，观察上第二个目标仍可触发；这提示计数点可能是首次实际生效，而非首次调用尝试，但该结论尚未完全确认。
- 上述命中/未命中观察不能直接推广到 `.chance` 失败、抗性失败或其他未生效原因。
# 常见错误
- 只把 `apply_once` 理解为群攻专用字段。
- 在单体技能或饰品 Trigger 中重复引用同名 Effect，却忽略 `true` 可能将其去重。
- 把尚未确认的“首次实际生效”模型推广到概率、抗性或所有调用系统。
- 把它当成从多个目标中随机选择一个目标的工具。
- 只在 AOE Effect 指向群体时检查重复，遗漏 `.target performer`、最终目标集合重叠或 `.skill_instant true` 重复修饰同一施术者／同一次技能结果等按目标数叠加的情况。
- 在用户未说明整次技能一次还是每个目标一次时，擅自决定是否写 `.apply_once true`。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:29`
```darkest
effect: .name "kill_self" .target "performer" .chance 100% .kill 1 .on_hit true .on_miss true .apply_once true .queue false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:33`
```darkest
effect: .name "kill_self_queued" .target "performer" .chance 100% .kill 1 .on_hit true .on_miss true .apply_once true .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:387`
```darkest
effect: .name "Shuffle Self" .target "performer" .shuffletarget .chance 100%	.on_hit true .on_miss true .apply_once true .can_apply_on_death true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版实例可确认字段存在及常见写法；重复去重范围与命中顺序属于专项机制结论。
- 未完全确认部分已分别标记，不得作为所有调用系统的确定规则。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
