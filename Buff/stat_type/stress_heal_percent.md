# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

stress_heal_percent
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
- 造成压力治疗效果（百分比）
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`10`。
- `amount` 正值：增益；负值：源表未填写（未知，不推定）；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type stress_heal_percent` 与 buffs.json 的 `"stat_type":"stress_heal_percent"` 对应。
# 引擎行为（重要）
- 压力治疗没有全局规则的上下限
- 压力治疗施加量 stress_heal_percent 与所受量 stress_heal_received_percent 同乘区加算：基础减压量×(1+施加量修正+所受量修正)，不是两端分别乘算。
- 原表基础1点，−500%/+1000%得到6点，+100%/+200%得到4点。第53条P1132–P1139/X1319–X1327，当前用户2026-11-03确认；非本轮实机测试。取整、不同来源、其他治疗及未知调用链不据此推定；详见Mechanics/52-压力伤害计算与精准加压.md。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"stress_heal_percent","stat_sub_type":"hunger","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
