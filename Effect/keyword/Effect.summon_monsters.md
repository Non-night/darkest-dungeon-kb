# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.summon_monsters
# 分类
召唤
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `目标怪物的【小类id】，格式类型为
.summon_monsters cultist_shrouded_D
最多4个，用空格隔开`：当怪物侧的rank总数（怪物侧单位的zise之和），加上正在召唤的单位的size大于4时，召唤将会失败，无事发生，因此一般情况下的召唤不会导致rank溢出崩溃
- 注意：当【怪物侧死亡与召唤同时发生】时，游戏对rank溢出的检查将会出错，把rank总数过大（加上正在死的单位）认定为足够（不加上正在死的单位）
- 因此，召唤行为请务必关注可能导致怪物死亡的时刻（攻击反伤之类的），警惕rank溢出导致的崩溃（召唤前 .kill_enemy_types corpse 或许能够缓解问题）
- 写在物品里，战斗外使用物品，会导致错误，若此次探索中未完成过战斗，游戏闪退，若完成过战斗，怪物的影像会出现，然后傻站着，无其它影响。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 当前用户于2026-09-30补充：召唤目标处于死而不僵状态时，召唤通常被阻断；召唤 Effect 同时显式写 `.can_apply_on_death true .can_apply_on_corpse true` 可突破该限制，少任一项均不行。此为召唤目标死亡状态的专项条件，不按召唤发起者是否死亡判断。
- 知识库编写者2026-09-19补充的“hp_reaction带出召唤仍被死亡门阻断”现限定为没有同时显式使用上述两个放行字段的常规情况；生命反馈入口本身不自动绕过死亡门。
- 详见：[Mechanics/28-spawn、生命反馈与size0执行链.md](../../Mechanics/28-spawn、生命反馈与size0执行链.md)
- 当前用户明确确认（2026-09-24）：同一条 Effect 的 `.summon_monsters` 写有多个候选，且 `.summon_count 1` 时，实际是从召唤列表中随机抽取一个候选；各候选的相对抽取概率由 `.summon_chances` 后按顺序对应的参数权重决定。
- 本结论只覆盖 `.summon_count 1` 的多候选情形；不据此推断其他召唤数量、零/负权重或抽取公式的边界。
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
