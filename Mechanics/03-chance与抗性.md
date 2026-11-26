# chance、抗性与攻击命中门

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 新版强制过抗：指定类型替代原判定

知识库编写者2026-11-05实测确认：无论Effect原本是否需要过抗，.force_resist_type均改用指定类型对应的施术者施加率和受术者抗性；替代原判定，不是追加第二次过抗。指定poison时仅看腐蚀施加率与腐蚀抗性，减益施加率与减益抗性完全不参与。该明确结论也覆盖原本按同侧处理、不经过减益抗性的效果；不再保留原先的两个选择疑问。

文档例子也允许自身力竭改为检查自身眩晕抗性。

### 社区实测原样记录

```darkest
effect: .name lp_test_debuff .target target .chance -1 .force_resist_type poison .buff_type hp_heal_amount .buff_amount 1 .on_hit true .on_miss true
```

该示例只使用施术者腐蚀施加率和目标腐蚀抗性，与减益施加率、减益抗性无关。原样记录用于追溯此次测试，不是具有完整调用方和资源的独立Mod。

完整resist_id值域、同行含多种效果时的具体作用粒度仍未确认；本次示例中的.chance -1原样保留，不据此补造一般概率公式或取值边界。

来源：新版文档B031–B032；知识库编写者2026-11-05明确报告实测；Sources/modding_update_20261105_effects.json。Agent未自行运行游戏测试。

## 强制过疾病抗性时的治疗、疾病与怪癖施加

知识库编写者确认，治疗 Effect 强制过疾病抗性时，按治疗判定概率减去目标疾病抗性计算成功率。180% 的治疗判定概率对 80% 疾病抗性，180% − 80% = 100%，进入该判定的治疗必定通过。

- 疾病施加 Effect 显式强制过疾病抗性时，是否改变疾病施加原有的概率计算仍未确认。
- 施加怪癖强制过疾病抗性时，最终成功率的计算方式仍未确认。

治疗的减算结论限于此治疗路径。来源见 `Sources/forced_disease_resist_probability_20261119.json`。

## 新版 Effect 型扰乱的位移施加率（2026-11-05采纳）

Effect 型延迟扰乱（Stumble）`.dotShuffle` 现在受到施术者位移施加率（Move Chance／`move_chance`）加成；目标位移抗性的既有判定保留。旧版“不计算施术者位移施加率”已被新版替代，不再用于当前创作。

此更新仅明确 Effect 型 `.dotShuffle`，不改写 Buff 型 `shuffle_dot` 的减益施加率／抗性路径；完整概率公式、上限及特殊目标例外未由新版文档补充。原数字布尔参数与 DOT 配套要求继续按现有词条核对。

证据：新版功能文档 B023–B024及 Sources/modding_update_20261105_effects.json；当前用户2026-11-05要求采纳，文档优先；未新增实机测试。旧迂回表第80条 P1342–P1344/X1596–X1599为旧版行为依据。

## 英雄侧仅战斗内成立的 Rule 组合

英雄侧仅战斗内成立的条件组合：`rule_type: "monster_type_count_min"`，`rule_data.float: 1`，`rule_data.string: ""`，`is_false_rule: true`。在原表所述常规有怪物且空类型无匹配的战斗场景中成立；脱战后缺少检测对象，返回 `null`，取反也不激活。该结论不推广到怪物持有者，也不保证战斗中已无怪物等特殊窗口的表现。这里的空字符串用于怪物类型匹配，不是技能 ID、职业 ID 或怪物名称本地化。战斗外两 Buff 抵消方案和读档移除风险须按各自完整边界另核，不能由本项自动保证。证据：迂回表第33条 P888/X1038、P891/X1041–P893/X1043，当前用户于2026-11-03确认按此边界补入；非本轮新增实机测试。

## 英雄侧仅战斗外净效果的两 Buff 组合

英雄侧仅战斗外净效果的两 Buff 组合：一条 `always` Buff 常驻提供数值，另一条采用已确认的仅战斗内条件（`monster_type_count_min`，数量1、空类型字符串、取反）提供等量反向数值。两条 Buff 均存在，且该属性与结算方式确能精确抵消时，战斗内净效果为0，战斗外保留常驻效果。这是两条 Buff 的净值组合，不是新增的战斗外 Rule，也不推广为任意属性均可相抵；战斗内条件的英雄侧、常规有怪物且空类型无匹配等边界仍适用。读档导致组合成员消失的风险须另按 P898 核对，不由净值关系保证生命周期稳定。证据：迂回表第33条 P895/X1046–P897/X1048，当前用户于2026-11-03确认按此边界补入；非本轮新增实机测试。

## 战斗内外组合的读档边界

指定 Rule 的读档／重启移除：`monster_type_count_min` Buff 写 `remove_if_not_active: true` 时，读档会使其消失，即使场上仍满足条件；原表也明确类比 `has_quirk` 配置该字段为 `true` 时的重启消失现象。用于两 Buff 抵消时，若抵消项消失而 `always` 项保留，组合净效果会被破坏。本项仅覆盖上述指定 Rule 与 `true` 配置，不推广到全部 Rule，也不据此保证 `false` 配置永不消失；不把它解释为持续时间正常到期。证据：迂回表第33条 P898/X1050，当前用户于2026-11-03确认按此边界补入；非本轮新增实机测试。

## 标志物用途与机制性质

“标志物”是用途而非性质：所有标志物都保留其原有机制性质，不能因称作标志物而获得额外的隔离、免疫、无副作用或专用判定规则。减益概率标志物本质上仍是减益概率，在相同条件下与常规用途的减益概率遵循完全一致的机制；其他标志物同理，须按实际字段、属性、来源、目标、时序与生命周期判断。本原则不补造任何具体属性尚未确认的行为；例如 skill Rule 响应期内增伤、减伤等非概率属性的同类影响仍未知。依据：当前用户于2026-11-03主动补充的通用原则，非本轮新增实机测试。

## 英雄Info抗性成长、死抗与疾病抗性上下界
知识库编写者于2026-10-28明确修正英雄Info `resistances:` 的等级成长与有效边界。此项为知识库编写者确认，不冒称新增实机测试或反编译证据。

