# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

attacking_monster_type
# 分类
防御型（受术）
# 参数类型
`rule_type` 固定字符串；配套 `rule_data.float` 为数值，`rule_data.string` 为字符串。
# 参数约束
- 该值已收录为 rule_type；float/string 的实际含义仍应按原版案例与社区说明填写。
- `is_false_rule: true` 只在有效判定范围内翻转普通 `true`／`false`；范围外的 `null` 不会被翻转为 `true`。
# 固定值 / 参数候选
- float 示例：`0`
- string 示例：`monster type`
# 语义
- 【被】某类怪物攻击时
- 注意一点：
  
  1.attacking_monster_type为被某类怪物攻击时触发，属于防御型条件，
  配合防御是参与计算的buff（抗性、闪避、防御、伤害减免等）才有意义。
  
  2.monster_type_count_min为场上有某类怪时触发，属于条件向buff，
  其他buff都能使用该条件，但速度buff尤其适合使用该条件。
  
  3.monster_type_count_min在怪物侧不适用（详见本表标题）
  
  4.monster_type_count_min不会计算size为0的单位
  4.monster_type_count_min【会】计算size为0的单位
  
  因速度判定是每个大回合（火把里的数字）开始，而不是挨打或者进攻，哪怕速度真的配其他两个有效，你也只有攻击和挨打瞬间提速，无法影响大回合开始，导致提速等于没提。
# 作用范围
- `防御型（受术）` rule；分类决定它在施术、受术或通用条件上下文中的可用性。
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
{"rule_type":"attacking_monster_type","is_false_rule":false,"rule_data":{"float":0.0,"string":""}}
```

# 来源与可信度
- 当前知识库的结构化规则表：rule_type、分类和专项值域。
- 主术语表 `Buff Rules`：社区语义、案例与实测备注。
