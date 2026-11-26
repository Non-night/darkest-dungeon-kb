# target_enemy_rank 站位检测语义

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 已确认语义

`target_enemy_rank` 是**当前目标的站位检测目标类型**。它不会从敌方队伍中重新选择一个站位，也不会扫描其他敌人。

```darkest
effect: .name "CHECK_CURRENT_TARGET_R2" .target target_enemy_rank .clear_rank_target 2 .chance 999999 .buff_ids "R2_MARK"
```

上例只有在技能已经选中的敌方目标处于二号位时才发生。当前目标处于一号、三号或四号位时，这条 Effect 彻底不发生：不会改选二号位的敌人，也不是“先选中后被阻止”。

`.clear_rank_target` 必须是单个站位值。缺少它、把它当作范围，或试图从三号位目标读取一号位，均不属于本机制已确认的用法。

## 与反向 Effect 的关系

```darkest
effect: .name "MARK_CURRENT_TARGET_R3" .target target_enemy_rank .clear_rank_target 3 .swap_source_and_target true .chance 999999 .buff_ids "R3_GATE"
```

当当前目标确实在三号位时，`.swap_source_and_target true` 只把这次已选中的目标和施术者交换，用于把 `R3_GATE` 写到施术者；它仍然没有选择或读取一号位、二号位的其他单位。

需要读取敌方队伍中另一个站位的体型时，使用 `target_group` 跨侧筛选。例如在施术者身上用 `target_in_rank` 与 `monsterSize` 修饰本次向各怪物施加 Buff 的概率，再借怪物载体和 `swap_source_and_target` 回传结果；也可按已有案例使用载体上的 `in_rank` 条件。这里的群体目标用于读取组成，不用于扩大位移范围。专题90的实际位移统一使用 `target`，站位限制由施术者身上的 `target_in_rank` Rule Buff 修饰 `move_chance`。用户指出 `target_enemy_rank` 在该专题推拉组合中存在问题，因此不得由本页的目标检测语义推出它适合作为该组合的位移目标；具体异常表现、原因及其他调用范围仍未提供。

## 证据边界

- `target_enemy_rank` 的“只检测当前已选目标”语义来自用户对实测行为的明确补充，并与官方 Fire's Edge 的 `.clear_rank_target` 实例一致。
- `target_enemy_rank`、`.clear_rank_target` 和 `.swap_source_and_target` 的组合时序仍必须按调用方、`queue` 层和实际目标逐项核对。
- 本页不把 `target_enemy_rank` 外推为群体筛选器；群体筛选的完整示例见[怪物推拉与 size-0 站位边界](90-怪物推拉与size0站位边界.md)。