| 英雄抗性 | 决心等级成长 | 有效范围 |
|---|---|---|
| 除死亡抗性、疾病抗性外的其他抗性，包括眩晕、位移、腐蚀、流血、减益、陷阱 | 每级增加10个百分点；6级比0级增加60个百分点 | 0%～500% |
| 死亡抗性 `.death_blow` | 不适用上述每级+10个百分点成长 | 0%～87% |
| 疾病抗性 `.disease` | 不适用上述每级+10个百分点成长 | 0%～95% |

Info抗性数值按0决心等级基础值理解；“+10%”在此指增加10个百分点，不是原数值乘1.1。等级成长与有效上下界是不同规则；有效边界不等于文件语法只能写该范围。本次修正限英雄，不自动外推怪物、技能的同名字段或所有原始数值的截断时点。陷阱已有的修正后截断规则保留。

疾病抗性0%～95%的边界独立确认为已知事实；这不确认疾病Effect的完整施加率公式、其中 `.chance` 的截取、暴击相加位置、暴击控制字段交互或最终概率超过100%的处理。此前高抗性不能完全免疫疾病的独立确认继续有效。

## `.chance` 的数值范围
- `.chance` 是当前 Effect 的基础生效概率，可写整数、小数或带 `%` 的数字。
- 未另行限制时，其数值边界按 float 可表示范围处理；不要擅自限制为 `0～100%` 或 `0～1`。
- 极端正值可用于保证成功，极端负值可用于保证失败；超出 float 范围仍可能出错。

负向基础概率不能直接等同于“必定失败”。对会叠加施术者施加率或其他外部正向修正的减益类 Effect，最终判定仍取决于基础 `.chance` 与这些修正的合计：只有外部正向修正不足以填平负基础值、使最终值仍低于 `0` 时，才表现为必定失败；若正向修正足以填平负值，Effect 仍可能成功。没有明确该 Effect 是否接受对应外部修正时，不得仅凭负数写法推断它是稳定条件门。

## Buff 的同侧、异侧与减益抗性
这里的“同侧/异侧”主要用于说明 **Buff 型效果** 是否进行目标减益抗性判定。统一规则及已确认的特殊目标清单见[Buff 同侧、异侧与减益概率判定](95-Buff同侧异侧与减益概率判定.md)；同侧不计算减益施加率和减益抗性。

- 英雄给怪物施加 Buff 时，无论该 Buff 的数值或显示被视为增益还是减益，都要判定怪物的减益抗性。
- 例：`.chance 50%`，目标减益抗性为 `10%`，且没有其他概率修正时，最终成功率为 `40%`。
- 部分特殊 `.target` 参数会使 Buff 施加过程不再判定目标减益抗性，社区称为“视为同侧”。当前没有在本页枚举所有此类 target；必须查 `.target` 精确词条和对应机制，不能根据目标名称猜测。
- 减益抗性的有效范围为 `0～500%`。

流血、腐蚀、眩晕、位移等具有自身施加率和抗性的 Effect，不因“同侧”而免除对应抗性判定，因此这类效果通常不使用同侧/异侧来解释。

## 施加率 Buff 与条件概率门
只有具有对应施加率 Buff 的 Effect，才能用“极端 `.chance` + 极端施加率修正”构造条件门。例如流血概率 Buff 只能修正流血 Effect 的施加率，不能任意控制所有刚性 Effect。

若只希望由条件 Buff 决定“必定成功/必定失败”，而不希望目标最高 `500%` 抗性干扰，条件计算后的概率通常应：

- 高于 `600%`：保证越过最高抗性后仍成功。
- 低于 `0%`：保证失败。

精确数值仍要同时考虑基础 `.chance`、施术者对应施加率 Buff、目标抗性及其他同类修正。

## size-0 概率门的过抗余量必查项

知识库编写者补充（2026-09-20）：只要 size-0 概率门使用的内容理论上会进入跨侧减益抗性／施加率计算，且设计没有要求保留真实的“过抗概率”差异，就不能只看名义上的 `+N`／`-N`，必须核对**最终施加率**的余量：

- 普通 Buff：应该成功的分支，最终施加率不得低于 `+1000%`；应该失败的分支，最终施加率不得高于 `-1000%`。
- 流血、腐蚀、眩晕：这三类带自身施加率和抗性的内容也必须按同样的 `+1000%`／`-1000%` 余量检查；不能因为它们不是普通 Buff 就省略过抗核对。
- 如果用治愈流血、治愈腐蚀或治愈燃烧构建概率门，应该成功的分支最终成功率不得低于 `+100%`，应该失败的分支最终成功率不得高于 `0%`。

这里的“最终”是把基础 `.chance`、对应施加率 Buff、目标抗性、同类修正和调用方目标语义全部合并后的结果，不是某一条 Buff 的单独 `amount`。若设计明确要求保留实际过抗概率、观察抗性差异或让失败分支仍有可见概率，则不套用这条“逻辑门安全余量”要求，但必须把该设计意图写清楚并单独复核。

这条是 size-0 逻辑门的必查项，与 `+40000/-40000` 等极大门控数值不是同一个层次：极大数值只是输入，`+1000%/-1000%` 是最终合计结果的最低余量。若最终合计达不到边界，不能声称该门已经抗跨侧过抗。

## 概率门 Buff 数值的最低幅度

知识库编写者补充（2026-09-20）：凡是用于构建概率门的 Buff，其门控数值本身也有硬性最低幅度，无论它是否最终用于跨侧目标：

- 正向开启门的 Buff 数值不得低于 `+1000%`；
- 负向关闭门或基准负门的 Buff 数值不得高于 `-1000%`。

这里检查的是门控 Buff 自己写入的数值，不是把多个常规 Buff 相加后的最终结果。使用 `+50%`、`-50%`、`+200%` 等较小门控值，即使在当前测试队伍里看起来能区分真假，也可能被其他同类常规 Buff 抵消、推高或翻转，从而破坏概率门。构建概率门时应直接采用至少 `+1000%`／至多 `-1000%` 的门控 Buff，再单独检查最终施加率、目标抗性和调用方语义。

