# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.guaranteed_town_event
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
- 参数为 `true` 时，将一个随机城镇事件加入队列。
- 参数为 `false` 时，不启用上述入队效果。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 随机城镇事件入队的基本说明来自 Fire’s Edge 表格；任务内调用边界尚未完全确认。
- 详见：[Mechanics/19-Effect性质不够确定.md](../../Mechanics/19-Effect性质不够确定.md)
- 当前资料尚未确认它在任务中的全部调用边界；不要据字段名扩展出指定事件 ID 或必定立即发生等语义。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\effects\rd.effects.darkest:6`
```darkest
effect: .name "On Quest Complete Guaranteed Town Event"  .target "performer" .curio_result_type "positive" .chance 100% .guaranteed_town_event true .on_hit true .on_miss true .queue true
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Fire’s Edge Modding Features 无夜译注表；原表对任务内行为保留疑问。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
