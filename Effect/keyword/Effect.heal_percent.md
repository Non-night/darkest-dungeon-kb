# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.heal_percent
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 参数为单个数值，表示最大生命值治疗比例；使用小数或百分号形式时保持单位一致。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- 按目标最大生命值的一定比例进行治疗。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 详见：[Mechanics/27-治疗源与真吸血.md](../../Mechanics/27-治疗源与真吸血.md)
- 同一逻辑 Effect 的 `.can_crit_heal` 可以控制 `.heal_percent` 是否允许治疗暴击。
- 治疗分类和固定暴击率由 `.source_heal_type` 决定。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\flagellant\effects\flagellant.effects.darkest:108`
```darkest
effect: .name flagellant_death_door_enter .target performer_group_other .chance 100% .heal_percent 0.10 .on_hit true .on_miss true .queue true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:213`
```darkest
effect: .name "HealSelf COM" .target "performer" .curio_result_type "positive" .chance 100%  .heal_percent 1.0 .on_hit true .on_miss false .queue true .source_heal_type curio
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\flagellant\effects\flagellant.effects.darkest:64`
```darkest
effect: .name "Flag Super Heal 1" .target "target" .curio_result_type "positive" .chance 100% .heal_percent 0.33	.on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
