# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

has_buff
# 分类
通用型（条件型）
# 参数类型
`rule_type` 固定字符串；配套 `rule_data.float` 为数值，`rule_data.string` 为字符串。
# 参数约束
- rule_data.string 填写 Buff 的 stat_type，而不是 buff 源类型；目前已知主要用于 Duelist 的反击条件，其他状态或 buff 源的兼容性未确认。其有效/失效转换检测有已知延迟，具体时点尚未确认。
- `is_false_rule: true` 只在有效判定范围内翻转普通 `true`／`false`；范围外的 `null` 不会被翻转为 `true`。
# 固定值 / 参数候选
- float 示例：术语表未指定
- string 示例：通常为空字符串或按规则填写 ID
# 语义
- 施术者具有指定 Buff 主类型且该 Buff 的 amount 大于 0 时有效。
- `rule_data.string` 应填写 Buff 的 `stat_type`，不是 buff 源类型；书写形式对应 `.buff_type` 的主类型。
- 目前已知的主要用法是 Duelist 的“反击生效时”条件；对其他状态或 buff 源是否普遍有效，译注资料明确记为未确认。
- 若指定的 Buff 主类型还需要 `stat_sub_type`，`has_buff` 不能指定副类型，因此通常无法检测该类具体 Buff；以 `combat_stat_add`、`hp_heal_amount` 为例。
- 该 Rule 从有效变无效、或从无效变有效的转换检测存在已知延迟；具体检查时点尚未确认，不能依赖本技能内刚施加或清除 Buff 后立刻反转。
- has_buff 不是精确的 Buff 身份检测：它具有非指向性，指定同类中任意 amount 大于 0 且当前生效的 Buff 都可能使其成立，而不是只检查某个具体 Buff ID。其刷新/生效状态更新频率也偏低，通常不能用于同一技能流程中的即时检测。
- 如果需要用 Buff 作为标志物或条件门，应优先使用极大概率数值配合 Rule 构建概率门，并核对 +1000%/-1000% 的抗干扰幅度要求；has_buff 只能作为最低优先级的备选方案，除非已针对具体调用时机和目标完成实测。
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
{"rule_type":"has_buff","is_false_rule":false,"rule_data":{"float":0.0,"string":""}}
```

# 来源与可信度
- 当前知识库的结构化规则表：rule_type、分类和专项值域。
- 主术语表 `Buff Rules`：社区语义、案例与实测备注。
- Fire’s Edge Modding Features翻译（无夜译注）.xlsx：Buffs 工作表第 22 行；英文原表仅写 bsrc_riposte，译注补充了实际 string 含义与限制。
