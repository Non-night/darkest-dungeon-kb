# buffs.json 结构

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

## 文件位置与名称
- Buff 定义文件必须创建在目标 Mod 根目录的 `shared\buffs` 文件夹中。
- 文件名必须是“至少 1 个字符的前缀 + `.buffs.json`”，后缀比较不区分大小写。
- 前缀可自行命名，但建议只使用稳定的英文字母、数字和下划线；避免空格和其他特殊字符。
- `.buffs.json`、`hero.json`、`hero.buffs.json.backup` 均不合法。
```text
shared\buffs\aaa.buffs.json
```
设计稿没有提供具体 Buff ID 时，Agent 应根据目标 Mod 的统一前缀创建稳定、唯一、可追踪的 ID，并同时完成 Effect 引用；不得仅创建空的 `shared\buffs` 文件夹，也不得因缺少现成 ID 而省略设计效果。即使原版已有行为相似的 Buff，也不得优先复用其 ID；默认应创建当前 Mod 独有的 Buff 定义，避免原版 ID 被覆盖或修改时连带改变当前 Mod。
## 标准 Buff 定义：必写项与可选项
这里需要区分两种“必写”：
1. **当前可确认的最低结构字段**：知识库与配套结构校验要求每条 Buff 至少具有 `id`、`stat_type`、`stat_sub_type`、`amount`、`rule_type`、`is_false_rule`、`rule_data`；其中 `rule_data.float` 与 `rule_data.string` 也必须同时存在。这是安全创作与校验基线，不等于已经逐项证明“省略任一字段必定导致引擎崩溃”。
2. **知识库创作规范要求显式书写的字段**：Agent 正常创建 Buff 时，不应只满足最低字段，而应使用下方标准骨架。即使某些字段可能存在引擎默认值，也不要无理由省略，以免语义不明确或让后续维护者错误推断。
### 解读任何 Buff 前的强制核验
对任何现有或新建 Buff，必须分别确认其 `stat_type`、`rule_type` 和 `duration_type`，且不得只凭名称推断其效果。尤其是 `rule_type`，必须查清：
1. 该 Rule 实际检测的对象和状态是什么；
2. 它在何种事件或更新点进行成立／失效判定；
3. Rule 不成立时是仅停用统计效果、触发 `remove_if_not_active` 移除，还是影响某个追加 Effect 的调用；
4. 该 Buff 的调用方、目标、来源与时序是否为这个 Rule 提供了必要上下文。
若 Rule 的语义或判定时点没有专项证据，必须明确写为未确认，不能根据 Buff 最终表现倒推出完整 Rule 机制。解析已有 Mod 时，作者描述、字段名和实际调用链可能不一致；必须核对实际文件、字段、引用关系和足够相关的原版／官方 DLC／测试证据后再作解释。发现用词偏差时，应基于证据明确纠正，不能顺着描述补造机制。
### Rule 的有效判定范围与三值逻辑
当前用户于2026-11-03补充的理论模型：所有 Rule 都有各自的有效判定范围；范围外返回 `null`，无论是否取反均表现为不生效；范围内返回普通 `true` 或 `false`，二者可由 `is_false_rule` 相互翻转。这里的范围是对象、调用方、目标、时序及必要状态所组成的有效判定上下文，不是 `rule_data.float` 的数值阈值。具体范围须逐 Rule、逐调用上下文查证；不能把缺失上下文当作普通 `false`，也不能从本模型补造某条 Rule 的具体范围或声称55条均已逐项实测。

| 原始判定 | 不取反 | 取反 |
|---|---|---|
| 范围内 `true` | 生效 | 不生效 |
| 范围内 `false` | 不生效 | 生效 |
| 范围外 `null` | 不生效 | 不生效 |

表中的生效仅指 Rule 激活，不保证 Buff 所修饰的 stat_type 在该调用时机有效，也不改变移除、追加 Effect 或生命周期的独立规则。具体 Rule 的范围不明时须保留未知，不能把“条件未满足”与“无法进行有效判定”混为一谈。

