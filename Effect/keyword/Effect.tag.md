# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.tag
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 只写 `.name`、`.target`、`.on_hit`、`.on_miss` 而不写任何效果字段会发生什么，目前未知，不得据此断言 `.tag 0` 是构造占位 Effect 的必需字段。
# 固定值 / 参数候选
- `0`
- `1`
# 语义

- 可将 `.tag 0` 用作一条不产生实际效果的占位字段，但这不是无报错的空操作。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.tag 0` 可作为 size0Spawner 的无影响 sentinel 占位选择：它不施加标记，但实际引用时可能产生红字；不能把它描述成完全无诊断输出的空操作。
- 详见：[Mechanics/28-spawn、生命反馈与size0执行链.md](../../Mechanics/28-spawn、生命反馈与size0执行链.md)

- 当前只能确认 `.tag 0` 本身不实际施加标记；是否存在其他隐藏副作用尚不明确。
- 知识库编写者2026-11-06明确补充：对Effect型标记声明强制过减益抗性，可使其像Buff型标记一样经过减益施加率与减益抗性判定，同时仍受‘无法被标记’干涉；Buff型标记则不受‘无法被标记’干涉。来源：Sources/effect_mark_forced_debuff_resist_20261106.json。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:368`
```darkest
effect: .name "Mark performer" .target "performer" .chance 100%	.tag 1  .duration 4 .on_hit true .on_miss true .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:366`
```darkest
effect: .name "Mark Target"	.target "target" .curio_result_type "positive" .chance 100%	.tag 1  .duration 3	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:728`
```darkest
effect: .name "BH Minor Mark"	.target "target" .curio_result_type "positive" .chance 100%	.tag 1  .duration 2	.on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
