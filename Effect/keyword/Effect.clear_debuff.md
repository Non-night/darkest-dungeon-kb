# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.clear_debuff
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔 `0` 或 `1`；`1` 启用清除。
- 只清除被游戏归类为减益且 `is_clear_debuff_valid` 为 `true` 的 Buff。
- 增益 Buff 即使将 `is_clear_debuff_valid` 写为 `true`，也不会被清除。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.clear_debuff 1`：清除目标身上允许被清除的减益 Buff。
- `.clear_debuff 0`：不启用该清除效果。
# 作用范围
- 清除对象是当前 Effect 的最终目标。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.clear_debuff 1` 只清除被归类为减益且 `is_clear_debuff_valid` 为 `true` 的 Buff，因此属于假驱散。
- 增益 Buff 即使将 `is_clear_debuff_valid` 写为 `true`，也不会被 `.clear_debuff` 清除。
- 详见：[Mechanics/15-Buff源与真驱散.md](../../Mechanics/15-Buff源与真驱散.md)
- `.clear_debuff` 受 Buff 的增益/减益分类及 `is_clear_debuff_valid` 限制，因此称为假驱散。
- 假驱散不同于对自身使用 `.steal_buff_source_type` 的真驱散；后者按来源移除该来源下的全部 Buff。
# 常见错误
- 认为 `is_clear_debuff_valid = true` 足以让增益 Buff 被 `.clear_debuff` 清除。
- 把 `.clear_debuff` 当作可以任意移除 Buff 的真驱散。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1932`
```darkest
effect: .name "medicinal_herbs" .target "performer" .item 1 .chance 100% .clear_debuff 1
```
- 官方 DLC `702540_shieldbreaker`：`DarkestDungeon\dlc\702540_shieldbreaker\effects\shieldbreaker.effects.darkest:143`
```darkest
effect: .name "Cure Debuffs".target "target" .chance 100% .clear_debuff 1 .on_hit true .on_miss false
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:10`
```darkest
effect: .name "district_medicinal_herbs_override" .target "performer" .item 1 .duration 3 .chance 100% .clear_debuff 1 .buff_ids medicinal_herbs2_disease_resist
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 Effect：`DarkestDungeon\effects\base.effects.darkest:1932`。
- `.clear_debuff` 的假驱散分类及清除限制属于已整理的行为结论。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
