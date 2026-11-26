# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.apply_with_result
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数使用 `true` 或 `false`。
- AWR 仅指 `.apply_with_result true .queue false`；由于 `.queue` 默认是 `false`，省略 `.queue` 也可处于 AWR。
- `.queue true` 时 `.apply_with_result` 没有时序意义。
- 友方技能、友方技能饰品 Trigger 及友方技能附魔（friendly_additional_effect_ids）均无独立 AWR 时序；写 .apply_with_result true .queue false 视同普通 queue false，不是 Effect 不执行。知识库编写者2026-11-06明确补充，来源：Sources/friendly_enchantment_no_awr_20261106.json。
- 反击在伤害、暴击等常规数值结算上属于特殊攻击技能，但不属于本机制所称的普通攻击技能，不能据此套用普通攻击技能的 AWR 分层。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- `.apply_with_result true`：在普通攻击技能的 `queue false` 层之前进入 AWR 时序，社区简称 AWR。
- AWR 也称直伤前时序，但它不等同于 `skill_instant`。
# 作用范围
- 只在普通攻击技能的 `queue false` Effect 上形成独立 AWR 层。
- 技能引用、饰品 Trigger 和 `crit: .effects` 引用的 Effect 都可按各自 `.apply_with_result`/`.queue` 设置进入对应层。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 只有普通攻击技能中的 `.apply_with_result true .queue false` 构成 AWR；queue true、友方技能和反击技能中没有该时序意义。
- AOE 会先对全部目标结算 AWR，再进入 queue false。
- 详见：[Mechanics/04-queue与AWR.md](../../Mechanics/04-queue与AWR.md)
- AWR 层内部的来源顺序为：技能 AWR → 饰品 Trigger AWR → 暴击特效 AWR。
- 相同时序中的多个 Effect 通常按引用书写顺序生效。
- AOE 会先依次完成每个目标的全部 AWR，再进入所有目标的 queue false，随后才进入 queue true。
- spawn、hp_reaction 等后续机制不能仅凭自身填写 AWR 就无条件倒流到触发它们的 Effect 之前。
- 选定攻击目标时，精准/闪避、伤害/防御、暴击/被暴击等主要面板计算已经完成；AWR 中才施加普通攻击、伤害或暴击 Buff 通常无法修改本次预计算。
- 目标的 `damage_received_percent` 易伤/硬减伤乘区在 AWR 后参与直伤，因此 AWR 中给目标施加临时易伤可以修改本次直伤。详见 `Mechanics/32-伤害公式与AWR易伤.md`。
# 常见错误
- 在 `.queue true`、友方技能或反击技能中期待 `.apply_with_result true` 产生 AWR。
- 把 AWR 解释成任意调用环境都能使用的通用提前结算字段。
- 把 AWR 与 `skill_instant` 视为同一机制。
- 忽略 AOE 按时序层分批遍历目标。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:35`
```darkest
effect: .name "kill_target" .target "target" .chance 100% .kill 1 .on_hit true .on_miss true .apply_once true .queue false .apply_with_result true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2084`
```darkest
effect: .name "Clear Enemy Rank Target With Result" .target "performer" .chance 100% .clear_rank_target 1234 .on_hit true .on_miss true .apply_with_result true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:31`
```darkest
effect: .name "kill_performer_group_other" .target "performer_group_other" .chance 100% .kill 1 .on_hit true .on_miss true .apply_once true .queue false .apply_with_result true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 `DarkestDungeon\effects\base.effects.darkest:2084` 展示省略 `.queue` 的 `.apply_with_result true`，结合 `.queue` 默认值可判定其处于 AWR。
- 适用范围与完整来源次序属于专项时序结论。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
