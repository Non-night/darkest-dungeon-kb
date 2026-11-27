# Buff 源与真驱散

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 2026-11-05 新版更新

新版所有饰品Trigger不再强制Buff源，允许Effect声明所需来源。原was_hit/kill_performer强制bsrc_trinket_additional_effect及必须转接size-0才能改源的限制已退休；生命周期和清除仍按实际来源检查。

详见[新版字段与修复](96-新版Modding更新Buff技能地牢饰品怪癖.md)及`Sources/modding_update_20261105_remaining.json`。

## 偷取的使用限制

偷取仍不建议使用：可能错误地偷走不该被偷的 Buff，只有在严格受控的环境中才可自由使用。收录偷取机制或含偷取的方案，不代表推荐在普通环境使用；“标志物”用途不提供隔离其他 Buff 的性质。当前用户于2026-11-03明确补充；非本轮新增实机测试。

## Buff 源声明
- `.buff_source_type <source>` 为 `buff_ids` 中声明的 Buff 指定来源。
- 参数是单个字符串；可以填写已收录或未收录的源标识。
- 未收录/非法参数不会创建新的自定义源类型；游戏引擎会将其统一视为 `combat_end` Buff 源。这里的 `combat_end` 是 Buff 源，不是持续时间类型。
- Buff 来源也可能由施加方式或其他专门字段决定。
- Buff 源会影响图标、清除方式和其他独有机制，不只是分类标签。完整的转置表见下文。

## 图标
源类型表的 `Icon` 行若写为 `None`，该来源下的 Buff 不具有图标；表格空白表示资料未填写，不等同于 `None`。

## 可见 Buff 的正负图标与 force_positive 合并显示

知识库编写者补充（2026-09-20）：对于大多数可见 Buff，正负数值通常分别显示在增益和减益图标里。这是带有“大多数／通常”限定的观察，不是所有 stat_type 都按 amount 正负分类的通用规则。

- 在可见来源、没有特殊处理的情况下，暴击 Buff A 为 +15%，同类 Buff B 为 -5%：增益图标显示 +15% 暴击，减益图标显示 -5% 暴击。
- 给 B 写 `"force_positive": true` 后，即使 B 本应显示为减益，也会进入增益图标，并与同类增益数值合并显示。该例只在增益图标显示 +10% 暴击，不再出现由 B 产生的减益图标；场上其他减益是否有图标不在此例结论内。
- `force_positive` 不把 B 的 -5% 改成 +5%。显示合并也不证明两个 Buff 实例、Rule、来源、持续时间或清除条件被合并，不能据此推断驱散行为。跨来源、不同 Rule／副类型等配置能否合并的完整条件尚未明确。

### 默认分类和来源例外

- 知识库编写者确认（2026-09-20）：`tag_blocked`（本次口述 tag_block，指无法被标记 Buff）在 `amount: 0` 时默认视为增益，无须另写 `force_positive: true`。这是分类结论；既有字段记录为 amount 大于 0 才阻止标记，零值不提供该实际效果。不要把 Pop 类型 `tag_block` 当成此 Buff 的 stat_type，也不推导其他数值分类或驱散结果。

- 亮度增减量变化 Buff `torch_increase_percent`、`torch_decrease_percent` 无论 amount 数值如何，默认都被视为减益，不能套用上述按正负分图标的通常表现。这里说的是默认分类，不否定显式 `force_positive: true` 的显示作用。
- “余生不回”来源 `bsrc_never_again` 下的同类 Buff 会自动合并正负数值；不要对该来源照搬普通可见来源的正负分开显示预期。此结论不等于任意不同类型 Buff 都能合并，也未指定其专属图标的完整表现。
- 无图标来源与可见来源分开判断；不能把 `force_positive` 当作让无图标来源生成图标的开关。

字段定义见 [Buff schema](../Buff/buff_schema.md)，长期 Buff 是否使用无图标源仍按本页对应小节处理。

## 长期 Buff 的无图标源选择

