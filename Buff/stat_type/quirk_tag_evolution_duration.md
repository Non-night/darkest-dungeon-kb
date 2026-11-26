# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

quirk_tag_evolution_duration
# 分类
Buff `stat_type`
# 参数类型
固定字符串；配套 `amount` 为数值，`stat_sub_type` 为字符串。
# 参数约束
- `stat_sub_type` 可自由填写，但仍应使用稳定、可追踪的 ID。
- 可用 rule 分类仍应结合具体 stat_sub_type 和引擎上下文判断。
# 固定值 / 参数候选
- 无固定副类型候选。
# 语义
- 怪癖进化时间的改变
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`82`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type quirk_tag_evolution_duration` 与 buffs.json 的 `"stat_type":"quirk_tag_evolution_duration"` 对应。
# 引擎行为（重要）
- 可用于制作自定义文本，amount的数值可以在buff合并于同一状态图标时相加显示。
- 回合开始的已确认相对顺序：愈合→流血／腐蚀→怪癖自然进化→before_turn Buff持续时间扣减。仅剩1回合的before_turn怪癖进化时间修正先参与本次进化，再到期；本回合进化才获得魔免不能阻止此前已结算的流血／腐蚀。第55条P1162/P1164–P1165，当前用户2026-11-03确认；非新实测，不推定燃烧、其他DOT或完整开始流程。见Mechanics/17-Buff持续时间类型与实际清除.md。
- 用途与数值范围须分开判断。原表第96条P1514-P1516/X1858-X1862记载：evolution_duration_min/max，以及quirk_tag_evolution_duration实际用于自然进化时，进化时间按整型变量处理，表述范围为±2147483648；自定义文本若采用upgrade_discount或quirk_tag_evolution_duration方案并配合XML，则可使用浮点数。不能把自然进化的整型范围套到仅显示文本的用法，也不能把文本迂回的浮点能力推广到实际自然进化。当前用户2026-11-04确认保留原表±2147483648写法；此为原表经验边界，不据此补推更精确的底层类型或端点。
- 这是常见的自定义 Buff 描述方案：利用同一状态图标上的 Buff 数值叠加来显示可变数值，因此适合需要把多个 Buff 的数值合并到描述中的场景。
- 副本中英雄／怪物 Buff 栏详情，仅在 Buff 原本能合并的前提下：本类型不携带附魔时纯文本和计数文本均可合并；文本 Buff 自身携带附魔时不合并。暴击源可与技能源合并且覆盖其普通图标，事件源与技能源不合并；不要求原本图标相同。特殊源内部规则本次未测，其他界面不作结论，所有附魔类型暂按同样处理而非逐类实测。详见 Mechanics/16-loc与loc2本地化覆盖优先级.md 与 Sources/buff_tooltip_merge_20261117.json。
- 与 `upgrade_discount` 相比，它不依赖打折类 `%d` 参数可能自动添加的负号；但文本长度上限相对 `upgrade_discount` 的精确比较尚未确认。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"quirk_tag_evolution_duration","stat_sub_type":"","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
