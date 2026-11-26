# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

crit_received_chance
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
- 调整 Buff 持有者成为攻击目标时受到暴击的概率（百分比）。
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`45`。
- `amount` 正值：减益；负值：增益；零值：增益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type crit_received_chance` 与 buffs.json 的 `"stat_type":"crit_received_chance"` 对应。
# 引擎行为（重要）
- 目标的 `crit_received_chance` 会加入攻击者针对该目标的最终暴击率计算；正值提高被暴击概率，负值降低被暴击概率。
- 攻击者自身暴击率修正、目标所受暴击率修正及其他相关项采用加算；所有修正汇总后，实际生效概率才截断在 0% 至 100%。
- 中间合计值允许超出上下限并保留抵消意义。例如合计暴击率先达到 110%，再受到 -10% 修正，最终为 100%，不是先把 110% 截断为 100% 再降到 90%。
- 反击是特殊的攻击技能，暴击与伤害等常规战斗数值沿用攻击技能结算，因此 `crit_received_chance` 同样参与反击的暴击判定。反击是否触发普通攻击类饰品 Trigger 或具有普通技能 AWR 层，必须按各机制的特殊规则另行判断。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"crit_received_chance","stat_sub_type":"","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