这条要求只针对承担概率门功能的 Buff；普通战斗 Buff、设计上刻意保留真实概率的 Buff，以及治愈流血/腐蚀/燃烧的特殊概率门下限，仍分别按本页前述规则处理。不要把 `+1000%/-1000%` 误写成所有 Buff 或所有 Effect 的通用数值公式。

## `actor_base_class` Rule 自身匹配时的永不生效边界

当前用户补充（2026-09-25）：如果 Buff 的 `rule_type` 为 `actor_base_class`，且 `rule_data.string` 等于该 Buff 持有者自身的职业 ID 或怪物大类 ID，则该 Buff 可以视为永不生效。例如英雄职业 ID 为 `AAA`，其持有的 Buff 使用 `actor_base_class`，且 `rule_data.string` 为 `AAA`，则该 Buff 可以视为不存在。

该结论只适用于“Rule 检查的实际作用目标就是 Buff 持有者自身”的情况；`actor_base_class` 是进攻型/施术型 Rule，若 Buff 持有者释放的 Effect 实际作用于其他单位，则必须按实际 Effect 目标重新判定，不能仅凭持有者 ID 相同就断言 Buff 永不生效。群体目标、饰品 Trigger、spawn、生命反馈和其他非技能调用同样要按最终受术者逐项核对。

## 多个同类概率门 Buff 的相互干扰

当前用户补充（2026-09-24）：如果有两个概率门使用同一种 Buff 类型，且其中一个概率门的 Rule 不是 `monsterType` 或 `actor_base_class`，就必须警惕它们相互干扰的可能性。

检查使用极大或负极大 Buff 构建概率门的写法时，不能只看每个门自己的 `amount` 是否达到 `+1000%`／`-1000%`，还必须把所有同类 `stat_type` Buff 之间可能发生的相互加算、抵消、推高或翻转纳入检查。具体要核对两个概率门的 Rule、施加对象、持有者、生命周期、清理顺序以及探测 Effect 的实际调用方，确认某个概率门不会被另一个同类 Buff 改变。

这里的 `monsterType`／`actor_base_class` 条件只是本条“必须特别警惕”的边界条件，不是对其他组合自动证明不存在干扰；未明确隔离前，不得把极大数值当作可以免检的安全保证。

## 直接条件无法执行时：size-0 + Rule + 极大概率 Buff 逻辑门

当一个判断不能由当前 Effect 的目标、当前技能的合法目标集合或单条 Rule 直接完成时，应主动检查是否适合使用 **size-0 载体 + Rule 条件 Buff + 极大正负概率修正** 构造逻辑门。这里的“逻辑门”是把条件真假转换成某个探测 Effect 的“必定进入／必定不进入”，再由 size-0 的生命反馈或其他 relay 把结果传回主流程；它不是把任意 Rule 变成通用的执行开关。

### 什么时候优先考虑这条路径

出现下列任一信号时，Agent 应先检索本节和 [Size-0 召唤物](05-size0召唤物.md)，不要直接堆叠更多未经核对的目标字段：

- 条件涉及另一个单位的体型、站位、模式、类型或跨侧队伍组成，而当前 Effect 只能拿到原始技能目标；
- `target_enemy_rank` 只能检测已选中的目标，不能读取所需的其他站位；
- Rule 能判定条件，但没有直接的“若 Rule 成立就执行后续 Effect”语法；
- 需要在后续推拉、召唤、set、模式切换或其他分支前先得到一个稳定的真假结果；
- 直接使用 `.target`、`target_group` 或跨侧筛选会扩大目标范围，无法满足目标最小化要求。

### 通用结构

```text
size0Spawner 生成中间载体
→ 在载体或正确的施术者侧安装始终存在的基准概率 Buff
→ 安装带 Rule 的极大正向或负向概率 Buff
→ 执行一个使用同一概率 stat_type 的探测 Effect
→ 探测成功/失败编码为 size-0 生命变化、relay Buff 或后续分支
→ 清除本阶段基准 Buff、Rule Buff、探测 Buff 和 relay 状态
```

最常见的布尔门是：

```text
基准：始终生效的 -N 概率修正
条件为真：Rule 成立时再加 +N 或更大的正向修正 → 打开探测 Effect
条件为假：Rule Buff 不生效，仍保留负基准 → 关闭探测 Effect
```

反向分支可以把正负基准互换，或使用 `is_false_rule`；不要把两个临时 Buff 的正负相抵误当成已经完成清理。每个阶段都应有明确的 ID、调用来源和二段驱散/清理顺序。`+40000`、`-40000` 是已收录推拉与跨侧筛选案例中的强门数值，不是所有概率系统的通用常量；实际数值必须按目标抗性、施术者施加率、其他同类 Buff 和最终概率上下限复核。

### 多条件不是同一 Buff 的多 Rule

Buff 每个定义只有一个 Rule；需要多个条件时，改用多个 Buff、ID 定向驱散、条件清理或其他已确认的组合机制，并分别核对时序和残留。不能把多个条件直接写成同一个 Buff 的两套 Rule。

### 必须先核对的概率类型与目标

- 只能修正与探测 Effect 匹配的概率 stat_type。例如 `debuff_chance` 只控制减益类 Effect，`move_chance` 只控制位移类 Effect；不能用任意 `chance` Buff 代替对应施加率。
- Rule Buff 的持有者、被检查目标和探测 Effect 的最终目标必须分开核对。进攻型/施术型 Rule 通常由施术者身上的 Buff 检查本次操作目标；跨侧筛选需要另查 `target_group`、反向 Effect 和实际目标映射。
- 目标抗性或施加率会参与最终概率时，正负极大值只是在当前已知范围内留下足够余量，不代表绝对数学无限大；遇到不同 stat_type、特殊 target、不同调用来源或未确认的抗性链，必须标记边界。
- 不能把 `.keyStatus`、`.skill_instant true` 或 `.monsterType` 与 `target`/`target_enemy_group` 组合来做这条逻辑门；它们有独立的崩溃和临时 Buff 限制。

### 与 size0Spawner 的衔接

