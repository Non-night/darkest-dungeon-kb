# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.set_monster_class_reset_hp
# 分类
扩展/专项字段
# 参数类型
布尔（合法值：`true`、`false`、`0`、`1`）
# 参数约束
- 当前知识库收录下列 8 个固定候选值；生成代码时应优先使用这些原样值。
# 固定值 / 参数候选
- `0`
- `1`
- `true`
- `false`
- `True`
- `False`
- `TRUE`
- `FALSE`
# 语义
- 合法参数为 `0`、`1`（数字布尔）；字段控制：变身后是否重置怪物生命（0为继承上一个同名怪的血量）
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 当前用户于 2026-09-30 确认该字段默认 `false`；省略／`false`／`0` 时继承前一怪物血量，显式 `true` 或 `1` 时重置为满血。
- 死而不僵目标上的 set 通常受死亡门阻断；set Effect 同时显式写 `.can_apply_on_death true .can_apply_on_corpse true` 时可突破。此时若 reset_hp 省略／false／0，继承血量也会继承死而不僵状态；写 true/1 后则成为满血正常状态并脱离死而不僵。当前用户于 2026-09-30 确认：治疗不能使继承的死而不僵状态解除。
- size-0 spawn 内 set 的列表延续与生命/Buff 继承配置是不同问题；A→B 示例中腐蚀保留不证明任何配置都保留。set 瞬间的 hp_reaction 触发细节仍未确认。
- 详见：[Mechanics/28-spawn、生命反馈与size0执行链.md](../../Mechanics/28-spawn、生命反馈与size0执行链.md)
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:136`
```darkest
effect: .name "xform coccoon A" .target "target" .chance 100% .set_monster_class_id cocoon_A .set_monster_class_reset_hp true .set_monster_class_reset_buffs true .on_hit true .on_miss true .queue true .apply_once true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:127`
```darkest
effect: .name "Syco Swap A" .target "performer" .chance 100% .set_monster_class_id sycophant_A .set_monster_class_reset_hp true .set_monster_class_reset_buffs true .on_hit true .on_miss true .queue true .apply_once true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:137`
```darkest
effect: .name "xform coccoon B" .target "target" .chance 100% .set_monster_class_id cocoon_B .set_monster_class_reset_hp true .set_monster_class_reset_buffs true .on_hit true .on_miss true .queue true .apply_once true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
