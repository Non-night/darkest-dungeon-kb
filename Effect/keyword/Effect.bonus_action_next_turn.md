# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.bonus_action_next_turn
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数类型为字符布尔；使用 `true` 或 `false`。
- 与同一逻辑 Effect 的 `.initiative_change` 正整数配合；自身加动已有明确结论。第59条第三台Size-0在spawn中给英雄加动另经当前用户2026-11-03确认：理论上必定连续、实际机制不明、大多数情况可用；不能外推所有跨对象调用或全链安全。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- 参数为 `true` 时，配合 `.initiative_change x`（x 为大于等于 1 的整数）使目标获得一个行动点，且该行动必定紧邻当前行动，不受速度影响。
- 该行为可能等价于临时极大加速、加动后再清除加速，但这只是实现层面的推测。
- 参数为 `false` 时，当前推测等同于省略该字段。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\effects\duelist.effects.darkest:65`
```darkest
effect: .name "Duelist Kill Bonus Action" 	.target "performer" .chance 100% .initiative_change 1 .bonus_action_next_turn true .on_hit true .on_miss false .queue true .requires_kill_target true
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Fire’s Edge Modding Features 无夜译注表。
- 官方 Duelist Effect 注释与实例。
- 知识库编写者提供的本地配置实测补充。
- 当前用户2026-11-03确认第59条Size-0 spawn跨对象加动用途，并限定理论连续、机制不明、多数情况可用；非本轮实机测试。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
