# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

combat_stat_add
# 分类
Buff `stat_type`
# 参数类型
固定字符串；配套 `amount` 为数值，`stat_sub_type` 为字符串。
# 参数约束
- `stat_sub_type` 必填，且必须来自固定候选表。
- 可用 rule 分类仍应结合具体 stat_sub_type 和引擎上下文判断。
# 固定值 / 参数候选
- `max_hp`
- `damage_low`
- `damage_high`
- `attack_rating`
- `crit_chance`
- `defense_rating`
- `protection_rating`
- `speed_rating`
- `riposte_on_hit_chance`
- `riposte_on_miss_chance`
# 语义
- 对指定 `stat_sub_type` 施加固定量／加法战斗属性修正；不是按当前属性值进行比例缩放。
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`2`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type combat_stat_add` 与 buffs.json 的 `"stat_type":"combat_stat_add"` 对应。
# 引擎行为（重要）
- 必须通过 `stat_sub_type` 指定被修改的战斗属性；它与 `combat_stat_multiply` 的结果不可互换，即使二者填写相同的 `amount`。
- `amount` 使用相应属性的内部单位。已明确：当 `stat_sub_type` 为 `attack_rating` 或 `defense_rating` 时，文件值 `0.01` 对应游戏内显示的 1 点精准或闪避，`0.10` 对应 10 点，`1` 对应 100 点。该换算目前只明确适用于精准与闪避，不得擅自推广到其他副类型。
- 所有 `combat_stat_*` 系战斗属性 Buff 都先结算固定值／add，再以加法结算后的结果计算百分比／multiply。
- Info 与界面中的精准、闪避常以百分号外观显示，但这不意味着“精准／闪避 +N%”必然属于倍率修正。若用户描述既可能指固定增加 N 点，也可能指按当前属性提高 N%，必须先询问用户，不能自行选择实现。
- 作为 Effect 简写 Buff 时，应使用 `.buff_type combat_stat_add`、`.buff_sub_type <属性>` 与 `.buff_amount <数值>`；不要和 `.combat_stat_buff 1` 加 `.attack_rating_add` 等另一套字段结构混用。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"combat_stat_add","stat_sub_type":"max_hp","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
