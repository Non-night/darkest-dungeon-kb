# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.set_monster_class_reset_scale
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 当前知识库收录下列 2 个固定候选值；生成代码时应优先使用这些原样值。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- 合法参数为 `true`、`false`（字符布尔）；不得改用 `0`/`1`。字段控制：变身后是否重置怪物比例
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:290`
```darkest
effect: .name "Cocoon Swap 2-3 group" .target "performer_group_other" .chance 100% .set_monster_class_id curtain_F .set_monster_class_reset_hp true .set_monster_class_reset_buffs true .set_monster_class_reset_scale true .on_hit true .on_miss true .queue true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:291`
```darkest
effect: .name "Cocoon Swap 1-3 group" .target "performer_group_other" .chance 100% .set_monster_class_id curtain_G .set_monster_class_reset_hp true .set_monster_class_reset_buffs true .set_monster_class_reset_scale true .on_hit true .on_miss true .queue true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:284`
```darkest
effect: .name "Baron Refill Cocoons 1-3" .target "performer" .chance 100% .summon_count 3 .summon_can_spawn_loot false .set_monster_class_reset_scale true .summon_monsters curtain_G curtain_G curtain_G .summon_chances 1.0 .summon_ranks 0 .on_hit true .on_miss true .apply_once true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
