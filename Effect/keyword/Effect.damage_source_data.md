# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.damage_source_data
# 分类
扩展/专项字段
# 参数类型
单个字符串（可加引号或不加引号）
# 参数约束
- 只接受一个字符串参数，可加引号或不加引号。
- 在 `.damage_source_type monster` 的用法中，参数应填写怪物小类 ID，不填写怪物大类 ID。
- 怪物目录结构为 `monsters\<大类ID>\<小类ID>`；小类 ID 格式为 `<大类ID>_<单字符差分>`。下划线后必须恰好一个字符，多字符后缀不合法。A-Z 大写字母与 0-9 数字已确认可用；`@`、`#` 疑似可用但尚待确认，其他单字符不预设。Size-0 也属于怪物，故默认适用。
- Size-0 首先属于怪物，故怪物来源数据和通用怪物性质默认也适用于 Size-0；明确记录的专项例外除外。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.damage_source_data <id>`：提供与 `.damage_source_type` 配套的伤害来源数据。
- 怪物来源的示例形式为 `countess_D`，其中 `countess` 是大类 ID，`countess_D` 是小类 ID。
# 作用范围
- 主要用于使伤害的来源数据与伤害来源类型共同参与伤害归因及相关表现。
- 不要把该字段理解为任意文本标签；参数必须与来源类型所需的数据格式匹配。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 怪物来源数据使用小类 ID；后缀必须恰好一个字符，不能多字符。A-Z 大写字母和 0-9 数字已确认可用，@/# 疑似可用但待确认。Size-0 也属于怪物。
- 详见：[Mechanics/19-Effect性质不够确定.md](../../Mechanics/19-Effect性质不够确定.md)
- 引号不是参数内容的一部分；带引号和不带引号均可。
- 已确认可用的差分字符包括单个大写字母 A-Z 和单个数字 0-9。
- `@` 与 `#` 疑似可用但尚待确认；不要写成确定合法或确定非法。其他字符形式也未确认。
- 唯一明确的长度限制是差分后缀必须恰好一个字符；多字符差分不合法。
- 官方案例还展示了 `.damage_source_type trinket` 配套饰品 ID 的写法；不要将怪物小类差分规则套用于其他来源类型。
# 常见错误
- 在怪物来源场景中填写大类 ID，而不是小类 ID。
- 一次填写多个参数，或把带空格的未加引号文本当成一个字符串。
- 使用多字符怪物小类后缀。
- 未经确认就把 `@`、`#` 或其他未确认字符形式判断为确定合法或确定非法。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:414`
```darkest
effect: .name hatch_health_damage_1 .target target .chance 100% .health_damage 15 .damage_type attack .damage_source_data countess_D .damage_source_type monster .on_hit true .on_miss true .queue true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:243`
```darkest
effect: .name "Thirsting Blade Self Atk On Miss" .target "performer" target .chance 100% .health_damage 5 .damage_type additionaleffect .damage_source_data "com_hel_thirsting_blade" .damage_source_type "trinket" .on_hit false .on_miss true .queue true .apply_once true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:415`
```darkest
effect: .name hatch_health_damage_2 .target target .chance 100% .health_damage 18 .damage_type attack .damage_source_data countess_D .damage_source_type monster .on_hit true .on_miss true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 官方 DLC `DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:414` 使用 `.damage_source_data countess_D` 与 `.damage_source_type monster`。
- 官方 DLC `DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:243` 使用 `.damage_source_data "com_hel_thirsting_blade"` 与 `.damage_source_type "trinket"`。
- A-Z 大写字母和 0-9 数字已确认可用；`@` 与 `#` 疑似可用但尚待确认，不能写成确定合法或确定非法。其他单字符形式尚未确认。下划线后恰好一个字符是明确长度边界，多字符差分不合法。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
