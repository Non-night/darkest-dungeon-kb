# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.stun
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 参数为单个持续时长数值；`.stun 1` 表示一次常规眩晕。
- `.stun` 参数不为 `0` 时，通常会将该 Effect 写为 `.queue true`；否则会产生红字报错。特殊设计若刻意需要 AWR/`queue false` 眩晕，可以接受该红字，但不得误称为无报错写法。
- 设计中写“眩晕概率 100%”默认指 `.chance 100%`，不是无视抗性。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- 对目标施加眩晕；参数表示持续的眩晕行动次数。
- 同一目标重复受到 `.stun 1` 不会简单叠加成多回合眩晕。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 详见：[Mechanics/32-伤害公式与AWR易伤.md](../../Mechanics/32-伤害公式与AWR易伤.md)
- 眩晕仍按施术者眩晕概率与目标眩晕抗性计算。只有设计明确写“必定成功”或“无视抗性”时，才使用不可抵抗或极端概率方案。
- AWR 中先成功眩晕，再给目标施加 `is_actor_status stunned` 的临时易伤，可使该易伤参与本次直伤。
- 防红字配套：只要 `.stun` 的参数不为 `0`，通常给同一逻辑 Effect 写 `.queue true`；不要依赖 `.queue` 的默认值 `false`。刻意使用 AWR/`queue false` 眩晕时仍可能生效，但会产生红字报错。
- 详见：[Effect 防红字配套字段](../../Mechanics/40-Effect防红字配套字段.md)。
# 常见错误
- 在不需要特殊 AWR/`queue false` 时序时，非零 `.stun` 却漏写 `.queue true`，无意义地产生红字报错。
- 把“眩晕概率 100%”直接解释为无视抗性。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:175`
```darkest
effect: .name "Stun 1" .target "target" .curio_result_type "negative" .chance 100% .stun 1	.on_hit true .on_miss false .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:176`
```darkest
effect: .name "Stun 2" .target "target" .curio_result_type "negative" .chance 110% .stun 1	.on_hit true .on_miss false .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:177`
```darkest
effect: .name "Stun 3" .target "target" .curio_result_type "negative" .chance 120% .stun 1	.on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
