# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.individual_target_actor_rolls
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数必须为 `true` 或 `false`。
- 仅当 Effect 的 `.target` 为群体目标时有意义。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- `true`：按每个群体最终目标、每个 Effect 重新进行概率判定。
- `false` 或省略：保留普通群体 Effect 的既有共享结果模型。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版扫描未找到直接实例；代码案例来自 Mod，但下方行为来自已收录的专项资料或实测结论，不以 Mod 案例单独作为引擎结论。
- 详见：[Mechanics/02-target与群攻重复.md](../../Mechanics/02-target与群攻重复.md)
- `true` 不只分离不同最终目标；即使多个 Effect 最终作用于同一单位、写在同一行，也不能保证沿用普通技能的共享概率。
- Effect 指向单体目标时，即使调用方技能是 AOE，各技能目标本来就分别判断概率，本字段没有实际作用。
- 单体技能中 `target` 与 `performer` 的多个 Effect 仍是同一次目标概率的衍生产物，不能因最终 target 字段不同而断言独立。
- Fire's Edge DLC 新增调用链的概率行为未确认。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- Mod「Werewolf - New Class」：`effects\werewolf.effects.darkest:112`
```darkest
effect: .name "WW_Roar_Stress" .target performer_group .chance 20% .stress 4 .on_hit true .on_miss true .queue true .individual_target_actor_rolls true
```
- Mod「浊心斯卡蒂--Skadi the corrupting heart」：`effects\seaborn_newborn.effects.darkest:10`
```darkest
effect: .name "group stress +5 0.5" .target "target_group" .chance 50% .stress 5 .on_hit true .on_miss true .individual_target_actor_rolls true .queue true
```
- Mod「The Blackguard Class Mod」：`effects\bg_revenant.effects.darkest:12`
```darkest
effect: .name "revenant_whispers_stress_1" .target "target"  .chance 66% .stress 10 .on_hit true .on_miss false	.queue true .individual_target_actor_rolls true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例回退：原版未找到该字段时，优先从 Workshop `262060` 选择 Mod 实例；Workshop 无实例时再从本地 `mods` 回退选择。
- 可信度原则：Mod 案例只证明该 Mod 如此书写；已由专项资料或实测记录明确的行为结论可直接作为创作依据，未确认边界仍按未知处理。
