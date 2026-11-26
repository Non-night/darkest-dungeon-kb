# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.clearguarded
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔 `0` 或 `1`。
- 只有参数为 `1` 时才清除目标的被守护状态；参数为 `0` 时等同于未填写该关键字。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.clearguarded 1`：清除当前 Effect 目标作为被守护者的守护。
- `.clearguarded 0`：不产生清除效果。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.clearguarded 1` 会无视 `.chance` 限制；只有在命中/未命中语义有效的场合才能用双 false 抑制。
- 详见：[Mechanics/03-chance与抗性.md](../../Mechanics/03-chance与抗性.md)
- 施加守护的前置清理要求见Mechanics/03-chance与抗性.md；知识库编写者2026-11-18确认需要前置清守护／被守护，但具体清理对象与字段组合、未前置的后果及群体守护处理仍未明确，不据此推定本字段必须对双方一律执行。
- `.clearguarded 1` 不受 `.chance` 限制。
- 迂回表第98条观察：正向守护技能的防多重守护检查只需在技能中检测到 `.clearguarded 1`，不校验其目标或是否实际清除；这是保险检测，不改变该关键字自身的实际目标与清除语义。
- 若需要在技能命中/未命中语义有效的场合阻止清除，使用 `.on_hit false .on_miss false`；该写法可能产生红字报错。
- 在 actout、道具 Effect、spawn Effect 等 `.on_hit` / `.on_miss` 无意义的场合，双 false 或省略二者都不能阻止该清除。
- 知识库编写者2026-11-05补充：.guard 1、.clearguarded 1、.clearguarding 1通常不受自身.chance和effect_chance制约；但对该Effect声明.force_resist_type后，可由指定类型对应施加率及effect_chance制约是否生效，目标抗性按指定类型处理。既有概率豁免结论仅限未强制过抗时。来源：Sources/guard_start_triggers_20261105.json。
# 常见错误
- 将 `.clearguarded 0` 当作会清除被守护状态。
- 认为 `.chance 0` 能阻止 `.clearguarded 1`。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1467`
```darkest
effect: .name "Clear Guarded Target" .target "target" .chance 100% .clearguarded 1 .on_hit true .on_miss true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1468`
```darkest
effect: .name "Clear Guard Target" .target "target" .chance 100% .clearguarding 1 .clearguarded 1 .on_hit true .on_miss true .has_description false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1470`
```darkest
effect: .name "Clear Guard Self" .target "performer" .chance 100% .clearguarding 1 .clearguarded 1 .on_hit true .on_miss true .has_description false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 Effect：`DarkestDungeon\effects\base.effects.darkest:1467-1470`。
- 用户补充的 `.clearguarded` 参数语义说明。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