当前用户补充：如果 Buff 预计长期存在，或不会在施加后很快被清除，施加时应优先把它放入无图标 Buff 源，避免长期 Buff 图标造成不需要的界面/演出问题。当前推荐优先使用：

```text
bsrc_quest_failure
bsrc_vampire
```

这两个来源在源表中明确为 `Icon: None`，且当前用户认为它们比其他无图标来源更适合作为长期 Buff 的来源。其他 `Icon: None` 来源可能带有不合适的默认清除、语义或专属流程，不应因为“无图标”三个字就随意替换；必须逐源核对其用途和生命周期。

这条建议只针对需要长期保留的 Buff。瞬时 Buff、立即清理的逻辑门 Buff 和明确需要图标/专属来源语义的 Buff，仍按各自调用链选择来源。无图标源不能替代 `duration_type`、清理 Effect 或 Rule 生命周期设计。

## `.steal_buff_source_type`
`.steal_buff_source_type <source>` 会偷取目标身上属于指定来源的全部 Buff。

- 一般情况下，匹配 Buff 从目标转移给 Effect 发起者。
- 目标就是 Effect 发起者自身时，匹配 Buff 会直接消失，称为**真驱散**。
- 若由 size0 等特殊单位发起偷取，并在完成后自灭，最终效果也等同于真驱散。

该字段按来源批量处理，不是只处理某个 Buff ID。

## `.clear_debuff`：假驱散
`.clear_debuff 1` 会清除目标身上同时满足以下条件的 Buff：

- Buff 被游戏归类为减益。
- Buff 的 `is_clear_debuff_valid` 为 `true`。

即使增益 Buff 将 `is_clear_debuff_valid` 写为 `true`，也不会被 `.clear_debuff` 清除。因此社区将 `.clear_debuff` 称为**假驱散**：它受 Buff 的增益/减益分类及 `is_clear_debuff_valid` 限制，不能任意移除 Buff。

真驱散与假驱散的区别：

- `.clear_debuff`：按减益分类和 `is_clear_debuff_valid` 清除。
- 对自身使用 `.steal_buff_source_type`：按 Buff 源移除该来源下的全部 Buff，属于真驱散。

## 驱散溢出与 ID 定向驱散
- 旧式偷取／真驱散一次处理的 Buff 数量大于 `1024` 时必定崩溃；实际起崩点不确定。`1000` 是安全极限参考，大于 `1000` 有较高崩溃概率，小于 `1000` 也不保证不崩溃，只是概率更低；不得把该参考理解为安全保证。恰好 `1000` 或 `1024` 的必现性未单独确认。
- 数量边界由当前用户于2026-11-03补充确认，非本轮新增实机测试。迂回表第34条 P902–P906/X1055–X1059 的963未崩溃、1005已崩溃仅保留为当时测试观察，不推导统一精确阈值。该问题亦称驱散溢出／偷取溢出；按源调用须检查单个目标指定源下的匹配数量。原表先集中多个目标 Buff 再对自身真驱散的流程会集中数量，不能泛化所有真驱散均经过此流程。
- `clear_buffs_on_rule_active` 是按 Buff ID 列表清除的 **ID 定向驱散**，与按来源或类型批量偷取不同。
- ID 定向驱散的作用域严格限制在清理 Buff 的**持有者自身**：它只会检查并清除该持有者身上 ID 与列表项相同的 Buff，不能清除场上其他英雄、怪物或特殊单位身上的 Buff。
- 所有 Effect 简写形式生成的 Buff ID 都是空字符串 `""`。若列表中包含 `""`，会清除持有者身上全部简写 Buff，而不是只清除某一种简写效果，因此通常不建议这样写。
- 已有测试在其数组中填写 `16385` 个 Buff ID，所有对应 Buff 均成功移除，游戏仅轻微卡顿，没有发生驱散溢出。
- 当前只能确认 ID 定向驱散至少通过了 `16385` 项规模的测试，不能据此断言其绝对没有上限；上万项列表也不应视为常规安全设计。
- ID 定向驱散的作用域只限清理 Buff 持有者自身；列表中的 `""` 会命中该持有者身上全部 ID 为空的 Effect 简写 Buff，通常不得作为常规清理方案。
- ID 定向驱散的即时检测、链式清除、自清除及二段驱散用法见：[瞬时效果、正负相抵与二段驱散](25-瞬时效果、正负相抵与二段驱散.md)。

