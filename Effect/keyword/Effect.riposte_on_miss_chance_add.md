# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.riposte_on_miss_chance_add
# 分类
反击
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.combat_stat_buff` 系简写字段，对 `riposte_on_miss_chance` 施加固定量／加法修正。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 战斗属性简写：固定量增加闪避时反击概率；英雄基础值为 `0`。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- 英雄默认 `riposte_on_miss_chance = 0`。本字段可写在 `.combat_stat_buff 1` 后并正常生效。
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
