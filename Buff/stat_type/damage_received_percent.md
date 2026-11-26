# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

damage_received_percent
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
- 目标所受直伤的独立百分比乘区；正值为易伤，负值为硬减伤。
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`28`。
- `amount` 正值：减益；负值：增益；零值：增益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type damage_received_percent` 与 buffs.json 的 `"stat_type":"damage_received_percent"` 对应。
# 引擎行为（重要）
- 注意：怪物侧一旦减伤超过100%时（如-120%所受伤害），在受到伤害攻击时，怪物将反而回血，生命值将会按照超过的伤害比例增加，且无视其生命上限，导致血条可能凸出去
- 直伤公式最后乘以 `(1 + 目标 damage_received_percent)`。该乘区在 AWR 后计算，因此 AWR 中给攻击目标施加临时易伤可以干涉本次直伤。
- 普通攻击、伤害或暴击 Buff 在 AWR 才施加时通常无法回头修改选定目标时已经完成的本次面板计算。详见：[伤害公式与 AWR 易伤](../../Mechanics/32-伤害公式与AWR易伤.md)。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"damage_received_percent","stat_sub_type":"","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