## 瞬间真驱散
瞬间真驱散是实现临时 Buff 的一种旧式方案：先施加临时 Buff，再执行依赖它的 Effect，最后对该来源使用 `.steal_buff_source_type`。它没有 Buff 残留，但仍受驱散溢出和来源误伤风险影响。

迂回表第 1 条 P349/X357 记录国内代码作者常将以下两个来源留给瞬间真驱散，以减少批量偷取对正常 Buff 的干扰：

```text
bsrc_last_hero
bsrc_flashback_start
```

当前用户于 2026-11-02 对原表 P350/X358 的用源经验作出更正：国外作者较常用 `bsrc_notspecified`、`bsrc_flashback_start`、`bsrc_last_hero` 做瞬间真驱散；国内较少使用 `bsrc_notspecified`，更常用后两者。`bsrc_battle_modifier` 可以用于瞬间真驱散，但不算常见，不能沿用原表把它与 `bsrc_notspecified` 一并列为 Sasiji 常用来源的概括。这些是作者实践的范围说明，不是引擎强制的源选择规则。

非必要不应将 `bsrc_notspecified`、`bsrc_flashback_start`、`bsrc_last_hero` 用作持久存在的 Buff 来源。`bsrc_battle_modifier` 在下方 Sasiji 来源表中的清除时机为 Any Update；按当前用户说明，它本来就不能承担持久 Buff 来源。`bsrc_flashback_start` 又称“蛇梦开始源”。

当前用户于 2026-11-02 补充确认：真光环源 `bsrc_battle_modifier` 需要图标且必定有图标，不得当作无图标来源。来源表 Icon 栏为空只表示未填写，不否定本次确认；其独立增益/减益图标与普通来源不共用，仍应按真光环的图标机制处理。

上述来源经验仅供解读旧式迂回。当前用户要求：在具备 `clear_buffs_on_rule_active` 的目标版本，瞬时 Buff 善后不采用按源瞬间真驱散，而应使用按 Buff ID 定向驱散；若目标版本不支持该字段，应单独说明兼容边界，不把旧方案默认为现行建议。流程、时序前提和 ID 定向替代方案见：[瞬时效果、正负相抵与二段驱散](25-瞬时效果、正负相抵与二段驱散.md)。

## 真光环源的短暂 buffFX 播放窗口
迂回表第86条 P1389–P1393/X1670–X1678 记录一种动画用途：由其他单位触发时，在具有相应动画资源的指定英雄上施加 `bsrc_battle_modifier` 来源的 Buff，借下一次 `Update` 前的短暂窗口播放 buffFX，随后由该来源的自动清除结束其存在。原表以队友触发阿比英灵饰品、在阿比本人播放动画为例；这里只保留该用途，不将具体 Mod 实现冒称本轮已核验。

此处仅使用来源的性质，不是怪物 `battle_modifier` 中 `.living_hero_buff_instance_ids`、`.living_other_enemy_buffs` 的真光环机制。清除按统一的 `Update` 机制处理，不固定为当前施法者回合结束，也不依赖被播放动画英雄的自身回合。窗口不保证动画完整播放、任意次数重播或无副作用；不用于依赖精确存续时间的功能迂回。真光环源需要且必有图标的已确认边界仍适用，不称无图标方案。这里的动画生命周期用途不撤销瞬时功能 Buff 优先按 ID 定向驱散的要求。当前用户于2026-11-04确认用途及以上边界；非本轮新增实机测试。

## Sasiji 的 Buff 源类型表（转置版）
以下内容将术语表工作簿中的横向表转置为“一行一个源”，供 Agent 直接检索。`—` 表示原表该单元格为空；原表明确写出的 `None` 保留为 `None`。

