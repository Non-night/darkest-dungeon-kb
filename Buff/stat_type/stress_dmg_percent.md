# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

stress_dmg_percent
# 分类
Buff `stat_type`
# 参数类型
固定字符串；配套 `amount` 为数值，`stat_sub_type` 为字符串。
# 参数约束
- `stat_sub_type` 可为空；非空时必须来自固定候选表。
- 可用 rule 分类仍应结合具体 stat_sub_type 和引擎上下文判断。
# 固定值 / 参数候选
- `hunger`
- `death_blow`
- `hero_crit`
- `hero_killing_blow`
- `mode`
- `control`
- `unkown`
- `town_idle`
- `quest_fail`
- `pass`
- `camping_relieve_stress`
- `camping_eat`
- `tile`
- `retreat`
- `effect`
- `capture`
- `monster_crit`
# 语义
- 调整 Buff 持有者造成的压力伤害（百分比）。
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`9`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type stress_dmg_percent` 与 buffs.json 的 `"stat_type":"stress_dmg_percent"` 对应。
# 引擎行为（重要）
- 注意：对怪物侧无效，该代码只对因我方引起的加压改变量有影响（比如狼人变身的加压），对怪物作为压力施法者的情形不适用
- 受限于全局规则的压力所受量上限，承受压力buff最大只能提升到300%，即无论如何提升受压，最多也只承受300%压力
- 该 Buff 只有持有者为英雄时有效；不要将它推广为怪物侧通用的压力施加量修正。
- 它与受术者的 `stress_dmg_received_percent` 位于同一Buff乘区，所有修正先加算；原版最终系数受全局规则限制在 20% 至 300%，之后再乘环境乘区（1＋亮度额外压力修正＋等级差额外压力修正）。亮度与等级差互相加算，见机制52及全局规则第37行。
- 本结论限于正向压力伤害；压力治疗、惊恐 DOT 与其他压力调用链必须单独确认。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"stress_dmg_percent","stat_sub_type":"hunger","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
