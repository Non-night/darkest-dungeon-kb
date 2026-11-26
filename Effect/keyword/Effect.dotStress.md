# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.dotStress
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `value`：持续压力，俗称恐惧（可以挂给怪物，但没有实际效果）
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 写有有效 DOT 的 Effect 通常同时写 `.can_apply_on_death true`；漏写会产生红字报错。
- 迂回表第113条P1745、P1754–P1755、P1764–P1765、P1770、P1783–P1792、P1794–P1798/X2211–X2291记录：同一逻辑Effect定义行同时声明 `.dotPoison`、`.dotBleed`、`.dotStress`、`.dotShuffle`、`.dotHpHeal` 中多个字段时，仅优先级最高的一种Effect型DOT生效，书写顺序不改变结果；优先级为腐蚀 > 流血 > 恐惧 > 延迟扰乱 > 愈合。Buff型DOT仍按其Buff定义处理；通过 `.buff_ids` 引用多个Buff时，可按既有多参数分行规则拆分。标记与潜行不受此限制；`.dotBurn` 等未列字段不推断。当前用户于2026-11-04确认按此边界补入；本轮未新增游戏测试。详见 Mechanics/66-负数DOT与不可治愈边界.md。
- 详见：[Mechanics/40-Effect防红字配套字段.md](../../Mechanics/40-Effect防红字配套字段.md)
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1772`
```darkest
effect: .name "Drum Stress DoT" .target "target" .curio_result_type "negative" .chance 70%  .dotStress 3 .duration 3	.on_hit true .on_miss false
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:306`
```darkest
effect: .name "galaxy horror" .target "target" .chance 100%  .dotStress 3 .duration 5	.on_hit true .on_miss false
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:376`
```darkest
effect: .name "Countess Terror" .target "target" .chance 100%  .dotStress 5 .duration 3	.on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
