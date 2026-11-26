# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.clearvirtue
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔 `0` 或 `1`。
- 只有参数为 `1` 时才清除目标的美德；参数为 `0` 时等同于未填写该关键字。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.clearvirtue 1`：清除当前 Effect 目标的美德。
- `.clearvirtue 0`：不产生清除效果。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版扫描未找到直接实例；下方案例来自 Mod，只能证明社区内容存在这种写法，仍需实机验证。
- 详见：[Mechanics/21-美德与压力机制.md](../../Mechanics/21-美德与压力机制.md)
- 清除美德后目标压力值保持不变；若压力高于 `100`，目标会暂时处于压力高于 100 但既无美德也无折磨的状态。
- 已有测试记录观察到：该状态下目标下次受压时压力会被复位到 `100`，随后重新判定美德/折磨；美德判定与折磨判定所使用的具体压力处理仍未完全确认。
- `.clearvirtue` 是否本质上等同于驱散美德源，尚未确认。
# 常见错误
- 将 `.clearvirtue 0` 当作会清除美德。
- 假定清除美德会自动把压力降为 `100` 或 `0`。
- 在未确认美德源驱散等价性的前提下，把 `.clearvirtue` 当作通用 Buff 源清除工具。
# 代码案例
- Mod「Exaelus' Arduous Edition Mod」：`effects\arduous_boss.effects.darkest:675`
```darkest
effect: .name "ARD_ORACLE_FINALCVIRT" .target "target" .chance 999% .clearvirtue 1 .on_hit true .on_miss false .queue true
```
- Mod「无夜的原版饰品重置」：`effects\Trinkets_Remake.effects.darkest:49`
```darkest
effect: .name "ARIA_BOX_clear_virtue" .target performer .chance 10% .clearvirtue 1 .on_hit true .on_miss true .apply_once true .queue true .has_description false
```
- Mod「The Abigail Williams Class」：`effects\AbigailWilliams.effects.darkest:1992`
```darkest
effect: .name "SAW_1st_reset_virtue" .target "target_group" .chance 10000% .clearvirtue 1 .on_hit true .on_miss true .has_description false .apply_once true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例回退：原版未找到该字段时，优先从 Workshop `262060` 选择 Mod 实例；Workshop 无实例时再从本地 `mods` 回退选择。
- 社区迂回测试记录：`暗黑地牢迂回代码整理2026-08-04-1833.docx`，`.clearvirtue` 专题（段落 5652-5657）。
- 用户补充的 `.clearvirtue` 参数与美德机制说明。
- 可信度原则：Mod 只确认该 Mod 如此书写；原版未提供直接实例，不能据此宣称为已验证的引擎规范。
