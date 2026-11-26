# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.clear_rank_target
# 分类
扩展/专项字段
# 参数类型
单个站位表达式（由站位数字组成，可带前缀；本字段支持范围见词条）
# 参数约束
- 参数为一个站位表达式；常规单位最多有一号位至四号位，站位以数字表示。例如 `1` 表示一号位，`12` 表示由一号位和二号位组成的站位范围，`1234` 可表示一至四号位。
- 通用站位表达式可见 `~12`、`?12`、`@12` 等形式，但不同字段支持的前缀并不完全相同。
- 当前资料记载 `.clear_rank_target` 接受 `@` 与 `~`，不接受 `?`。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.clear_rank_target <ranks>`：为怪物侧 AI 的 `rank_target` 特殊机制提供站位参数。
# 作用范围
- 本字段属于怪物侧 `rank_target` 特殊机制，不能仅按普通技能目标表达式推断完整行为。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 参数是站位表达式；`12`、`@12` 在 info 技能中表示可选范围而不是 AOE，但该语义是否完整适用于本字段尚未确认。
- 当前资料记载本字段接受 `@` 与 `~`，不接受 `?`。
- 详见：[Mechanics/20-站位参数表达式.md](../../Mechanics/20-站位参数表达式.md)
- 在 `*.info.darkest` 的技能定义中，`12` 表示一号位或二号位构成的可选范围，`1234` 同理表示一至四号位构成的可选范围；`@12` 表示友方一号位或二号位构成的可选范围。它们本身都不是 AOE。
- `~12` 表示同时选择一号位和二号位；`?12` 表示从一号位和二号位中随机选择一个。
- 当前尚不确定 `12` 与 `@12` 在 `.clear_rank_target` 中是否完全沿用 `*.info.darkest` 的非 AOE、可选范围语义。
# 常见错误
- 看到 `12` 或 `@12` 就直接把它解释为同时作用于一、二号位。
- 未区分字段上下文，直接把 `*.info.darkest` 的技能站位语义完整套用到 `.clear_rank_target`。
- 在 `.clear_rank_target` 中使用当前资料记载为不接受的 `?` 前缀。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2083`
```darkest
effect: .name "Clear Enemy Rank Target" .target "performer" .chance 100% .clear_rank_target 1234 .on_hit true .on_miss true
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:98`
```darkest
effect: .name "RW Backdraft Cure Burn" .target "target_enemy_rank" .clear_rank_target 1 .chance 100% .cure_burn 1 .on_hit true .on_miss true .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2085`
```darkest
effect: .name "Clear Target Enemy Rank Target" .target "target" .chance 100% .clear_rank_target 1234 .on_hit true .on_miss true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 Effect：`DarkestDungeon\effects\base.effects.darkest:2083-2085`。
- 站位表达式及 `.clear_rank_target` 的上下文边界来自用户补充说明与现有社区术语表。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
