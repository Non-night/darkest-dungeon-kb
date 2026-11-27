# spawn 定向、目标与反向

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 默认施术者和目标
- 未发生中途变身时，`spawn: .effects` 或 `hp_reaction: .effects` 所属单位就是 Effect 的施术者。size-0 的 spawn 内 set 后，最初 spawn 剩余列表在当前形态继续，hp_reaction 改读当前形态定义，详见[连续 set 执行链](28-spawn、生命反馈与size0执行链.md)。
- 普通 spawn Effect 未使用定向时，`.target target` 的默认目标就是生成并执行该 spawn 的怪物自身。

## 怪物可同时拥有多个 `enemy_type` / 种族

当前用户明确补充（2026-09-25）：怪物允许拥有多个种族/`enemy_type`。具体写法是连续写多行 `enemy_type:`，例如：

```darkest
enemy_type: .id "aaa"
enemy_type: .id "bbb"
```

这表示同一个怪物同时属于 `aaa` 和 `bbb` 两个 `enemy_type`。该规则同样适用于 size-0；size-0 首先是怪物，不能因为它是中间单位就排除通用怪物的多 `enemy_type` 规则。需要使用 `kill_enemy_types`、种族筛选、标签或其他按 enemy_type 匹配的机制时，必须按实际写入的全部 ID 检查；不要默认只存在一个 enemy_type，也不要把怪物大类 ID 自动当成唯一 enemy_type。

原版基础游戏案例：`DarkestDungeon\monsters\unclean_giant\unclean_giant_A\unclean_giant_A.info.darkest:2-3` 的 Unclean Giant A 连续写有 `enemy_type: .id "man"` 和 `enemy_type: .id "beast"`。这是多行结构的原版直接实例；它不是 size-0 实例。

## effect_chance 与 actor_base_class 模拟定向，减少 size-0

知识库编写者于2026-11-05明确补充：可以用 **`effect_chance` + `actor_base_class` + 对群 Effect** 模拟类似 Spawn 定向的最终生效目标筛选。`effect_chance` 的 `stat_sub_type` 指定最终 Effect ID，Buff 配置 `actor_base_class` Rule，按每个实际目标的英雄职业 ID 或怪物大类 ID分别判定；在群体调用中，让匹配目标通过该 Effect 的概率门，其他目标不通过。

- 若生命反馈二段式的二号机**仅用于定向**，可换用此方案，省去二号机。
- 若单个 size-0 **仅用于获得 Spawn 定向**，大概率也可换用此方案；保留“大概率”的适用范围限定，逐项核对原载体是否还有其他职责。
- `actor_base_class` 在实际目标为 Buff 持有者自身时失效。目标已经明确为自身时，无需再使用 size-0 定向，直接以 `effect_chance` 制约最终 Effect 即可。

该方案通过施加概率控制最终生效目标，群体 Effect 的调用范围仍是群体；概率 Buff 应由实际施术者持有，Rule 逐个检查最终受术者。按[概率门](03-chance与抗性.md)核对基础概率、其他施加率、目标抗性、门控幅度及残留清理，确保未匹配目标不会靠基础概率生效。`actor_base_class` 按职业／大类匹配，不能凭此区分同职业／同大类的多个实体。对通常无视概率的守护及清除守护，先核对 `.force_resist_type` 的既有要求。若原 size-0 另有生命反馈、状态、时序或分支职责，须分别保留或迁移后再省去。

来源：`Sources/effect_chance_directed_filter_20261105.json`；知识库编写者明确补充，Agent未自行运行游戏测试。不补造完整可运行代码或未经验证的新调用时序。

## `.spawn_target_actor_base_class_id`
- 该字段把 spawn Effect 的默认目标改为场上所有匹配指定英雄职业 ID 或怪物 base class ID 的单位。
- 同一 ID 存在多个单位时，可能全部成为目标；`.apply_once` 不能把它稳定缩减为一个随机目标。
- `.spawn_target_actor_base_class_id` 必须写在 `.target` 之前。

## 苦修者的同职业组队限制与旧式二段式

在原版与官方 DLC 的正常编队规则下，苦修者（`flagellant`）是唯一不能与同职业英雄同队的原版职业。原版定义给苦修者写了 `tag: .id "flagellant"`，并用 `incompatible_party_member: .id flagellant_limit .hero_tag flagellant` 禁止同标签英雄同队。来源为 `dlc/580100_crimson_court/features/flagellant/heroes/flagellant/flagellant.info.darkest` 第 51、64 行。

知识库编写者于 2026-11-26 确认，按原版编队规则，苦修者可以直接使用依赖职业唯一性的旧式二段式。队伍里有苦修者时，旧式 Spawn 定向用 `.spawn_target_actor_base_class_id flagellant` 配合 `.target target` 就能唯一找到该苦修者。其他原版职业可能有多个同职业队友，因此不能把这种定向当作稳定的单体定位。这条结论的范围是旧式职业定向。修改编队限制或采用新版定向时，按实际规则重新确定目标集合。

## 定向只在 spawn 调用中生效

知识库编写者确认（2026-09-20）：`.spawn_target_actor_base_class_id` 只在 `spawn: .effects` 调用中改变默认目标。在 `hp_reaction` 等非 spawn 位置引用同一个 Effect 时，该定向字段写与不写的结果相同：字段被忽略，Effect 本身仍按该调用方的默认目标及 `.target` 映射执行，并非整条 Effect 被阻断。

