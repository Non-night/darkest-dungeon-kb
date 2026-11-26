# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.bark
# 分类
扩展/专项字段
# 参数类型
单个字符串
# 参数约束
- 单参数关键字；参数按一个字符串处理。现有原版实例均只填写一个本地化条目 ID。
- 参数不是直接显示的喊话文本，而是 `loc` / `loc2` 中的本地化条目 ID。
- 生成 Mod 时，必须在本地化 XML 源文件中定义同 ID 条目，并将其编译为游戏读取的本地化文件。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.bark <localization_id>`：使目标英雄进行喊话；实际显示内容取自对应本地化条目。
# 作用范围
- 喊话只能发生在英雄身上，具体目标由 `.target` 与调用方共同决定。
- 目标为怪物时不会发生任何事；当前不确定是否同时产生红字报错。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 本地化冲突先比较格式：`loc` 高于 `loc2`，且跨格式覆盖无视 Mod 优先级；只有格式相同时才按 Mod 优先级。
- 详见：[Mechanics/16-loc与loc2本地化覆盖优先级.md](../../Mechanics/16-loc与loc2本地化覆盖优先级.md)
- `.bark` 只保存本地化条目 ID；游戏显示的是当前语言 `loc` / `loc2` 中该 ID 对应的文本。
- 当前游戏的 Mod 上传器默认将本地化 XML 编译为 `loc2`；创作时仍应在 XML 源文件中维护对应条目。
- 怪物不能通过 `.bark` 喊话；以怪物为目标时该效果不发生。是否出现红字报错当前未确认。
# 常见错误
- 把参数直接写成想显示的台词，而没有填写本地化条目 ID。
- Effect 引用了某个 ID，但本地化 XML 及编译后的 `loc` / `loc2` 中没有对应条目。
- 在同一 `.bark` 后填写多个参数。
- 把怪物作为目标并期望其喊话。
- 处理本地化冲突时只比较 Mod 优先级，忽略 `loc` 的格式优先级高于 `loc2`。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:541`
```darkest
effect: .name test_egg_increment_bark_1 	.target target .chance 100% .bark egg_increment_bark_1 .on_hit true .on_miss true .queue true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:125`
```darkest
effect: .name "grind bark" .target "target" .bark str_boss_miller_grind .chance 100% .on_hit true .on_miss false .queue true .apply_once true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:542`
```darkest
effect: .name test_egg_increment_bark_2 	.target target .chance 100% .bark egg_increment_bark_2 .on_hit true .on_miss true .queue true
```
# 本地化配套案例
Effect 引用：
```darkest
effect: .name test_egg_increment_bark_1 	.target target .chance 100% .bark egg_increment_bark_1 .on_hit true .on_miss true .queue true
```
对应 XML：`DarkestDungeon\dlc\580100_crimson_court\localization\CC.string_table.xml:32`
```xml
<entry id="egg_increment_bark_1"><![CDATA[My guts roil!]]></entry>
```
`.bark` 参数 `egg_increment_bark_1` 与 XML 的 `entry id` 完全一致；CDATA 中的内容才是实际显示的喊话文本。

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- Effect 实例：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:541`。
- 对应本地化定义：`DarkestDungeon\dlc\580100_crimson_court\localization\CC.string_table.xml:32`。
- `loc` / `loc2` 的覆盖顺序及怪物目标行为属于社区实测结论；怪物目标是否产生红字报错当前未确认。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
