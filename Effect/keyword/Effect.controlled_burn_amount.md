# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.controlled_burn_amount
# 分类
扩展/专项字段
# 参数类型
单个整数
# 参数约束
- 参数为单个整数，表示烈焰缠绕每次触发施加的燃烧数量。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- 启用烈焰缠绕，并规定其每次触发施加多少燃烧。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:85`
```darkest
effect: .name "RW CB Rank Effect 1" .target "target" .chance 100% .on_hit true .on_miss true .controlled_burn_amount 2 .controlled_burn_duration 3
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:86`
```darkest
effect: .name "RW CB Rank Effect 2" .target "target" .chance 100% .on_hit true .on_miss true .controlled_burn_amount 2 .controlled_burn_duration 3
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:87`
```darkest
effect: .name "RW CB Rank Effect 3" .target "target" .chance 100% .on_hit true .on_miss true .controlled_burn_amount 3 .controlled_burn_duration 3
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Fire’s Edge Modding Features 无夜译注表。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
