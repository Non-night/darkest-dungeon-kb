# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.force_resist_type
# 分类
扩展/专项字段
# 参数类型
单个字符串（resist_id）
# 参数约束
- 单个字符串（resist_id）；完整值域未提供。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- 知识库编写者2026-11-05实测确认：无论Effect原本是否需要过抗，.force_resist_type均改用指定类型对应的施术者施加率和受术者抗性；替代原判定，不是追加第二次过抗。指定poison时仅看腐蚀施加率与腐蚀抗性，减益施加率与减益抗性完全不参与。该明确结论也覆盖原本按同侧处理、不经过减益抗性的效果；不再保留原先的两个选择疑问。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 本字段依据新版功能文档采纳；旧离线案例快照不含本字段，本次未重新扫描游戏或 Mod，也未伪造配置实例。
- 治疗 Effect 强制过疾病抗性时，按治疗判定概率减去目标疾病抗性计算成功率。180% 的治疗判定概率对 80% 疾病抗性，180% − 80% = 100%，进入该判定的治疗必定通过。 疾病施加 Effect 显式强制过疾病抗性时，是否改变疾病施加原有的概率计算仍未确认。 施加怪癖强制过疾病抗性时，最终成功率的计算方式仍未确认。
- 完整resist_id值域、同行含多种效果时的具体作用粒度仍未确认；本次示例中的.chance -1原样保留，不据此补造一般概率公式或取值边界。
- 实测原样Effect：effect: .name lp_test_debuff .target target .chance -1 .force_resist_type poison .buff_type hp_heal_amount .buff_amount 1 .on_hit true .on_miss true
- 知识库编写者2026-11-05补充：.guard 1、.clearguarded 1、.clearguarding 1通常不受自身.chance和effect_chance制约；但对该Effect声明.force_resist_type后，可由指定类型对应施加率及effect_chance制约是否生效，目标抗性按指定类型处理。既有概率豁免结论仅限未强制过抗时。来源：Sources/guard_start_triggers_20261105.json。
- 知识库编写者2026-11-06明确补充：对Effect型标记声明强制过减益抗性，可使其像Buff型标记一样经过减益施加率与减益抗性判定，同时仍受‘无法被标记’干涉；Buff型标记则不受‘无法被标记’干涉。来源：Sources/effect_mark_forced_debuff_resist_20261106.json。
# 常见错误
- 同时使用原类型与强制类型两套抗性，或只替换抗性而仍保留原类型施加率。
# 代码案例
- 文档仅提供字段片段，未提供完整 Effect；旧离线案例快照不含本字段，本次未重新扫描外部安装源。参见参数约束中的原文片段，不将其冒称为完整可运行代码。

# 来源与可信度
- 新版文档B031–B032；Sources/modding_update_20261105_effects.json。
- 知识库编写者2026-11-05报告实测，原样Effect与结论见来源账本；Agent未自行实测。
- Sources/forced_disease_resist_probability_20261119.json
- 可信度原则：当前未找到可直接引用的原版或已安装 Mod 实例，但该行为来自已收录专项资料，可按词条中的明确结论使用；不得自行扩展未说明的边界。
