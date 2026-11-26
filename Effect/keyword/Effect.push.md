# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.push
# 分类
扩展/专项字段
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 参数为数值；可按已知实例使用整数、小数或带 `%` 的数值形式，但实际位移格数的非整数边界行为尚未确认。
- 有效击退 Effect 通常同时写 `.can_apply_on_death true`，以避免相关红字报错。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.push <number>`：对目标施加击退，数值表示击退格数。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 击退在 AWR 与 `queue false` 按严格书写顺序判定是否理论成功，但实际位移暂存；同层多个理论成功的推拉只有最后一个实际生效。
- `queue true` 的击退位于该层末尾且会红字报错；不得作为安全常规写法。
- 同层定身总先于击退；定身阻止击退会错误击退目标后方相邻单位。
- 详见：[Mechanics/04-queue与AWR.md](../../Mechanics/04-queue与AWR.md)
- 在 AWR 和 `queue false` 中，理论成功判定遵循严格书写顺序；实际位移暂存到 `queue false` 结束、`queue true` 开始前。
- 同一时序中多个理论成功的推拉只有严格书写顺序最后一个实际生效；被抵抗的推拉不占候选。
- `queue true` 中位于该层末尾，且写法会产生红字报错；不要作为安全常规实现。
- 与 `.immobilize` 同层时定身先于击退；定身阻止击退会错误击退目标向后相邻的有效单位。
- 详见：[queue、AWR 与暴击特效时序](../../Mechanics/04-queue与AWR.md)。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:57`
```darkest
effect: .name "Push 3D" .target "target" .push 3	.chance 130%	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:59`
```darkest
effect: .name "Push 3F" .target "target" .push 3	.chance 150%	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:54`
```darkest
effect: .name "Push 3A" .target "target" .push 3 	.chance 100%	.on_hit true .on_miss false .can_apply_on_death true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