如果逻辑门结果要由生命反馈回传，载体必须遵循 [size0Spawner 默认模板](05-size0召唤物.md)：小初始最大生命、百分比扩展、回满、第二次扩展不回血，以及方向 sentinel。死而不僵目标上的召唤或 set 通常会被阻断；只有对应 Effect 同时显式写 `.can_apply_on_death true .can_apply_on_corpse true` 才能突破。需要的中间对象和变身应优先在自灭前完成；若依赖双字段例外，须同时核对 set 的 HP 继承/重置结果。逻辑门只解决“条件真假如何传递”，不改变 size-0 的时序、死亡、碰撞箱或清理边界。

这是一种**条件性通用设计模式**，不是任何 Rule、任何 Effect 或任何调用来源都已经实测可复用的万能开关。先用直接 Rule 能完成的最小写法；只有直接路径缺少目标、时序或分支能力时，才引入 size-0 逻辑门。引入后先尝试让一个 size-0 同时承担探测、生命反馈和 relay；只有单个载体无法满足并发状态或时序隔离时，才增加第二个 size-0。

## `.on_hit` 与 `.on_miss`
- 两者主要在攻击技能中决定 Effect 是否进入结算；同次攻击带出的饰品 Trigger 和附魔 Buff Effect 也使用本次攻击的命中/未命中结果。
- `.on_hit true`：攻击命中时允许该 Effect 触发。
- `.on_miss true`：攻击未命中时允许该 Effect 触发。
- 友方技能不会被闪避，因此通常显式写为双 true，使 Effect 正常执行。
- 当前观察认为友方技能中的双 false 会使 Effect 不触发；不要把双 false 用作友方技能的常规 Effect。
- `.on_hit`、`.on_miss` 省略时默认均为 `false`。

在 actout、道具 Effect、spawn Effect 等没有攻击命中语义的调用位置，这两个字段可能没有普通攻击技能中的限制作用；必须结合调用方机制判断。

## `.keyStatus`、`.skill_instant` 与 `.monsterType` 的特殊概率
包含以下条件字段的 Effect 具有特殊 `.chance` 行为：

- `.keyStatus <status>`
- `.skill_instant true`
- `.monsterType <monster_type>`

已知规则：

- `.chance` 低于 `100%` 时会产生红字，同时概率会被强制视为 `100%`。
- `.chance` 高于 `100%` 时会进入无动画翻页迂回的特殊行为。
- 除非明确设计无动画翻页，不允许让包含上述有效字段的 Effect 使用高于 `100%` 的 `.chance`；常规写法使用 `100%`。

## `.keyStatus`、`.skill_instant`、`.monsterType` 的致命目标组合
同一条 Effect 只要满足以下任一条件：

- 存在有效 `.keyStatus <status>`；
- 写有 `.skill_instant true`；
- 存在有效 `.monsterType <monster_type>`；

则其 `.target` **绝对不得**写为以下任一值：

- `target`
- `target_enemy_group`

上述任一条件字段与任一致命目标值组合时，游戏必定立即崩溃。这不是红字、无效 Effect 或概率失败，不能作为可容忍写法。

既有资料还把 `target_group`、`target_group_other` 列为 `.skill_instant true` 的不安全目标；在其准确崩溃边界得到进一步确认前，同样禁止这样组合。

## 疾病 Effect 的施加率、疾病抗性与必定获得疾病：未确认信息
已确认行为：知识库编写者于 2026-10-21 明确确认，单靠堆高疾病抗性无法完全免疫通过 Effect 施加的疾病。此项为独立确认结论，不依赖下述公式是否成立；不据此确认具体概率下限，也不外推到其他疾病来源。

疾病施加 Effect 显式强制过疾病抗性时，是否改变疾病施加原有的概率计算仍未确认。 前文的治疗算例仅说明治疗判定。

未确认公式：知识库编写者同日转述以下信息，并明确不确定公式是否精准，也不确定最终值大于 100% 时如何处理。公式证据等级为社区参考／未确认，不是已验证引擎算法。

仅针对通过 Effect 获得疾病，所获信息为：
`P = (1 - clamp(疾病抗性, 0, 95%)) × clamp(Effect .chance, 0, 100%) + C`，其中暴击时 `C = 20 个百分点`，非暴击时为 `0`。
- 英雄疾病抗性有效边界0～95%已由知识库编写者于2026-10-28独立确认，不再随公式列为未知；疾病计算中 `.chance` 0～100% 的截取规则仍未确认。此边界确认不证明完整公式或其内部截取时点；不改变 `.chance` 字段允许负值或超过100%的通用语法事实。
- 暴击加成在乘算后的相加位置尚未验证；与 `.crit_doesnt_apply_to_roll`、全局暴击概率修正的具体交互也未由本次信息确认，不得绕过既有暴击控制规则作无条件承诺。
- 最终值超过 100% 的处理未知；不得自行补写钳制、溢出或必定成功行为。

以下仅为上述公式成立时的条件推论，不是新增实测结论：
- 若想在指定时机必定获得疾病，可考虑先大幅降低疾病抗性，使最终抗性 ≤0；但这还需要疾病 Effect 实际进入施加判定，且非暴击时有效 `.chance` 达到 100%。仅降低抗性不足以单独保证染病；施加前置状态还须核对实际执行时序。
- 非暴击且有效 `.chance = 100%` 时，按公式最低仍为 5%；暴击且乘算后加 20 个百分点时，同条件为 25%。这两个数值仍为未确认公式的条件推论；高抗性无法完全免疫的独立确认不证明这些数值。不能把“高疾病抗性时概率较低”无条件推广到暴击或其他调用来源。
- 不外推到奇物、扎营、事件等非本次范围的疾病来源；在精确公式确认前，不将这套推论作为稳定条件门或确定性染病方案。

## 暴击对 Effect 概率的影响
攻击技能暴击时：

- `.crit_doesnt_apply_to_roll true`：当前 Effect 的 `.chance` 不获得暴击概率加成。
- 省略该字段或写 `false`：当前 Effect 的 `.chance` 增加 `20%`。
- 该 `20%` 由全局规则决定，若全局规则被修改，应以实际全局值为准。
- DOT 在攻击暴击时还存在额外变化；该额外效果的具体内容，以及是否同样受 `.crit_doesnt_apply_to_roll` 控制，当前尚未确认。

