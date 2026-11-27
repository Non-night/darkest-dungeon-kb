# target、群攻重复与 apply_once

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


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

### 饰品目标的调用边界与描述差异

知识库编写者2026-11-11实测：技能中直接引用目标为 `this_trinket` 或 `other_trinket` 的Effect，其中一切效果均不会生效；饰品静态Buff附魔中也相同。饰品Trigger之外的其他调用位置使用这两个目标大概率均无意义，但这部分仍是推测，不能写成已完全验证。饰品Trigger内 `.set_trigger_limit` 等既有支持不因此撤回。

实测描述差异：`this_trinket` 不会专门渲染“目标：”“队伍：”等目标描述，而 `other_trinket` 会渲染目标描述。未确定后者具体显示的本地化文字，不补造标签名称；描述渲染不等于Effect实际生效。来源：`Sources/trinket_target_effect_scope_20261111.json`；Agent未自行游戏测试。

### 新增目标的其他边界
- 文档没有说明空位、大体型、阵营边界、首尾目标缺失、多名相邻者的处理与新目标的特殊抗性规则；不能套用旧目标特例补造这些行为。
- AOE 仍需逐次计算最终受术者集合；新增相邻目标不自动提供整次技能去重。`performer_adjacents`／`target_adjacents` 可产生多个目标，实际独立掷骰语义仍按对应机制证据核对。
- 来源：新版《Darkest Dungeon Modding Update | Feature List》B010–B017；Review/2026-11-05-Modding-Update/source.md；当前用户于2026-11-05要求采纳，且已明确新版文档优先。本次没有新增实机测试。

## 群攻调用
群攻技能通常按每个单体目标分别调用其 Effect；`.target` 再把本次调用提供的目标映射为最终目标。

## Effect 自带对群与 `.target` 的区别

当前用户补充：`kill_enemy_types` 虽然名称和参数看起来像“对一组怪物操作”，但它本身不自带对群范围；它仍然只作用于该 Effect 的最终目标，最终目标由 `.target` 决定。若 `.target target`，只处理当前目标；若明确写 `.target target_group` 或其他群体目标，才按该目标映射处理。

目前 Effect 中确认的自带对群效果只有 `.shuffleparty`（群体乱位）。除 `.shuffleparty` 外，其他 Effect 都不能仅凭字段名称或参数看起来像复数，就推断为自动作用于目标群体；必须逐条检查 `.target` 和调用方提供的目标集合。

| 写法 | 最终范围 |
|---|---|
| `kill_enemy_types` + `.target target` | 当前 Effect 目标；按参数筛选能处理的 enemy_type，不自动扩展到目标群体 |
| `kill_enemy_types` + `.target target_group` | 由 `.target target_group` 映射出的群体 |
| `.shuffleparty` | 当前确认的 Effect 自带对群逻辑；仍须核对调用方和目标上下文 |

| 调用情况 | apply_once | 常见结果 |
|---|---:|---|
| 群攻，Effect 指向 `target` | false | 对每个技能目标各生效一次 |
| 群攻，Effect 指向 `target` | true | 同名 Effect 通常只实际生效一次 |
| 群攻，Effect 指向群体 | false | 每个调用目标都触发一次全体 Effect，造成全体重复 N 次 |
| 群攻，Effect 指向群体 | true | 首次实际生效后抑制同名 Effect 的后续重复，通常全体一次 |
| 单体技能内重复调用同名 Effect | true | 已观察到只实际生效一个 |
| 饰品 Trigger 等流程重复调用同名 Effect | true | 也会受到去重干涉 |

## AOE 中必须检查是否需要 `apply_once`
AOE 技能会按照调用方提供的每个目标分别调用所引用的 Effect。因此，不能只看到技能本身是“一次群攻”，就默认其中每条 Effect 也只执行一次。

检查重点**不只是 Effect 是否再次指向群体**，而是每轮调用产生的最终受术者集合是否重叠。只要同一最终单位会在多个 AOE 调用轮次中再次成为受术者，就可能按技能目标数反复承受同一 Effect。典型情况包括但不限于：

- `.target performer`：每轮调用最终都落回同一个施术者；
- `.target performer_group`：每轮调用都再次作用于施术者方全体；
- `.target target_group` 等群体映射：不同外层调用产生重叠的最终目标集合；
- `.skill_instant true` 用于修饰同一个施术者或同一次技能结果：如果未写 `.apply_once true`，可能随每个 AOE 目标重复施加，使技能目标越多，当前技能获得的修正越强；
- 其他任何让不同外层调用最终落到同一单位或同一组单位的目标映射或条件简写。

