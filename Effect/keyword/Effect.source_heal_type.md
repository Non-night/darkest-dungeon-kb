# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.source_heal_type
# 分类
扩展/专项字段
# 参数类型
枚举/固定候选值
# 参数约束
- 参数必须来自固定候选表；不得自造治疗源。
# 固定值 / 参数候选
- `hero_skill`
- `hero_skill_multi_target`
- `monster_skill`
- `monster_skill_multi_target`
- `camp_skill`
- `camp_skill_multi_target`
- `companion`
- `eat`
- `act_out`
- `damage_heal`
- `effect`
- `flashback`
- `dot`
- `curio`
# 语义
- `hero_skill` / `hero_skill_multi_target`：单体/群体英雄技能治疗。
- `monster_skill` / `monster_skill_multi_target`：单体/群体怪物技能治疗。
- `camp_skill` / `camp_skill_multi_target`：单体/群体扎营治疗。
- `companion`、`eat`、`act_out`、`damage_heal`、`effect`、`flashback`、`dot`、`curio`：分别为同伴、食物、act out、真吸血、常规 Effect、闪回、愈合 DOT、奇物治疗。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 详见：[Mechanics/27-治疗源与真吸血.md](../../Mechanics/27-治疗源与真吸血.md)
- 治疗源决定对应治疗/受疗 Buff 的 `stat_sub_type` 匹配，并决定固定治疗暴击率。
- 完整逐项表及真吸血见相关机制文档。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:334`
```darkest
effect: .name "HealSelf 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 3	.on_hit true .on_miss false .queue true .source_heal_type hero_skill
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:335`
```darkest
effect: .name "HealSelf 2" .target "performer" .curio_result_type "positive" .chance 100% .heal 4	.on_hit true .on_miss false	.queue true .source_heal_type hero_skill
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:336`
```darkest
effect: .name "HealSelf 3" .target "performer" .curio_result_type "positive" .chance 100% .heal 5	.on_hit true .on_miss false	.queue true .source_heal_type hero_skill
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