## Effect 概率骰子共享与隔离
同一次常规技能内的 Effect、技能与多数进攻向饰品 Trigger 存在已测试的概率骰子共享；低概率成功时较高概率也成功，相同概率则同时成功。命中／闪避骰子与 Effect 概率骰子独立，ActorDot、受击／反击、击杀 Trigger、虚拟道具等调用边界另有已确认的隔离规则。

这不是“任何同一时序必定共享”的规则：`.individual_target_actor_rolls true`、不同单位、不同 ActorDot、受击 Trigger 等均会改变边界。完整的已测范围、推测和 Fire's Edge DLC 新内容的未确认边界见 [Effect 概率骰子共享与隔离](51-Effect概率骰子共享与隔离.md)。

## Effect 型标记强制过减益抗性

知识库编写者2026-11-06明确补充：对 Effect 型标记声明强制过减益抗性，可以使其像 Buff 型标记一样经过减益施加率与减益抗性判定，同时仍受“无法被标记”干涉。Buff 型标记不受“无法被标记”干涉；需要同时满足过减益抗性和可被阻止标记两项设计要求时，可以采用该 Effect 型写法。来源：`Sources/effect_mark_forced_debuff_resist_20261106.json`；Agent未自行运行游戏测试。

## 守护与清除守护的通常概率豁免及强制过抗例外
未声明 `.force_resist_type` 时，以下字段在参数为 `1` 时会无视 `.chance`，也不受指定 Effect 的 `effect_chance` 制约：

- `.guard 1`：建立守护。
- `.clearguarded 1`：清除目标的被守护状态。
- `.clearguarding 1`：清除目标作为守护者提供的守护。

知识库编写者于2026-11-05补充：若对该 Effect 声明 `.force_resist_type`，守护及清除守护即可受强制类型对应的施加率以及 `effect_chance` 制约；指定类型的目标抗性按本页强制过抗规则处理。不能将通常情况下的概率豁免推广到强制过抗情形。来源：`Sources/guard_start_triggers_20261105.json`。

如果需要在技能命中/未命中语义有效的场合阻止它们，使用双 false：

```darkest
.on_hit false .on_miss false
```

双 false 可能产生红字报错。在 actout、道具 Effect、spawn Effect 等命中门无意义的场合，双 false 不能阻止上述三个字段执行。

## 施加守护的前置清理要求与群体守护边界

知识库编写者于2026-11-18确认：**所有施加守护都需要前置清除守护／被守护的处理。**此条作为守护实现要求记录，不再仅将前置清理写成可选的稳定性建议。这里的清除字段为 `.clearguarded 1`（清除被守护）与 `.clearguarding 1`（清除作为守护者提供的守护）；具体需要清哪一方、哪种状态、哪些字段组合及其准确时序，尚未明确，不能擅自解释为双方必须同时清除这两种状态。

**未前置清守护的具体后果不清楚。**知识库编写者首条补充使用“非法操作”一词，随后明确“没有前置清守护会怎么样我也不清楚”；以后一句为准，不把“非法操作”写成已确认的引擎判定或统一失败表现，也不统一断言会报错、整条技能不执行、消耗回合、守护失效或崩溃。

群体守护**可能需要特殊处理**，具体规则与处理流程仍未确认。不能直接假定把单体守护改成群体目标就能正常工作，也不能自行补造逐目标清理、重复执行次数或已建立守护关系的保留／移除规则。

下节原表关于技能防多重守护检查的结果，仍按其原始条件保留：其中“整技不执行”等是特定样本的既有观察，不是本次补充确认的所有调用方通用后果。“非技能调用不适用同一技能检查”也不等于非技能施加守护可省略本条前置要求。来源：`Sources/guard_preclear_requirement_20261118.json`；知识库编写者补充与澄清，非本轮实机测试。

## 技能虚假守护标志与防多重守护检查

迂回表第97条 P1521–P1524/X1871–X1877 记载，红钩对技能中的 `.guard` 有防多重守护检查：若技能目标已经被守护，而技能此前没有清除该目标的被守护状态，技能会整体不执行，表现为无技能动画、该技能的所有 Effect 均不执行、消耗回合并出现类似守护失败的提示。P1522限定此检查为技能守护，不扩展到怪癖 act-out、饰品等非技能调用引出的守护。

多守护一仍可能成立。原表第97条 P1523/X1875 记录：多个守护者可指向同一目标，按 rank 顺序决定当前守护者；当前守护者因故无法守护（原表例为处于 AOE 范围等情况）时会顺延至下一位。这是原表所述观察，不据此补造同 rank 优先级、全部失效原因或其他守护调用的排序规则。P1524/X1877 原本将前置移除已有目标守护作为设计建议；2026-11-18知识库编写者进一步确认前置清理为所有施加守护的实现要求，现按上节记录。原表只覆盖其具名检查，不用它否定该实现要求，也不由此补全未知的统一失败后果。

双 false 的虚假 `.guard` 标志物另有特殊交互。原表第97条 P1527/X1882 观察到：目标已被守护时，即使技能用 `.guard 1` 配合 `.chance 0%` 和双 false 使虚假守护不会实际施加，防多重守护检查仍会阻止整条技能。因此，用于技能禁用式 Buff 冷却的虚假守护标志只需 `.guard 1 .on_hit false .on_miss false`；这里双 false 仍仅在命中／未命中语义有效的技能调用中能抑制实际守护，不能推广到 act-out、道具、spawn 等调用。

若该类技能目标可能已经被守护，原表第97条 P1530–P1535/X1887–X1895 给出的绕过办法是在虚假守护标志前放置虚假移除守护：`.chance 0% .clearguarded 1 .clearguarding 1 .on_hit false .on_miss false`。这组代码依靠清守护字段与双 false 在技能调用中的特殊组合，目的是让内建检查看到前置清除标记，同时不实际改变守护状态；不能将它当作非技能调用中的通用零效果写法。当前用户于2026-11-04澄清，虚假守护标志自身无须 `.chance 0%`，是否能靠双 false 抑制仍取决于命中门是否对此调用有效。若未处理目标已有守护的分支，虚假 `.guard` 冷却标志仍可能令整条技能无法执行。本节按原表记录此迂回及当前用户的字段取舍，非本轮新增实机测试。


