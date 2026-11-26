# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.set_mode
# 分类
扩展/专项字段
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.set_mode <mode_id>`：让 Effect 的最终受术者尝试进入指定模式。
- size-0 作为条件载体、且设计目标是对侧全体时，可用非指向性的 `.target target_enemy_group` 承载这次模式切换；这是一种目标映射选择，不是 spawn 定向。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 知识库编写者2026-09-19补充：size-0 对英雄或怪物进行条件模式切换时，若设计目标是对侧全体，可用 `.target target_enemy_group` 非指向性处理；没有对应模式定义的单位无事发生。模式 ID 过于简单或常见时，其他同名模式单位也可能被干涉，必须使用唯一的 Mod 前缀 ID。
- 详见：[Mechanics/28-spawn、生命反馈与size0执行链.md](../../Mechanics/28-spawn、生命反馈与size0执行链.md)
- 知识库编写者补充：对英雄或怪物使用 size-0 操作模式时，`.target target_enemy_group` 可以把 Effect 送到对侧全体；拥有该精确 mode ID 定义的单位才会受模式切换影响，没有对应模式定义的单位无事发生，怪物侧同理。
- 该写法通常不需要 `.spawn_target_actor_base_class_id`，但 `target_enemy_group` 会覆盖对侧全体；只有设计明确允许对侧所有同 ID 模式单位被处理时才可使用。
- 这条行为只说明“无对应模式定义的单位不受影响”，不保证模式 ID 在全局唯一，也不替代对目标侧、调用方和时序的核对。
# 常见错误
- 把 `.target target_enemy_group` 当作按职业、base class 或站位的精确筛选。
- 使用过于简单或常见的模式 ID（例如原版已有的 `beast` 或其他普通单词），却没有评估其他单位的同名模式定义；这些单位可能一起被切换。
- 因为多数模式名不重复，就把对侧群体切换写成无条件安全；应使用带 Mod 前缀且唯一的模式 ID。
- 忽略普通 `.set_mode` 在 AOE 流程中可能截断其后目标处理的既有边界。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:462`
```darkest
effect: .name "switch_mode_beast_self" .target "performer" .set_mode beast .chance 100% .on_hit true .on_miss false .queue false
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:36`
```darkest
effect: .name "switch_mode_land_self" .target "performer" .set_mode land .chance 100% .on_hit true .on_miss true .queue false
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\additional.color_of_madness.effects.darkest:41`
```darkest
effect: .name "COM switch_mode_land_self" .target "performer" .set_mode land .chance 100% .on_hit true .on_miss true .queue false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 知识库编写者2026-09-19补充：size-0 对英雄/怪物进行条件模式切换时，可用 `target_enemy_group` 非指向性处理；无对应模式定义的单位无事发生。
- 模式 ID 过于常见时的同名定义干涉风险来自上述目标范围与模式匹配条件；不把“大多数模式名不重复”升级为全局唯一保证。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
