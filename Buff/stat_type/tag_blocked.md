# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

tag_blocked
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
- 无法被标记（amount为1）
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`41`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type tag_blocked` 与 buffs.json 的 `"stat_type":"tag_blocked"` 对应。
# 引擎行为（重要）
- 大于0时生效，小于等于0时不生效
- 知识库编写者补充（2026-09-20）：所称 tag_block Buff 在本库按规范 stat_type tag_blocked 记录；amount 为 0 时，默认视为增益，无须 force_positive: true 才获得这一默认分类。
- 默认增益分类与实际阻止标记分开：既有记录为 amount > 0 时阻止标记，amount <= 0 时不生效。因此 amount: 0 默认是增益，但不提供阻止标记的实际效果。不外推其他数值的显示分类或驱散行为；tag_block 是已收录的 Pop 类型名，不作为 Buff stat_type 的替代拼写。
- 知识库编写者2026-11-06明确补充：对Effect型标记声明强制过减益抗性，可使其像Buff型标记一样经过减益施加率与减益抗性判定，同时仍受‘无法被标记’干涉；Buff型标记则不受‘无法被标记’干涉。来源：Sources/effect_mark_forced_debuff_resist_20261106.json。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"tag_blocked","stat_sub_type":"","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
