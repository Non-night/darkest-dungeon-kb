# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

actorStatus
# 分类
进攻型（施术）
# 参数类型
`rule_type` 固定字符串；配套 `rule_data.float` 为数值，`rule_data.string` 为字符串。
# 参数约束
- 未取反时 rule_data.string 仅允许 tagged、poisoned、bleeding、stunned、virtued、afflicted、burning。
- `is_false_rule: true` 只在有效判定范围内翻转普通 `true`／`false`；范围外的 `null` 不会被翻转为 `true`。
# 固定值 / 参数候选
- float 示例：`0`
- string 示例：`tagged`、`poisoned`、`bleeding`、`stunned`、`virtued`、`afflicted`、`burning`
# 语义
- 技能或effect的作用目标具有特定的状态时激活此rule修饰的buff
  此种buff在effect指向多个目标时，会根据每个目标单独判定
  因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
  经测试，dazed不可用
- 该进攻型 Rule 的 Buff 位于施术者身上；Rule 判定时检查被修饰操作的受术者状态，而不是检查 Buff 持有者自己的状态。群体目标会按每个最终目标分别判断。
- `actorStatus` 的 `rule_data.string` 是要在目标身上查找的状态。若 Buff 修饰技能层百分比加伤、穿甲等技能属性，读取当前技能目标；若 Buff 修饰腐蚀概率等由具体 Effect 结算的属性，读取该 Effect 的最终目标。不能把两种目标上下文混为一谈。
- 已明确验证：战斗中玩家鼠标碰到任一怪物的碰撞箱时，`actorStatus` 会进行一次生效性判定。该判定可能用于更新英雄攻击技能面板，但这一目的只是推测。
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
{"rule_type":"actorStatus","is_false_rule":false,"rule_data":{"float":0.0,"string":""}}
```
### 技能层属性：穿甲 Buff 在施术者身上，检查技能目标是否眩晕
```text
{
  "id": "KB_actorStatus_stunned_skill_pen",
  "stat_type": "ignore_protection",
  "stat_sub_type": "",
  "amount": 0.5,
  "remove_if_not_active": false,
  "rule_type": "actorStatus",
  "is_false_rule": false,
  "rule_data": {"float": 0.0, "string": "stunned"},
  "is_clear_debuff_valid": false,
  "has_description": true
}
// 该 Buff 已存在于施术者后，技能目标仍由技能本身提供。
combat_skill: .id "KB_attack" .level 0 .type "melee" .atk 100% .dmg 3 5 .crit 5% .launch 4321 .target 1234

```
### Effect 层属性：腐蚀概率 Buff 在施术者身上，检查腐蚀 Effect 的最终目标是否眩晕
```text
{
  "id": "KB_actorStatus_stunned_poison_chance",
  "stat_type": "poison_chance",
  "stat_sub_type": "",
  "amount": 0.5,
  "remove_if_not_active": false,
  "rule_type": "actorStatus",
  "is_false_rule": false,
  "rule_data": {"float": 0.0, "string": "stunned"},
  "is_clear_debuff_valid": false,
  "has_description": true
}
// 该 Buff 已存在于施术者后，actorStatus 检查下面这个 Effect 的 target。
effect: .name "KB_poison" .target "target" .chance 100% .poison 3 .duration 3 .on_hit true .on_miss false

```
# 来源与可信度
- 当前知识库的结构化规则表：rule_type、分类和专项值域。
- 主术语表 `Buff Rules`：社区语义、案例与实测备注。
- 用户对目标类 Rule 悬停判定的实测与推测说明。
