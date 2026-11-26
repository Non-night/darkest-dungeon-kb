# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.virtue_blockable_chance
# 分类
扩展/专项字段
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 仅接受一个数值参数，可写整数、小数或带 `%` 的数值。
- Effect 参数必须大于 `0` 才会实际产生美德阻挡概率。
- 所有可能被随机到的美德，都必须在 `reaction_act_outs` 中提供 `id` 为 `block_effect` 且 `chance > 0` 的条目；当前不确定任意正数是否均可，保守写法为 `1`。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.virtue_blockable_chance <chance>`：目标处于支持阻挡 effect 的美德状态时，本 effect 被该美德阻挡而不生效的概率。
# 作用范围
- 用于 Effect 定义行。
- 配套定义位于 `shared\trait\*.trait_library.json` 或 `shared\trait\trait_library.json`；未采用全英雄自定义美德时，必须覆盖检查所有最终可能被随机到的美德。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 所有可能随机到的美德都必须启用 `block_effect`；原版五种美德的 `chance` 均为 `1`。
- 详见：[Mechanics/13-文件覆盖、逆序覆盖与同ID合并.md](../../Mechanics/13-文件覆盖、逆序覆盖与同ID合并.md)
- 原版五种美德的 `block_effect.chance` 均为 `1`；在没有 Mod 修改这些美德定义时，本字段具备正常运行的前置条件。
- 若 Mod 将可能随机到的美德覆盖为缺少 `block_effect`、`chance = 0` 或其他无效状态，使用本字段可能导致游戏崩溃。
- Trait 侧 `block_effect.chance` 是否必须等于 `1` 尚未确认，创作时应写 `1`。
# 常见错误
- Mod 覆盖原版美德后未重新检查 `block_effect.chance`。
- 只补充部分可能随机到的自定义美德。
- 使用尚未验证的非 `1` 正数作为 Trait 侧 `block_effect.chance`。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1535`
```darkest
effect: .name "CaptureBosun" .target "target" .chance 100% .capture 1 .on_hit true .virtue_blockable_chance 100%
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 Effect：`DarkestDungeon\effects\base.effects.darkest:1535`。
- 原版 Trait：`DarkestDungeon\shared\trait\trait_library.json:711`、`:787`、`:863`、`:939`、`:1015`；五种美德的 `block_effect.chance` 均为 `1`。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
