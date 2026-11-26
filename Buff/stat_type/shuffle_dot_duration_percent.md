# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

shuffle_dot_duration_percent
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
- 调整 Buff 持有者作为施术者所施加的扰乱持续时间（百分比）。
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`65`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type shuffle_dot_duration_percent` 与 buffs.json 的 `"stat_type":"shuffle_dot_duration_percent"` 对应。
# 引擎行为（重要）
- 该 Buff 修正持有者作为施术者所施加的扰乱持续时间，不是修改持有者受到的扰乱。是否会追溯修改目标身上已经存在的 DOT，尚未专项确认。
- 自 2026-08-19 更新后，该类外放持续时间修正不再只作用于 Effect 型 DOT；Buff 型 DOT 同样受其影响。
- 多个同类持续时间 Buff 的数值先相互加算，再修正持续时间；计算产生非整数时四舍五入。例如 `amount: 0.5` 表示施加持续时间增加 50%。
- 知识库编写者本次会话更正（入库日期 2026-10-17）：任意 DOT 的最终施加持续时间为负时，都无法成功施加。因此，负向 DOT 持续时间修正不再构成此前所述“产生永久 DOT”的安全问题；旧版负持续时间转为永久 DOT 的说法已被本结论取代。这里检查最终施加持续时间，不是仅凭修正 Buff 的 amount 为负判断施加失败；不得将此结论推广到普通非 DOT Buff。
- 最终修正恰为 `-100%` 时仍可正常尝试施加 DOT；若施加成功，持续时间为 0 的非燃烧 DOT 会生效一次后消失。因此对非燃烧 DOT 而言，持续 0 次在实际触发次数上可近似等同持续 1 次。
- 除燃烧外，上述 DOT 的默认持续类型均为 `before_turn`；燃烧不适用这里的‘持续 0 次仍触发一次’结论。
- 知识库编写者提供无夜2026-11-05 15:06–15:28聊天及范围澄清：Effect型与Buff型DOT的量为正或负均可存在；最终持续时间为负则不可存在。合法性看修正后的最终量与最终持续时间，不看初始值；修正Buff的影响范围保持已有规则不变。Effect型DOT另有描述观察：初始负量可存在，但施加该DOT的Effect不显示该DOT描述；初始负持续时间不可存在，但施加该DOT的Effect仍显示该DOT描述；这两条描述观察按聊天原述保留，不将“初始”改写为描述生成也必看最终值。任何类型的Buff型DOT均不由施加它的Effect生成该DOT的自动描述，因此无法以此出现在技能自动描述中。这里的“描述”明确指施加该DOT的Effect是否显示描述，不指持有者身上的状态说明或图标，也不限制手动自定义文本。 来源：Sources/dot_legality_description_20261105.json。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"shuffle_dot_duration_percent","stat_sub_type":"","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
