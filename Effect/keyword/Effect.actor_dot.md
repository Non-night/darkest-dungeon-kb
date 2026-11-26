# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.actor_dot
# 分类
扩展/专项字段
# 参数类型
单个字符串（可加引号或不加引号）
# 参数约束
- 仅接受一个参数，参数类型为字符串；带引号与不带引号的字符串均可。
- 参数必须与某个 ActorDot 定义的 `id` 完全一致。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.actor_dot <ad_id>`：给 effect 的最终目标施加 ActorDot（简称 AD 或 ADot）；参数是所引用 ActorDot 的 `id`。
# 作用范围
- 用于 Effect 定义行，ActorDot 施加给该 effect 的最终目标。
- 本字段只负责引用并施加 ActorDot；定义格式、阶段规则与动画素材要求属于 ActorDot 机制。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- ActorDot 按触发事件推进，不按普通持续回合推进；触发晚于饰品 Trigger 的 queue true。
- 施术者须留场且在自身 fx 提供有效素材；release须非单帧，龙骨转换结果还须非静态。原生Spine静态非单帧release可用，其余三段特殊要求未确认。具体制作来源、版本及历史实测见ActorDot专题。
- 详见：[Mechanics/06-ActorDot.md](../../Mechanics/06-ActorDot.md)
- 引用不存在的 ActorDot ID 时，该 effect 生效时只产生红字报错，不会给目标留下无效 ActorDot，也不会引起黑屏报错、游戏闪退或卡死。
- 报错术语见：[Mechanics/12-报错类型与日志.md](../../Mechanics/12-报错类型与日志.md)。
# 常见错误
- `.actor_dot` 后填写多个参数。
- 引用 ID 与 ActorDot 定义中的 `id` 不一致或尚未定义。
- 只编写引用 Effect，却未按 ActorDot 机制文档完成定义、最后阶段和施术者动画素材。
- 让可能死亡、被传送或快速消失的单位施加持续存在的 ActorDot，导致触发时施术者不在场。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:540`
```darkest
effect: .name test_egg_1 					.target target .chance 100% .actor_dot egg .on_hit true .on_miss true .queue true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:397`
```darkest
effect: .name "Parasite Egg Inject" .target target .chance 100% .actor_dot egg .on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Effect 引用案例：官方 DLC `580100_crimson_court` 的 `crimson_court.effects.darkest`。
- ActorDot 结构与安全规则集中收录于 `Mechanics/06-ActorDot.md`。
- 实机结论：引用不存在的 ActorDot ID 只产生红字报错，不会生成无效 ActorDot，也不会导致黑屏、闪退或卡死。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
