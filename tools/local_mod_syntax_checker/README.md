# Darkest Dungeon 本地 Mod 静态检查器

这是供其他 Agent 调用的只读命令行工具。它检查 Mod 源文件并输出带路径、行列、级别、诊断码和来源的 JSON/文本诊断；不会修复或改写 Mod、游戏、VSIX 或 Buff 检查器文件。

## 快速运行

这是 Python 工具，Agent 无需构建 .NET 项目即可调用：

```powershell
python tools/local_mod_syntax_checker/checker.py --root "<Mod根目录>" --json
```

如果 Mod 引用了原版、DLC 或其他依赖 Mod 的定义：

```powershell
python tools/local_mod_syntax_checker/checker.py --root "<Mod根目录>" --reference-root "<游戏本体目录>" --reference-root "<依赖Mod目录>" --strict-references --json
```

参数：

- `--root <目录>`：必填，Mod 根目录。
- `--reference-root <目录>`：本次运行临时追加的游戏本体、DLC 或依赖 Mod 检索目录，可重复；不传时不读取任何游戏/Mod 外部目录。
- Python 与 C# 入口都跳过名称以 `.` 开头的文件和目录，涵盖目标 Mod 与引用目录。诊断和 ID 索引共用此扫描范围。
- 已知扩展名但不处于标准可扫描目录的文件只报告 `KB-FILE-UNREADABLE-PATH` 信息，不继续做内容语法检查。
- 路径判断以游戏实际功能目录为准，支持 DLC 直接功能路径 `dlc/<DLC-ID>/effects/...`、DLC 的 `features/<feature>/effects/...`，以及更深层的 `features/<feature>/modes/<mode>/effects/...`；原版根目录的 `modes/<difficulty>/effects/...` 也会被识别（该层用于难度专属配置，并非 DLC 包装层）。这些包装段会被剥离后再判断 `effects/`、`monsters/`、`trinkets/` 等功能路径。
- 默认引用索引包含游戏本体及 DLC，但不扫描游戏根下其他 Mod。需要解析其他 Mod 的定义时，通过一个或多个 `--reference-root <该依赖 Mod 根目录>` 显式提供；若该 Mod 位于游戏 `mods/` 目录中，也应传入具体 Mod 根目录，不要传整个 `mods/` 目录。
- 怪物定义 ID 另检查长度：大类 ID ≤30 字符，完整小类 ID ≤32 字符；超限分别报告 `KB-MONSTER-BASE-NAME-TOO-LONG` 与 `KB-MONSTER-SUBCLASS-NAME-TOO-LONG`。
- 工具不写死游戏安装盘符：本地 Mod 路径位于 `steamapps/common/DarkestDungeon` 下时，自动定位其所属游戏根；Steam Workshop Mod 位于 `steamapps/workshop/content/262060/<modID>` 下时，自动定位同一 Steam 库的 `common/DarkestDungeon`。游戏本体、DLC 和依赖 Mod 目录不再固定或自动依赖其他设备路径；需要这些定义时，AGENT 必须在本次运行向当前用户索要目录，并通过 `--reference-root <目录>` 传入。未传入时只检查目标 Mod 与知识库内置规则。
- `--strict-references`：保留兼容参数；当前 Effect/Mode/Buff/rarity/颜色等无法解析的空引用已经直接报告为 error。
- `--json`：输出 Agent 适合直接解析的 JSON。

验证：

```powershell
python -m py_compile tools/local_mod_syntax_checker/checker.py
python tools/local_mod_syntax_checker/test_checker.py
python tools/local_mod_syntax_checker/test_update_rules.py
```

Agent 默认调用 `checker.py`，无需 .NET；目录中的 C# 入口仍维护，可用于完整 Buff 专项检查。两入口的新版基础字段共用 `update_rules.json`，并非所有历史检查项完全等价。

## Build 28385 新版适配

