# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.chance
# 分类
扩展/专项字段
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 参数为单个数字，可写整数、小数或带 `%` 的数字。
- 除 float 可表示范围外，没有通用数值范围限制；可以为负数或超过 `100%`。
- `.keyStatus`、`.skill_instant true`、`.monsterType` 存在特殊概率规则，必须同时查看本词条的引擎行为。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.chance <value>`：规定当前 Effect 的基础生效概率；省略时默认值应该是 `1`，即 `100%`。
# 作用范围
- 作用于当前 Effect 的概率判定；具有专属施加率和抗性的效果还会继续进行对应计算。
- `.chance` 与 `riposte_on_hit_chance`、`riposte_on_miss_chance` 是不同的概率门；省略 `.chance` 不会提高反击概率。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 详见：[Mechanics/03-chance与抗性.md](../../Mechanics/03-chance与抗性.md)
- Buff 施加到异侧目标时会减去目标减益抗性；流血、腐蚀等按各自施加率和抗性计算。
- 目标减益抗性的有效范围为 `0～500%`；条件概率门常把最终概率控制在低于 `0%` 或高于 `600%`，避免抗性改变真假结果。
- `.keyStatus`、`.skill_instant true`、`.monsterType` 的 `.chance` 低于 `100%` 时会产生红字并强制视为 `100%`；高于 `100%` 时进入无动画翻页特殊行为。常规写法使用 `100%`。
- 攻击技能暴击时，省略 `.crit_doesnt_apply_to_roll` 或写 `false` 会使概率增加全局规则规定的值，当前默认是 `20%`。
- 同一次常规技能内的 Effect 与指定进攻向饰品 Trigger 共享概率骰子；命中骰子、ActorDot、受击/反击、击杀 Trigger、道具等边界另有已测试的隔离规则。不得把该结论套用到 Fire's Edge DLC 新内容。详见 `Mechanics/51-Effect概率骰子共享与隔离.md`。
- Buff 同侧/异侧看最终指向；同侧不计算减益施加率和减益抗性。指向异侧仍按同侧的已确认特例为 target_enemy_group、target_group_other、target_enemy_rank；target_enemy_random 仅当前用户2026-11-02表示“好像”的待确认线索。target、target_group 等常规目标按最终指向判断。普通 Effect 独立抗性及其他生效门另核。统一已有证据见 Mechanics/95-Buff同侧异侧与减益概率判定.md。
- 知识库编写者2026-11-05补充：.guard 1、.clearguarded 1、.clearguarding 1通常不受自身.chance和effect_chance制约；但对该Effect声明.force_resist_type后，可由指定类型对应施加率及effect_chance制约是否生效，目标抗性按指定类型处理。既有概率豁免结论仅限未强制过抗时。来源：Sources/guard_start_triggers_20261105.json。
# 常见错误
- 将 `.chance` 错误限制为 `0～100%` 或 `0～1`。
- 对不受对应施加率 Buff 影响的刚性 Effect 使用条件概率门。
- 非无动画翻页设计中，让 `.keyStatus`、`.skill_instant true` 或 `.monsterType` Effect 使用不等于 `100%` 的概率。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:57`
```darkest
effect: .name "Push 3D" .target "target" .push 3	.chance 130%	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:54`
```darkest
effect: .name "Push 3A" .target "target" .push 3 	.chance 100%	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:55`
```darkest
effect: .name "Push 3B" .target "target" .push 3 	.chance 110%	.on_hit true .on_miss false .can_apply_on_death true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