## 强制过抗读取抗性：原值概率利用、加减平移与量程分段

**本迂回可以直接利用具体抗性值作为另一条 Effect 的成功概率，也可以通过前置加减抗性／对应施加率，对这个值作加减平移。先前记录的转化比例及粒度限制已按知识库编写者要求移除，不再用于否定新方案。** 对0%～500%抗性的分段只是量程处理；分段后仍在读取并使用具体抗性值，不是只获取区间标签。知识库编写者于2026-11-06明确澄清；Agent未自行运行游戏测试。

### 基础流程与抑制方向

以自身死抗作为实际 Effect 成功概率为例：先以100%基础概率向自身尝试施加一个抑制 Buff，声明强制过死抗；该 Buff 用 `effect_chance` 抑制实际 Effect。再尝试执行实际 Effect，其基础概率至少100%，不自带过抗，且须保证未受抑制时必定成功、被抑制时不成功。

- 读取 Effect 成功：获得抑制 Buff，实际 Effect 不生效。
- 读取 Effect 失败：未获得抑制 Buff，实际 Effect 生效。

因此，实际 Effect 利用的是读取检查的失败概率，而不是成功概率。原记录把抑制分支写反，也错误概括为“只支持离散区间判断”，这些说法均撤回。

### 原值、加减与转化用途

在无对应施加率干扰、且处于有效概率范围时，英雄死抗67%，可令另一条 Effect 以67%为成功概率。若读取前先降低10个百分点死抗，则可得到57%成功概率；这是67%减去10个百分点，不是乘以90%。前置加减对应施加率／抗性可用于这种加减平移；但“增加10个百分点死抗穿透”能否等效实现，知识库编写者仍标为不确定，不得当作已确认写法。

知识库编写者给出的正向例子“每有100%流血概率，+10%腐蚀概率”保留。这里的流血概率和腐蚀概率分别是bleed_chance、poison_chance施加率，100%和10%均指百分点，不是把现有腐蚀施加率乘1.1。该例不再作为排除其他比例或粒度的依据。按知识库编写者本次要求，旧的转化比例限制从当前结论中移除；移除限制不等于已实机实现任意换算。该例未指定不足100个百分点的余量如何处置，不自行补充取整或随机折算规则。

### 共享骰点定位与补偿读取：仅记推理思路，不提供代码

知识库编写者于2026-11-06提出并授权记录。证据等级为**推理思路／未实机验证**，不是已落地代码或已测精确数值读取接口。

1. 在同一次所需概率共享范围内，用一组不同基础概率、没有额外施加率或抗性干扰的探针，根据成功与失败分界，定位共享随机骰点r所在区间。定位的是骰点，不是某条Effect自己的最终成功率；骰点0～100%的范围也不限制目标抗性R的量程。
2. 设读取Effect基础概率为C，实际读取施术者对应施加率为S，实际读取受术者对应抗性为R。暂以r≤C+S−R表示判定，恰好相等时的引擎行为另待核对。
3. 若在读取前将同一个骰点r加入读取概率，则r≤C+S−R+r可消去随机项，变为R≤C+S，也就是R−S≤C。改变C并定位成败分界，就构成对R−S的阈值检测。
4. 实际只能取得估计骰点r_hat时，阈值还带有r_hat−r的误差；可达精度取决于骰点定位和阈值扫描精度，不宣称无限精度。S未知或未补偿时，仍不能将R−S冒充为R；只有S为0、已知或另被补偿时，才可恢复目标抗性R。

上述推导支持的是“给读取概率加骰点”的路径。若仅从普通最终Effect概率P中减去r，判定r≤P−r等价于P≥2r，并未消除随机项；若最终Effect来自补集迂回，则需另核补集与骰点方向，不能直接当作等价替换。

探针、骰点补偿与读取必须保持同一次所需概率共享，不能跨独立调用边界；探针本身也必须排除额外概率修正和过抗干扰。附魔共享范围仍是推测，spawn共享仍待实测。本次只记思路，不新增具体Effect/Buff代码，不补造骰点传递、善后流程、引擎相等边界或完整执行结果。先前比例限制不再作为本思路及后续用途的否定依据。

### 对应施加率干扰

实际读取的是目标抗性，或目标抗性减去读取施术者对应施加率后的结果。例如施术者流血施加率会等量抵消目标流血抗性。可考虑由 size0 独立承担检测方并控制其对应施加率；但这不自动保证整个迂回可用：**spawn 内读取与最终 Effect 能否保留所需概率共享尚不确定，因此不能保证 size0 能完美承担防施加率干扰功能，到底能不能实现有待实测。** 控制检测方施加率与保留概率共享是两个分别需要满足的条件；不能说召唤 size0 本身会关闭施加率判定，也不能反向断言 spawn 必定不共享或 size0 必定不可用。疾病抗性、陷阱抗性没有对应施加率干扰；英雄读英雄死抗大概率不受干扰，但怪物读英雄死抗不一定。此待测限定由知识库编写者2026-11-06明确补充。

2026-11-09范围补充：知识库编写者推测**严格同一个size0单位实例**的各条spawn之间大概率共享，尚未完全确认；不是同小类不同单位共享，也不改变本段整条读取流程仍待验证的状态。来源 `Sources/spawn_sharing_and_mode_start_enchantment_20261109.json`，详见[概率共享专题](51-Effect概率骰子共享与隔离.md)。

另须区分已确认的跨调用边界：技能Effect与该技能召唤出的size0的spawn Effect必定概率独立，这原已属于“召唤者与召唤物独立”的范围，知识库编写者2026-11-09以两边最终成功率均为30%的例子进一步明确。因此，读取、补集或骰点补偿若依赖同一概率骰子，不能一部分放技能中、另一部分放召唤物spawn中并假设共享。这个限制不否定由同一个size0独立承担完整检测的候选方案；该方案内部所需共享仍按上一段保留待测。来源同账本 `SKILL-SPAWN-INDEPENDENT-01`。

