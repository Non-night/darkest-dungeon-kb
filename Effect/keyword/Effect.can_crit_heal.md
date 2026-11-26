# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.can_crit_heal
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数必须为 `true` 或 `false`。
- 只影响同一逻辑 Effect 中的 `.heal` 和 `.heal_percent`。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- `true`：允许同一逻辑 Effect 的 `.heal` 或 `.heal_percent` 治疗暴击。
- `false`：禁止这些治疗暴击。
# 作用范围
- 同一逻辑 Effect 包括同一 Header 内换行，以及不同 Header 的同名 `.name` 分行；跨 Mod 的同名 Effect 文件仍参与叠加。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 详见：[Mechanics/27-治疗源与真吸血.md](../../Mechanics/27-治疗源与真吸血.md)
- 本字段只控制是否允许治疗暴击；具体固定暴击率由治疗源决定。
- 同一逻辑 Effect 不包含 `.heal` 或 `.heal_percent` 时，本字段没有对应治疗可控制。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:502`
```darkest
effect: .name "CrocHeal 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 12 .can_crit_heal false .on_hit true .on_miss true .queue true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\additional.color_of_madness.effects.darkest:26`
```darkest
effect: .name "COM CrocHeal 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 12 .can_crit_heal false .on_hit true .on_miss true .queue true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:503`
```darkest
effect: .name "CrocHeal 2" .target "performer" .curio_result_type "positive" .chance 100% .heal 15 .can_crit_heal false .on_hit true .on_miss true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
