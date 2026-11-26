# Effect 概率骰子共享与隔离

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 结论边界
本页只记录已经给出测试结论的概率骰子边界。这里的“共享”指多个 Effect 使用同一个随机数：较低概率的 Effect 成功时，较高概率 Effect 也必定成功；概率相同时则同时成功。它不等同于攻击命中、抗性、暴击或效果最终数值的共享。

未列出的调用方、字段组合或 Fire's Edge DLC 新内容不得按本页自行补全为共享或独立。

## 已确认共享的范围
- 同一个技能内的多个 Effect 共享概率骰子；AWR、`queue false`、`queue true` 不会把这个骰子拆开。
- 技能 Effect 与同次攻击的饰品攻击、友方、近战、远程、暴击 Trigger 共享概率骰子。
- 位移、DOT 等复杂概率在已测试的单体情形中也遵循上述共享；不得外推到未测试的群体或特殊调用。
- 怪物技能内部 Effect 与英雄技能内部 Effect 一样共享。
- 同一个扎营技能内、面向同一受术者的多个不同 Effect 共享。
- 同一个 ActorDot 内的不同 Effect 共享。
- 单体技能中一个 Effect 指向 `target`、另一个指向 `performer`，仍是同一次目标概率的衍生产物；不能只因最终受术者字段不同就断言独立。

反击技能 Effect 与饰品反击 Trigger **推测**共享，现有测试量较小，不能作为需要严格隔离的设计前提。

## 已确认独立的范围
- 攻击命中概率与 Effect 概率独立，包括普通精准/闪避和保底命中；即使两者理论数值相同也不共享。
- 技能与 ActorDot 独立；不同 ActorDot 彼此独立。
- 英雄受击 Trigger 与反击 Trigger 独立。
- 怪物技能 Effect 与目标英雄的受击 Trigger、反击 Trigger 独立；英雄技能 Effect 与怪物反击 Effect 独立。
- 饰品击杀 Trigger 与其他饰品进攻 Trigger 独立。
- 饰品受击 Trigger 的多个 Effect 相互独立，即使进攻者、受击者和实际最终目标相同。
- 技能与道具独立，包括虚拟道具与道具套娃调用。
- 知识库编写者测试结论将不同单位视为独立概率边界，包括召唤者与召唤物。2026-11-09进一步明确：**技能Effect与该技能召唤出的size0单位的spawn Effect必定概率独立。** 例如技能内最终成功率30%的Effect已成功，随后召唤size0，其spawn内最终成功率同为30%的Effect仍未必成功；不能以前者结果推知后者，也不能将技能与召唤物spawn当作同一次共享骰子。这里是对既有“召唤者与召唤物独立”的具体化，不是新增一条不同边界；不要扩展到没有独立单位的普通spawn嵌套。严格同一个size0内部各条spawn大概率共享仍只是推测，与此已确认跨单位独立边界不冲突。来源：`Sources/spawn_sharing_and_mode_start_enchantment_20261109.json` / `SKILL-SPAWN-INDEPENDENT-01`；非本轮Agent实机测试。

原表第270条 P5053/X6591 较早保留了敌方反击是否独立的疑问；后续 P5070/X6613 已确认**英雄技能 Effect 与怪物反击 Effect 相互独立**，该具体关系不再列为未知。击杀 ActorDot 与饰品击杀 Trigger 是否共享仍未知；“击杀 ActorDot 限制更严格，因此可能独立”仅为推测。

## `.individual_target_actor_rolls true`
- 本字段只在 Effect 自身 `.target` 为群体时有实际意义。
- `true` 时，红钩会按每个最终目标、每个 Effect 重新产生概率骰子。它不只是让不同目标之间分离；即使多个 Effect 面向同一个最终目标，甚至并写在同一行，也不能保证保留普通技能中的共享关系。
- 因此早期“打 123、40% 标记且 40% 自疗 999”中，1 未标记、2/3 标记时自疗为 1998 的观察，只能说明当时调用链的按目标关联；后续测试已否定把它泛化成 `true` 下同目标必共享的规则。
- `false` 或省略时，保留普通群体 Effect 的既有共享结果模型，但不能外推到复杂调用方。
- 单体技能的 `target`／`performer` 混合不应误作“不同目标”来套用本字段。

## 设计与排查
概率隔离只能依赖已确认的调用边界，不要试图通过 AWR、`queue false` 或 `queue true` 分离同一次技能或进攻 Trigger 的骰子。要让群体中的每个最终目标各自判定时，使用 `.individual_target_actor_rolls true`，同时接受它也会破坏原本同目标 Effect 的共享概率。

## spawn 抗性读取的概率共享待测

知识库编写者2026-11-09进一步提出：**严格同一个size0单位实例的各条spawn所调用的Effect，大概率共享概率骰子，但尚未完全确认。** 这里不是“同一个怪物小类”：同一小类生成的不同单位不在此推测范围，也不将召唤者与召唤物视为共享。该补充为明确了实例范围的推测，不是共享已确认；不能据此把size0抗性读取或去施加率干扰的整个流程升级为已验证可用。来源：`Sources/spawn_sharing_and_mode_start_enchantment_20261109.json` / `SPAWN-SHARE-INSTANCE-01`。

知识库编写者2026-11-06明确补充：spawn 内读取Effect与最终Effect是否共享所需概率不确定，因此不能保证由size0独立检测就能完美防止施加率干扰，实际能否实现有待实测。控制size0对应施加率并不能替代共享概率前提。这里不是确认spawn独立，也不是确认size0不可用；详见[抗性读取](03-chance与抗性.md)及`Sources/resistance_readback_via_forced_resist_20261106.json`。

## Fire's Edge DLC 边界
Fire's Edge DLC 新增的任何内容，包括但不限于附魔 Buff，当前都没有完成上述概率骰子测试。不得把本页的原版、常规技能、饰品或 ActorDot 结论直接套用到 Fire's Edge 新字段和新调用链。

知识库编写者于2026-11-06补充的**推测**：附魔同类 Trigger 的概率共享范围可能与饰品同类 Trigger 一致；即饰品同类 Trigger 已知共享时，推测附魔同类 Trigger 也共享。这不是附魔共享概率已经实测确认，也不是所有附魔 Trigger 均共享。按此推测使用抗性读取案例时须保留推测标记。案例及两次补集关系见[抗性读取](03-chance与抗性.md)，来源：`Sources/resistance_readback_via_forced_resist_20261106.json`。

## 证据等级
本页的已确认范围来自用户转述的社区专项测试；“推测”和“未知”已逐项保留，不得在生成 Mod 代码时升级为确定行为。
