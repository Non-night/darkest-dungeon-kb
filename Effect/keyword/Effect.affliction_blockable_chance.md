# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.affliction_blockable_chance
# 分类
扩展/专项字段
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 仅接受一个数值参数，可写整数、小数或带 `%` 的数值。
- Effect 参数必须大于 `0` 才会实际产生折磨阻挡概率。
- 所有可能被随机到的折磨，都必须在 `reaction_act_outs` 中提供 `id` 为 `block_effect` 且 `chance > 0` 的条目；当前不确定任意正数是否均可，保守写法为 `1`。
- 除非已补全所有可能随机到的折磨，或为全部英雄提供完整的自定义折磨体系，否则禁止使用本字段。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.affliction_blockable_chance <chance>`：目标处于支持阻挡 effect 的折磨状态时，本 effect 被该折磨阻挡而不生效的概率。
# 作用范围
- 用于 Effect 定义行。
- 配套定义位于 `shared\trait\*.trait_library.json` 或 `shared\trait\trait_library.json`；未采用全英雄自定义折磨时，必须覆盖检查所有最终可能被随机到的折磨。
# 引擎行为（重要）
- 游戏本体、官方 DLC、本地 mods 与 Workshop 262060 均未找到直接 effect 定义实例。
- 所有可能随机到的折磨都必须启用 `block_effect`；原版折磨虽有该条目，但 `chance` 均为 `0`。
- 详见：[Mechanics/13-文件覆盖、逆序覆盖与同ID合并.md](../../Mechanics/13-文件覆盖、逆序覆盖与同ID合并.md)
- 原版八种折磨均存在 `block_effect` 条目，但其 `chance` 都为 `0`，并未启用 effect 阻挡。直接使用本字段可能导致游戏崩溃。
- Trait 侧 `block_effect.chance` 必须大于 `0`；是否必须等于 `1` 尚未确认，创作时应写 `1`。
- Effect 参数小于等于 `0` 不会产生折磨阻挡；其不会导致崩溃的结论目前仅为推测。
# 常见错误
- 未修改原版折磨，也未建立完整自定义折磨体系，却直接使用本字段。
- 只补充部分可能随机到的折磨。
- 将 Trait 侧 `block_effect.chance` 保持为 `0`，或使用尚未验证的非 `1` 正数。
# 代码案例
- 游戏本体、官方 DLC、Workshop `262060` 与本地 `mods` 中均未检索到可直接引用的 `effect:` 定义实例。

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 原版 Trait：`DarkestDungeon\shared\trait\trait_library.json:78`、`:158`、`:238`、`:318`、`:395`、`:475`、`:554`、`:635`；八种折磨的 `block_effect.chance` 均为 `0`。
- 数值边界：Effect 参数大于 `0` 才会实际产生阻挡；小于等于 `0` 的不崩溃结论目前仅为推测。
- 可信度原则：当前只有字段目录或文档层面的信息，没有原版或已安装 Mod 的直接实例；生成代码前应额外验证。
