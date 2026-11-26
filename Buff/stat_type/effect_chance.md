# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

effect_chance
# 分类
Buff `stat_type`；新版文档新增
# 参数类型
stat_type为字符串；amount为数值；具体范围未提供。
# 参数约束
stat_sub_type：必填：Effect ID。
# 固定值 / 参数候选
不补造文档未提供的枚举、amount开关阈值或存档数字ID。
# 语义
修改stat_sub_type指定Effect ID的施加概率，与其他状态施加率叠加；例如Bleed 5同时受effect_chance及bleed_chance影响。
# 作用范围
Buff定义；按实际施术者/持有者上下文核对。
# 引擎行为（重要）
- 新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json
- 仅有文档语法与语义；未提供完整可运行实例。
- 未提供新增存档数字ID或默认amount增减益分类。
- 知识库编写者2026-11-05补充：守护及清除守护通常同时无视自身.chance与effect_chance；对该Effect声明.force_resist_type后，可用指定类型对应施加率及effect_chance控制是否生效。来源：Sources/guard_start_triggers_20261105.json。
- 社区测试反馈（暂行，非绝对结论）：九封2026-11-17报告，使用当前技能ID作为skill Rule条件的effect_chance Buff，其指定Effect概率修饰在所述测试中未生效；正向增加及负向抑制均有失效反馈。A为queue false，B为queue true，新增测试为AWR；不是A/B/C各在三个时序的九种组合全测。C未写特定技能限制时修饰生效，其Rule具体写法及时序未提供。仅报告effect_chance与skill Rule的组合表现，不判定skill Rule整体、其他施加率属性或Buff实体失效；其他Rule暂未发现问题不等于全部验证通过。 来源：Sources/effect_chance_skill_rule_20261117.json；详见Mechanics/72-skill-rule时效与全场范围.md。
- 已确认：英雄身上的effect_chance不能修饰饰品Trigger引出的、目标为this_trinket的Effect的.chance。来源为YuriRoseHime2026-11-17社区测试反馈，知识库编写者同日明确确认。仅限该持有者／调用方／目标组合，不推广到所有饰品Trigger、other_trinket或常规单位目标，也不表示Effect自身.chance无效；不与技能／饰品静态附魔中饰品目标不生效的独立测试混同。Agent未新增游戏实测。来源：Sources/trinket_effect_chance_20261117.json；详见Mechanics/48-饰品AdditionalEffects触发与顺序.md。
- 社区补充测试反馈（暂行，非绝对结论）：YuriRoseHime于2026-11-17 13:21:52报告，即使effect_chance来自静态Buff，也不能修饰目标为this_trinket的Effect的.chance。未提供该静态Buff的具体载体、完整代码及调用参数；不能据此推广至other_trinket、所有Effect目标或静态Buff整体失效。此前英雄持有effect_chance、饰品Trigger调用this_trinket的已确认记录保留原有证据状态；本次新增范围单独暂行记录。 来源：Sources/trinket_effect_chance_20261117.json。
- 知识库编写者2026-11-05补充：effect_chance配合actor_base_class Rule及对群Effect，可按每个最终目标筛选生效对象，模拟Spawn定向；生命反馈二段式中仅为定向存在的二号机可省去，仅为定向存在的单台size0大概率也可替换。actor_base_class在实际目标为自身时失效；自身目标无需size0定向，直接用effect_chance制约最终Effect。须核对概率门、其他抗性及原载体是否有额外职责。来源：Sources/effect_chance_directed_filter_20261105.json；详见Mechanics/07-spawn定向.md。
# 常见错误
不要把缺失的存档数字ID、amount分类或完整计算顺序补成确定事实。
# 代码案例
仅文档字段片段，不提供未经验证的完整Buff或amount示例。
# 来源与可信度
Sources/modding_update_20261105_remaining.json；新版社区资料，后续社区实测修正见相应记录。本轮未新增实机测试。