- 2026-11-08按已采纳的2026-11-05更新清单逐项修复，而非只放行 `.force_selection` / `.ignore_hp_scale`。详见 `UPDATE_COVERAGE.md`。
- 两入口共享5个 Header 限定布尔字段、16项 Effect 参数规则和10个新增目标；`.dotShuffle` 不再被旧数值布尔表限制为0/1。字段缺参数、类型错误、未知字段、错误 Header 仍报错；不推定省略默认值或未公开的字符串枚举。
- Buff 的25种附魔数组与 `force_negative` 均检查字段类型；空数组合法。Python 从内置 Core 字段表读取类型，避免再次维护过期副本。已补齐的7种 Buff 属性继续保留主副类型检查，不扩大偷取属性值域。
- 守护/移除守护使用 `.force_resist_type` 时，不再误报“不受概率约束”；饰品目标允许 `other_trinket`。删除已过时的部分 Rule 必不能触发攻击附魔诊断，不据此取消仍有实测依据的迷乱/眩晕风险提示。
- 新饰品 Trigger 数组、扎营 `effect` 的 `sub_type` / `has_description`、事件 `specific_recruit` 参数、怪癖 `evolution_duration_type` 已补基础类型/值域检查。怪癖新单位依原说明为 `combat_end` / `quest_end`。
- 上述 JSON 专题仍输出 `KB-COVERAGE-PARTIAL`，明确尚未完整验证的结构/组合/运行时行为；无 error 不代表完整游戏验证。追加 props、BGM 和怪癖图片资源的引擎加载效果不属于语法校验。

## VSIX 与 Buff 检查器接入

- 2026-11-08修复内置规则副本过期：支持 `effect_chance`、`crit_dmg_multiply`、`crit_dmg_add`、`heal_crit_chance_add`、`heal_crit_chance_multiply`、`hp_heal_amount_received`、`disable_combat_skill`。前者和最后一项要求非空动态副类型，其余五项不使用副类型；不因此扩大 `.steal_buff_stat_type` 的允许范围。Python与保留的C#入口均补回归检查，不改外部VSIX/独立检查器或目标Mod。
- Python 工具从知识库的 `tools/info_schema_data.json`、`RAG/effect_keywords.jsonl` 与 VSIX 规则对应的静态数据读取 Info/Effect 字段，覆盖 Header、关键字、值域、引用、结构与常见危险组合。
- Python 工具直接检查 Buff JSON 的结构、必需字段、rule_data、always 取反等高频错误；完整 Buff 专项规则已随 `tools/local_mod_syntax_checker/vendor/BuffGrammarChecker.Core/` 内置，不依赖外部 Buff 检查器目录。
- 不修改 VSIX、Buff 检查器、游戏本体、Workshop 内容或 Mod。

```powershell
dotnet build tools/local_mod_syntax_checker/LocalModSyntaxChecker.csproj
```

内置规则副本不会实时读取或修改外部插件；外部规则变化仍需审核后同步，并运行两个测试文件。C# 构建时把共享新版规则嵌入程序集，因此修改规则后须重新构建 C# 入口。

## 检查范围与来源区分

### VSIX 诊断（`source` 指向 VSIX 文件）

- `.effects.darkest`、`.info.darkest`、`.art.darkest`、`.override.darkest` 的 Header/关键字、字段上下文、参数值与数量/长度、注释、中文代码字符、引号配对/间距，以及 VSIX 对动态 `_effects` 名称和 6 个 Effect ID/64 字符后备限制的诊断。
- VSIX 明确实现的 Effect 顺序/互斥、饰品目标、简写 Buff 主副类型、`skill_instant` 等危险目标组合，以及 Info 特殊列表/`death_class:` 冲突。
- `spawn: .effects` 上限 31 的 VSIX 诊断是**一项独立规则**：参数长度按 VSIX 源码的“去掉空白后”计数，刚到上限报 warning，超限报 error。

这表示命令行覆盖当前 VSIX 源码中的静态诊断规则，不代表游戏引擎语法或运行时行为验证。

### Buff 定义检查（`source` 指向 BuffGrammarChecker.Core）

Python 对 `*.buffs.json` 以及 `shared/buffs/` 下的 JSON 做基础结构、字段类型、主副类型、rule_type 与部分高频错误检查，并输出 `KB-COVERAGE-BUFF-PARTIAL`。它不调用 C#，也不声称覆盖全部 Rule 联动和特殊 ID 语义；基础 Buff 诊断定位目前是文件级，消息包含数组下标。

C# 入口调用内置 `BuffFileValidator`，保留完整专项语义与行列/JSON 路径诊断。如需这部分检查，构建后运行：

