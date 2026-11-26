# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.can_apply_on_corpse
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数类型为字符布尔；官方 DLC 存在 `true` 写法。
- 一般尸体目标的完整语义仍未由英文原表或专项测试全部确认。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- 一般尸体目标的完整行为仍未知。
- 当前用户2026-10-01确认：所有 Effect 若要作用于死而不僵目标，均须与 `.can_apply_on_death true` 同时显式写 `.can_apply_on_corpse true`；少写任一字段都不能通过该目标门。若有 `.swap_source_and_target true`，检查交换后施术者（即 `.target` 映射单位）是否死而不僵。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 当前用户2026-10-01确认：所有Effect的死亡门均看 `.target` 映射出的最终检查单位；没有同时显式写 `.can_apply_on_death true .can_apply_on_corpse true` 时，死而不僵目标不生效。若 `.swap_source_and_target true`，实际检查的是交换后施术者，即原 `.target` 单位。两个true显式写出后所有Effect均可生效；狗贼二段式二号机召唤需保留该门。一般尸体语义仍未全确认。
- 详见：[Mechanics/19-Effect性质不够确定.md](../../Mechanics/19-Effect性质不够确定.md)
- 英文原表未收录该字段；官方实例只能证明字段存在，不能单独证明其全部目标判定边界。
- 当前用户2026-10-01提供通用 Effect 黑盒结论；狗贼二段式二号机召唤是依赖死亡门的专门例外，两个字段必须均省略或均false。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:124`
```darkest
effect: .name "On attack hit Burn"  .target "target" .curio_result_type "positive" .chance 100% .dotBurn 3 .dot_irresistible true .on_hit true .on_miss false .queue true .is_trigger_effect true .can_apply_on_death true .can_apply_on_corpse true
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:123`
```darkest
effect: .name "On attack hit Burn 2"  .target "target" .curio_result_type "positive" .chance 100% .dotBurn 2 .dot_irresistible true .on_hit true .on_miss false .queue true .is_trigger_effect true .can_apply_on_death true .can_apply_on_corpse true
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 无夜译注补充：英文原表无此字段。
- 官方 Runaway Effect 的 `.can_apply_on_corpse true` 实例。
- 当前用户2026-09-30提供死而不僵目标的召唤/set双字段专项测试。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
