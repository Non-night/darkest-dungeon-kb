# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.summon_does_roll_initiatives
# 分类
召唤
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数为数字布尔，只使用 `0` 或 `1`；不得改写为 `true` / `false`。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `1`：召唤物生成时获得 1 个行动点；其实际行动顺序仍按速度参与结算。
- `0`：召唤物生成时不获得行动点。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 本字段控制的是召唤物在生成时是否获得行动点，不表示 `.summon_does_roll_initiatives 1` 会立刻无视速度插入行动。
- 获得行动点后的行动先后仍由速度结算。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1544`
```darkest
effect: .name "Summon Anchor 1" .target "performer" .chance 100% .summon_count 1 .summon_can_spawn_loot true .summon_monsters drowned_anchor_A .summon_chances 1.0 .summon_does_roll_initiatives 1 .on_hit true .on_miss true .apply_once true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:318`
```darkest
effect: .name "spawn sprout" .target performer .chance 100% .summon_count 1 .summon_can_spawn_loot false .summon_monsters sprout_D .summon_chances 1.0 .summon_ranks 1234 .summon_does_roll_initiatives 1 .on_hit true .on_miss true .apply_once true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:109`
```darkest
effect: .name "Summon CC Party" .target "performer" .chance 100% .summon_count 3 .summon_can_spawn_loot true .summon_monsters sycophant_A sycophant_A sycophant_A .summon_chances 1.0 .summon_limits 3 .summon_ranks 432 .summon_does_roll_initiatives 1 .on_hit true .on_miss true .apply_once true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 用户补充：写 `1` 时召唤物在生成时获得 1 个行动点，行动顺序按速度结算；写 `0` 时生成时不获得行动点。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
