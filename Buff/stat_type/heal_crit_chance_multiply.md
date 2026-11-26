# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

heal_crit_chance_multiply
# 分类
Buff `stat_type`；新版文档新增
# 参数类型
stat_type为字符串；amount为数值；具体范围未提供。
# 参数约束
stat_sub_type：文档未定义副类型，不补造固定候选。
# 固定值 / 参数候选
不补造文档未提供的枚举、amount开关阈值或存档数字ID。
# 语义
按倍率修改施术者治疗暴击率，不等同于普通攻击暴击率。
# 作用范围
Buff定义；按实际施术者/持有者上下文核对。
# 引擎行为（重要）
- 新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json
- 仅有文档语法与语义；未提供完整可运行实例。
- 未提供新增存档数字ID或默认amount增减益分类。
# 常见错误
不要把缺失的存档数字ID、amount分类或完整计算顺序补成确定事实。
# 代码案例
仅文档字段片段，不提供未经验证的完整Buff或amount示例。
# 来源与可信度
Sources/modding_update_20261105_remaining.json；新版社区资料，后续社区实测修正见相应记录。本轮未新增实机测试。
