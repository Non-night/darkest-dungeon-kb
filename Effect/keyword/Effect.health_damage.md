# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.health_damage
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `value`：也被称为真实伤害，无视防御，可以被 damage_received_percent 和 格挡 干涉，造成的击杀不会激活饰品及ad的击杀effect
注意：真伤击杀容器（锅）时会出现BUG，从容器完全消失到可能造成游戏崩溃的可能性均有，虽然其中的英雄不会消失，因此避免使用真伤攻击容器
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 真伤的 queue 时序会影响击杀型 ActorDot 是否来得及结算。
- 当前用户于2026-10-08确认：因真伤死亡的怪物不会触发英雄击杀 Trigger，也不参与流血/腐蚀 DOT 的最后成功施加者击杀 Trigger 归属判定；燃烧致死同样不会触发击杀 Trigger。
- 当前用户于2026-10-10给出设计建议：非 Size-0 怪物的真伤无特殊设计时通常声明 `.damage_type attack`；若要求无视护体格挡则使用 `bleed`、`poisoned` 或 `burn` 之一。该建议基于容器 Bug 规避推测，不能当作已确认的修复方案；Size-0 不适用，需按具体链条单独判断。
- 生命反馈 size-0 的 size0Spawner 流程中，实际真伤必须排在初始最大生命扩展、回满与第二次最大生命扩展之后；反击或饰品被命中 Trigger 中仍需遵守 size-0 与 `.health_damage` 的已知风险。
- 详见：[Mechanics/10-最后一杀与非直伤击杀.md](../../Mechanics/10-最后一杀与非直伤击杀.md)
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:545`
```darkest
effect: .name test_health_damage_1 .target target .chance 100% .health_damage 5 .on_hit true .on_miss true .queue true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:170`
```darkest
effect: .name "Thing Consume Self 1" .target "performer" .chance 100% .health_damage 5 .on_hit true .on_miss false .queue true .apply_once true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:546`
```darkest
effect: .name test_health_damage_2 .target target .chance 100% .health_damage 10 .on_hit true .on_miss true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
