# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.dotPoison
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `value`：腐蚀伤害
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 写有有效 DOT 的 Effect 通常同时写 `.can_apply_on_death true`；漏写会产生红字报错。
- 迂回表第113条P1745、P1754–P1755、P1764–P1765、P1770、P1783–P1792、P1794–P1798/X2211–X2291记录：同一逻辑Effect定义行同时声明 `.dotPoison`、`.dotBleed`、`.dotStress`、`.dotShuffle`、`.dotHpHeal` 中多个字段时，仅优先级最高的一种Effect型DOT生效，书写顺序不改变结果；优先级为腐蚀 > 流血 > 恐惧 > 延迟扰乱 > 愈合。Buff型DOT仍按其Buff定义处理；通过 `.buff_ids` 引用多个Buff时，可按既有多参数分行规则拆分。标记与潜行不受此限制；`.dotBurn` 等未列字段不推断。当前用户于2026-11-04确认按此边界补入；本轮未新增游戏测试。详见 Mechanics/66-负数DOT与不可治愈边界.md。
- 详见：[Mechanics/40-Effect防红字配套字段.md](../../Mechanics/40-Effect防红字配套字段.md)
- 知识库编写者提供无夜2026-11-05 15:06–15:28聊天及范围澄清：Effect型与Buff型DOT的量为正或负均可存在；最终持续时间为负则不可存在。合法性看修正后的最终量与最终持续时间，不看初始值；修正Buff的影响范围保持已有规则不变。Effect型DOT另有描述观察：初始负量可存在，但施加该DOT的Effect不显示该DOT描述；初始负持续时间不可存在，但施加该DOT的Effect仍显示该DOT描述；这两条描述观察按聊天原述保留，不将“初始”改写为描述生成也必看最终值。任何类型的Buff型DOT均不由施加它的Effect生成该DOT的自动描述，因此无法以此出现在技能自动描述中。这里的“描述”明确指施加该DOT的Effect是否显示描述，不指持有者身上的状态说明或图标，也不限制手动自定义文本。 负量DOT可存在不等于已验证所有历史抵消、元素护盾、魔免方案；这些方案的合并、结算、转移和清理行为仍须分别核对。本轮没有Agent新增游戏实测。 来源：Sources/dot_legality_description_20261105.json。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:108`
```darkest
effect: .name "Blight 1" .target "target" .curio_result_type "negative" .chance 100%  .dotPoison 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:109`
```darkest
effect: .name "Blight 2" .target "target" .curio_result_type "negative" .chance 110%  .dotPoison 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:110`
```darkest
effect: .name "Blight 3" .target "target" .curio_result_type "negative" .chance 120%  .dotPoison 3 .duration 3	.on_hit true .on_miss false .can_apply_on_death true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
