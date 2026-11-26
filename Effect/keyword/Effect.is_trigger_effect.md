# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.is_trigger_effect
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数类型为字符布尔；使用 `true` 或 `false`。
- 只在需要消耗饰品 Trigger 可用次数的触发 Effect 中启用。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- 参数为 `true` 时，该 Effect 每次被触发都会使发起饰品的触发次数上限减少 `1`。
- 参数为 `false` 时，不启用上述触发次数消耗。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 该字段操作的是饰品 Trigger 次数限制，不是技能使用次数或 Buff 持续时间。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:113`
```darkest
effect: .name "On dodge attacker shuffle single trigger effect"  .target "target" .shuffletarget .chance 100% .on_hit false .on_miss true .apply_once true .can_apply_on_death true .is_trigger_effect true
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\effects\rd.effects.darkest:1`
```darkest
effect: .name "On turn end self heal trigger effect"  .target "performer" .curio_result_type "positive" .chance 100% .heal 6 .on_hit true .on_miss true .queue true .is_trigger_effect true .source_heal_type hero_skill .buff_duration_type combat_end
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:125`
```darkest
effect: .name "On Combat End Gain a Pile of Ash"  .target "this_trinket" .curio_result_type "positive" .chance 100% .gain_trinket "pile_of_ash" .on_hit true .on_miss true .queue true .is_trigger_effect true
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Fire’s Edge Modding Features 无夜译注表。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
