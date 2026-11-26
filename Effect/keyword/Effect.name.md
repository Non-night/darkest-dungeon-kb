# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.name
# 分类
核心流程
# 参数类型
字符串
# 参数约束
- 每条 Effect 定义都必须包含 `.name`，且名称必须非空。
- 不加引号时不得含空格或制表符。
- 除非当前用户专门要求，否则尽量不要在 `.name` 中使用空格，优先使用下划线。
- 建议使用简短、稳定的 ASCII 英文、数字与下划线 ID，并确保定义处与引用处完全一致。
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- Effect 的名称和内部标识；每条 Effect 定义都必须包含 `.name`，其他位置引用时必须与定义值完全一致。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
- 名称包含未加引号的空白。
- 名称超长，或引用处与定义处拼写不一致。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:57`
```darkest
effect: .name "Push 3D" .target "target" .push 3	.chance 130%	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:54`
```darkest
effect: .name "Push 3A" .target "target" .push 3 	.chance 100%	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:55`
```darkest
effect: .name "Push 3B" .target "target" .push 3 	.chance 110%	.on_hit true .on_miss false .can_apply_on_death true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
