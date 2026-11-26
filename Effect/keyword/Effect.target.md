# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.target
# 分类
核心流程
# 参数类型
枚举/固定候选值
# 参数约束
- 参数为单个字符串，必须使用已收录的目标类型。
- 使用 `target_enemy_rank` 时，同一逻辑 Effect 必须填写 `.clear_rank_target <站位>`。
- `this_trinket` 只用于存在明确饰品发起者的调用流程；依赖该目标的饰品字段不得改用普通单位目标。
- 同一条 Effect 只要存在有效 `.keyStatus`、`.monsterType` 或 `.skill_instant true`，`.target` 就绝对不得写为 `target` 或 `target_enemy_group`；该组合会使游戏立即崩溃。
- 知识库编写者2026-11-05明确补充：使用同名Effect分行迂回时，各分行不得省略.target；省略会黑屏报错，按Esc可继续正常游戏，但对应Effect是否正常生效尚未确认。不能依赖其他分行提供.target来省略本行字段。此要求针对Effect分行，不推广为技能Info中.target的默认规则。 来源：Sources/effect_split_target_required_20261105.json。
# 固定值 / 参数候选
- `performer`
- `performer_group`
- `performer_group_other`
- `target`
- `target_group`
- `target_group_other`
- `target_enemy_group`
- `global`
- `target_enemy_rank`
- `this_trinket`
- `target_enemy_random`
- `target_hero_random`
- `performer_adjacent_random`
- `performer_adjacents`
- `performer_adjacent_front`
- `performer_adjacent_behind`
- `target_adjacent_random`
- `target_adjacents`
- `target_adjacent_front`
- `target_adjacent_behind`
- `other_trinket`
# 语义
- `.target <target_type>`：指定 Effect 的实际作用对象。
- `target_enemy_rank`：只对 `.clear_rank_target` 指定站位中的敌方目标生效。
- `this_trinket`：目标为触发该 Effect 的饰品本身；配合 `.buff_ids` 可使该饰品永久获得对应 Buff。
- `target_enemy_random`：随机选择一个怪物作为目标。
- `performer_group_other`：选择 Effect 施术者所在一侧除施术者本人以外的全体队友。
- `target_hero_random`：随机选择一名英雄；与 target_enemy_random 的随机怪物区分，不按施术者友敌关系替换。
- `performer_adjacent_random`：以施术者为参照，随机选择一个相邻单位。
- `performer_adjacents`：以施术者为参照，选择两侧相邻单位。
- `performer_adjacent_front`：选择施术者前方相邻单位。
- `performer_adjacent_behind`：选择施术者后方相邻单位。
- `target_adjacent_random`：以原目标为参照，随机选择一个相邻单位。
- `target_adjacents`：以原目标为参照，选择两侧相邻单位。
- `target_adjacent_front`：选择原目标前方相邻单位。
- `target_adjacent_behind`：选择原目标后方相邻单位。
- `other_trinket`：选择另一装备饰品槽；三个及以上槽位时，取最左侧非发起饰品所在槽，可能为空，即使更后面的槽已装备饰品。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 群攻技能会按其每个单体目标分别执行 Effect；检查重点是各次调用的最终受术者集合是否重叠，只要同一单位被多个调用轮次再次选中，就可能按目标数重复生效，Effect 再指向群体只是典型案例。
- 群体最终目标通常按 rank 从低到高应用。
- 详见：[Mechanics/02-target与群攻重复.md](../../Mechanics/02-target与群攻重复.md)
- 当前用户2026-11-04确认：同名 Effect 分行重复填写 `.target` 时，后写／后加载的值覆盖前者；加载顺序沿用已记录的 `.buff_ids` 分行顺序。为只补充多参数而不改变目标，应保持各处 `.target` 一致；这不是不同目标时禁止合并的语法条件。未填写字段的默认／继承行为不由此推断，详见机制18。
- `target_enemy_rank` 不会自行提供站位范围；缺少 `.clear_rank_target` 时不要使用。
- `this_trinket` 可供触发次数修改、获得/销毁饰品及饰品自身 Buff 等字段定位发起饰品。
- `target_enemy_random` 的目标选择由引擎随机完成。
- spawn 定向只改变 spawn 流程的默认目标，不改变 `performer_group_other` 对施术者侧队友的选择；因此该目标值与是否填写 `.spawn_target_actor_base_class_id` 无关。
- `.swap_source_and_target true` 在目标已经选定后逐个交换施术者与受术者；当目标为 `performer_group_other` 时，表现为各队友分别成为施术者，并对原施术者释放该 Effect。
- 致命组合：有效 `.keyStatus`、`.monsterType`、`.skill_instant true` 三者任一与 `.target "target"` 或 `.target "target_enemy_group"` 位于同一条 Effect 时，游戏必定立即崩溃。
- Buff 同侧/异侧看最终指向；同侧不计算减益施加率和减益抗性。指向异侧仍按同侧的已确认特例为 target_enemy_group、target_group_other、target_enemy_rank；target_enemy_random 仅当前用户2026-11-02表示“好像”的待确认线索。target、target_group 等常规目标按最终指向判断。普通 Effect 独立抗性及其他生效门另核。统一已有证据见 Mechanics/95-Buff同侧异侧与减益概率判定.md。
- 新目标的空位、大体型、阵营边界及特殊抗性语义未由文档说明，不从旧目标特例外推。other_trinket 是饰品目标；三个及以上槽位选最左非自身槽，可为空。
- 知识库编写者2026-11-11实测：技能直接引用或饰品静态Buff附魔中，目标this_trinket/other_trinket的Effect内一切效果均不生效。饰品Trigger之外的其他调用位置大概率同样无意义，仍是推测。this_trinket不额外渲染目标描述，other_trinket会；描述显示不证明运行时生效。不否定饰品Trigger内set_trigger_limit等已有支持。来源：Sources/trinket_target_effect_scope_20261111.json。
# 常见错误
- 写 `target_enemy_rank` 却漏写 `.clear_rank_target`。
- 把 `this_trinket` 理解为饰品佩戴者；它指向发起 Effect 的饰品本身。
- 把 `target_enemy_random` 理解为随机任意单位；该值选择的是随机怪物。
- 将 `target` 或 `target_enemy_group` 与有效 `.keyStatus`、`.monsterType`、`.skill_instant true` 任一项写在同一条 Effect。
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

