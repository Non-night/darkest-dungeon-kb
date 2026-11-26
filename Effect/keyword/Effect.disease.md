# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.disease
# 分类
扩展/专项字段
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `any
disease ID`：any 随机赋予疾病
- 可以指定获得某个疾病，比如猩红诅咒
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 疾病施加 Effect 显式强制过疾病抗性时，是否改变疾病施加原有的概率计算仍未确认。
- 已确认行为：知识库编写者于 2026-10-21 明确确认，单靠堆高疾病抗性无法完全免疫通过 Effect 施加的疾病。此项为独立确认结论，不依赖下述公式是否成立；不据此确认具体概率下限，也不外推到其他疾病来源。
- 知识库编写者 2026-10-21 转述未确认公式：P=(1-clamp(疾病抗性,0,95%))*clamp(.chance,0,100%)+暴击时20个百分点。公式精确性、暴击相加位置、暴击控制字段交互及最终值超过100%的处理均未确认。
- 仅按该公式推导：降低疾病抗性至≤0不足以单独保证染病；非暴击时还需有效.chance=100%及实际进入施加判定。具体概率下限仍未确认；100%基础概率下非暴击最低5%，暴击按该公式为25%。不得当作确定性实现依据。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:208`
```darkest
effect: .name "Disease" .target "target" .curio_result_type "negative" .chance 33% .disease any	.on_hit true .on_miss false .crit_doesnt_apply_to_roll true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:179`
```darkest
effect: .name "Thing Disease 1" .target target .chance 20% .disease sky_taint .on_hit true .on_miss false
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:479`
```darkest
effect: .name vampire .target target .chance 100% .disease disease_vampire_passive .on_hit true .on_miss true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 知识库编写者于2026-10-21转述，明确不确定公式精确性及超过100%的行为。
- 知识库编写者于2026-10-21独立确认：高疾病抗性无法完全免疫 Effect 疾病施加；未宣称本次提供新的实测过程。
- Sources/forced_disease_resist_probability_20261119.json
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
