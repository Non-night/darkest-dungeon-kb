# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.gain_trinket
# 分类
扩展/专项字段
# 参数类型
单个字符串（ID；可按原版实例加引号或不加引号）
# 参数约束
- 参数为单个字符串，引用饰品 ID。
- 同一逻辑 Effect 的 `.target` 必须为 `this_trinket`。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- 在战斗结束时获得指定饰品。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:125`
```darkest
effect: .name "On Combat End Gain a Pile of Ash"  .target "this_trinket" .curio_result_type "positive" .chance 100% .gain_trinket "pile_of_ash" .on_hit true .on_miss true .queue true .is_trigger_effect true
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Fire’s Edge Modding Features 无夜译注表。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