### 基础属性
| ID Number | 源 ID | 中文名称/释义 | Icon | 游戏内默认来源 | Safe to use |
|---:|---|---|---|---|---|
| 0 | `bsrc_notspecified` | （红钩原版未使用） | None | ? | Yes |
| 1 | `bsrc_skill` | 技能 | — | Default for Skills | — |
| 2 | `bsrc_instantSkill` | skill_instant专属 | None | No Default Sources, .skill_instant Cause buff source | — |
| 3 | `bsrc_affliction` | 折磨 | None | Afflictions | Yes |
| 4 | `bsrc_virtue` | 美德 | None | Vitrue | Yes |
| 5 | `bsrc_quirk` | 怪癖 | None | Quirks | — |
| 6 | `bsrc_trinket` | 饰品 | None | Trinkets | — |
| 7 | `bsrc_trinket_set` | 饰品套装效果 | None | Trinket Sets | — |
| 8 | `bsrc_campingskill` | 扎营 | — | Camp buffs | — |
| 9 | `bsrc_deathsdoor` | 死门 | None | Deathdoor | Yes |
| 10 | `bsrc_town` | 城镇活动 | — | Happens in stress  healing facilities | — |
| 11 | `bsrc_curio` | 奇物 | — | Curios | Yes |
| 12 | `bsrc_stun` | 眩晕 | — | After Stun | Yes |
| 13 | `bsrc_guard` | 守护 | None | Default source of .guard effect | Yes |
| 14 | `bsrc_riposte` | 反击 | — | No Default Sources, .riposte Cause buff source | Yes |
| 15 | `bsrc_item` | 物品 | — | No Default Sources, .item Cause buff source | Yes |
| 16 | `bsrc_disease` | 疾病 | None | Diseases | — |
| 17 | `bsrc_companion` | 同伴（投锚手给船长加buff） | — | Crew fight, Anchored gives it to captain | Yes |
| 18 | `bsrc_deathsdoor_recovery` | 重创（死门恢复） | — | Deathdoor Recover | Yes |
| 19 | `bsrc_deathsdoor_recovery_heart_attack` | 心衰恢复 | — | Heartattack | Yes |
| 20 | `bsrc_quest_failure` | 任务失败 | None | Quest Fail Parameter | Yes |
| 21 | `bsrc_completed_darkest_dungeon_quest_party_hero` | DD本成功完成任务“老兵”入队给队友的经验值增益 | None | Hero that was in DD gives Aura of exp | Yes |
| 22 | `bsrc_town_event` | 城镇事件 | — | Town Event | — |
| 23 | `bsrc_vampire` | 血裔 | None | ? | Yes |
| 24 | `bsrc_never_again` | DD本的“余生不回”规则 | — | Going again to Darkest Dungeon | Yes |
| 25 | `bsrc_battle_modifier` | 怪物侧的真光环 | — | Aura like Virago Shroom | — |
| 26 | `bsrc_district` | 区域建筑 | None | Districts | — |
| 27 | `bsrc_torchsettings` | 火把 | None | torch | — |
| 28 | `bsrc_flashback_start` | 破盾闪回（蛇梦）开始 | None | No Default Sources, forced source for couple effects | — |
| 29 | `bsrc_flashback_result` | 破盾闪回（蛇梦）结束 | — | Buff After Flashback, also in camp after beating them | — |
| 30 | `bsrc_crit` | 暴击 | — | No Default Sources, forced source for couple effects | Yes |
| 31 | `bsrc_trinket_additional_effect` | 饰品触发的effect | — | Effects from trinkets | — |
| 32 | `bsrc_quest_modifier` | 任务修正 | None | ? | — |
| 33 | `bsrc_last_hero` | 最后存活英雄（马戏团DLC） | None | Butcher Circus | Yes |
| 34 | `combat_end` | （红钩原版未使用，注意这是buff源类型，不是“一场战斗”的那个持续时间类型，勿混淆） | — | Not used by anything, base source of invalid sources | Yes |

