# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.summon_chances
# 分类
召唤
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `value`：召唤概率，最高为1.00（这里其实和红钩其他地方的概率一样，是按分子分母比值算概率，因此并非必须低于1.0），不用百分数。
对应summon_monsters的最多召唤四种不同怪物，此处也分别对应最多4个参数，用空格隔开
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 当前用户明确确认（2026-09-24）：同一条 Effect 有多个 `.summon_monsters` 候选且 `.summon_count 1` 时，`.summon_chances` 后按候选顺序对应的参数是随机抽取的相对权重；本结论不规定权重归一化公式或零/负权重行为。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1549`
```darkest
effect: .name "Summon Ecto 1" .target "performer" .chance 100% .summon_count 1 .summon_can_spawn_loot false .summon_monsters ectoplasm_A .summon_chances 1.0 .on_hit true .on_miss true .apply_once true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1550`
```darkest
effect: .name "Summon Ecto 2" .target "performer" .chance 100% .summon_count 1 .summon_can_spawn_loot false .summon_monsters ectoplasm_B .summon_chances 1.0 .on_hit true .on_miss true .apply_once true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1551`
```darkest
effect: .name "Summon Ecto 3" .target "performer" .chance 100% .summon_count 1 .summon_can_spawn_loot false .summon_monsters ectoplasm_C .summon_chances 1.0 .on_hit true .on_miss true .apply_once true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
