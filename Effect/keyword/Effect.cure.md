# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.cure
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔 `0` 或 `1`；只有 `.cure 1` 才产生治愈效果。
- `.cure 1` 在一定意义上可视为同时处理流血与腐蚀，但不应据此忽略 `.cure_disease` 的特殊顺序规则。
- 当同一逻辑 Effect 中同时出现 `.cure_disease 1` 与 `.cure 1` 时，先写 `.cure_disease 1`，再写 `.cure 1`。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.cure 1`：治愈目标的流血与腐蚀。
- `.cure 0`：不产生已确认的治愈效果。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.cure 1` 可处理流血与腐蚀；与 `.cure_disease 1` 同一逻辑 Effect 时必须先写疾病治愈，再写 `.cure`。
- VS 插件诊断还确认同一行 `.cure` 与 `.cure_burn` 同时出现时后写者生效；该结论只覆盖泛用 `.cure`，不推广到 `.cure_bleed`、`.cure_poison`。
- 详见：[Mechanics/19-Effect性质不够确定.md](../../Mechanics/19-Effect性质不够确定.md)
- 只有参数为 `1` 时有效；单独出现并写为 `0` 时无效。
- `.cure` 与 `.cure_disease` 的组合顺序存在特殊性，详见不确定性备忘录。
- VS 插件的 Effect 诊断确认：同一行同时写 `.cure` 与 `.cure_burn` 时，后写关键字生效；该诊断不覆盖 `.cure_bleed`、`.cure_poison` 与 `.cure_burn` 的组合。来源：`For_the_Darkest_Dungeon/Error/EffectErrorTagger.cs`，2026-11-04核对。
# 常见错误
- 在 `.cure_disease 1` 之前写 `.cure 1`。
- 将 `.cure 0` 当作会治愈流血或腐蚀。
- 将 `.cure 1` 无条件当作可以替代 `.cure_disease 1`。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:358`
```darkest
effect: .name "Cure" .target "target" .curio_result_type "positive" .chance 100% .cure 1	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:359`
```darkest
effect: .name "Cureself" .target "performer" .curio_result_type "positive" .chance 100% .cure 1	.on_hit true .on_miss false .queue true .apply_once true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:360`
```darkest
effect: .name "Cure Self" .target "performer" .curio_result_type "positive" .chance 100% .cure 1 .apply_once true  .on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 用户补充的 `.cure` 参数、生效条件及与 `.cure_disease` 的顺序说明。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
