# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.protection_rating_add
# 分类
Buff/战斗属性
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 参数为单个数值；作为简写 Buff 使用时，应与 `.combat_stat_buff 1` 或其他已确认可建立 combat stat 简写 Buff 的字段配套。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.protection_rating_add <number>`：生成主类型为 `combat_stat_add`、副类型为 `protection_rating`、`amount` 等于所填参数的简写 Buff。
- `.protection_rating_add 1%` 对应游戏内固定增加 1 个百分点防御，不是把现有防御乘以 1%。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 由该 Effect 简写形式生成的 Buff ID 为空字符串。
- 该 Buff 属于 `combat_stat_*` 系，参与先加后乘：先结算 `combat_stat_add` 固定值，再基于加算结果结算 `combat_stat_multiply`。
# 常见错误
- 把 `.protection_rating_add 1%` 解释成按现有防御进行 1% 的倍率增长。
- 忽略 Effect 简写 Buff 的 ID 为空，进而在 ID 定向驱散中误用空字符串。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:989`
```darkest
effect: .name "Hound Debuff 1" .target "target" .curio_result_type "negative" .chance 130% .combat_stat_buff 1  .protection_rating_add -20% 	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:990`
```darkest
effect: .name "Hound Debuff 2" .target "target" .curio_result_type "negative" .chance 140% .combat_stat_buff 1  .protection_rating_add -22% 	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:991`
```darkest
effect: .name "Hound Debuff 3" .target "target" .curio_result_type "negative" .chance 150% .combat_stat_buff 1  .protection_rating_add -25% 	.on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
