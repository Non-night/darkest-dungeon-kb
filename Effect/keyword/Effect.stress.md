# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.stress
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 参数为数值；本条已确认结论仅适用于施加正向压力伤害的 `.stress`。
- 每条 `.stress` 独立计算最终压力后四舍五入；无 Buff、无环境修正时，`.stress 0.5` 等效为 1 点压力。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.stress <amount>`：对最终受术者施加压力伤害。
- 压力施加量 `stress_dmg_percent` 与压力所受量 `stress_dmg_received_percent` 先加算为同一Buff乘区；原版最终系数限于全局规则的 20% 至 300%，再乘环境乘区（1＋亮度额外压力修正＋等级差额外压力修正），最后四舍五入。亮度与等级差先加算，不能分别乘算，详见机制52；第91/288条及全局规则第37行经当前用户2026-11-04确认，非新增实机测试。
# 作用范围
- `stress_dmg_percent` 仅在持有者为英雄时有效；不得推定怪物侧会按相同规则获得加压能力。
- 压力治疗、惊恐 DOT、心衰减压、负数 `.stress` 及 Fire's Edge DLC 新调用链不在本结论范围内。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 同一 queue false 层的压力 Popup 可以合并显示，但每条 `.stress` 仍独立结算与取整；不要用 Popup 总数替代逐段计算。
- 亮度系数以及压力 Buff 乘区的上下界来自全局规则；目标 Mod 修改过全局规则时必须读取实际值。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:554`
```darkest
effect: .name "beast_stress_1"	.target "performer" .chance 100% .stress 10 .on_hit true .on_miss false .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:555`
```darkest
effect: .name "beast_stress_2"	.target "performer" .chance 100% .stress 9  .on_hit true .on_miss false .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:556`
```darkest
effect: .name "beast_stress_3"	.target "performer" .chance 100% .stress 8  .on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 用户提供的压力计算与精准加压实测说明。
- Mechanics/52-压力伤害计算与精准加压.md。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