群体映射仍是最直观的放大案例。例如：

```text
AOE 技能目标数 = 4
Effect.target = performer_group
Effect.apply_once = false
```

该 Effect 会因 4 个技能目标而被调用 4 次，并在每次调用中作用于整个施术者方队伍，即全队各承受 4 次；AOE 只有 3 个调用目标时，全队各承受 3 次。但即使最终目标只是同一个施术者，只要每轮调用都重新作用于该施术者，也同样存在按 AOE 目标数重复叠加的问题。

因此，制作或审查 AOE 技能时，必须逐条检查其引用的 Effect：

1. 该 Effect 是否会按每个 AOE 目标重复调用；
2. 每轮调用经过 `.target`、`.skill_instant` 或其他机制映射后，最终受术者分别是谁；
3. 各轮最终受术者集合是否重叠，是否会让同一单位多次获得伤害、治疗、压力、Buff、DOT、技能修正或其他可明显叠加的结果；
4. 设计需要“整次技能只执行一次”，还是有意要求“随技能目标数量增加而重复叠加”。

如果重复结果会明显叠加，而用户的设计没有明确说明是否允许随 AOE 目标数量增加，则这是会改变技能强度和机制的实质性歧义，**必须先询问用户设计意图**，不得自行添加或省略 `.apply_once true`：

- 用户要求整次技能只执行一次：通常考虑 `.apply_once true`，同时仍须检查同名 Effect 去重会不会误伤同一流程中的其他预期调用。
- 用户要求每个 AOE 目标都带出一次：保留重复调用，通常不写 `.apply_once true`。
- 用户尚未说明：先确认，不能把任一方案当成默认答案。

不得反向推断“AOE 中的 `.skill_instant` 一律必须写 `.apply_once true`”。`.skill_instant` 只是最典型的重复风险之一；是否去重仍取决于设计究竟要求整次技能一次，还是允许随目标数叠加。

## `individual_target_actor_rolls`
- 仅当 Effect 自身的 `.target` 是群体目标时，该字段才有意义。
- `true` 请求对群 Effect 逐最终目标判定。同一批目标经常一起成功或一起失败，观察结果不足以确认实际骰子独立。多个 Effect 落到同一最终目标时也不能依赖共享。
- `false` 或省略时，对群 Effect 各目标是否共享骰子尚未确认。
- AOE 技能对不同技能目标各自独立判定。Effect 自身使用单体目标时，本字段没有实际作用。
- 单体技能中对 `target` 与 `performer` 的 Effect 仍是同一次目标概率的衍生产物；不能仅因最终 target 字段不同就断言概率独立。
- 早期测试曾观察到按目标分离且同一目标仍共享的 40% 标记／自疗案例；后续的群体 target + `true` 测试已证明该现象不能泛化为保证。概率边界见 [Effect 概率骰子共享与隔离](51-Effect概率骰子共享与隔离.md)。

## apply_once 的范围
- `.apply_once true` 不只处理群攻；它会干涉同一次技能或同一调用流程中的同名 Effect 重复生效。
- 去重疑似以 Effect 的 `.name` 为判断键，可暂按“单次技能内，同名 Effect 最多实际生效一次”推理；该内部判定尚未完全确认。
- 它不是跨技能、跨回合或全局锁，也不能作为随机选择一个目标的工具。
- 非技能系统同样可能受影响，但饰品 Trigger 等系统如何划分“同一个调用流程”尚未完整确认。

## 命中顺序：未完全确认
对于 `.on_hit true .on_miss false .apply_once true` 的群攻 Effect：如果第一个目标未命中、第二个目标命中，观察上第二个目标仍可能触发该 Effect。这提示 `apply_once` 可能在首次实际生效时才被消耗，而不是在首次调用尝试时立即被消耗。

该结论目前只涉及命中/未命中条件，不得直接推广到 `.chance` 失败、抗性失败或其他未生效原因。

## 其他边界
- 群体最终目标的应用顺序，社区资料记录为 rank 从低到高。
- 想做一次全体效果时，应避免群攻技能 + 群体 `.target` + `.apply_once false`，否则会按调用目标数重复全体 Effect。
