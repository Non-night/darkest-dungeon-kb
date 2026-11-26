# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.buff_is_clear_debuff_valid
# 分类
Buff/战斗属性
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数为布尔值，使用已收录的 `true` 或 `false`。
- 当前推测本字段会像 `.duration` 一样覆盖被引用 Buff 定义中的 `is_clear_debuff_valid`，但该覆盖关系尚未确认。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- `.buff_is_clear_debuff_valid <bool>`：为本 Effect 产生或施加的 Buff 设置 `is_clear_debuff_valid`。
# 作用范围
- 可用于 `.buff_ids` 引用的 Buff，也存在与 Effect 简写 Buff 配套的原版实例。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 详见：[Mechanics/17-Buff持续时间类型与实际清除.md](../../Mechanics/17-Buff持续时间类型与实际清除.md)
- `.duration` 与 `.buff_duration_type` 覆盖 Buff 定义的行为已经确认；本字段是否以相同方式覆盖 `is_clear_debuff_valid` 目前仅为推测。
- 在覆盖关系确认前，不要让 Effect 与 Buff 对该属性填写互相冲突的值。
# 常见错误
- 把本字段覆盖 Buff 定义的行为写成已确认结论。
- 在 Effect 与 Buff 中填写互相冲突的值，并依赖尚未确认的覆盖顺序。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1052`
```darkest
effect: .name "Mortal Weakness Stress" .target "performer" .curio_result_type "negative" .chance 100% .buff_ids "mortal_weakness_stress" .buff_is_clear_debuff_valid false .on_hit true .on_miss true .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1051`
```darkest
effect: .name "Mortal Weakness" .target "performer" .curio_result_type "negative" .combat_stat_buff 1 .defense_rating_add -25% .speed_rating_add -3 .duration 1 .buff_duration_type combat_end .buff_is_clear_debuff_valid false .on_hit true .on_miss true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版同时存在 `.buff_ids` 和 Effect 简写 Buff 的使用实例；覆盖 Buff 定义中同名属性的行为目前为类比持续时间字段所得的推测。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
