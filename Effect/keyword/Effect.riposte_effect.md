# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.riposte_effect
# 分类
反击
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 一个反击 Buff 只能有一个副类型；同一条／同名逻辑 Effect 中不能靠多个 `.riposte_effect` 构造多个附带 Effect。
- 多参数形式的现有测试记录为只有第一个参数生效。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- 指定 `.riposte 1` 所生成反击 Buff 的副类型；反击触发时调用对应名称的 Effect。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 指定反击 Buff 的副类型；不同 Effect 生成的多个反击 Buff 可以在反击时分别触发各自的附带 Effect。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- 不同 Effect 分别生成的多个反击 Buff 可以共存；它们的不同 `.riposte_effect` 会在反击发生时全部触发，不会互相冲突。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:19`
```darkest
effect: .name "Riposte Example"  .target "performer" .curio_result_type "positive" .chance 100% .riposte 1 .riposte_on_hit_chance_add 100% .riposte_on_miss_chance_add 100% .on_hit true .on_miss true .duration 2 .damage_low_add 0.01 .damage_high_add 0.01 .attack_rating_add 0.01 .crit_chance_add 5% .riposte_effect "Wyrd Bleed 5"
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
