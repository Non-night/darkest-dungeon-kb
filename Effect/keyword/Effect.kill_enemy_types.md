# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.kill_enemy_types
# 分类
扩展/专项字段
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.kill_enemy_types <enemy_type>`：尝试处理该 Effect 的最终目标，但只对匹配指定 `enemy_type` 的目标生效。
- 该字段本身不提供群体目标，也不会自动扫描并处理目标群体；最终范围由同一 Effect 的 `.target` 和调用方目标决定。
- `.target target` 时只检查当前 Effect 目标；需要处理多个单位时，必须由 `.target target_group`、多次调用或其他已确认的目标映射提供多个最终目标。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 可用于 size-0 自灭；与最后一杀、击杀型 ActorDot 的时序需要一并考虑。
- 当前用户补充：在没有确认该 Effect 在当前调用环境失效或不适用时，size-0 善后默认优先使用匹配实际 enemy_type 的 `.kill_enemy_types`，不要默认改用 `.kill 1`。
- `kill_enemy_types` 不自带对群范围；它只作用于该 Effect 的最终目标，是否为群体由 `.target` 决定。
- 详见：[Mechanics/10-最后一杀与非直伤击杀.md](../../Mechanics/10-最后一杀与非直伤击杀.md)
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1944`
```darkest
effect: .name "clear_corpses" .target "target_group" .chance 100% .kill_enemy_types corpse .on_hit true .on_miss false .queue false .can_apply_on_death true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