```powershell
dotnet tools/local_mod_syntax_checker/bin/Debug/net8.0/LocalModSyntaxChecker.dll --root "<Mod根目录>" --json
```

### 知识库静态检查（`source` 指向知识库记录）

- `*.darkest`/`*.json` 的 UTF-8 无 BOM；Info 非注释行达到 511 字符时报告可能截断；Effect 定义文件检查 `effects/` 目录与非空自定义文件前缀。
- 本地化 `*.string_table.xml` 的 XML 解析、必需的 `english` 基准语言、空 Entry ID、可识别格式参数的跨语言数量/类型/具名名称一致性，以及 `{colour_start|ID}` 颜色引用。
- 本地引用索引：Effect ID 来自 Effect `.name`，Mode ID 来自 `mode: .id`，Buff ID 来自 `buffs[].id`，颜色 ID 来自 `colour: .id`；并检查 `valid_modes`、动态模式 Effect、`set_mode`、Info Effect 列表与 `.buff_ids` 中的本地引用。
- `spawn: .effects` 另有知识库的保守安全检查：**单独**按 ID 内部原始长度（包含空格、不含外层引号）超过 31 时给 KB warning。该值是保守安全边界，知识库注明底层精确计数边界未知；这不是 VSIX 的计数方式，也不会替代上面的 VSIX 31 字符规则。

### 当前用户明确要求的引用闭包

- Info 技能的 `.effect` 和动态 `.<mode_id>_effects`：Effect ID 必须能在 Mod、游戏本体或 DLC 扫描集合找到 `.name` 定义。
- 每个 `.<mode_id>_effects` 中的 mode ID 必须能在扫描集合找到 `mode: .id` 定义；并且同一技能行必须有 `.valid_modes` 且包含该 mode ID，否则报告 `KB-INFO-MODE-EFFECT-NOT-VALID`，该模式差分视为未写入。
- 空引用会在 Mod、游戏本体、DLC 和显式 `--reference-root` 全部扫描后仍找不到时报告 error；其他未扫描的依赖 Mod 目录需要通过 `--reference-root` 提供。

### 知识库字段约束的其他静态引用检查

除当前用户点名的 Info 引用外，工具也按知识库字段记录检查 `.valid_modes`、受支持的 Info Effect 列表、Effect `.set_mode` 与 `.buff_ids`。这些是 `source` 标为知识库静态约束的检查，不应与当前用户新增的检查混为一谈。Buff 的完整专项语义仅在 C# 入口由 `BuffGrammarChecker.Core` 验证；两入口均不额外推断 Buff 字符串数组中的 ID 引用关系。

## 额外自动检查范围

除 VSIX 与 Buff 规则外，Python 检查器还覆盖知识库中适合静态化的内容：

- 编码：`*.json`、`*.darkest`、本地化 XML 的 UTF-8/BOM。
- 路径：只有处于标准可扫描目录的文件才进入内容检查；不在标准目录的已知文件只反馈不会被游戏读取。检查 Effect `effects/`、颜色 `colours/`、本地化 `localization/`、Buff `shared/buffs/`、饰品 `trinkets/`、英雄目录与怪物目录层级，以及 `project_paths.txt`。
- Info：未知 Header、Header 与关键字不匹配、无 Header 关键字、`death_class` 冲突、Info 511 字符截断、`.valid_modes`/`.effect`/动态 `_effects`/受支持 Effect 列表的 ID 引用。
- Effect：未知关键字、`.name` 为空、`.set_mode`、`.buff_ids` 引用缺失。
- 本地化：XML 解析、`english` 基准节点、空 Entry ID、格式参数签名差异、颜色 ID 缺失。
- 饰品：`trinkets/*.entries.trinkets.json`、`trinkets/*.rarities.trinkets.json` 的目录、顶层数组、饰品 ID、Buff ID、rarity、visual_rarity、award_category；饰品 Buff 和稀有度引用会与扫描到的定义闭包对照。
- 怪物：`monsters/<大类>/<大类>_<单字符差分>/<同名前缀>.info.darkest|.art.darkest` 的路径、目录名、文件名前缀；允许大写，小类目录名与 info/art 文件名前缀必须包括大小写完全一致，不能先转小写再比较；大类最多 30 字符、完整小类最多 32 字符；小类后缀允许已确认的单个 A-Z 或 0-9；如果大类/小类目录下继续嵌套目录，并在其中或其子目录放置 info/art 文件，则报告错误。
- Mod 元数据：`project.xml` 的其他常用字段缺失与 XML 错误，以及 Mod 根目录名包含 `error` 的禁用片段。`PublishedFileId` 是首次工坊发布后由上传器回写的项目 ID；自用 Mod 可以始终没有该 ID，计划发布但尚在测试的 Mod 也可以没有。普通静态检查对该字段省略或留空均不报警，不因 `UploadMode` 指向上传就要求预填 ID。
- 诊断来源区分：VSIX 规则、知识库规则、当前用户要求的引用闭包、Buff 专项规则分别写入 `source`，Agent 不应把静态规则误报成实机行为。

