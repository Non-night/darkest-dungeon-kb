# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.healstress
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `value`：压力治疗，即减压
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 迂回表第114条P1801/X2296、P1803/X2299、P1804/X2300、P1805/X2301、P1807/X2304记录：同一Effect定义行同时写压力治疗 `.healstress` 与固定值生命治疗 `.heal` 时，应先写 `.healstress`、后写 `.heal`；反向顺序会使 `.heal` 不生效。改用百分比治疗 `.heal_percent` 时不受此顺序限制。仅限同一Effect定义行，不推广到不同Effect、分行、queue/AWR或其他字段。当前用户于2026-11-04确认知识库尚无一般边界并要求补入；本轮未新增游戏测试。
- 详见：[Mechanics/27-治疗源与真吸血.md](../../Mechanics/27-治疗源与真吸血.md)
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:487`
```darkest
effect: .name "human_stress_heal_party_1" .target "performer_group_other" .chance 100% .healstress 2 .on_hit true .on_miss false .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:488`
```darkest
effect: .name "human_stress_heal_party_2" .target "performer_group_other" .chance 100% .healstress 2 .on_hit true .on_miss false .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:489`
```darkest
effect: .name "human_stress_heal_party_3" .target "performer_group_other" .chance 100% .healstress 2 .on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