### 自动清除时机
| 源 ID | Clear Debuff | Battle End | Camp | Quest End | Quitting Game | Death |
|---|---|---|---|---|---|---|
| `bsrc_notspecified` | No | No | Yes | Yes | Yes | No |
| `bsrc_skill` | Yes | No | Yes | Yes | No | No |
| `bsrc_instantSkill` | Not Valid | Not Valid | Not Valid | Not Valid | No | Not Valid |
| `bsrc_affliction` | No | No | Yes | No | Yes | No |
| `bsrc_virtue` | No | No | No | Yes | Yes | No |
| `bsrc_quirk` | No | No | No | No | Yes | No |
| `bsrc_trinket` | No | No | No | No | Yes | Yes |
| `bsrc_trinket_set` | No | No | No | No | Yes | Yes |
| `bsrc_campingskill` | Yes | No | Yes | Yes | No | No |
| `bsrc_deathsdoor` | No | No | No | Yes | Yes | No |
| `bsrc_town` | No | No | No | Yes | No | No |
| `bsrc_curio` | Yes | No | Yes | Yes | No | No |
| `bsrc_stun` | No | No | Yes | Yes | No | No |
| `bsrc_guard` | No | Yes | No | Yes | No | No |
| `bsrc_riposte` | No | Yes | No | Yes | No | No |
| `bsrc_item` | Yes | No | No | Yes | No | No |
| `bsrc_disease` | No | No | No | No | Yes | No |
| `bsrc_companion` | No | No | No | No | Yes | No |
| `bsrc_deathsdoor_recovery` | No | No | No | Yes | Yes | No |
| `bsrc_deathsdoor_recovery_heart_attack` | No | No | No | Yes | Yes | No |
| `bsrc_quest_failure` | No | No | No | Yes | No | No |
| `bsrc_completed_darkest_dungeon_quest_party_hero` | No | No | No | Yes | Yes | No |
| `bsrc_town_event` | No | No | No | No | No | No |
| `bsrc_vampire` | No | No | No | No | No | No |
| `bsrc_never_again` | No | No | No | Yes | Yes | No |
| `bsrc_battle_modifier` | No | Not Valid | Not Valid | Not Valid | Not Valid | Not Valid |
| `bsrc_district` | No | No | No | No | No | No |
| `bsrc_torchsettings` | No | Yes | No | Yes | Yes | No |
| `bsrc_flashback_start` | No | No | No | Yes | No | No |
| `bsrc_flashback_result` | No | No | No | Yes | No | No |
| `bsrc_crit` | Yes | No | Yes | Yes | No | No |
| `bsrc_trinket_additional_effect` | No | No | No | Yes | No | No |
| `bsrc_quest_modifier` | No | No | No | Yes | Yes | No |
| `bsrc_last_hero` | No | No | No | Yes | Yes | No |
| `combat_end` | No | No | No | No | Yes | No |

