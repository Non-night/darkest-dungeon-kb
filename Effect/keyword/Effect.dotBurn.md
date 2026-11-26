# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.dotBurn
# 分类
扩展/专项字段
# 参数类型
单个整数
# 参数约束
- 参数为单个整数，表示施加的燃烧 DOT 数量。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.dotBurn <amount>`：给目标施加指定数量的 Effect 型燃烧。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 写有有效 DOT 的 Effect 通常同时写 `.can_apply_on_death true`；漏写会产生红字报错。
- 详见：[Mechanics/40-Effect防红字配套字段.md](../../Mechanics/40-Effect防红字配套字段.md)
- 知识库编写者确认（2026-09-20）：燃烧没有对应的目标燃烧抗性。
- 当基础 `.chance` 为 100% 或更高时，不写 `.dot_irresistible true` 的自动描述可能显示“燃烧[x]（100%基础概率）”；写为 `true` 后该基础概率文字不显示。对燃烧而言，这通常是描述清理，而不是绕过实际燃烧抗性。
- 燃烧在持有者行动结束后结算，不使用普通持续回合数；结算后默认减少燃烧前层数的 50%，剩余层数向下取整。
- 知识库编写者在本次会话补充（入库日期 2026-10-17） 确认：Effect 型燃烧被施加时会与已有 Effect 型燃烧合并；例如 8 层后再施加 7 层，存档中表现为一个 15 层实例。合并具体发生于施加瞬间还是随后 Update 尚未确认。
- 知识库编写者本次会话确认：Effect 型燃烧在施加时或随后 Update 时会被强制设为 `duration: 10000`；确切时点未确认。对群偷取没有“施加”过程，因此偷取 Effect 型燃烧不会触发该合并。
- 带有燃烧的单位死亡时触发野火蔓延：左侧或右侧相邻目标随机一个获得一半燃烧层数，向下取整；是否受燃烧衰减速率 Buff 影响尚未确认。
- 该 Effect 所属攻击造成暴击时，燃烧施加量增加 `50%`。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:368`
```darkest
effect: .name "RW Sunstone Searing Self Burn" .target "performer" .chance 100% .dotBurn 2 .dot_irresistible true .on_hit true .on_miss true .queue true .apply_once true
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:5`
```darkest
effect: .name "RW Burn 2" .target "target" .curio_result_type "negative" .chance 100% .dotBurn 2 .dot_irresistible true .on_hit true .on_miss false .can_apply_on_death true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:566`
```darkest
effect: .name "When hit Self Burn"  .target "performer" .curio_result_type "negative" .chance 100% .dotBurn 1 .dot_irresistible true .on_hit true .on_miss false .apply_once true
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Fire’s Edge Modding Features 无夜译注表。
- 知识库编写者补充（2026-09-20）。
- 知识库编写者在本次会话补充（入库日期 2026-10-17） 的会话补充与实测结论。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
