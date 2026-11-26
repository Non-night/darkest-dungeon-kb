# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.refreshes_skill_uses
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
- `true of false`：刷新"每场战斗限制使用次数"技能的使用次数（比如破盾的蝰蛇之舞）
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 注意：即使此effect的chance为0，该设置项也依然生效，且执行此effect的当前技能不会被其刷新
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:302`
```darkest
effect: .name "spice_2"  .target "target" .curio_result_type "positive" .chance 100% .stress 40 .buff_ids "com_shard_dust_thirdhit_spd_buff"      "com_shard_dust_thirdhit_dmg_low_buff" "com_shard_dust_thirdhit_dmg_high_buff" "com_shard_dust_thirdhit_crit_buff" .on_hit true .on_miss false .queue true .refreshes_skill_uses true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:298`
```darkest
effect: .name "spice_0"  .target "target" .curio_result_type "positive" .chance 100% .stress 10 .buff_ids "com_shard_dust_firsthit_spd_buff"      "com_shard_dust_firsthit_dmg_low_buff" "com_shard_dust_firsthit_dmg_high_buff" "com_shard_dust_firsthit_resolve_check_debuff" "com_shard_dust_firsthit_stress_dmg_debuff" .on_hit true .on_miss false .queue true .refreshes_skill_uses true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:300`
```darkest
effect: .name "spice_1"  .target "target" .curio_result_type "positive" .chance 100%  .stress 20 .buff_ids "com_shard_dust_secondhit_dmg_low_buff" "com_shard_dust_secondhit_dmg_high_buff" "com_shard_dust_secondhit_spd_buff" "com_shard_dust_secondhit_resolve_check_debuff" "com_shard_dust_secondhit_stress_dmg_debuff" .on_hit true .on_miss false .queue true .refreshes_skill_uses true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
