# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.spawn_target_actor_base_class_id
# 分类
扩展/专项字段
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 参数为英雄职业 ID 或怪物 base class ID。
- 必须写在 `.target` 之前；只在 spawn 定向流程中使用。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- 把 spawn Effect 的默认目标改为场上所有匹配指定 base class ID 的单位。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 定向会替换 spawn Effect 的默认目标；同 base class id 存在多个单位时可能全部成为目标。
- 配合 `.swap_source_and_target true` 时，被定向单位成为施术者，原 spawn 怪物成为受术者。
- 同一怪物连续多次 set 的 spawn 定向存在失效例外；从第二次 set 起另有对英雄跨侧 Buff 被视为同侧的问题。不得按普通定向规则保证连续链可用，详见专题28。
- 详见：[Mechanics/07-spawn定向.md](../../Mechanics/07-spawn定向.md)
- 知识库编写者确认（2026-09-20）：该字段只在 spawn 调用中生效；hp_reaction 等非 spawn 调用忽略它，但不阻断 Effect。生命反馈中 `.target target` 的默认目标为触发反馈的单位自身，即使反馈插入 spawn 也不继承定向。其他调用方的默认目标须分别核对。
- 同 ID 多单位可能全部成为目标。
- 定向后 `.target target_group` 会映射到被定向单位所在一侧的全体。
- 配合 `.swap_source_and_target true` 时，被定向单位成为施术者，原 spawn 怪物成为受术者。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:43`
```darkest
effect: .name "farmer_spawn_speed_buff_A" .spawn_target_actor_base_class_id foreman  .target "target" .chance 100% .combat_stat_buff 1 .speed_rating_add 1	.duration 2 .on_hit true .on_miss false .queue true .apply_once true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:44`
```darkest
effect: .name "farmer_spawn_speed_buff_B" .spawn_target_actor_base_class_id foreman  .target "target" .chance 100% .combat_stat_buff 1 .speed_rating_add 2	.duration 2 .on_hit true .on_miss false .queue true .apply_once true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:45`
```darkest
effect: .name "farmer_spawn_speed_buff_C" .spawn_target_actor_base_class_id foreman  .target "target" .chance 100% .combat_stat_buff 1 .speed_rating_add 3	.duration 2 .on_hit true .on_miss false .queue true .apply_once true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
