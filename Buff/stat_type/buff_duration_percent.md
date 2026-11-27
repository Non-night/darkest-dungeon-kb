# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

buff_duration_percent
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
- 施术者侧持续时间修正，影响持有者作为施术者新施加的 Buff。
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`86`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type buff_duration_percent` 与 buffs.json 的 `"stat_type":"buff_duration_percent"` 对应。
# 引擎行为（重要）
- 2026-11-27 常规技能普通 Buff 实测：先读基础时长 D，按 D × (1 + Σ amount) 算出时长，再就近取整。正值恰好半单位向上，实测 2.5 → 3。同类 amount 加算。
- 常规技能的简写 Effect .duration 对已测正小数先截断，完整 Buff JSON 的 duration 对已测带小数点写法回退到默认 3。两者在本测试中省略或取到基础 0 均按默认 3。
- 乘算取整后的 0 可以施加，after_turn 在本次个人回合结束时移除。结果 -1 表示无限计时。一般 skill 源 Buff 扎营时清除，此例显示持续至扎营，实际清除取决于 Buff 源和特殊类型的规则。其他负整数与负半数边界待测。
- 迂回表第 243 条实测：作为修正属性本身，buff_duration_percent 在 bsrc_campingskill 源下可跨过再次扎营。受修正的新 Buff 按其自身规则清除。详见 [扎营清除例外](../../Mechanics/15-Buff源与真驱散.md#扎营有自动清除例外的-buff-类型)。
- 旧术语表关于低于 100% 即永久的概括已被普通 Buff 实测修正。社区反馈反击、守护、标记也受影响，可暂按同一公式估算，具体计算规则仍待实测。DOT 是否受影响仍待确认。详见 [持续时间专题](../../Mechanics/17-Buff持续时间类型与实际清除.md) 与 Sources/buff_duration_percent_20261127.json。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"buff_duration_percent","stat_sub_type":"","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