### 0%～500%抗性的量程分段

以下既有量程案例仍保留；不额外加入施加率抵消步骤时，案例读取值仍为抗性减读取施术者对应施加率。

对于0%～500%的抗性，需要分成5个100%区间读取：0～100、100～200、200～300、300～400、400～500。**分段与直接利用具体抗性值并不冲突**；它解决一次概率窗口覆盖不了全部量程的问题，不代表只能获得区间标签。英雄死抗0%～87%，不因这一方案而要求分5段。等效计算概率可以是267%等超过100%的值；它不表示事件发生频率超过100%，更不表示最终Effect重复执行。

知识库编写者早期给出的分段草案：以500%基础概率读取的 Effect 为 A；A 成功时抑制下一条 B，A 失败时 B 未被抑制而必定成功，B 的作用是抑制后续全部操作。随后按400%、300%、200%、100%继续读取。该A/B方案作为历史设计过程保留；当前单次最终Effect的代码案例采用下方的共享概率修正方案，不再把历史草案当作唯一实现。

如果使用 size0 但定向不方便，可混合 `target_in_rank`、`effect_chance`、对群反向、技能标记等流程实现特定站位定向；`effect_chance` + `actor_base_class` 的仿 Spawn 定向也可作为选项，但 `actor_base_class` 在实际目标为自身时会失效。来源：`Sources/resistance_readback_via_forced_resist_20261106.json`；知识库编写者明确补充，Agent未自行实测。

### 不使用size0的施加率抵消流程（2026-11-07）

知识库编写者提供的设计方案，Agent未自行运行游戏测试；只记录流程，不新增具体代码。

1. 先按原有抗性读取流程读取目标抗性减实际读取施术者对应施加率，尝试抑制最终Effect；必须在降低抗性之前完成这一步。
2. 极大降低最终Effect实际受术者对应抗性，使该抗性实际生效值归零。
3. 只调用一次最终Effect，额外声明相同抗性类型的force_resist_type；零抗性下重新计入对应施加率，以抵消读取阶段减去的施加率。
4. 完成后善后，清理本流程的临时减抗与概率修正，避免改变其他效果；不是清空目标所有同类Buff。

**抵消对象与条件：**R为读取阶段受术者的原对应抗性，S_read为实际读取施术者的对应施加率；零抗性最终阶段重新加入S_final。设计意图为读取时减、发生时加，只有S_final与S_read来自同一对应数值且执行期间未变化时，才能按(R−S_read)+S_final=R抵消。不要求所有设计中读取受术者与最终受术者必为同一个单位，但归零必须落在最终Effect实际读取抗性的受术者上。

**反向时的施术者与受术者：**不可机械套用旧目标版示例：旧版读取由A对B，最终Effect反向由B对A；此时读取用A的施加率，最终用B的施加率，且最终受术者为A。若两者数值不一致，不能声称自动抵消，也不能只降低B抗性就声称最终判定是零抗性。须重新核对施术者、受术者、概率Buff持有者与必要的流程调整。自身版前后均自身施术，不存在因反向换人导致的这一差异。

**不适用范围：**不适用于最终Effect原本就要求过抗且需保留该正常判定的情况：前置清零抗性会破坏它本来应有的过抗判定；force_resist_type还会替代原抗性类型而不是追加第二套判定。不能把本方案当作保留原过抗行为的通用补丁。

**备选方案：**最终Effect本就要求过抗时，仍须考虑穷举探测后补偿或size0去干扰化等方案；骰点补偿目前仅为思路，size0的spawn概率共享仍待实测，不因列为备选而升级为已验证可用。

继续满足原读取迂回的共享概率、量程和调用时序前提；临时减抗本身须可靠生效且最终有效抗性确实为0。没有本轮新增可运行代码或游戏测试，不能把代数抵消代替对完整执行链的验证。

来源：`Sources/resistance_readback_via_forced_resist_20261106.json`的application_rate_cancellation_without_size0。


### 共享概率下的两次补集：最终Effect只执行一次

知识库编写者明确确认：在所需概率共享范围内，五个读取Effect使用500%、400%、300%、200%、100%基础概率；每成功一次，给**同一个最终Effect**减100个百分点概率。最终Effect基础概率500%，全部读取后只调用一次。两次补集关系使其等效计算概率为被读取抗性减读取施术者对应施加率；不是把抗性换算成多次执行，也不是只能在不共享骰子的假设下求期望。

例如被读取流血抗性267%、实际读取施术者流血施加率0：500%、400%读取必成，300%读取成功率33%，200%、100%读取必败。辅助Buff使最终Effect本次计算值出现200%或300%，**但它与读取分支使用共享骰子，因此整个流程等效267%概率，而不只是期望数值267%。** 不得把读取分支和最终Effect当作独立随机事件推算；也不表示辅助Buff直接存储了浮点数267。Agent此前以200%或300%为由否认共享概率下等效267%的限制撤回。

前提是实际调用链共享所需概率：技能与已确认共享的饰品Trigger按[概率骰子边界](51-Effect概率骰子共享与隔离.md)核对，不泛化所有Trigger。附魔的同类Trigger共享范围与饰品同类Trigger一致，目前仅为知识库编写者推测，不能升级为实测结论。不要用individual_target_actor_rolls true或跨独立调用边界破坏共享条件。

### 流血抗性代码案例：自身版与目标版

定义原调用方施术者为A、原调用方单体目标为B。这里的“流血概率”明确指bleed_chance施加率，不是读取Effect自己的基础.chance。

**案例没有排除施加率干扰。自身版等效A的流血抗性减A的流血施加率；目标版等效B的流血抗性减A的流血施加率。** 不能省略“谁的抗性”和“谁的施加率”，也不能称作已隔离施加率的纯抗性值。