### 其他清除方式与机制
| 源 ID | Also Cleared By | Uniq Properties | 补充说明 |
|---|---|---|---|
| `bsrc_notspecified` | None | None | — |
| `bsrc_skill` | None | None | — |
| `bsrc_instantSkill` | on Updates 状态更新时（任意单位回合结束/开始、镜头缩放等）<br>交错按下技能而不实际施法时，也会自动移除前一个的该源类型 | None | — |
| `bsrc_affliction` | Base: 0 Stress If Afflicted （压力0时自动移除折磨） | ignore_stealth buff is shown on Affliction icon during affliction<br>无视潜行buff会在折磨图标上显示描述（原因出自农场折射） | — |
| `bsrc_virtue` | Base: 200 Stress if virtued（压力200时自动移除美德）<br>.clear_virtue 强制移除美德代码 | ignore_stealth buff is shown on Virtue icon during Vitrue<br>无视潜行buff会在美德图标上显示描述（原因出自农场折射） | — |
| `bsrc_quirk` | None | None | — |
| `bsrc_trinket` | None | None | — |
| `bsrc_trinket_set` | None | None | — |
| `bsrc_campingskill` | None | None | — |
| `bsrc_deathsdoor` | 英雄0血时显示的【红骷髅图标】脱离死门时清除此源的buff | Shown on Death Door Icon | — |
| `bsrc_town` | None | None | — |
| `bsrc_curio` | None | None | — |
| `bsrc_stun` | None | None | — |
| `bsrc_guard` | None | Infinite Duration | — |
| `bsrc_riposte` | .clear_riposte 1 | Buffs Affect Only Riposte<br>此源内的buff仅对反击有效 | — |
| `bsrc_item` | None | None | — |
| `bsrc_disease` | None | None | — |
| `bsrc_companion` | None | None | — |
| `bsrc_deathsdoor_recovery` | remove_deaths_door_recovery_buffs<br>注意：强制扣除生命上限到死门然后脱离死门时则不会自动移除 | Count as Recovery for Camp Skills <br>对于扎营代码而言，本源视为“移除重创”里的所谓重创 | 若进入死门前不具有心衰减益<br>离开死门时得到源为重创减益的重创减益buff |
| `bsrc_deathsdoor_recovery_heart_attack` | remove_deaths_door_recovery_buffs<br>注意：强制扣除生命上限到死门然后脱离死门时则不会自动移除 | Count as Recovery for Camp Skills<br>对于扎营代码而言，本源也视为“移除重创”里的所谓重创 | 若进入死门前具有心衰减益<br>离开死门时优先得到源类型为心衰减益的心衰减益debuff<br>而非死门恢复减益debuff |
| `bsrc_quest_failure` | None | None | — |
| `bsrc_completed_darkest_dungeon_quest_party_hero` | None | None | — |
| `bsrc_town_event` | None | Only Buffs have icon<br>当前用户于2026-10-12更正：amount <= 0 的 Buff 无法显示描述；amount > 0 时增益和减益均可显示描述。 | — |
| `bsrc_vampire` | None | None | — |
| `bsrc_never_again` | None | None | — |
| `bsrc_battle_modifier` | Any Update | buff and debuff icons Dont Stack with ones from other sources<br>真光环具有独立的一组增益和减益图标，且可由光环发起者怪物进行自定义 | — |
| `bsrc_district` | None | None | — |
| `bsrc_torchsettings` | None | None | — |
| `bsrc_flashback_start` | None | Makes Horror uncurable<br>此源以及扎营源引出的恐惧均不可被治愈（鸦片酊） | — |
| `bsrc_flashback_result` | None | None | — |
| `bsrc_crit` | None | None | — |
| `bsrc_trinket_additional_effect` | None | Buffs from Was-Hit triggers Always have this source<br>饰品受击特效引出buff永远为此源，另行声明无效 | — |
| `bsrc_quest_modifier` | None | None | — |
| `bsrc_last_hero` | None | None | — |
| `combat_end` | None | It doesnt show how much add/remove from stats in character sheet<br>此源引出的增减益即使对角色面板属性有影响，鼠标移到对应属性也不可见具体修正详情 | 非法（不实际存在）的源类型声明，将一律被纳入该源类型 |

## 扎营有自动清除例外的 Buff 类型

上表 `Camp` 一列是按源类型划分的通常规则。迂回表第 243 条《声明为扎营自动移除的源类型时，存在并不会在扎营时自动移除的特例buff一览表》记录了以 `bsrc_campingskill` 测试时，跨过再次扎营仍保留的 46 个 `stat_type`。条目 154 另记录 `quirk_tag_evolution_duration` 在 `bsrc_crit` 和扎营源上的同类表现。两条均为社区历史测试；第 243 条整份清单的测试源为 `bsrc_campingskill`，其他源和当前版本未逐项复测。

