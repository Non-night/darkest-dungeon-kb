# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.queue
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数使用 `true` 或 `false`；省略 `.queue` 时默认为 `false`。
- 下述前后时序主要描述技能流程。size-0 的 `spawn: .effects` 直接调用沿用召唤实际发生的时序，被引用 Effect 自身的 `.queue` 不参与分层。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- `.queue false`：技能的靠前常规时序，可近似理解为与技能动画同时发生。
- `.queue true`：技能的靠后时序，可近似理解为等待技能动画结束后发生。
# 作用范围
- 可区分技能 Effect、饰品 Trigger Effect 和暴击特效的靠前/靠后结算层。
- AWR 是攻击技能中位于普通 `queue false` 之前的独立子时序，详见 `.apply_with_result`。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.queue` 默认值为 `false`；false 通常与技能动画同时表现，true 通常在技能动画结束后表现。
- 攻击技能按 AWR、queue false、queue true 分层，并在每层内依次处理技能、饰品 Trigger、暴击特效。
- 技能 Effect 的依赖链必须先检查大时序，再检查同层书写顺序；较晚层的 Effect 即使写在列表前面，也不会早于较早层执行。
- 详见：[Mechanics/04-queue与AWR.md](../../Mechanics/04-queue与AWR.md)
- 攻击技能的常规顺序为：技能 AWR → 饰品 Trigger AWR → 暴击特效 AWR → 技能 queue false → 饰品 Trigger queue false → 暴击特效 queue false → 技能 queue true → 饰品 Trigger queue true → 暴击特效 queue true → 对应 ActorDot。暴击特效层仅在发生暴击时存在，ActorDot 层仅在单位携带对应类型 AD 时存在。
- 相同时序、相同来源中的多个 Effect，通常按调用位置的引用书写顺序生效。
- 大时序优先于引用书写顺序：只有处于同一大时序、同一来源的 Effect 才能通常按从左到右的严格顺序推理；列表中写在前面的 `queue true` 仍晚于写在后面的普通 `queue false`。
- 当前用户于2026-11-07转述外部来源作者无夜的攻击技能实测：同一目标的两个 Effect 都为 `queue true` 时，先眩晕后迷乱正常，先迷乱后眩晕会回合卡死；将迷乱改为 `queue false`、眩晕保持 `queue true` 时，本次直接技能 Effect 测试正常。
- 当前用户另报告：AWR 自附魔（Rule 为 `always`）引出的 `queue true` 眩晕，与技能 `queue false` 迷乱在目标原本没有 daze 时测试正常；目标已有 daze 时曾观察到随后回合卡死，正在复现，已有 daze 是否为必要条件以及该现象是否稳定均未确认。
- 存在“前置 Effect 建立状态／Buff／标记，后续 Effect 读取、消费或清除”的依赖链时，必须先验证两者的大时序，再检查同层书写顺序。例如眩晕在 `queue true`、依赖新眩晕的减闪避在 `queue false` 时，减闪避会先检查，不能读取本技能稍后施加的眩晕。
- AOE 会先按目标站位从前到后结算整个 AWR 层，再按相同目标顺序结算 queue false 层，最后结算 queue true 层；不会先把某一目标的全部时序一次结完。
- 上述动画描述不是精确帧级时钟，实际表现可能随技能动画长度变化；部分非技能调用位置没有可用的 queue 时序意义。
- queue false 中的减压、加压或真伤跳字各自会显示为同类 Effect 最终数值的合计；这只合并视觉 Popup，不合并各 Effect 的独立结算。
- 过抗类 Effect 的 Pop 当前仅观察到相同概率可能共用、不同概率可能分开；未确认其是否适用于所有 Pop 类型或时序。
# 常见错误
- 认为省略 `.queue` 会使用不确定时序；其默认值已确认为 `false`。
- 把 `queue false` 与 AWR 合并成同一个时序。
- 认为 AOE 会先完成第一个目标的 AWR、queue false、queue true，再处理第二个目标。
- 忽略技能、饰品 Trigger、暴击特效在同一时序层中的固定先后。
- 只按 `.effect` 列表的书写顺序安排依赖链，忽略 AWR、普通 `queue false`、`queue true` 等大时序会先重排实际执行顺序。
- 把依赖新状态的 Effect 放在较早时序层、把建立状态的 Effect 放在较晚时序层，并误以为交换文本位置即可让后者先执行。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:29`
```darkest
effect: .name "kill_self" .target "performer" .chance 100% .kill 1 .on_hit true .on_miss true .apply_once true .queue false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:33`
```darkest
effect: .name "kill_self_queued" .target "performer" .chance 100% .kill 1 .on_hit true .on_miss true .apply_once true .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:175`
```darkest
effect: .name "Stun 1" .target "target" .curio_result_type "negative" .chance 100% .stun 1	.on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 Effect 可确认 `.queue false`、`.queue true` 及省略 `.queue` 的实际写法。
- 技能、饰品 Trigger、暴击特效、AOE 与 ActorDot 的相对次序属于专项时序结论。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
