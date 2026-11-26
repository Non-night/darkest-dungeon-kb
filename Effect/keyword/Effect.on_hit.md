# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.on_hit
# 分类
核心流程
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数必须为 `true` 或 `false`；省略时默认 `false`。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- `true`：攻击命中时允许该 Effect 触发。
- `false`：攻击命中时不因命中门触发该 Effect。
# 作用范围
- 主要用于攻击技能，以及同次攻击带出的饰品 Trigger 和附魔 Buff Effect。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 详见：[Mechanics/03-chance与抗性.md](../../Mechanics/03-chance与抗性.md)
- 友方技能不会被闪避，常规 Effect 通常把 `.on_hit` 与 `.on_miss` 都写为 `true`。
- spawn、actout、道具等没有普通攻击命中语义的调用位置不能只按攻击技能规则推理。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
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
