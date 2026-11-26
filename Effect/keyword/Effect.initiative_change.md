# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.initiative_change
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `value`：value为正为获得行动回合，value为负为移除行动回合，出现移除行动回合的次数大于当前次数时，不会出现扣除下一个大回合的行动数，所以不用担心
在不结束回合的技能中，使用此设置项扣除所有行动点，技能会在施放后结束回合，但发动者身上本应在技能施放后减少剩余时间的buff不会减少剩余时间
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 正数增加行动、负数移除行动；未写 `.bonus true` 的加动绝不重排行动序列；写了时重排是机制行为而非风险，单纯扣除行动在initiative层面不引起重排。
- 在反击、spawn等回合外流程中改动行动点须核对具体条件；第59条扣加回合链、bonus_action_next_turn连续行动与Buff/流血/腐蚀/act_out/燃烧边界见机制09。
- 详见：[Mechanics/09-initiative行动点.md](../../Mechanics/09-initiative行动点.md)
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:548`
```darkest
effect: .name test_initiative_add 		.target target .chance 100% .initiative_change 1 .on_hit true .on_miss true .queue true
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\effects\duelist.effects.darkest:65`
```darkest
effect: .name "Duelist Kill Bonus Action" 	.target "performer" .chance 100% .initiative_change 1 .bonus_action_next_turn true .on_hit true .on_miss false .queue true .requires_kill_target true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:549`
```darkest
effect: .name test_initiative_remove 	.target target .chance 100% .initiative_change -1 .on_hit true .on_miss true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
