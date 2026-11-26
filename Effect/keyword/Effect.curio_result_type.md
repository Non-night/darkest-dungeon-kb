# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.curio_result_type
# 分类
扩展/专项字段
# 参数类型
枚举/固定候选值
# 参数约束
- 参数为单个字符串；使用已收录的四个候选值：`positive`、`negative`、`neutral`、`none`。
- 只有当该 Effect 被奇物互动流程引用时才填写；非奇物调用不需要添加该字段。
# 固定值 / 参数候选
- `positive`
- `negative`
- `neutral`
- `none`
# 语义
- `.curio_result_type <type>`：指定奇物互动结果播放的动画类型。
- `positive`、`negative`、`neutral`、`none` 分别表示正面、负面、中性和不显示互动动画。
# 作用范围
- 仅影响奇物互动结果的表现层动画，不改变 Effect 本身的目标、概率、伤害、治疗或 Buff 逻辑。
- 原版及早期 Mod 中有些非奇物 Effect 也填写了该字段；在这些调用场合该字段没有实际意义，不应据此推断为必填项。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 该字段只有在 Effect 被奇物互动流程引用时才产生实际意义。
- 非奇物调用中的 `.curio_result_type` 可视为无意义的冗余字段；无需为了模仿原版或早期 Mod 而添加。
- 原版和早期 Mod 在非奇物 Effect 中保留该字段的具体原因尚不明确，不将其解释为引擎要求或注释语法。
# 常见错误
- 在非奇物 Effect 中添加该字段，并误认为它会改变 Effect 的实际效果。
- 将该字段当作所有 Effect 都必须填写的通用字段。
- 把 `positive`、`negative` 等参数当成 Effect 生效结果或 Buff 类型，而不是奇物互动动画类型。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:87`
```darkest
effect: .name "Stress 1" .target "target" .curio_result_type "negative" .chance 100% .stress 10		.on_hit true .on_miss false	.queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:88`
```darkest
effect: .name "Stress 2" .target "target" .curio_result_type "negative" .chance 100% .stress 15		.on_hit true .on_miss false	.queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:89`
```darkest
effect: .name "Stress 3" .target "target" .curio_result_type "negative" .chance 100% .stress 25		.on_hit true .on_miss false	.queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 用户补充：`.curio_result_type` 仅用于奇物互动效果的互动动画；原版和早期 Mod 的非奇物用法没有实际意义。
- 原版实例：`DarkestDungeon\effects\base.effects.darkest:87-89`。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
