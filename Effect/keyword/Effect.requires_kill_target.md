# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.requires_kill_target
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
- 参数为 `true` 时启用击杀目标条件；参数为 `false` 时不启用该条件。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 普通尸体不计入击杀目标；大型尸体及特殊 corpse 类型目标尚未确认。
- 详见：[Mechanics/19-Effect性质不够确定.md](../../Mechanics/19-Effect性质不够确定.md)
- 当前用户于2026-10-08确认：在英雄攻击技能中，只要该 Effect 发生前技能目标已经死亡，该 Effect 就会生效；目标因普通直伤或真伤死亡均可。
- 当前用户另行确认：因真伤死亡的怪物不会触发英雄击杀 Trigger，也不参与流血/腐蚀 DOT 的最后成功施加者击杀 Trigger 归属；燃烧致死同样不会触发击杀 Trigger。
- 该结论只覆盖英雄攻击技能引用场景；怪物使用、友方技能使用和非技能位置调用尚未测试。
- 击杀普通尸体不满足该条件；大型尸体及特殊 corpse 类型目标是否满足条件尚未确认。
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
- 当前用户2026-10-08补充的英雄攻击技能实测边界。
- 用户补充的尸体边界结论。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