生命反馈的默认目标是触发反馈的单位自身。因此，即使生命反馈是在 spawn 执行期间插入的，也不能继承 spawn 定向；须按本次直接调用来源判断。

以下保留知识库编写者提供的调用位置对照。`xxx` 表示场上已有的英雄职业 ID，`aaa` 是本例 Effect ID。此片段省略了触发生命反馈的 Effect，不是完整 size-0 模板；实际生成仍需保留生命反馈 sentinel、初始化和善后。

Effect 定义：

```text
effect: .name "aaa" .spawn_target_actor_base_class_id xxx .target target .tag 1 .on_hit true .on_miss true
```

同一 size-0 的 Info 调用：

```text
spawn: .effects "aaa"
hp_reaction: .hp_ratio 0.25 .is_under true .effects "aaa"
```

1. size-0 被召唤，spawn 调用 `aaa`：定向字段生效，`.target target` 指向英雄 `xxx`，英雄被标记。
2. 当省略的生命变化流程实际触发该 hp_reaction，它再次调用 `aaa`：定向字段被忽略，`.target target` 指向触发生命反馈的 size-0 自身，size-0 被标记。
3. 两次调用完成后英雄与 size-0 都有标记。这是两次不同调用分别生效，不是 `aaa` 自带对群，也不是 spawn 定向被生命反馈继承。

其他非 spawn 调用同样忽略此定向字段，但其默认目标须按各调用方确定，不能一律解释为自身。连续 set 的 spawn 定向异常仍按本页既有例外处理。

## 与 `.target` 的组合
spawn 定向先建立“被定向职业”这一目标基础，再由 `.target` 映射最终范围。




## “定向反向 + actor_base_class”概率门的标准目标/施术者关系

当前用户明确指出（2026-09-25）：所谓“定向反向 + `actor_base_class`”的正确写法，核心不是让 `actor_base_class` 去检查 Buff 持有者自身，而是先用 `.spawn_target_actor_base_class_id` 定向找到目标，再用 `.swap_source_and_target true` 交换施术者与受术者，令原本被定向到的英雄职业/怪物大类单位成为 Effect 的施术者，原 size-0 成为受术者。此时挂在被反向后施术者身上的 `actor_base_class` Buff，检查的是 Effect 的实际目标——原 size-0——而不是该 Buff 持有者自身。

因此，若要让反向后的 `actor_base_class` Rule 匹配 size-0，`rule_data.string` 应填写 size-0 的怪物大类 ID；不能填写被定向英雄的职业 ID来期待它检查英雄自身，也不能把“Buff 持有者 ID 自身匹配则永不生效”的边界误套到这个反向调用。正确核对顺序必须是：定向目标 → `.swap_source_and_target true` 后的施术者/受术者交换 → Buff 实际挂载者 → Effect 最终目标 → `actor_base_class` Rule 判定对象。

该关系同样适用于怪物大类定向，但仍须按实际目标、同侧/跨侧概率、调用来源和 `target` 映射逐项检查；`spawn_target_actor_base_class_id` 只在 spawn 调用中生效，`hp_reaction` 等非 spawn 调用不能继承这一定向。

## 与 `.swap_source_and_target` 的组合
`.swap_source_and_target true` 会交换当前 Effect 的施术者与受术者：

- 原本的定向目标成为 Effect 施术者。
- 原本发起 spawn Effect 的怪物成为受术者。


## 连续 set 的定向例外
同一怪物连续多次 set 的 spawn 不能照搬普通定向规则：资料记录定向失效，且从第二次 set 起对英雄跨侧 Buff 异常按同侧处理，减益施加率/抗性不再参与。定向失效自身的精确起始序号未单独确认；新召唤的 size-0 与原地变身不同。精确来源与边界见[连续 set 执行链](28-spawn、生命反馈与size0执行链.md)。

## 时序边界
spawn 定向只解决“谁是目标”，不解决“何时执行”。完整的 spawn 顺序、生命反馈插入和 size-0 死亡行为见：[spawn、生命反馈与 size-0 执行链](28-spawn、生命反馈与size0执行链.md)。


## size0 对群反向与站位概率门定向

知识库编写者于2026-11-06补充了一种可单独复用的站位定向流程。若英雄友方技能需要借助 size0 对特定英雄站位定向，可以先让目标单位按站位获得临时概率门：1号位对应 `aaa`，2号位对应 `bbb`，3号位对应 `ccc`，4号位对应 `ddd`；不满足对应条件的目标移除或不保留相应门。然后召唤 size0，由 size0 对英雄侧使用**对群反向** Effect，依次执行 `aaa`、`bbb`、`ccc`、`ddd`。

这里 `aaa`、`bbb`、`ccc`、`ddd` 都是对应站位的 `effect_chance` 门；**最终 Effect 本身也使用对群目标**，通过这些门筛选最终生效对象，而不是把最终 Effect 写成单体目标。例子中四个站位门和最终 Effect 的基础 `.chance` 都是**小于0且大于-99998**的值。最终执行后再用善后驱散清除临时门。

该流程可以通过调整站位门、对群反向调用、最终 Effect 和善后驱散，定向任意需要的站位目标。它是可按调用方和目标需求微调的设计模板，不是未经完整核验的固定可运行代码；应另行检查 size0 的召唤时序、死亡/战斗结束兜底、目标集合和清理是否完整。来源：`Sources/size0_rank_targeting_by_group_effect_chance_20261106.json`；Agent未自行运行游戏测试。
