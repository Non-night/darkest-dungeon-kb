# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.item
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数为数字布尔；道具使用 Effect 必须写 `.item 1`，不得用 `true` 代替。
- 道具 ID 与被自动调用的 Effect `.name` 必须同名。例如道具 ID 为 `aaa` 时，使用道具会调用 `.name "aaa"` 的 Effect。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- 道具被使用时，引擎按道具 ID 自动查找并调用同名 Effect。
- `.item 1` 将该 Effect 标记为道具使用 Effect，并使其 Buff 源按 `bsrc_item` 处理。
# 作用范围
- 只用于由道具使用流程调用的 Effect；普通技能、饰品 Trigger、spawn 等调用不应仅为模仿格式而添加。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 使用道具时自动调用与道具 ID 同名的 Effect；该 Effect 必须写 `.item 1`。
- 详见：[Mechanics/39-道具同名Effect调用.md](../../Mechanics/39-道具同名Effect调用.md)
- 调用关系依赖名称匹配，不应把道具 ID 与 Effect `.name` 写成不同字符串。
- 当前尚未明确缺少同名 Effect 或漏写 `.item 1` 时的具体失败表现；实现时必须同时满足同名与 `.item 1` 两项要求。
# 常见错误
- 只创建道具定义，却没有创建与道具 ID 同名的 Effect。
- 同名 Effect 中漏写 `.item 1`，或误写为 `.item true`。
- 在非道具调用的普通 Effect 中无理由添加 `.item 1`。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1926`
```darkest
effect: .name "bandage" .target "performer" .item 1 .chance 100% .cure_bleed 1
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:20`
```darkest
effect: .name "holy_water_vamps_debuff" .target "performer" .item 1 .duration 12 .chance 100% .buff_ids SPD-5 BLIGHTRESIST-40
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:16`
```darkest
effect: .name "district_laudanum_override" .target "performer" .item 1 .duration 3 .chance 100% .clearDotStress 1 .buff_ids laudanum2_stress_buff
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 无夜补充：道具使用时调用与道具 ID 同名的 Effect，且该 Effect 必须写 `.item 1`。
- Sasiji Buff 源类型表：`.item` 对应 `bsrc_item`。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
