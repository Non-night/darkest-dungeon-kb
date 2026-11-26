# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

wildfire_apply_adjacent_targets
# 分类
Buff `stat_type`
# 参数类型
固定字符串；配套 `amount` 为数值，`stat_sub_type` 为字符串。
# 参数约束
- 该类型没有副类型；JSON 中字段仍必须存在，并写为空字符串 `""`。
- 可用 rule 分类仍应结合具体 stat_sub_type 和引擎上下文判断。
# 固定值 / 参数候选
- 无固定副类型候选。
# 语义
- 使 Wildfire 向两个相邻目标传播。
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`91`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type wildfire_apply_adjacent_targets` 与 buffs.json 的 `"stat_type":"wildfire_apply_adjacent_targets"` 对应。
# 引擎行为（重要）
- 无该 Buff 时，燃烧持有者死亡触发 Wildfire 时，左侧或右侧相邻目标随机一个获得死亡单位一半的燃烧层数，向下取整。
- 当任一英雄持有该 Buff 时，Wildfire 的传播目标机制改变为向相邻目标传播，现有记录将其描述为两个相邻目标；该 Buff 与燃烧施加者无关。
- 传播层数是否受 `hp_dot_burn_decay_percent` 等燃烧衰减速率 Buff 影响，尚未确认。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"wildfire_apply_adjacent_targets","stat_sub_type":"","amount":0.1}
```
官方实例：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\shared\buffs\runaway.buffs.json:374`

```json
{"stat_type":"wildfire_apply_adjacent_targets","stat_sub_type":"","amount":0}
```
# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
