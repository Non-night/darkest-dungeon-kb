# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.dot_irresistible
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数类型为字符布尔；使用 `true` 或 `false`。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- 参数为 `true` 时，使同一逻辑 Effect 施加的 DOT 无法被抵抗。
- 参数为 `false` 时，不启用上述无视抵抗效果。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 对燃烧，知识库编写者确认不存在对应的目标燃烧抗性；当基础 `.chance` 为 100% 或更高时，写 `true` 通常用于不显示自动描述中的“100%基础概率”，而不是为了对抗燃烧抗性。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:368`
```darkest
effect: .name "RW Sunstone Searing Self Burn" .target "performer" .chance 100% .dotBurn 2 .dot_irresistible true .on_hit true .on_miss true .queue true .apply_once true
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:5`
```darkest
effect: .name "RW Burn 2" .target "target" .curio_result_type "negative" .chance 100% .dotBurn 2 .dot_irresistible true .on_hit true .on_miss false .can_apply_on_death true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:566`
```darkest
effect: .name "When hit Self Burn"  .target "performer" .curio_result_type "negative" .chance 100% .dotBurn 1 .dot_irresistible true .on_hit true .on_miss false .apply_once true
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Fire’s Edge Modding Features 无夜译注表。
- 知识库编写者补充（2026-09-20）。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
