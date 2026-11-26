# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

round
# 分类
Buff `duration_type`
# 参数类型
固定字符串
# 参数约束
- 这是 12 个已知合法 `duration_type` 之一；不要使用合法表以外的值，非法值的引擎结果当前未确认。
- 与数值字段 `duration` 配合。
# 语义
- 小回合；每次正常个人回合结束后，持续时间减 1。
# 作用范围
- 可写在 Buff 定义的 `duration_type` 中；Effect 使用对应字段 `.buff_duration_type`。
- Effect 引用 Buff 时，Effect 的 `.duration` / `.buff_duration_type` 会覆盖 Buff 定义中的对应字段。
# 引擎行为（重要）
- 正常扣减事件：小回合；每次正常个人回合结束后，持续时间减 1。
- 若 Buff 在当前行动者的技能期间施加给其自身，当前个人回合尚未结束；`duration 1` 会在该技能结束后的本次个人回合结束时减至 0。`after_turn 1` 具有相同表现。
- 若正常回合结束流程被跳过，持续时间可能不会减少。
- 知识库编写者2026-11-08实测确认：回合结束附魔turn_end_additional_effect_ids先触发，再进行round/after_turn持续时间扣减；1回合附魔Buff及1回合抑制Buff在该次触发时仍有效。同一时序严格顺序与类型组合已测，时序分离未测。来源：Sources/turn_end_additional_before_duration_20261108.json。
- 所受增减益时间修正可能改变实际持续时间；常规设计无需为这种极端组合增加复杂兜底，只有明确使用相关机制时再检查。
- 持续类型只规定正常扣减事件；`remove_if_not_active`、`remove_on_battle_complete` 和 Buff 源的自动清除仍可能使 Buff 提前消失。
# 常见错误
- 把 `round` 当成整轮；`round` 是正常个人回合结束，`after_round` 才是战斗整轮结束。
- 只依据 `duration` 与 `duration_type` 推算真实存续时间，忽略 Buff 自身移除参数和 Buff 源。
# 来源与可信度
- 主术语表 `Buff Durations`。 原表简述：小回合，每次行动后扣除1。
- 逐类型触发时机、覆盖规则与清除边界按已整理的社区测试结论记录。 原表备注：如果不结束回合的技能中使用“.initiative_change 负数”扣除所有行动点，会导致技能结束时行动权转交其它单位，但由于回合结束过程被扣除行动代码所跳过，而导致基于回合结束才减少的剩余时间在此时不减少
- 详见：[Mechanics/17-Buff持续时间类型与实际清除.md](../../Mechanics/17-Buff持续时间类型与实际清除.md)