### 单个 Buff 只能写一个 Rule
知识库编写者补充（2026-09-22）：每个 Buff 定义只能有一个 `rule_type`，没有把两个 Rule 直接并列写入同一个 Buff 的简单写法。`rule_type`、`is_false_rule` 与 `rule_data` 描述的是这一条 Rule；不能在一个 Buff 中追加第二套独立 Rule，期待引擎自动把它们按 AND、OR 或其他组合逻辑处理。
如果设计需要多个条件，只能按具体调用链组合多个 Buff、ID 定向驱散、条件清理、Rule 触发后的追加 Effect、二段驱散或其他已确认机制，近似伪造所需效果。多个 Buff 的组合不自动等于严格的 AND/OR：必须逐个核对施加对象、判定时点、来源、清理顺序、Rule 失效行为和可能的残留。不能仅因为两个 Buff 各自有一个 Rule，就宣称已经得到一个可靠的双 Rule Buff。
### 进攻型（施术）Rule 的目标判定
- 进攻型 Rule 的 Buff 位于施术者身上；Rule 生效时检查被修饰操作的受术者／目标状态，不是检查 Buff 持有者自身的状态。
- `actorStatus` 的检查对象由被修饰的属性决定：技能层的百分比加伤、穿甲等属性读取技能目标；腐蚀概率等依靠具体 Effect 结算的属性读取该 Effect 的最终目标。技能目标和 Effect 目标不能混为一谈。
- 群体技能或群体 Effect 必须对每个最终受术者分别判定；不能因为 Buff 都由同一个施术者持有，就把 Effect 层判定改写成技能 Header 的目标集合。
- 这条目标解析规则不能未经专项证据推广到反击、饰品、ActorDot、`act_out` 或其他调用来源；这些来源仍须按各自的实际调用链核对。
### 通常必须显式书写
| 字段 | 书写要求 |
|---|---|
| `id` | 必须为当前 Mod 创建稳定、唯一的 Buff ID；不得优先复用原版或其他 Mod 的 ID。 |
| `stat_type` | 必须写合法 Buff 类型。 |
| `stat_sub_type` | 字段本身必须存在。当前 `stat_type` 要求副类型时填写对应合法值；不使用副类型时写空字符串 `""`。 |
| `amount` | 必须填写该 Buff 的数值。即使类型主要用于标记或其他附加机制，也应显式写出设计所需值。 |
| `remove_if_not_active` | 通常必须显式写为 `false`。没有明确的“Rule 不成立时立即移除”需求，不得擅自写为 `true`。 |
| `rule_type` | 通常不得省略。无条件生效时也应显式写 `"always"`。 |
| `is_false_rule` | 通常不得省略；不取反时写 `false`。 |
| `rule_data` | 通常不得省略，并且必须同时写出 `float` 与 `string`。未使用的槽位仍分别写 `0` 与 `""`。 |
| `is_clear_debuff_valid` | 标准创作骨架中应显式写出，明确该 Buff 是否允许被常规减益清除机制移除。 |
| `has_description` | 标准创作骨架中应显式写出；有明显玩家可读意义的常规 Buff 默认写 `true`，只有纯辅助逻辑 Buff 等例外才默认写 `false`。 |
### `has_description` 的创作默认规则
- 对具有明显玩家可读意义的 Buff（例如常规眩晕抗性增加、减压量增加等），默认必须写 `"has_description": true`，让游戏显示其自动生成的效果描述。
- 只有主要承担内部寄存器、逻辑门或清理流程、且不需要作为技能描述自定义文本显示的辅助 Buff（例如数值极大的寄存器／逻辑门 Buff、会瞬间清除自身的清理 Buff 等），才可按辅助用途默认写 `false`。
- 用于技能描述自定义文本的 Effect／Buff 必须保留 `has_description: true` 或可见默认；写 `false` 会使该自定义文本不显示在技能描述中。
- 用户明确要求隐藏某个有实际意义的 Buff 描述时，才可覆盖上述默认规则写 `false`；不得仅因 Buff 是由技能、饰品或其他系统施加，就自动隐藏描述。
- 这是面向代码生成的创作规范；`has_description` 的字段值域仍只有字符布尔 `true`／`false`，具体显示效果以游戏版本和调用上下文为准。
```json
{
  "id": "mod_unique_buff_id",
  "stat_type": "combat_stat_add",
  "stat_sub_type": "speed_rating",
  "amount": 1,
  "remove_if_not_active": false,
  "rule_type": "always",
  "is_false_rule": false,
  "rule_data": {
    "float": 0,
    "string": ""
  },
  "is_clear_debuff_valid": false,
  "has_description": true
}
```
### `remove_if_not_active` 的默认创作规则
- 指定 Rule 的读档／重启移除：`monster_type_count_min` Buff 写 `remove_if_not_active: true` 时，读档会使其消失，即使场上仍满足条件；原表也明确类比 `has_quirk` 配置该字段为 `true` 时的重启消失现象。用于两 Buff 抵消时，若抵消项消失而 `always` 项保留，组合净效果会被破坏。本项仅覆盖上述指定 Rule 与 `true` 配置，不推广到全部 Rule，也不据此保证 `false` 配置永不消失；不把它解释为持续时间正常到期。证据：迂回表第33条 P898/X1050，当前用户于2026-11-03确认按此边界补入；非本轮新增实机测试。
- 默认写法是 `"remove_if_not_active": false`。
- 知识库编写者于2026-11-07补充：Buff 定义省略 `remove_if_not_active` 时会产生红字报错，但不一定因此失效；当前观察为大概率仍能正常生效。该表现不能替代显式填写字段，也不能据此推断所有 Buff 类型、Rule 或调用方式都稳定可用。
- `true` 的含义是：Rule 不成立时直接移除该 Buff；它不是“条件不满足时暂时停用，条件恢复后自动回来”。因此它会改变 Buff 的存在性和真实存续时间，并可能使 Buff 在设计预期之前永久消失。
- 只有设计明确要求“条件一失效就移除”，或者某个特定 `stat_type` 已有明确证据表明必须依靠 `true` 才能让 Rule 控制其存在时，才可写为 `true`。
- 已知例外包括 Buff 型流血、腐蚀、愈合、恐惧、扰乱：这些类型只有在 `remove_if_not_active: true` 时，Rule 才实际控制其存在；具体边界应继续读取对应 `Buff/stat_type` 词条。
- 静态怪癖／饰品提供的 DOT 另有原表观察：`remove_if_not_active: false` 时，Rule 不成立也仍触发其 DOT，等效 `always`；静态 DOT 转移后还可能不自行重现。此观察限原表所述调用，当前版本未确认；详见 `Mechanics/66-负数DOT与不可治愈边界.md`。
- 静态怪癖/饰品提供的 DOT 是另一个需单独检查的调用方式：原表第112条观察到，写 `remove_if_not_active: false` 时，即使 Rule 不成立，该静态 DOT 仍会触发，等效 `always`；转移后还可能不自动重现。该观察限原表所述静态 DOT 来源，当前版本未确认，不推广到所有 DOT Buff；完整边界见 `Mechanics/66-负数DOT与不可治愈边界.md`。
- 静态饰品 Buff 等调用场合还可能对 `true` 有额外风险。不得因为看到其他案例使用了 `true` 就机械照抄，必须先确认调用方式和所需移除语义。
- 即使该字段为 `false`，Buff 仍可能因持续时间到期、`remove_on_battle_complete`、Buff 源自动清除、ID 定向驱散或其他机制提前消失。
### 条件必写或按设计填写
- `duration` 与 `duration_type`：需要在 Buff 自身规定持续时间时配套填写；若由引用它的 Effect 统一覆盖，可不在 Buff 中重复定义。
- `description_tooltip_id`：需要自定义提示文本时填写；应同时检查本地化 ID。它即使在 `has_description: false` 时也能强制显示自定义描述。
- `attack_additional_effect_ids`：需要附魔 Buff 在攻击时追加调用 Effect 时填写；自附魔的 AWR/queue 时序、一次性清理和 `skill_instant` 替代路径见 [附魔、自附魔与 AWR / queue 时序边界](../../Mechanics/92-附魔自附魔时序与 AWR 边界.md)。
- `consume_on_rule_active`：仅在已确认可用的未取反 `riposte` Rule 组合中使用；不能把它当成通用 Rule 消耗字段。
- `clear_buffs_on_rule_active`：需要 ID 定向驱散时填写 Buff ID 数组。
### 其他可选字段
`remove_on_battle_complete`、`fx`、`suppress_apply_poptext`、`force_positive`，以及上述只有特定机制需要时才填写的字段。可选表示“按设计决定是否出现”，不表示可以忽略其配套条件、值域或已知风险。
### `description_tooltip_id`
- 参数类型：单个字符串。
- 引用自定义 Buff 提示文本的本地化 ID，以自定义文本替换自动生成的 Buff 描述；即使 `has_description` 为 `false`，也会强制显示该自定义描述。
- 本地化 XML 中应定义同名 ID，并使用 `buff_tooltip_` 前缀。
- 既有固定自定义文本中的字面百分号可写单个 `%`；这不否认 `%d` 等数值占位符的支持，含占位符文本的字面百分号规则见下方未知边界。
- 知识库编写者2026-10-28修正：新写法 `description_tooltip_id` 的本地化文本支持 `%d` 之类的数值占位符，取值使用对应 Buff 的 `amount`，且可像打折／进化写法一样堆叠显示。此前否认可引用或堆叠 Buff 数值的结论已撤回，不再作为当前规则。本条是知识库编写者明确修正，非本轮新增实机测试。
- 副本中英雄／怪物 Buff 栏详情，在 Buff 原本能合并的前提下：本新写法不带附魔时，纯文本不合并，`%d`／`%d%%` 计数文本可合并；文本 Buff 自身携带附魔时不合并。暂按所有附魔类型处理，非逐类实测。暴击源可与技能源合并并覆盖其普通图标，事件源与技能源不合并；不要求原本图标相同，特殊源内部仍按自身规则且本次未测。其他界面不作结论。需合并纯文本可用不携带附魔的折扣型／进化型，需逐条显示可直接在附魔 Buff 上写文本。证据与全部限定见 [副本 Buff 栏详情的自定义文本合并与附魔边界](../Mechanics/16-loc与loc2本地化覆盖优先级.md)及 Sources/buff_tooltip_merge_20261117.json。
- 不承诺任意printf参数或全部stat_type：具名技能combat_stat_add.attack_rating自定义 `%d` 使用roundf(100×amount)，含数值格式串的字面百分号样本用 `%%`；纯文本单%及其他消费者另论。技能.buff_ids应用描述读全局Buff定义amount，非角色当前叠层；不撤回Buff栏可合并显示的旧证据。全部参数／合并条件仍未穷尽。
- 2026-11-17技能应用描述专项证据：现代Buff项保留255个UTF-8字节（不含NUL）；同类别instant纯文本项为 `(P[:255]+SPACE)[:255]`；旧打折／进化正文先127后加SPACE。历史256／128不再作为所有消费者的硬边界，当前饰品及Buff栏未由此次研究重测。模式名63、模式汇总255、公共／最终511是其他独立阶段。详见 [技能描述专题](../Mechanics/100-技能描述容量拼接排版与面板战斗可见性.md)。
- Rule 不可能直接控制 `description_tooltip_id` 对应自定义文本是否显示；Rule 与文本 Entry 的消费没有已确认的条件绑定接口。`has_description` 也是静态配置，不是 Rule 显示开关。
`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\shared\buffs\runaway.buffs.json:50`
```json
"description_tooltip_id" : "buff_tooltip_rw_play_with_fire_burn_on_hit"
```
对应本地化实例：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\localization\runaway.string_table.xml:4603`。
### `attack_additional_effect_ids`
#### 同一 Buff 承载多种附魔（判断，尚未实测）
知识库编写者判断（2026-11-08，非实测确认）：同一个 Buff 理应可以同时承载多个不同类型的附魔字段，例如同时填写 `attack_additional_effect_ids` 与 `friendly_additional_effect_ids`。不应默认认为二者互斥，也不应仅因附魔类型不同就强制拆成两个 Buff。

这不表示各类型的触发条件、时序和目标语义相同；仍须分别遵循对应类型的规则。例如友方技能附魔没有独立 AWR 时序，不能因为与攻击附魔位于同一个 Buff 就取得攻击附魔的 AWR 语义。该判断不是任意附魔组合均已验证兼容，也未确认不同类型同时满足条件时的调用顺序、去重或共享概率。

证据：`Sources/buff_multiple_additional_effect_types_20261108.json`。字段各自存在不等于已实测确认同一 Buff 中的组合行为。

- 参数类型：Effect ID 字符串数组。
- 持有该 Buff 的单位进行攻击时，在命中或未命中结算中调用数组引用的 Effect。
- Buff 的 `rule_type` 当前不成立时，不调用这些 Effect。
- 多个此类 Buff 按 Buff 的施加顺序结算，包括由同一条 Effect 依次施加的 Buff。
- 其结算晚于同一时序层的饰品触发器；所引用 Effect 自身的时序字段有效，包括 AWR。
- 多个同名 Buff 可以重复调用同名 Effect；若该 Effect 写有 `.apply_once true`，仍会受到 `.apply_once` 的去重限制。
- 单个 Buff 的数组实测可以写入 `16384` 个 Effect ID。该次测试中，游戏卡顿数分钟后恢复运行，但只有 `16383` 个 Effect 正常生效；最后一个未生效的原因未知，不能据此断言固定有效上限就是 `16383`。
- 即使只引用 `1024` 个 Effect，也观察到明显卡顿。卡顿程度可能与玩家的电脑配置有关，但该影响尚未确认。
- 极限测试只证明引擎可以处理上述规模而未立即崩溃，不代表该规模适合实际 Mod；常规创作应避免大量引用，也不得依赖第 `16384` 个 Effect 必定生效。
`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\shared\buffs\runaway.buffs.json:51`
```json
"attack_additional_effect_ids" : [ "RW Play With Fire Burn On Hit" ]
```
### `suppress_apply_poptext`
- 参数类型：布尔值。
- 写为 `true` 时，施加该 Buff 不显示“增益”或“减益”气泡；抵抗气泡仍可正常显示。
`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\shared\buffs\duelist.buffs.json:83`
```json
"suppress_apply_poptext" : true
```
### `consume_on_rule_active`
- 参数类型：布尔值。
- 设计语义：写为 `true` 时，在该 Buff 的 rule 生效后消耗并移除该 Buff。
- **稳定可用的组合目前只有 `rule_type: "riposte"` 且 `is_false_rule: false`**，也就是未取反的 `riposte` Rule。
- 该字段无法正常地泛用于其他 Rule。其他 Rule 的逐项结果尚未全部整理，但现有测试表明绝大多数 Rule 都不能让 `consume_on_rule_active` 正常执行。
- 因此创作时把它视为 `riposte` 专用字段：除未取反的 `riposte` 外，不得依赖它自动消耗 Buff；若其他 Rule 需要在成立时移除 Buff，应改用已有明确支持该 Rule 的清理机制，而不是假定本字段有效。
- `rule_type: "riposte"` 若配合 `is_false_rule: true`，不属于已确认有效组合，不得按可用行为生成。
`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\shared\buffs\duelist.buffs.json:730`
```json
"consume_on_rule_active" : true
```
### `force_positive`
- 参数类型：布尔值。
- 知识库编写者确认（2026-09-20）：在可见来源下，原本显示为减益的同类 Buff 写 `force_positive: true` 后进入增益图标，并与同类增益数值合并显示。例如 +15% 暴击与 -5% 暴击原本分属两个图标，给负值 Buff 设置该字段后增益图标显示 +10%，该负值 Buff 不再产生减益图标。
- 大多数可见 Buff 通常按正负分图标，但不是无例外规则：`torch_increase_percent`、`torch_decrease_percent` 默认无论数值都视为减益；`bsrc_never_again`（余生不回源）下同类 Buff 自动合并正负数值。
- 这里只确认图标及同类数值的显示合并，不表示 amount 改变正负，也不证明 Buff 实例、Rule、持续时间或清除条件合并。跨来源、不同 Rule／副类型的完整合并条件未明确，不能据此推断驱散行为。详见 [Buff 源与图标](../Mechanics/15-Buff源与真驱散.md)。
- 写为 `true` 时，强制将该 Buff 在 Buff 栏、提示文本和施加气泡中视为增益；该字段描述的是显示分类，不表示会改写 `amount` 或 Buff 的实际机制。
`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\shared\buffs\duelist.buffs.json:744`
```json
"force_positive" : true
```
### `clear_buffs_on_rule_active`
- 参数类型：Buff ID 字符串数组。
- 该 Buff 的 rule 生效时，移除数组中列出的全部 Buff ID。
- 社区称该机制为 **ID 定向驱散**：它按明确的 Buff ID 列表移除 Buff，不按 Buff 源或 Buff 类型整类偷取。
- **作用域只限当前 Buff 的持有者自身**：它只扫描并清除持有者身上与列表 ID 相同的 Buff，不能影响场上其他单位，即使其他单位持有同 ID Buff 也不会被清除。
- 所有由 Effect 简写形式生成的 Buff ID 均为空字符串 `""`。因此，如果数组中包含 `""`，持有者身上所有 Effect 简写 Buff 都会被一并清除，不能只定向某一种简写 Buff。该写法容易误伤来自技能、饰品、反击及其他机制的简写 Buff，通常不建议使用。
- 任意 rule 成立时均可触发清除；检测几乎发生在条件满足的同时。`attacking_monster_type` 测试中，清除甚至早于伤害结算。
- 若该 Buff 即将被另一个 Buff 清除，它会先执行自己的 ID 定向驱散，再被清除。
- 列表可以包含当前 Buff 自身的 ID：它会先完成列表清除，再清除自身；该行为与列表书写顺序无关。
- 数组实测写入 `16385` 个 Buff ID 时，所有对应 Buff 均成功移除，游戏仅出现轻微卡顿；该规模下没有出现旧式真驱散的驱散溢出。
- 当前结论只能确认至少 `16385` 个 ID 的测试结果，尚不能断言该字段绝对没有数量上限。极限测试规模也不应视为常规安全用量。
- 瞬时 Buff 的二段驱散用法见：[瞬时效果、正负相抵与二段驱散](../Mechanics/25-瞬时效果、正负相抵与二段驱散.md)。
`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\shared\buffs\runaway.buffs.json:338`
```json
"clear_buffs_on_rule_active" : [
  "rw_run_conditional_stealth"
]
```
## Effect 覆盖
Effect 通过 `.buff_ids` 引用 Buff 时，Effect 的 `.duration` 和 `.buff_duration_type` 分别覆盖 Buff 定义中的 `duration` 和 `duration_type`；Effect 未填写对应字段时，才使用 Buff 定义中的对应字段。
推测 `.buff_is_clear_debuff_valid` 也会覆盖 Buff 定义中的 `is_clear_debuff_valid`，但该覆盖关系尚未确认。创作时不要在 Effect 与 Buff 中填写互相冲突的值。
## rule_data
`float` 与 `string` 都是必需字段，即便某条 rule 不使用其中之一，也建议分别填 `0.0` 与空字符串。
```json
{
  "buffs": [
    {
      "id": "example_buff",
      "stat_type": "combat_stat_add",
      "stat_sub_type": "speed_rating",
      "amount": 2.0,
      "rule_type": "always",
      "is_false_rule": false,
      "rule_data": {"float": 0.0, "string": ""},
      "duration": 1.0,
      "duration_type": "round",
      "remove_on_battle_complete": true,
      "is_clear_debuff_valid": false
    }
  ]
}
```
## 三层判断
1. JSON/字段/值域是否合法。
2. rule 在当前施术、受术或通用上下文中是否能得到有效判定目标。
3. stat_type 在该时机是否真的能生效、是否安全。
本页主要覆盖第 1 层和部分第 2 层。第 3 层应采用原版证据或已有测试记录中的明确结论；明确结论无需重复测试，未确认边界应避免依赖或另行验证。

## 新版 Buff 触发器、force_negative（2026-11-05）
这些字段属于Buff定义，参数为Effect ID字符串数组；可附条件。下表是文档字段速查，不能把饰品的_additional_effects拼法替换到Buff中。来源：新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json
| 字段 | 条件与边界 |
|---|---|
| `attack_additional_effect_ids` | 与饰品对应项不同，Buff版本也支持反击；知识库编写者2026-11-11补充：这些攻击/暴击/近战/远程附魔均可在反击中触发并引出真正AWR，若需限定反击上下文可配合反击Rule。反击附魔及反击暴击附魔中的AWR则按queue false处理。来源：Sources/riposte_turn_start_enchantment_awr_20261106.json。 |
| `friendly_additional_effect_ids` | 反击属于攻击类技能，因此不会触发本附魔。与友方技能及友方技能饰品Trigger一样，不存在独立AWR；写AWR视同普通queue false。来源：Sources/friendly_enchantment_no_awr_20261106.json。 |
| `move_skill_additional_effect_ids` | 仅在战斗中触发。 |
| `attack_crit_additional_effect_ids` | 与饰品对应项不同，Buff版本也支持反击；知识库编写者2026-11-11补充：这些攻击/暴击/近战/远程附魔均可在反击中触发并引出真正AWR，若需限定反击上下文可配合反击Rule。反击附魔及反击暴击附魔中的AWR则按queue false处理。来源：Sources/riposte_turn_start_enchantment_awr_20261106.json。 |
| `melee_attack_additional_effect_ids` | 与饰品对应项不同，Buff版本也支持反击；知识库编写者2026-11-11补充：这些攻击/暴击/近战/远程附魔均可在反击中触发并引出真正AWR，若需限定反击上下文可配合反击Rule。反击附魔及反击暴击附魔中的AWR则按queue false处理。来源：Sources/riposte_turn_start_enchantment_awr_20261106.json。 |
| `ranged_attack_additional_effect_ids` | 与饰品对应项不同，Buff版本也支持反击；知识库编写者2026-11-11补充：这些攻击/暴击/近战/远程附魔均可在反击中触发并引出真正AWR，若需限定反击上下文可配合反击Rule。反击附魔及反击暴击附魔中的AWR则按queue false处理。来源：Sources/riposte_turn_start_enchantment_awr_20261106.json。 |
| `riposte_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `riposte_crit_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `on_dodge_additional_effect_ids` | 此组heroes=友方，monsters=敌方。 |
| `was_hit_additional_effect_ids` | 此组heroes=友方，monsters=敌方。 |
| `was_hit_all_heroes_additional_effect_ids` | 此组heroes=友方，monsters=敌方。 |
| `was_hit_all_monsters_additional_effect_ids` | 此组heroes=友方，monsters=敌方。 |
| `kill_performer_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `kill_all_heroes_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `kill_all_monsters_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `riposte_kill_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `was_killed_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。死亡单位同时是performer和target。 |
| `was_killed_all_heroes_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `was_killed_all_monsters_additional_effect_ids` | 此组heroes=英雄，monsters=怪物，按字面阵营。 |
| `quest_start_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `combat_start_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `turn_start_additional_effect_ids` | 个人回合开始触发。2026-11-24更正：反击不会触发本附魔，见 Sources/riposte_turn_start_enchantment_awr_20261106.json。与act_out的相对时序待测，已确认早于流血／腐蚀结算。2026-11-10更正：新引出的回合开始附魔不能在当前回合触发，旧无限式基础撤回；可跨回合递推，或同回合预写分支用effect_chance控制开启。修正写法仍可能称无限式，不代表真实无限调用。来源：Sources/kaze_infinite_enchantment_chain_20261106.json。与流血/腐蚀/愈合等其他回合开始阶段的完整顺序仍按各自记录核对。 |
| `turn_end_additional_effect_ids` | 推测反击不会触发本附魔，待实测。个人回合结束附魔先触发，再扣减小回合型round/after_turn Buff持续时间；1回合附魔及抑制Buff此时仍有效。严格顺序及类型组合已实测，时序分离未测。2026-11-11补充：所讨论结束方式中仅撤退失败不触发，移动或跳过仍可触发；不同于饰品turn_end_additional_effects在移动、跳过及撤退失败均不触发。完整目标及与其他Trigger排序不由本条确认。来源：Sources/turn_end_additional_before_duration_20261108.json；Sources/turn_end_trigger_and_ad_last_operation_20261111.json。 |
| `round_end_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |
| `battle_finished_successfully_additional_effect_ids` | 支持条件；完整目标与跨trigger排序未提供。 |

### 战斗开始切换英雄模式（2026-11-05）
Buff 的 `combat_start_additional_effect_ids` 和饰品战斗开始时效果若对英雄侧切模式，必须完整遵守[战斗开始切模式流程](../Mechanics/28-spawn、生命反馈与size0执行链.md)，否则崩溃；实际切模式 size-0 必须在自身 Spawn 中自加行动点，再触发自身生命反馈切模式。
来源：知识库编写者2026-11-05补充；`Sources/guard_start_triggers_20261105.json`；Agent未自行实测。

`force_negative: true`把Buff显示为减益，与force_positive方向相反；不改写amount。两字段同时填写时优先级未知。
