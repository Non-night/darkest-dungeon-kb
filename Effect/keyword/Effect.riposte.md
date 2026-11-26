# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.riposte
# 分类
反击
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 可与 `.combat_stat_buff 1` 系简写能够搭配的战斗属性字段配合使用。
- 正常情况下，同一条逻辑 Effect 只写 `.riposte 1` 或 `.combat_stat_buff 1` 之一；两者同时写会红字报错，最终生效结果未知。
- `riposte_skill:` 只定义实际触发时使用的反击技能；反击技能定义本身不写、也不能写持续回合。
- 有限时长的反击通常由开启反击的 Effect 声明 `.duration N`；这里的持续回合本质上是该 Effect 所生成的反击 Buff 的持续时间。
- 如果饰品设计的是永久反击，则不需要为反击技能或相关饰品 Buff 另写持续回合数；应按饰品 Buff 的生命周期处理。
- 知识库编写者2026-11-24更正：反击不会触发回合开始附魔。反击属于攻击类技能，因此也不会触发友方技能附魔。反击是否触发回合结束、轮次结束等时间点附魔尚待实测，目前推测不会。反击内 AWR 的附魔类型边界见 Mechanics/92-附魔自附魔时序与 AWR 边界.md。来源见 Sources/riposte_turn_start_enchantment_awr_20261106.json。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.riposte 1`：生成 `buff_type = riposte` 的 Effect 简写 Buff，并把该 Buff 声明为反击源 `bsrc_riposte`。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.riposte 1` 生成 `buff_type = riposte`、来源为 `bsrc_riposte` 的 Effect 简写 Buff；其默认持续机制尚不明确。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- 获得反击 Buff（也即开启反击）无需拥有反击技能定义，但没有 `riposte_skill:` 反击技能定义的角色不会实际触发反击。开启状态与存在可执行的反击技能是两个条件，不能把缺少定义当成无法获得反击 Buff，也不能把获得状态当成已具备实际反击能力。 当前用户于2026-11-03明确；原表第52条 P1126-P1127为历史证据，非本轮新增实机测试。
- 若同时写 `.riposte_effect "aaa"`，`aaa` 会成为反击 Buff 的副类型。
- 反击持续时间的归属应按“开启反击的 Effect／相关 Buff”理解，而不是按 `riposte_skill:` 技能定义理解；具体 Buff 源、清除时机和饰品卸下后的生命周期仍需结合调用方核对。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2101`
```darkest
effect: .name "brigand_barrel_spawn_riposte" .target "performer" .chance 100% .riposte 1 .riposte_on_hit_chance_add 100% .riposte_on_miss_chance_add 100% .duration -1 .on_hit true .on_miss false
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\effects\duelist.effects.darkest:11`
```darkest
effect: .name "duelist_riposte"  .target "performer" .curio_result_type "positive" .chance 100% .riposte 1 .riposte_on_hit_chance_add 100% .riposte_on_miss_chance_add 100% .duration 2  .on_hit true .on_miss true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:83`
```darkest
effect: .name "RevenantRiposteA"  .target "target" .chance 100% .riposte 1 .riposte_on_hit_chance_add 100% .riposte_on_miss_chance_add 100% .duration -1 .on_hit true .on_miss true .damage_low_multiply -40% .damage_high_multiply -40% .crit_chance_add 0%
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
