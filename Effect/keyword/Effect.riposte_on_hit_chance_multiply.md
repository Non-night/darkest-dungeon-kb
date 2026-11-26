# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.riposte_on_hit_chance_multiply
# 分类
反击
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.combat_stat_buff` 系简写字段，对 `riposte_on_hit_chance` 施加百分比／乘法修正。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 游戏本体、官方 DLC、本地 mods 与 Workshop 262060 均未找到直接 effect 定义实例。
- 战斗属性简写：百分比调整被命中时反击概率；英雄基础值为 `0`。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- 英雄默认 `riposte_on_hit_chance = 0`。本字段可写在 `.combat_stat_buff 1` 后并正常生效。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体、官方 DLC、Workshop `262060` 与本地 `mods` 中均未检索到可直接引用的 `effect:` 定义实例。

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 可信度原则：当前只有字段目录或文档层面的信息，没有原版或已安装 Mod 的直接实例；生成代码前应额外验证。
