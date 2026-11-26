# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.cure_bleed
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔 `0` 或 `1`；只有 `.cure_bleed 1` 才有效。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.cure_bleed 1`：治愈目标的流血。
- `.cure_bleed 0`：无效。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 只有 `.cure_bleed 1` 有效；单独写 `0` 时无效。
- 第115条原表例外：与 `.cure_disease 1` 同一 Effect 行时，二者无论先后均观察为生效；不推广到 `.cure`、`.cure_burn` 或分行。
- 详见：[Mechanics/19-Effect性质不够确定.md](../../Mechanics/19-Effect性质不够确定.md)
- 单独出现且写为 `0` 时一定无效；不要依赖其与其他 `cure` 字段组合时的未确认边界。
- 治愈流血不判定任何抗性。施术者持有的 `cure_bleed_chance` 与本 Effect 的 `.chance` 直接加算；`amount: 1` 对应 100 个百分点。
- 原表观察：同一 Effect 行内 `.cure_bleed 1` 与 `.cure_disease 1` 同时出现时，无论两者先后，疾病与流血治愈均可生效。这只记录该同行组合；不推广到分行、`.cure`、`.cure_burn` 或其他字段。迂回表第115条P1818–P1819/X2320–X2321，当前用户于2026-11-04确认补入，非本轮游戏实测。
# 常见错误
- 将 `.cure_bleed 0` 当作会治愈流血。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1926`
```darkest
effect: .name "bandage" .target "performer" .item 1 .chance 100% .cure_bleed 1
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 用户补充的 `.cure_*` 参数与单独写假时的生效条件说明。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