- `ambush_chance`
- `activity_side_effect_chance`
- `vampire_evolution_duration`
- `quirk_evolution_death_immune`
- `disable_combat_skill_attribute`、`hp_dot_bleed`、`hp_dot_poison`
- `hp_dot_heal`、`stress_dot`、`shuffle_dot`、`vampire`
- `torch_increase_percent`、`torch_decrease_percent`
- `stress_on_miss`
- `stress_from_idle_in_town`
- `shard_reward_percent`、`shard_consume_percent`
- `hp_dot_bleed_duration_received_percent`、`hp_dot_bleed_duration_percent`、`hp_dot_bleed_amount_received_percent`、`hp_dot_bleed_amount_percent`
- `hp_dot_poison_duration_received_percent`、`hp_dot_poison_duration_percent`、`hp_dot_poison_amount_received_percent`、`hp_dot_poison_amount_percent`
- `stress_dot_duration_received_percent`、`stress_dot_duration_percent`
- `stress_dot_amount_received_percent`、`stress_dot_amount_percent`
- `hp_heal_dot_duration_received_percent`、`hp_heal_dot_duration_percent`、`hp_heal_dot_amount_received_percent`、`hp_heal_dot_amount_percent`
- `shuffle_dot_duration_received_percent`、`shuffle_dot_duration_percent`
- `guard_duration_received_percent`、`guard_duration_percent`
- `cure_bleed_received_chance`、`cure_poison_received_chance`、`cure_bleed_chance`、`cure_poison_chance`
- `transfer_debuff_from_attacker_chance`、`transfer_buff_from_attacker_chance`
- `quirk_tag_evolution_duration`
- `buff_duration_percent`
- `riposte_duration_percent`

迂回表中 `upgrade_discount` 在使用可由扎营清除的源时正常清除，`quirk_tag_evolution_duration` 则保留。用于自定义描述时，冷却或充能逻辑与其可见描述应分别核对扎营后的状态。`disable_combat_skill_attribute` 也在例外清单中，使用它实现的冷却可能跨过扎营。

后续存档对照还记录了 `hp_dot_burn_amount_percent` 的扎营源实例留存，详见[再次扎营的存档对照](49-扎营技能文件、通用专属分类与图标.md)。

### 存档编号与 DLC 新增类型的待验证关系

知识库编写者推测，随 DLC 新增的 `stat_type` 可能都能跨扎营保留，目前暂未发现已确认首发归属且经直接对照的反例。存档编号只能辅助定位批次。迂回表第 243 条自述覆盖当时的 Buff 类型，正文列出保留项，未附逐项负结果日志。按现有编号表对照，已列出的例外散布在 `4–86`。`1–87` 另有 41 个编号未列为例外，其中 `23`（`upgrade_discount`）有明确的正常清除对照。

| 编号 | 本地游戏定义与扎营证据 |
|---|---|
| `31`、`38–39` | `31` 为 `vampire`，`38–39` 为 `quirk_evolution_death_immune`、`vampire_evolution_duration`，后两项可在猩红庭院 `crimson_court.buffs.json` 中核对。三项均列入第 243 条。可将 `31` 视为目前可辨认的血病相关批次线索。 |
| `41–42`、`44` | `tag_blocked`、`ignore_protection`、`guard_blocked` 均见破盾 DLC 的 `shared/buffs/shieldbreaker.buffs.json`，均未列入保留清单。其首次引入版本与逐项清除结果尚待核对。 |
| `46–48` | 农庄 DLC 的 `shared/buffs/com.buffs.json` 直接使用 `damage_reflect_percent`（`46`）、`shard_reward_percent`（`47`）和 `shard_consume_percent`（`48`）。`47–48` 有历史保留记录，`46` 未列入清单，首发归属与直接清除结果待核对。 |
| `88–94` | 当前编号表里的连续燃烧相关区段。`89`（`hp_dot_burn_amount_percent`）已有再次扎营留存实例。`88`、`90–94` 未见同条件测试记录。 |

Fire's Edge Modding Features 新文档中另有七个尚未核定数字 ID 的属性：`crit_dmg_add`、`crit_dmg_multiply`、`disable_combat_skill`、`effect_chance`、`heal_crit_chance_add`、`heal_crit_chance_multiply`、`hp_heal_amount_received`。目前按文档确认其为新记录字段，首发版本、是否属于付费 DLC 与扎营保留行为分别待核对。现有资料可以定位 `88` 为燃烧相关编号区段的起点，DLC 新增类型尚无统一编号分界。

