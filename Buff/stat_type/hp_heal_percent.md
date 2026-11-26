# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

hp_heal_percent
# 分类
Buff `stat_type`
# 参数类型
固定字符串；配套 `amount` 为数值，`stat_sub_type` 为字符串。
# 参数约束
- `stat_sub_type` 可为空；非空时必须来自固定候选表。
- 可用 rule 分类仍应结合具体 stat_sub_type 和引擎上下文判断。
# 固定值 / 参数候选
- `hero_skill`
- `hero_skill_multi_target`
- `monster_skill`
- `monster_skill_multi_target`
- `camp_skill`
- `camp_skill_multi_target`
- `companion`
- `eat`
- `act_out`
- `damage_heal`
- `effect`
- `flashback`
- `dot`
- `curio`
# 语义
- 治疗施加量的百分比改变
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`7`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type hp_heal_percent` 与 buffs.json 的 `"stat_type":"hp_heal_percent"` 对应。
# 引擎行为（重要）
- 常规生命治疗两端百分比hp_heal_percent与hp_heal_received_percent先加算后限幅；原版百分比系数0～2，上限关联全局规则heal_buff_percent_max=2.0。heal_buff_percent_min在规则资料中列为0，但当前用户2026-11-03明确治疗下限固定为0、不可变。后置hp_heal_amount另算，不将此写为总治疗量上限或彻底禁疗。与压力伤害stress_dmg_buff_min/max的全局限幅关联见Mechanics/27-治疗源与真吸血.md及Mechanics/54-极小乘极大数值迂回.md；迂回表第54条确认，非新实测。
- 治疗源由对应 Effect 的 `.source_heal_type` 或调用方式决定；真吸血 `damage_heal` 的倍率会与未限定来源及同来源治疗修正共同加减。详见：[治疗源与真吸血](../../Mechanics/27-治疗源与真吸血.md)。
- 百分比治疗修正先于固定治疗量结算；后置的 `hp_heal_amount` 不会被本字段再次相乘，所以极端负百分比无法封锁 `+1` 固定治疗。
- 新版新增固定受疗hp_heal_amount_received，旧无固定受疗说法不再适用。新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"hp_heal_percent","stat_sub_type":"hero_skill","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