未自动化的内容仍包括：运行时 Effect 时序、AWR/queue、目标集合最终行为、游戏内 Entry 消费、`.loc2` 二进制、官方 `localization.exe` 的完整编译器诊断，以及任何需要实机或 app.log 才能确认的行为。

## 本地化检查边界

Entry ID 消费规则不是完整白名单；重复 Entry 在知识库记录中有可编译案例，故不会一概报错，也不会因未知 ID 判错。格式检查只比较能识别的转换字符 `d f u i s c` 和具名参数；不凭单个 `%` 断言错误，因为固定 `description_tooltip_id` 文本和格式字符串的百分号转义条件不同。若 XML 使用编译器未记录的格式扩展，不会被硬拒绝。

工具不解析二进制 `.loc`/`.loc2`，也不代替官方 `localization.exe`。自动编译仍须检查控制台诊断和生成物，不能只看退出码或 `SUCCESS!`；静态通过也不证明 Entry 在游戏运行时被消费或显示。

## VSIX 逐项对照状态

Python 工具的 VSIX 规则来自知识库内置副本，对照源为：

- `VSIX/Error/EffectErrorTagger.cs`
- `VSIX/Error/InfoBaseErrorTagger.cs`
- `vendor/vsix/DarkestData.cs`

目前已移植并由回归测试覆盖的诊断族包括：

- Effect：行内注释、中文代码字符、引号配对/相邻、Effect Header/块结构、未知关键字、`.name`、饰品目标、`.cure`/`.heal` 顺序、DOT 同行冲突、列表参数数量/长度、spawn 定向顺序、`skill_instant`/`.keyStatus`/`.monsterType` 目标、`.use_item_id` 配套、简写 Buff 主副类型、守护 `.chance`、`daze`、`affliction_blockable_chance`、特殊 Buff 源和枚举值。
- Info / Art / Override：Header、关键字上下文、动态 `_effects`、跨行参数、布尔/固定值、特殊多值列表、mode 名长度、字符串参数长度、参数数量、死亡类别冲突、`.was_killed_effects`、中文代码字符、引号和行内注释。
- 值域与 Buff 主副类型从内置 `vendor/vsix/DarkestData.cs` 读取；已采纳的新版目标不得被旧副本覆盖。新增规则通过 `update_rules.json` 共享，历史字段表只作基础，不再视为最新游戏规则的唯一来源。

`test_checker.py` 中的 VSIX parity tests 会对上述诊断族逐项构造触发案例；新增或修改 VSIX 规则后，应先更新对照实现和 parity tests，再报告覆盖状态。静态工具仍不声称覆盖 VSIX 编辑器 UI 的着色、补全、错误列表跳转或实时刷新行为。

## 诊断级别与出口码

- `error`：静态语法/结构错误，或启用严格引用后仍缺少定义；退出码 `1`。
- `warning`：不确定的外部引用、建议性规则或可能风险；默认不改变退出码。
- `info`：VSIX 的建议类诊断；默认不改变退出码。
- 参数/工具/依赖故障：stderr 说明原因，退出码 `2`。

## 外部源同步

知识库内已保存 Size-0 模板、VSIX DarkestData.cs 和 BuffGrammarChecker.Core 源码。需要从当前设备刷新时运行：

`powershell
python tools/sync_external_sources.py
` 

同步规则：外部源目录/文件不存在则忽略；只比较知识库内已经存在的同相对路径、同文件名文件；发现内容不一致时以外部源覆盖知识库副本；外部新增文件不会导入，知识库已有文件不会因外部缺失而删除。