所有effect_chance均采用简写。最终Effect治疗1只是观察载荷，不是读取流程必须治疗。按顺序在同一普通queue false层调用；只引用一次最终Effect，且它不能额外自带过抗或忽略概率。辅助Buff持续1但没有即时清理：重复执行前必须确认上次Buff已消失；不要把它当成已经具备生产环境善后清理的完整机制。分段案例覆盖有效读值0%～500%；被施加率平移到范围外的数值不由本案例保证保留。观察治疗还需排除满血、治疗修正及治疗暴击等干扰。

#### 自身版：无需反向

A自身的流血抗性 - A自身的流血施加率bleed_chance；不是完全不受施加率影响的纯抗性读取。

全部.target performer，不反向。读取施术者、读取受术者、辅助Buff持有者、最终Effect施术者、最终治疗对象均为A。

```darkest
effect: .name "BR_Self_Read_500" .target performer .chance 500% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Self_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Self_Read_400" .target performer .chance 400% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Self_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Self_Read_300" .target performer .chance 300% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Self_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Self_Read_200" .target performer .chance 200% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Self_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Self_Read_100" .target performer .chance 100% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Self_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Self_Final" .target performer .chance 500% .heal 1 .on_hit true .on_miss true .queue false .has_description false
```

调用顺序：

```text
"BR_Self_Read_500" "BR_Self_Read_400" "BR_Self_Read_300" "BR_Self_Read_200" "BR_Self_Read_100" "BR_Self_Final"
```

#### 目标版：读取不反向，最终Effect反向

原目标B的流血抗性 - 原施术者A的流血施加率bleed_chance；不是B抗性减B施加率，也不是A抗性减B施加率。

五个读取Effect均.target target且不反向：A读取B，辅助effect_chance Buff落在B。最终Effect为.target target .swap_source_and_target true：改由B向A施放，读取B持有的概率修正，示例治疗对象为A。不得仅把自身版本的performer机械替换为target而遗漏最终Effect的反向。

```darkest
effect: .name "BR_Target_Read_500" .target target .chance 500% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Target_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Target_Read_400" .target target .chance 400% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Target_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Target_Read_300" .target target .chance 300% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Target_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Target_Read_200" .target target .chance 200% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Target_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Target_Read_100" .target target .chance 100% .force_resist_type bleed .buff_type effect_chance .buff_sub_type "BR_Target_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "BR_Target_Final" .target target .swap_source_and_target true .chance 500% .heal 1 .on_hit true .on_miss true .queue false .has_description false
```

调用顺序：

```text
"BR_Target_Read_500" "BR_Target_Read_400" "BR_Target_Read_300" "BR_Target_Read_200" "BR_Target_Read_100" "BR_Target_Final"
```

**目标恰好为自身时的兼容性：**目标B可以恰好就是原施术者A。此时读取为A读取A，辅助Buff落在A；最终Effect的反向交换同一单位后仍为A对A施放，依然能使用A持有的effect_chance修正，不会因反向多执行一次或减两次概率。因此本目标版兼容目标为自身，无需另加分支或同时调用自身版。等效值退化为A的流血抗性减A的流血施加率。该结论来自知识库编写者明确说明反向自身仍可响应，加上对本案例目标、持有者及调用次数的语义核查；不是Agent新增实机测试。

来源：`Sources/resistance_readback_via_forced_resist_20261106.json`。概率共享下等效267%的结论与附魔范围推测由知识库编写者2026-11-06明确补充；代码为会话设计案例，Agent未自行进行游戏测试。


### 英雄死抗读取代码案例：自身版与目标版

英雄死亡抗性death_blow有效范围0%～87%，仅需一段100%基础概率读取。A为原施术者，B为原调用方的单体目标。实际等效值分别为**A的死抗减A的死击施加率deathblow_chance**、**B的死抗减A的死击施加率deathblow_chance**；不要把deathblow_chance与death_blow混为一项。

本代码没有主动隔离施加率。英雄读取英雄死抗大概率没有对应施加率干扰，不等于确定没有，怪物读取英雄死抗也不保证没有。读取与最终Effect须共享所需概率并按顺序在同一普通queue false层调用；附魔共享仅为推测，spawn共享待实测。读取成功则给最终Effect减100个百分点；最终Effect基础100%、不额外过抗且只调用一次。治疗1是测试载荷，辅助Buff持续1但没有即时清理，再次使用前须确认旧Buff已消失。

#### 死抗自身版：无需反向

A自身的死亡抗性death_blow - A自身的死击施加率deathblow_chance。

全部.target performer，无需反向。读取、辅助Buff持有者和最终Effect施术者均为A，示例治疗对象也是A。

```darkest
effect: .name "DB_Self_Read" .target performer .chance 100% .force_resist_type death_blow .buff_type effect_chance .buff_sub_type "DB_Self_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "DB_Self_Final" .target performer .chance 100% .heal 1 .on_hit true .on_miss true .queue false .has_description false
```

调用顺序：

```text
"DB_Self_Read" "DB_Self_Final"
```

#### 死抗目标版：兼容目标为自身

原目标B的死亡抗性death_blow - 原施术者A的死击施加率deathblow_chance。

读取Effect使用.target target且不反向，A读取B并把辅助Buff施加给B。最终Effect使用.target target .swap_source_and_target true，由B对A施术，使用B持有的概率修正；示例治疗对象是A。

```darkest
effect: .name "DB_Target_Read" .target target .chance 100% .force_resist_type death_blow .buff_type effect_chance .buff_sub_type "DB_Target_Final" .buff_amount -100% .duration 1 .on_hit true .on_miss true .queue false .has_description false .suppress_resist_popup true
effect: .name "DB_Target_Final" .target target .swap_source_and_target true .chance 100% .heal 1 .on_hit true .on_miss true .queue false .has_description false
```

调用顺序：

```text
"DB_Target_Read" "DB_Target_Final"
```

**目标恰好为自身时的兼容性：**B可以恰好是A。此时读取A的死抗减A的死击施加率，辅助Buff在A，反向后最终Effect仍是A对A施放，可正常响应；不需要额外分支或同时执行自身版，不因反向多施加Buff或多执行最终Effect。

来源：`Sources/resistance_readback_via_forced_resist_20261106.json`。知识库编写者2026-11-06接受记录这两版死抗代码；不是Agent新增的游戏实测结果。
