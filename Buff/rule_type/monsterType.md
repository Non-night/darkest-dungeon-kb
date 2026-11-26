# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

monsterType
# 分类
进攻型（施术）
# 参数类型
`rule_type` 固定字符串；配套 `rule_data.float` 为数值，`rule_data.string` 为字符串。
# 参数约束
- 该值已收录为 rule_type；float/string 的实际含义仍应按原版案例与社区说明填写。
- `is_false_rule: true` 只在有效判定范围内翻转普通 `true`／`false`；范围外的 `null` 不会被翻转为 `true`。
# 固定值 / 参数候选
- float 示例：`0`
- string 示例：`自己定义的monster type`、`unholy`、`man`、`beast`、`eldritch`、`vampire`、`corpse（尸骸）`、`husk（农场瘪壳怪）`
# 语义
- 技能或effect的作用目标具有特定的monster type时激活此rule修饰的buff
  此种buff在effect指向多个目标时，会根据每个目标单独判定
  因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
- 迂回表第62条 P1204/X1411、当前用户2026-11-03确认：这四种目标型进攻 Rule 不必依附技能，可在非技能调用的 Effect 中修饰适配的进攻向属性，按实际调用及最终目标判定；不适用于防御向 Buff。技能层与 Effect 层目标须分别核对，且不保证任意 stat_type 或具体非技能配置均生效、无干扰；非本轮新增实机测试。
# 作用范围
- `进攻型（施术）` rule；分类决定它在施术、受术或通用条件上下文中的可用性。
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
{"rule_type":"monsterType","is_false_rule":false,"rule_data":{"float":0.0,"string":""}}
```

# 来源与可信度
- 当前知识库的结构化规则表：rule_type、分类和专项值域。
- 主术语表 `Buff Rules`：社区语义、案例与实测备注。
