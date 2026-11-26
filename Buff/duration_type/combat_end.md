# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

combat_end
# 分类
Buff `duration_type`
# 参数类型
固定字符串
# 参数约束
- 这是 12 个已知合法 `duration_type` 之一；不要使用合法表以外的值，非法值的引擎结果当前未确认。
- 与数值字段 `duration` 配合。
# 语义
- 每场战斗结束时，持续时间减 1。
# 作用范围
- 可写在 Buff 定义的 `duration_type` 中；Effect 使用对应字段 `.buff_duration_type`。
- Effect 引用 Buff 时，Effect 的 `.duration` / `.buff_duration_type` 会覆盖 Buff 定义中的对应字段。
# 引擎行为（重要）
- 正常扣减事件：每场战斗结束时，持续时间减 1。
- 持续时间为 2 时，表示从施加所在战斗起持续两场战斗：本场结束减至 1，下一场结束减至 0 后消失。
- 持续类型只规定正常扣减事件；`remove_if_not_active`、`remove_on_battle_complete` 和 Buff 源的自动清除仍可能使 Buff 提前消失。
# 常见错误
- 把 `round` 当成整轮；`round` 是正常个人回合结束，`after_round` 才是战斗整轮结束。
- 只依据 `duration` 与 `duration_type` 推算真实存续时间，忽略 Buff 自身移除参数和 Buff 源。
# 来源与可信度
- 主术语表 `Buff Durations`。 原表简述：每场战斗结束。
- 逐类型触发时机、覆盖规则与清除边界按已整理的社区测试结论记录。
- 详见：[Mechanics/17-Buff持续时间类型与实际清除.md](../../Mechanics/17-Buff持续时间类型与实际清除.md)
