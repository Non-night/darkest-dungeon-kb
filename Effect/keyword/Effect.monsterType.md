# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.monsterType
# 分类
扩展/专项字段
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 参数为一个怪物 type 字符串；可使用自定义 monster type。
- 常规条件 Effect 的 `.chance` 使用 `100%`；非无动画翻页设计不得使用其他概率。
- 同一条 Effect 中存在有效 `.monsterType` 时，`.target` 绝对不得写为 `target` 或 `target_enemy_group`；该组合会使游戏立即崩溃。
- 本字段与 `.keyStatus` 类似，属于 `.combat_stat_buff` 系列的条件简写。
- 需要长效Buff时不可保留默认bsrc_instantSkill来源；显式.buff_source_type覆盖后须按新源核对生命周期、重复和清理。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.monsterType` 是 Effect 的条件简写机制：仅当本次攻击目标具有指定 monster type 时，启用当前 Effect 中的简写战斗属性 Buff；常规写法通常与 `.combat_stat_buff` 系列搭配。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.monsterType` 与 `.keyStatus` 类似，属于 `.combat_stat_buff` 系列条件简写。
- 与 `.buff_ids` 同用时按 `.skill_instant true` 处理；默认bsrc_instantSkill受Update清除，显式.buff_source_type覆盖可按新源生命周期处理，仍检查重复与残留。
- 详见：[Mechanics/35-Effect条件简写与目标最小化.md](../../Mechanics/35-Effect条件简写与目标最小化.md)
- `.chance` 低于 `100%` 时会产生红字并强制按 `100%`；高于 `100%` 时进入无动画翻页特殊行为。
- 致命组合：有效 `.monsterType` 与 `.target "target"` 或 `.target "target_enemy_group"` 位于同一条 Effect 时，游戏必定立即崩溃。
- `.monsterType` 引出的简写 Buff 默认属于 `bsrc_instantSkill` 源，并会在游戏 Update 时消失。
- 同一条 Effect 使用 `.buff_ids` 引出外部 Buff 时，`.monsterType` 会被视为等同于 `.skill_instant true`：默认来源下这些 Buff 按 skill-instant 机制施加和清除；显式.buff_source_type覆盖后按新源生命周期处理。
# 常见错误
- 将有效 `.monsterType` 与 `.target "target"` 或 `.target "target_enemy_group"` 写在同一条 Effect。
- 试图用 `.buff_ids` 绕开 `bsrc_instantSkill` 的 Update 清除，让 `.monsterType` 引出的 Buff 存续超过 1 回合。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:267`
```darkest
effect: .name "Man Killer 1" .target "performer" .chance 100% .curio_result_type "positive" .monsterType "man" .combat_stat_buff 1 .damage_low_multiply 15%	.damage_high_multiply 15%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:268`
```darkest
effect: .name "Man Killer 2" .target "performer" .chance 100% .curio_result_type "positive" .monsterType "man" .combat_stat_buff 1 .damage_low_multiply 20%	.damage_high_multiply 20%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:269`
```darkest
effect: .name "Man Killer 3" .target "performer" .chance 100% .curio_result_type "positive" .monsterType "man" .combat_stat_buff 1 .damage_low_multiply 25%	.damage_high_multiply 25%	.on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
