# Effect 定义基础

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

## 文件位置与名称
- Effect 定义文件必须创建在目标 Mod 根目录的 `effects` 文件夹中。
- 文件名格式为 `*.effects.darkest`；`*` 是至少一个字符的自定义前缀。
- 前缀可以自行命名，但通常只使用稳定的英文字母、数字和下划线；不建议加入空格或其他特殊字符，以免触发尚未明确的识别问题。
- Effect 的 `.name` 除非当前用户另有要求，通常也优先使用下划线而不是空格；这是默认命名习惯，不是对既有含空格名称的统一判非法。
```text
effects\aaa.effects.darkest
```
## `.darkest` 注释
- `.darkest` 使用 `//` 创建注释。
- 注释必须独立成行；不得把 `//` 追加在有效代码行末尾。
```darkest
// 技能一级流血
effect: .name "AAA Bleed 1" .target "target" .chance 100% .dotBleed 2 .duration 3 .on_hit true .on_miss false
```
- 一般应保留必要的独立行注释，以提高代码可读性。
- 极少数情况下，独立行注释也可能触发异常识别：若游戏表现为某条注释下方的所有内容均像“没有写入”一样不生效，应优先检查该注释，暂时删除、重写或移动它，再观察后续内容是否恢复。
- 上述异常不常见；正常创作不需要因此取消全部注释。
## 定义格式
- 每条 Effect 定义以 `effect:` 开头。
- `.name` 必须出现，用于定义该 Effect 的名称；该名称也是其他配置引用此 Effect 时使用的内部标识。
- 同一 `effect:` Header 内换行继续书写的内容属于同一条物理定义。
- 不同 Header 只要 `.name` 参数相同，也会在一定意义上被引擎视为同一个逻辑 Effect；这种跨 Header 的写法称为“分行”。跨 Mod 的同名 Effect 文件仍参与叠加，不能按普通同名文件覆盖规则假定旧定义已丢失。证据：迂回表第88条 P1424–P1427/X1718–X1721，当前用户于2026-11-04确认；非本轮新增实机测试，不推广到其他文件类型。
- “同名视为同一条”不是所有字段都可直接无条件合并的证明；具体关键字仍需结合其词条判断。已知它可能突破某些单条 Effect 的数量限制，例如 `.buff_ids` 的有效引用数量。
- 当前用户2026-11-04澄清：同名 Effect 分行中，多参数关键字相互补充，重复的单参数关键字后写／后加载覆盖前者。`.target` 不同最终只使用后一个；分行通常只想补充多参数内容，因此应保持不希望改变的 `.target` 等单参数一致。单参数覆盖沿用已记录的 `.buff_ids` 同文件、跨文件及跨 Mod 加载顺序；完整文件名排序的未知边界仍保留。未填写字段的默认／继承行为另查具体词条。见[Effect 同名与分行](../Mechanics/18-Effect同名与分行.md)。证据：第88条 P1419–P1420/X1712–X1713及当前用户澄清，非新增实机测试。
- Effect 定义本身不会主动执行；它需要在技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等位置被引用。
## 从设计到定义
- 设计稿只需提供效果语义、数值、目标、持续时间和触发条件；不要求设计者预先写出最终 Effect/Buff ID。
- 当用户要求创建或完善 Mod 时，Agent 可以并且应当为所需机制创建稳定的自定义 ID、Effect 定义和 Buff 定义，再完成引用闭包。
- 写 Mod 时永远不得优先复用原版已有的 Effect/Buff。默认使用目标 Mod 的统一前缀创建独立 ID 和完整定义；原版内容只作为字段结构与数值写法参考。
- 直接复用原版 ID 会使当前 Mod 受到同名 Effect 分行、同 ID Buff 覆盖、其他 Mod 修改和加载顺序影响。只有用户明确要求，或机制必须依赖无法替代的原版特殊 ID 时才可例外，并应说明兼容风险。
- “设计稿没有给出现成 `.effects.darkest` 或 `.buffs.json` 定义”不能作为省略已明确设计效果的理由。
- 只有设计语义本身存在会改变行为的歧义，或所需引擎行为尚未确认时，才应明确提出缺口；不得把普通的 ID 命名和定义编写工作推回给用户。
## 相同 Effect 的定义复用
- 如果多个引用位置需要的 Effect 在字段、参数、目标、条件、时序、生效次数要求等方面完全相同，并且这些位置的调用环境相似，则默认只创建一个目标 Mod 自有的 Effect 定义，再在各处重复引用同一个 `.name`。
- 最常见的情况是同一技能的不同等级都需要完全相同的效果。此时不要无理由创建 `effect_level_0`、`effect_level_1` 等多份内容相同的 Effect；各等级应引用同一个自定义 Effect ID。
- “复用同一 Effect”不等于复用原版或其他 Mod 的 Effect。除非满足前述例外条件，仍应使用目标 Mod 自己的独立 ID，避免同名分行、覆盖和加载顺序干扰。
- 如果同一技能所有等级对该 Effect 的引用位置和相对顺序也完全一致，并且抽取后不会改变 Effect 列表顺序或触发时序，可把这一个引用写入无等级共用分行。
- 如果各等级需要把该 Effect 放在不同的等级专用 Effect 之间，或抽入共用分行会改变预期引用顺序、时序或生效次数，则仍在每个等级行分别引用同一个 Effect ID；不要为了减少文本而复制 Effect 定义或破坏顺序。
推荐：
```darkest
combat_skill: .id "example_skill" .level 0 .atk 95%  .effect "mod_shared_effect"
combat_skill: .id "example_skill" .level 1 .atk 100% .effect "mod_shared_effect"
combat_skill: .id "example_skill" .level 2 .atk 105% .effect "mod_shared_effect"
```
如果时序和合并顺序允许，也可写为：
```darkest
combat_skill: .id "example_skill" .level 0 .atk 95%  .target 34
combat_skill: .id "example_skill" .level 1 .atk 100% .target 34
combat_skill: .id "example_skill" .level 2 .atk 105% .target 34
combat_skill: .id "example_skill" .effect "mod_shared_effect"
```
第二种写法仍需遵守技能分行中 `.target` 的特殊规则：非自身目标必须在每个等级的第一条定义中先有非空 `.target`；同等级后续行或无等级共用行不能补救首行缺失，其余分行无须重复填写。完整说明见：[技能同 ID 分行与无等级共用分行](../Mechanics/37-技能同ID分行与无等级共用分行.md)。
## Effect 定义的推荐排序
- 在同一 `*.effects.darkest` 中存在多组定义时，默认按**效果类别／功能**组织，而不是把某一技能等级所需的所有 Effect 全部堆在一起后再写下一个等级。
- 例如，等级间数值不同的流血 Effect 宜按“该技能的各等级流血”连续排列，减益 Effect 再按“该技能的各等级减益”连续排列。这样更便于人类纵向核对同类效果的成长差异。
- 如果若干 Effect 共同组成一个依赖严格顺序的迂回、施加—结算—善后链或其他不可拆分的逻辑单元，应优先把整套 Effect 放在一起，并按真实执行顺序排列；此时不要为了按类别分组而拆散迂回。
- 文件内定义顺序的可读性整理，不得改变技能或其他调用位置中的 Effect **引用顺序**。真正的触发顺序仍以调用方的引用顺序、AWR／queue 等时序和相应机制规则为准。
- 推荐排序优先级为：引擎语义与时序正确 > 迂回逻辑完整 > 同类效果聚合 > 等级顺序与视觉对齐。
完整排版原则见：[代码排版对齐与等级称呼歧义](../Mechanics/41-代码排版对齐与等级称呼歧义.md)。
## 常见骨架
`.name`、`.target`、`.on_hit`、`.on_miss` 通常都会显式出现，但目前没有完整资料证明除 `.name` 外还存在哪些通用必填字段。
```darkest
effect: .name "Push 3A" .target "target" .push 3 .chance 100% .on_hit true .on_miss false .can_apply_on_death true
```
- `.on_hit` 与 `.on_miss` 省略时默认值为 `false`，因此语法上可以不写；为避免 Effect 因两者均为 `false` 而不在命中或未命中时执行，通常显式填写。
- 上例来自游戏本体 `DarkestDungeon\effects\base.effects.darkest`。
- 同名 Effect 与分行的边界说明见：[Effect 同名与分行](../Mechanics/18-Effect同名与分行.md)。
## 默认值边界
- “几乎所有 Effect 关键字都可能存在默认参数值”目前只是推测，尚无逐字段完整整理。
- Agent 不得根据该推测补造具体默认值。关键行为依赖某字段时，应显式填写已确认的参数。
## 致命目标组合
- 同一条 Effect 只要存在有效 `.keyStatus`、`.monsterType` 或 `.skill_instant true`，`.target` 就绝对不得写为 `target` 或 `target_enemy_group`。
- 上述组合会使游戏必定立即崩溃，不是可忽略的红字或无效 Effect。
- 既有资料还把 `target_group`、`target_group_other` 列为 `.skill_instant true` 的不安全目标；在边界进一步确认前也不得使用。
## 目标最小化原则
- 没有绝对必要时，任何 Effect 都不得作用于设计范围之外的目标；`.target` 必须与实际设计对象一致。
- 不得为了绕开崩溃、迁就某种简写或减少代码量，把单体效果扩大成群体效果；`target_group` 不是 `target` 的通用替代品。
- 若某种简写无法在正确目标范围内安全实现设计，应更换实现方案，而不是扩大受术者范围。
- `.keyStatus`、`.skill_instant true`、`.monsterType` 的简写 Buff、默认来源和使用边界见：[Effect 条件简写与目标最小化](../Mechanics/35-Effect条件简写与目标最小化.md)。
