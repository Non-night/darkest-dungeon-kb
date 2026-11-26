# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.crit_chance_multiply
# 分类
Buff/战斗属性
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 接受一个数值参数，可写整数、小数或带 `%` 的数值。
- 属于 `.combat_stat_buff` 系战斗属性简写 Buff 的属性修正字段；应与对应的简写 Buff 声明配套使用。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.crit_chance_multiply <number>`：为对应的简写 Buff 提供暴击率倍率修正。
# 作用范围
- 与 `.combat_stat_buff 1` 等简写 Buff 声明配套时，属于普通/通用战斗属性 Buff；这里的普通/通用不是 Buff 源类型。
- 具体可用的其他简写 Buff 配套形式尚未穷举。
# 引擎行为（重要）
- 游戏本体、官方 DLC、本地 mods 与 Workshop 262060 均未找到直接 effect 定义实例。
- 参数可写整数、小数或带 `%` 的数值；属于 `.combat_stat_buff` 系战斗属性简写 Buff。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- 参数形式与 `.attack_rating_add`、`.attack_rating_multiply` 等已整理的数值型战斗属性字段相同。
# 常见错误
- 将 `.crit_chance_multiply` 当作独立于简写 Buff 的普通数值效果。
- 忽略其所在的 `.combat_stat_buff` 或其他简写 Buff 配套声明。
# 代码案例
- 游戏本体、官方 DLC、Workshop `262060` 与本地 `mods` 中均未检索到可直接引用的 `effect:` 定义实例。

# 来源与可信度
- 用户补充：`.crit_chance_multiply` 属于 `.combat_stat_buff` 系简写 Buff，参数形式同已整理的数值型战斗属性字段。
- 可信度原则：当前只有字段目录或文档层面的信息，没有原版或已安装 Mod 的直接实例；生成代码前应额外验证。
