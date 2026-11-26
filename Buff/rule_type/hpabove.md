# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

hpabove
# 分类
通用型（条件型）
# 参数类型
`rule_type` 固定字符串；配套 `rule_data.float` 为数值，`rule_data.string` 为字符串。
# 参数约束
- 未取反时 float <= 1；取反时 float > 0。
- `is_false_rule: true` 只在有效判定范围内翻转普通 `true`／`false`；范围外的 `null` 不会被翻转为 `true`。
# 固定值 / 参数候选
- float 示例：`value`
- string 示例：通常为空字符串或按规则填写 ID
# 语义
- 未取反时，Buff 持有者当前生命比例大于等于 `rule_data.float` 时有效；阈值为闭区间。
- 取反时，持有者当前生命比例严格小于 `rule_data.float` 时有效；取反结果为开区间。
# 作用范围
- `通用型（条件型）` rule；分类决定它在施术、受术或通用条件上下文中的可用性。
- 当前用户于2026-11-03补充的理论模型：所有 Rule 都有各自的有效判定范围；范围外返回 `null`，无论是否取反均表现为不生效；范围内返回普通 `true` 或 `false`，二者可由 `is_false_rule` 相互翻转。这里的范围是对象、调用方、目标、时序及必要状态所组成的有效判定上下文，不是 `rule_data.float` 的数值阈值。具体范围须逐 Rule、逐调用上下文查证；不能把缺失上下文当作普通 `false`，也不能从本模型补造某条 Rule 的具体范围或声称55条均已逐项实测。
- 本词条中阈值、ID 或状态的取反关系，均以处于有效判定范围内为前提；分类和参数合法性不能代替具体上下文边界。
# 引擎行为（重要）
- 每一种 Rule 的一次判定都可能返回 `true`、`false` 或 `null`。`null` 表现为不激活；`is_false_rule` 只能翻转普通 `false`，不能把 `null` 翻转为 `true`。具体何时返回 `null` 仍须按该 Rule 的判定目标和调用上下文确认。
- 语法合法、规则求真、stat_type 能否在该时机生效是三个不同问题。
# 常见错误
- 忘记同时提供 `rule_data.float` 与 `rule_data.string`。
- 把 `is_false_rule` 取反当成能修复所有 null 上下文。
- 对只能使用通用型 rule 的 stat_type 配置进攻型/防御型 rule。
# 代码案例
```json
{"rule_type":"hpabove","is_false_rule":false,"rule_data":{"float":0.0,"string":""}}
```

# 来源与可信度
- 当前知识库的结构化规则表：rule_type、分类和专项值域。
- 主术语表 `Buff Rules`：社区语义、案例与实测备注。
- 用户对生命比例 Rule 阈值边界的补充说明。
