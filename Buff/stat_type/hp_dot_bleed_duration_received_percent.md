# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

hp_dot_bleed_duration_received_percent
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
- 流血所受时间改变（百分比）（仅对effect写法流血有效）
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`60`。
- `amount` 正值：减益；负值：增益；零值：增益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type hp_dot_bleed_duration_received_percent` 与 buffs.json 的 `"stat_type":"hp_dot_bleed_duration_received_percent"` 对应。
# 引擎行为（重要）
- 需要注意以下几点：
  这些种类的buff仅能修饰写在effect里的dot效果（effect写法的流血腐蚀恐惧愈合）
  对于上面的hp_dot_bleed、hp_dot_poison、hp_dot_heal、stress_dot、shuffle_dot等buff写的dot没有效果（buff写法的流血腐蚀恐惧愈合）
  1、对已经挂上的dot无效，这部分的代码只影响之后挂上的的dot
  2、当dot的持续时间被缩减至100%以下（不含100%）时，持续时间将变为永久
        比如-100%受到惊恐的回合，此时受到惊恐效果时，惊恐的持续时间为0，这时候等于无视惊恐，但是，在这个基础上再减少1%（-101%受到惊恐的回合），此时受到惊恐效果时，持续时间为永久，然而，dot所属的源仍然会在特定时机，清除其中的所有dot，即使其持续时间未结束，具体不同来源的buff会在何时被统一清除，见本Excel表格中“Sources”表中的“Buff sources”栏，和“源buff类型”表中的内容
  3、改变量可以随意写，这个没有什么限制
  
  关于dot持续时间变零甚至为负，所带来的影响的相关测试，详见《关于buff_duration_percent 引出的增减益（以及视为增减益的DOT、反击、守护等）经过造成持续时间和所受持续时间buff的修正后，最终持续时间成为零和成为负时的相关测试》一文。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"hp_dot_bleed_duration_received_percent","stat_sub_type":"","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
