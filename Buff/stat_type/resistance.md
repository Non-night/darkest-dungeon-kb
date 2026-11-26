# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

resistance
# 分类
Buff `stat_type`
# 参数类型
固定字符串；配套 `amount` 为数值，`stat_sub_type` 为字符串。
# 参数约束
- `stat_sub_type` 必填，且必须来自固定候选表。
- 可用 rule 分类仍应结合具体 stat_sub_type 和引擎上下文判断。
# 固定值 / 参数候选
- `stun`
- `move`
- `poison`
- `bleed`
- `disease`
- `debuff`
- `death_blow`
- `trap`
# 语义
- 眩晕抗性（面板最高500%）
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`11`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type resistance` 与 buffs.json 的 `"stat_type":"resistance"` 对应。
# 引擎行为（重要）
- 常规抗性存在面板上限（500%）和下限（0%），但对应的施加率并不存在上下限。
  
  减益抗性仅当异侧时有效，即老生常谈的【同侧不过抗，异侧需过抗】规则。
  
  死门抗性可通过调整致死率，实现等效于更高的死门抗性，但是致死率buff的修改对非直伤无效果，全局规则致死率则因非常不提倡改动全局规则而通常不会去使用。
  
  面板抗性具有上下限，并不意味着更高的正抗性buff或者更低的负抗性debuff是无意义的，因为结算前需要与对应施加率做抵消。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"resistance","stat_sub_type":"stun","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
