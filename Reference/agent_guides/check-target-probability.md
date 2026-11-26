# 目标、概率、Rule与次数

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


只在当前任务涉及本组时展开。若本页历史维护建议与现行专题或当前用户明确约束冲突，先核对适用范围；不要机械执行所有检查。

- 参数单位、布尔形式、固定值是否正确？使用 `attack_rating` 或 `defense_rating` 固定增加时，是否按文件值 `0.01 = 游戏内 1 点精准／闪避` 换算？

- 用户对精准、闪避或其他战斗属性的描述是否可能同时解释为固定增加与倍率提高？若存在合理争议，是否已经先向用户问清，而没有自行选择 `combat_stat_add` 或 `combat_stat_multiply`？若两者并存，是否按所有 `combat_stat_*` 系 Buff 的“先加后乘”顺序计算？是否误把该顺序套用于治疗，而忽略治疗是先百分比、后固定值？

- 调用方提供几个目标？`.target` 后最终是谁？最终受术者集合是否严格等于设计范围，是否错误扩大到设计之外的单位？

- Effect 会不会按群攻目标重复？不要只检查 `performer_group`、`target_group` 等群体目标；应检查每个 AOE 调用轮次产生的最终受术者集合是否重叠，任何让同一最终单位反复成为受术者的写法都可能按目标数叠加，包括 `.target performer`、群体映射及用于修饰同一施术者／同一次技能结果的 `.skill_instant true`。

- 若上述重复会明显叠加，而用户没有明确说明是否应随 AOE 目标数量增加，是否已经先询问用户是“整次技能一次”还是“每个目标一次”，而没有擅自添加或省略 `.apply_once true`？

- 若使用 `.keyStatus`、`.skill_instant true` 或 `.monsterType`，是否误把条件简写用于瞬时效果，是否误判第二次施加时序，是否忽略 `bsrc_instantSkill` 的 Update 清除边界？若通过 `.buff_ids` 引出 Buff，是否识别到 `.keyStatus`、`.monsterType` 会按 `.skill_instant true` 处理？

- 设计要求 Buff 存在超过 1 回合时，是否已避免默认 `bsrc_instantSkill` 来源；若保留 `.keyStatus`、`.skill_instant true` 或 `.monsterType`，是否明确用 `.buff_source_type` 覆盖来源，并检查残留、重复施加和清理？

- 使用 `clear_buffs_on_rule_active` 时，是否确认它只能清除清理 Buff 持有者自身的 Buff，不能跨单位生效？列表是否误写空字符串 `""`，从而把持有者身上所有 Effect 简写 Buff 一并驱散？

- 若临时易伤只用于干涉本次直伤，是否在本次直伤后的技能 `queue false` 时序按明确 Buff ID 尽早清除？清理目标和 Buff ID 是否严格限于设计范围？

- 技能 Effect 存在“前置状态／Buff／标记 → 后续读取、消费或清除”的依赖链时，是否同时检查了大时序与严格时序？是否先按 AWR → 普通 `queue false` → `queue true` 及来源层级确定实际先后，再只对同一大时序、同一来源的 Effect 使用书写顺序推理？是否出现依赖 Effect 位于 `queue false`、前置 Effect 却位于 `queue true`，导致依赖 Effect 在状态建立前就检查并失效？

- 饰品使用 `transform_on_quest_complete_chance` 时，是否将其作为饰品条目同级 JSON 浮点字段，而不是 Effect 关键字？是否同时提供有效的 `transform_on_quest_complete` 目标？省略时是否按默认值 `1` 理解？

- 多个相似调用位置所需的 Effect 是否完全相同？若完全相同，是否只创建一个目标 Mod 自有的 Effect 并重复引用，而没有按技能等级复制多份相同定义？若所有等级引用相同 Effect，是否检查过能否安全放入无等级共用分行；若抽取会改变引用顺序、触发时序或生效次数，是否保留各等级分别引用同一个 Effect ID？

- 设计稿用 `●`／`○` 表示站位时，是否按所代表阵营换算：英雄侧通常从左到右为 `4321`，怪物侧通常为 `1234`？英雄启动 `●●●○` 是否换算为 `.launch 432`，英雄攻击技能的敌方目标 `●●●○` 是否换算为 `.target 123`？若是怪物设计稿，是否先向用户确认圆点方向而没有擅自推定？

- 使用同 ID `combat_skill:` 分行时，是否区分了带 `.level` 的等级行与不带 `.level` 的无等级共用分行？非自身目标是否在每个等级的第一条定义显式写了非空 `.target`，没有靠同等级后续行或无等级行补救？其余分行无须重复写目标；下方无等级行可覆盖已建立的目标站位。

- 每条新建或修改的 Buff 是否完整显式填写 `rule_type`、`is_false_rule`、`rule_data.float`、`rule_data.string`？无条件 Buff 是否仍写了 `rule_type: "always"`？

- `remove_if_not_active` 是否默认写为 `false`？若写为 `true`，是否确有“Rule 不成立时立即移除”的设计需求，或对应 stat_type 有明确证据要求如此；是否误把它理解成暂时停用？

- 先判断 Effect 简写 Buff 所属系列，再检查主副类型、配套字段、rule 分类、持续时间覆盖关系、提前移除条件与 Buff 源。

4. **风险与边界**：直接说明已有结论覆盖的时序、目标、软锁等边界；仅对未确认项附带验证或规避建议。

收到“帮我写 DD Mod 代码”时，先提取：文件类型、调用方、目标、触发时机、期望执行次数、持续时间、是否允许回合外行为、失败兜底。若需求涉及技能、武器或护甲等级，还要先确认用户采用代码零基等级还是玩家口语一基等级；孤立的 `1` 至 `4` 级存在歧义时不得自行决定。

- 用户明确要求创建、实现、修复或完善某个 Mod 时，才可在明确目标 Mod 根目录内创建或修改完成需求所必需的配置。

- 允许为明确设计自行创建 Effect/Buff ID、`effects\*.effects.darkest`、`shared\buffs\*.buffs.json` 及其他必要标准配置；设计稿未提供现成定义不是省略功能的理由。

- 修改现有目标 Mod 时遵循最小变更原则，不改无关文件，不删除可能供兼容使用的定义。

- Effect 的最终目标必须与设计对象一致；没有绝对必要时不得作用于设计之外的目标，也不得用 `target_group` 代替 `target` 来规避限制。

- 群体 `.target` 的死而不僵门必须按每个最终目标独立检查，不能因一个目标失效而跳过同群体其他目标。

- 未经用户允许，不得修改游戏本体、官方 DLC、其他 Mod、Workshop 内容、插件/辅助软件、知识库、设计稿或目标 Mod 之外的文件；知识库补充任务适用上一条的二次确认规则。

4b. 如果目标、Rule 或调用时序无法直接给出真假分支，必须检索 `Mechanics/03-chance与抗性.md` 的“size-0 + Rule + 极大概率 Buff 逻辑门”小节，检查是否可以用匹配的概率 stat_type、Rule 门控 Buff 和 size0Spawner 载体传递结果；不得只凭感觉堆叠正负概率。

4d. 创建预计长期存在的 Buff 时，施加阶段优先检查无图标源，默认优先 `bsrc_quest_failure` 或 `bsrc_vampire`；其他无图标源必须逐源核对，不得仅因 Icon 为 None 就替换。