# Fire’s Edge 新目标值案例
- `target_enemy_rank`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:98`
```darkest
effect: .name "RW Backdraft Cure Burn" .target "target_enemy_rank" .clear_rank_target 1 .chance 100% .cure_burn 1 .on_hit true .on_miss true .queue true
```
- `this_trinket`：`DarkestDungeon\dlc\4964110_fires_edge\effects\rd.effects.darkest:7`
```darkest
effect: .name "On Quest Complete This Trinket DMG" .target "this_trinket" .curio_result_type "positive" .chance 100% .buff_ids "TB_DMG_B_1_L" "TB_DMG_B_1_H" .on_hit true .on_miss true .queue true
```
- `target_enemy_random`：`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\effects\runaway.effects.darkest:126`
```darkest
effect: .name "On Round End If in Inventory Random Monster Burn" .target "target_enemy_random" .curio_result_type "positive" .chance 100% .dotBurn 2 .dot_irresistible true .is_in_inventory true .on_hit true .on_miss true .queue true .is_trigger_effect true .can_apply_on_death true
```

## 新版新增目标类型（2026-11-05采纳）

| `.target` 值 | 目标语义 |
|---|---|
| `target_hero_random` | 随机选择一名英雄；与 target_enemy_random 的随机怪物区分，不按施术者友敌关系替换。 |
| `performer_adjacent_random` | 以施术者为参照，随机选择一个相邻单位。 |
| `performer_adjacents` | 以施术者为参照，选择两侧相邻单位。 |
| `performer_adjacent_front` | 选择施术者前方相邻单位。 |
| `performer_adjacent_behind` | 选择施术者后方相邻单位。 |
| `target_adjacent_random` | 以原目标为参照，随机选择一个相邻单位。 |
| `target_adjacents` | 以原目标为参照，选择两侧相邻单位。 |
| `target_adjacent_front` | 选择原目标前方相邻单位。 |
| `target_adjacent_behind` | 选择原目标后方相邻单位。 |
| `other_trinket` | 选择另一装备饰品槽；三个及以上槽位时，取最左侧非发起饰品所在槽，可能为空，即使更后面的槽已装备饰品。 |

- 相邻目标以 performer 或原 target 为参照；不要把说明文字中的 `x_front`／`x_behind` 当成实际枚举，实际字段含 `_adjacent_`。
- `other_trinket` 是饰品目标，不是饰品佩戴者。文档明确支持以饰品为目标的 `.set_trigger_limit`；不要继续一概要求目标只能为 `this_trinket`。其他操作字段能否作用于另一槽位饰品，应按字段证据分别核对。
- 文档没有说明空位、大体型、阵营边界、首尾目标缺失、多名相邻者的处理与新目标的特殊抗性规则；不能套用旧目标特例补造这些行为。
- AOE 仍需逐次计算最终受术者集合；新增相邻目标不自动提供整次技能去重。`performer_adjacents`／`target_adjacents` 可产生多个目标，实际独立掷骰语义仍按对应机制证据核对。
- 来源：新版《Darkest Dungeon Modding Update | Feature List》B010–B017；Review/2026-11-05-Modding-Update/source.md；当前用户于2026-11-05要求采纳，且已明确新版文档优先。本次没有新增实机测试。

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Fire’s Edge Modding Features 无夜译注表的 `New target` 部分。
- 官方 Fire’s Edge DLC 的 Runaway 与饰品 Effect 实例。
- 新版《Darkest Dungeon Modding Update | Feature List》B010–B017；Review/2026-11-05-Modding-Update/source.md；当前用户于2026-11-05要求采纳，且已明确新版文档优先。本次没有新增实机测试。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
