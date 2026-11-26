# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.guard
# 分类
Buff/战斗属性
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔 `0` 或 `1`。
- 只有参数为 `1` 时才建立守护；参数为 `0` 时等同于未填写该关键字。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.guard 1`：建立守护。
- `.guard 0`：不产生守护效果。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.guard 1` 会无视 `.chance` 限制；在命中/未命中语义有效的场合可用双 false 抑制，但在 actout、道具 Effect、spawn Effect 等场合双 false 无法抑制。
- 详见：[Mechanics/03-chance与抗性.md](../../Mechanics/03-chance与抗性.md)
- 知识库编写者2026-11-18确认：施加守护需要前置清除守护／被守护；未前置的具体后果不清楚，不统一断言非法、报错、整技失效或崩溃。具体清理对象、字段组合及准确时序未明确；群体守护可能需要特殊处理，流程待确认。原表技能检查仅按具名条件保留。来源：Sources/guard_preclear_requirement_20261118.json。
- `.guard 1` 建立守护时不受 `.chance` 限制；即使 `.chance` 判定为不生效，守护仍会执行。
- 若需要在技能命中/未命中语义有效的场合阻止守护，使用 `.on_hit false .on_miss false`；该写法可能产生红字报错，但通常不会造成实质性问题。
- 在 actout、道具 Effect、spawn Effect 等 `.on_hit` / `.on_miss` 无意义的场合，双 false 或省略二者都不能阻止该守护。
- 技能中存在 `.guard` 时，目标已有守护且此前没有清除其被守护状态，可能触发红钩防多重守护检查，使整条技能不执行；该特殊机制及虚假守护标志的双 false 限制见Mechanics/03-chance与抗性.md。即使虚假 `.guard` 配 `.chance 0%` 和双 false，已有守护目标仍可能触发检查。
- 迂回表第98条补充：保险前提为施术者或目标任一方具有被守护或守护者状态；正向守护检查技能是否含 `.clearguarded 1`，反向守护检查是否含 `.clearguarding 1`。按原表观察，检查不校验清除目标或该 Effect 是否实际执行；虚假清理的双 false 仅在相应技能命中门有效时能阻止实际清除，`.chance 0%` 不能阻止清除。完整范围见Mechanics/03-chance与抗性.md。
- 知识库编写者2026-11-05补充：.guard 1、.clearguarded 1、.clearguarding 1通常不受自身.chance和effect_chance制约；但对该Effect声明.force_resist_type后，可由指定类型对应施加率及effect_chance制约是否生效，目标抗性按指定类型处理。既有概率豁免结论仅限未强制过抗时。来源：Sources/guard_start_triggers_20261105.json。
# 常见错误
- 将 `.guard 0` 当作会建立守护。
- 认为 `.chance 0` 能阻止 `.guard 1`。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:377`
```darkest
effect: .name "Guard 1"  .target "target" .curio_result_type "positive" .guard 1 .on_hit true .on_miss true .duration 2
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:140`
```darkest
effect: .name "Steward Human Guard" .target "target"  .guard 1 .on_hit true .on_miss true .duration 3 .queue true
```
- 官方 DLC `702540_shieldbreaker`：`DarkestDungeon\dlc\702540_shieldbreaker\effects\shieldbreaker.effects.darkest:87`
```darkest
effect: .name "Snake Guard 1"  .target "target" .curio_result_type "positive" .guard 1 .on_hit true .on_miss true .duration 3
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 用户补充的 `.guard` 与 `.chance` 时序/判定说明。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