对照依据：[存档 Buff 类型编号表](../Buff/stat_type_amount_classification.md)、迂回表第 243 条、上述本地游戏定义，以及 `Sources/modding_update_20261105_remaining.json`。

## 用 `in_camp` 定向驱散模拟扎营清除

对于扎营时不会自动清除的特殊 Buff，可在同一持有者身上挂一个清理 Buff。清理 Buff 用 `rule_type: in_camp` 和 `remove_if_not_active: false`，以便在非扎营期间留存。它的 `clear_buffs_on_rule_active` 列出目标 Buff 的专用 ID 和清理 Buff 自身的 ID。扎营 Rule 成立时，列表会先处理清除目标，再移除清理 Buff 自身。目标 Buff 应使用有专用 ID 的完整定义，空 ID 会匹配该持有者身上的全部简写 Buff。清理 Buff 的源和持续时间须允许它留到需要清理的扎营节点。见[扎营 Rule](../Buff/rule_type/in_camp.md)和[定向驱散及自清除](25-瞬时效果、正负相抵与二段驱散.md#clear_buffs_on_rule_active-的关键性质)。

- **目标 Buff 在扎营内获得**时，先同步挂一个能在战斗中触发的一次性附魔，可选战斗开始、轮次结束、个人回合开始或个人回合结束。选定节点发生时，附魔给目标 Buff 的持有者施加上述清理 Buff，成功挂上后再定向驱散承载这次附魔的 Buff。如果直接在当前扎营挂清理 Buff，`in_camp` 当时可能已经成立，目标 Buff 会立刻被清掉。如果下次扎营前未经过选定节点，例如连续扎营且中途没有战斗，清理 Buff 尚未挂上，下次扎营就会漏清。
- **目标 Buff 仅在扎营外获得**时，在每条施加路径上直接给同一持有者挂清理 Buff，例如战斗或奇物施加时一并挂上。只要清理 Buff 成功施加并存续到下次扎营，`in_camp` 成立时就会清除目标和自身。这条路径在下一次扎营前无需经过战斗节点，可覆盖连续扎营的情形。

方案由知识库编写者于 2026-11-27 提出。上述顺序依据已有 Rule 和定向驱散机制推导，整套组合、进入扎营时的实际生效节点，以及夜袭等特殊衔接仍待实机核对。

## `bsrc_town_event` 的 Buff 描述显示边界

当前用户于 2026-10-12 更正：`bsrc_town_event` 并非不能显示减益描述。实际边界按 Buff 的 `amount` 判断：`amount <= 0` 时该来源的 Buff 无法显示描述；`amount > 0` 时，无论该 Buff 按默认分类属于增益还是减益，都可以显示描述。不要把“无法显示非正 amount 的描述”简化为“无法显示减益”。

此规则描述的是 Buff 描述显示，不代表图标分类或实际增益/减益效果由来源决定；仍需分别按 Buff 的 stat_type、amount 与来源规则判断。

## `.clearvirtue` 与美德源
- `.clearvirtue 1` 是否等同于驱散美德来源的 Buff，尚未确认。
- 在该关系确认前，不要用 `.clearvirtue` 推断或替代 `.steal_buff_source_type` 的来源清除逻辑。

## 使用边界
- 使用前必须确认同一来源下是否还有其他不应被清除的 Buff。
- 社区资料不建议对 `bsrc_district` 或 `bsrc_skill` 使用真驱散。
- 迂回表第 1 条 P352/X362 的设计安全告诫，经当前用户于 2026-11-02 确认纳入：真驱散只用于迂回的机制设计，不作为提升强度的手段；不得借它直接解除其他作者设计中本应不可驱散的增减益。原表警示这可能破坏对方设计，甚至造成崩溃或不可逆的存档变动；后两项是风险警告，不等于已证明每次如此操作都会发生。
