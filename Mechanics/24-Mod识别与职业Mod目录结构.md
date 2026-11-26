# Mod 识别与职业 Mod 目录结构

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 上传器内置官方帮助的来源

知识库编写者于 2026-09-20 提供双击 `steam_workshop_upload.exe` 后输出的 `sample_project.xml` 使用说明。它属于官方工具内置帮助的转录，不是本次 Agent 实际运行上传器所得；具体工具版本未知。本页据此确认文档声明的用途、候选值与可选项，不把尚未实测的解析、边界和上传覆盖行为当作已验证。

官方流程：复制生成的项目文件，填写字段后拖到上传器；上传器按 `UploadMode` 处理。`dont_submit` 只生成本地化文件和 `modfiles.txt`，不提交；其他所列模式涉及上传。上传器会向项目文件写入 `PublishedFileId`，用于后续更新，应继续保留该项目文件。此历史教程不是当前任务的上传授权。

`Title` 是 Mod 名称。`Tags` 是可选关键词数组。官方说明将 `ItemDescriptionShort`、`ItemDescription`、`Tags`、`ModVersionMajor`、`ModVersionMinor`、`TargetBuild` 标为 Optional；未标 Optional 的字段不能仅据这段输出进一步推断所有省略行为。

### Win32 上传器生成模板

当前用户于 2026-11-21 补充：Windows Steam 版进入游戏根目录的 `_windows\win32`，直接双击 `steam_workshop_upload.exe`，不传入 `project.xml`，可以生成 `sample_project.xml`。把模板复制到自己的 Mod 根目录，改名为 `project.xml`。本机已静态确认该路径有 x86 上传器和模板，随附模板使用 `direct_upload`。本地编译先将项目的 `UploadMode` 改为 `dont_submit`，再把项目文件交给上传器。生成模板的行为由当前用户说明和既有帮助转录支持，本轮未执行工具。见 [本轮教程证据](../Sources/tutorial_corrections_20261121.json)。

## 可被游戏引擎识别的 Mod 根目录
一个 Mod 文件夹必须同时包含以下两个文件，才可被游戏引擎识别为 Mod：

```text
project.xml
preview_icon.png
```

- `preview_icon.png` 必须为 `512×512` 像素；上传器帮助另要求文件小于 1MB，位于 `ModDataPath` 指向的 Mod 数据目录。1MB 的字节口径及其他格式、色彩空间要求未确认。
- `project.xml` 应以 `DarkestDungeon\_windows\sample_project.xml` 为格式范本。多写、少写或改动结构后会产生什么结果，当前资料未确认；创作时应保留范本结构，只替换字段值。

## Windows Steam 订阅 Mod 与在线版存档位置

- **订阅 Mod**：在相应 Steam 库的 `steamapps\workshop\content\262060\<作品ID>`。从游戏目录往上两级可定位到 `steamapps`；若对应下载不在此库，再查其它 Steam 库。`262060` 是游戏 App ID，作品 ID 取自创意工坊作品页的 `id=`。这与游戏根目录下的本地 `mods` 是不同目录。参考订阅版时建议复制到独立开发目录再编辑，避免 Steam 更新覆盖。
- **在线版存档**：从 Steam 客户端安装目录进入 `userdata\<账号数字目录>\262060\remote\profile_*`，不以游戏所在资料库为起点。备份前退出游戏，若使用 Steam 云则等同步完成，整份复制目标 `profile_*` 到存档目录外；不确定选哪一槽时可备份整个 `remote`。

本机只读确认了两种目录结构，见[本轮教程证据](../Sources/tutorial_corrections_20261121.json)。不将这些路径外推到其它平台或非 Steam 版本。

## `PreviewIconFile`

`project.xml` 中可以合法书写：

```xml
<PreviewIconFile>preview_icon.png</PreviewIconFile>
```

该字段指向 Mod 封面，也就是通常放在 Mod 根目录的 `preview_icon.png`。这是合法的 `project.xml` 配置项，不应因为它未出现在当前收录的官方范本片段中就删除或判定为非法。

当前尚未确认：

- `PreviewIconFile` 是否必写；
- 省略该字段后会发生什么；
- 参数能否填写相对路径，或能否指向根目录以外的图像；
- 该字段具体影响游戏内 Mod 识别、Mod 管理界面、上传器、Workshop 展示中的哪一个或哪些环节。

通常没有修改该字段的必要。创建普通 Mod 时可保留常见写法，使其继续指向根目录的 `preview_icon.png`；不要在缺少明确需求和验证的情况下改名、改路径，或从字段存在性继续推导未确认的行为。

## `ModDataPath`

官方内置帮助要求填写 Mod 数据目录的**绝对路径**。该目录应独立于游戏本体数据目录，包含用于覆盖或新增游戏内容的 Mod 文件，不能直接拿游戏数据目录作为上传目录。

知识库既有本地观察是在项目文件与 Mod 数据同目录的布局下使用；路径不匹配时观察到编译／上传识别失败，而本地游戏仍能加载 Mod。这是具体布局下的观察，不能提升为“官方要求项目文件必须与数据目录同目录”的普遍规则。官方帮助未要求二者同目录；项目文件在其他位置时的具体可用组合尚未专项核验。

常规同目录布局可让 `ModDataPath` 指向项目文件所在的 Mod 根目录。斜杠形式、末尾分隔符等边界继续保留为观察性信息，不编造解析器硬性规则。

## `Language`

`project.xml` 中的 `Language` 用于标记这个 Mod 所属的语言，例如：

```xml
<Language>schinese</Language>
```

其中 `schinese` 表示简体中文。该字段对 Mod 的实际运行好像没有明显影响；它究竟影响上传器元数据、Workshop 分类、筛选或其他界面，以及填写错误或省略时会发生什么，当前均未确认。因此应将“指定 Mod 所属语言”视为已知核心语义，但不能继续断言它具有某种已经验证的运行时作用。

合法参数可以参照游戏 `localization` 目录中的语言文件名。当前游戏目录可见的语言名包括：

```text
brazilian
czech
english
french
german
italian
japanese
koreana
polish
russian
schinese
spanish
```

这些名称应当都可作为 `Language` 参数使用，但当前结论主要来自语言文件名与字段用途的对应关系；除已有实例外，尚未逐项验证全部参数。填写时应直接使用对应语言的内部名称，不要擅自改写为中文名、地区代码或其他缩写。
## `UpdateDetails`

`project.xml` 中可以写：

```xml
<UpdateDetails>本次更新内容</UpdateDetails>
```

也可以留空：

```xml
<UpdateDetails/>
```

根据官方范本中的说明文字，可以推测该字段用于填写上传或更新 Mod 时的本次更新说明。但其具体由上传器如何读取、会自动显示在哪里，以及首次上传时是否使用，当前均未确认。

已知将该字段留空不会影响 Mod 的正常使用，因此没有明确需要时可以保留空元素。即使上传后需要补充或修改更新日志，也可以在 Steam 中再次编辑；不必为了本地运行或完成 Mod 结构而强行填写该字段。

Agent 应把“用于本次更新说明”明确标成依据官方范本文字得到的合理推测，而不是已经完整验证的机制。不得把 `UpdateDetails` 当成游戏内运行所需配置，也不要自行编造更新日志内容。
## `Visibility`

官方帮助列出三个预定义值：

| 值 | 官方说明 |
|---|---|
| `private` | 仅自己可见 |
| `friends` | 仅好友可见 |
| `public` | 所有人可见 |

它描述上传项目的可见性。更新时是否覆盖 Steam 已手动设置的可见性、省略或非法值如何处理，仍未知；不能据此推导本地 Mod 是否可加载。未经当前用户要求，不擅自更改可见性。

## `UploadMode`

官方帮助列出四个模式：

| 值 | 官方说明 |
|---|---|
| `direct_upload` | 直接上传 Mod 数据目录 |
| `copy_and_upload` | 必要时把文件复制到另一个目录，再上传 |
| `strip_and_upload` | 剔除原版文件后上传数据目录 |
| `dont_submit` | 只生成本地化文件和 `modfiles.txt`，不提交 |

复制目标目录、原版文件识别与剔除算法、是否修改输入目录及失败恢复行为，帮助没有说明；不能凭模式名自行实现或依赖这些细节。省略／非法值行为未知。

知识库既有记录还包括上传器生成的 `steam_workshop_uploader.log`；这是日志记录，不是本段官方帮助明列的输出。不要把 `dont_submit` 的“不提交”误解成“不写本地生成文件”。

## `modfiles.txt` 完整性验证

### 基本性质
`modfiles.txt` 是上传程序在假上传或真上传时自动生成的完整性验证文件。它不仅记录文件是否存在，还包含与文件字节数有关的验证信息。因此生成该文件后，再新增文件，或只给已有文件追加内容、改变文件长度，都可能使实际 Mod 内容与旧验证记录不一致。

仅以下两类 **mods 加载方式**会执行该完整性验证：

1. 从游戏根目录的 `mods` 文件夹加载；
2. 从 Steam Workshop 的 `262060` 订阅下载目录加载。

二者在这一点上没有本质差异。放在游戏根目录 `dlc` 文件夹中的 DLC 加载方式不会验证 `modfiles.txt`，官方 DLC 也使用这一加载方式。

### 通常行为
在 mods 加载方式下：

- 当 `modfiles.txt` 正常存在并生效时，实际存在但未记录的新文件，或长度与记录不符的旧文件及其新增内容，可能无法通过完整性验证，并被引擎视为不存在；
- 当 `modfiles.txt` 被删除或无法生效时，引擎通常会被迫检索全部文件，因此绝大多数新增和修改内容能够被正确读取。

所以进行任何 Mod 修改时，完成修改后必须删除旧的 `modfiles.txt`，避免旧验证记录导致修改无效、文件读取错位或其他异常。不得因为只修改了已有文件的内部内容就保留旧文件，因为字节数变化同样可能触发验证不一致。

如果最终需要重新上传，或 Mod 使用了下述依赖 `modfiles.txt` 的特例资源，应在删除旧文件并完成全部修改后，再通过假上传或真上传生成一份与当前内容相匹配的新 `modfiles.txt`；不能继续使用修改前生成的旧文件。

### 删除或不验证时反而失效的已知特例
少数特定文件在 `modfiles.txt` 被删除或无法生效时，反而会被视为不存在。目前确认的特例包括：

```text
Cursors\arrow.png
Fx\torch_load
Dungeons\_shared\shared.json
```

分别对应：

- 读档后的鼠标光标贴图；
- 读档界面中下方的读档火炬动画，不是副本中的火炬动画；
- 监狱房间定义文件。

`Dungeons\_shared\shared.json` 即使改成带自定义前缀的文件名，在没有有效 `modfiles.txt` 时仍不能正常读取。此前“添加前缀即可恢复”的结论来自残留的游戏根目录测试文件，属于已纠正的错误结论，不得继续采用。

这些特例目前看来极少，但是否还有其他特例尚未确认。排查“删除 `modfiles.txt` 后某个资源反而完全失效”时，不能只依赖通常的强制全文件检索规律。

### 三种加载方式
应区分：

1. **mods 加载**：游戏根目录 `mods` 或 Workshop `262060` 目录，会验证有效的 `modfiles.txt`；
2. **DLC 加载**：游戏根目录 `dlc` 目录，不验证 `modfiles.txt`，通常会强制检索内容，但上述少数特例可能因此失效；
3. **游戏根目录直接覆盖**：文件直接覆盖游戏根目录对应内容，既不依赖 `modfiles.txt`，也不等同于 DLC 的强制加载方式。上述特例位于游戏根目录时可以在没有 `modfiles.txt` 的情况下被读取。

虽然直接覆盖游戏根目录构成第三种加载行为，但通常不推荐 Mod 采用这种安装方式。Agent 不得为了绕过 `modfiles.txt` 特例而擅自修改或覆盖游戏本体。
## `VersionMajor` 与 `VersionMinor`

**拼写来源差异**：上传器内置帮助写的是 `ModVersionMajor` 和 `ModVersionMinor`，两者可选，组成 Mod 名旁的显示版本号，例如 `Foo (3.2)`。下列既有 XML 范本与记录使用 `VersionMajor`／`VersionMinor`。未核验解析器是否同时接受两套名字或是否因版本而异；不得直接改名，也不能宣称它们是已确认的别名。

这两个字段共同组成游戏内显示的 Mod 版本号：

```xml
<VersionMajor>1</VersionMajor>
<VersionMinor>0</VersionMinor>
```

以上组合会显示为类似：

```text
1.0
```

- `VersionMajor` 是版本号前半部分；
- `VersionMinor` 是版本号后半部分。

旧拼写字段的乱填、非整数、负数、空值或省略行为仍未确认，也未确认它们是否参与上传器的新旧版本判断。已知核心作用是组成游戏内显示版本号，因此不要在没有用户要求时擅自递增、重置或修改现有 Mod 的版本字段。

## `TargetBuild`

官方帮助将它列为可选字段，含义是 **Mod 设计用于运行的游戏构建版本**。因此用途不是未知；但是否进行兼容性阻断、合法值范围、非法值行为和 `0` 的特殊意义仍未知。已有范本使用 `<TargetBuild>0</TargetBuild>`，不能据此把 `0` 宣称为适配所有版本。

## `Tags`

`project.xml` 中可以使用以下嵌套结构填写一个或多个标签：

```xml
<Tags>
    <Tags>New Class</Tags>
</Tags>
```

外层 `<Tags>` 是标签列表容器，每个内层 `<Tags>` 保存一个标签字符串。为什么容器和列表项使用同一个元素名，目前未知；应按官方范本和现有 Mod 的结构仿写，不要为了“修正命名”而改成其他标签名。

标签字符串可以自定义。目前 Steam Workshop 页面上可见的分类与标签如下，其中 `GENERAL` 和 `CLASS MODS` 是分组标题，不是实际标签：

### `GENERAL` 分组

```text
Gameplay Tweaks
Overhauls
Trinkets
Monsters
Localization
UI
```

### `CLASS MODS` 分组

```text
New Class
Class Tweaks
Skins
```

Workshop 页面中显示在这些名称后面的括号数字是使用该标签的项目数量，**不是标签字符串的一部分**。例如应填写：

```xml
<Tags>New Class</Tags>
```

而不是：

```xml
<Tags>New Class(898)</Tags>
```

括号中的数量会随 Workshop 内容变化，不应写入 Mod 配置，也不应作为固定知识维护。

目前尚未确认：

- 自定义标签是否会在 Workshop 中显示为新的可筛选标签，还是仅作为普通元数据保存；
- 标签是否区分大小写；
- 是否存在数量或长度上限；
- 留空或省略整个列表时会发生什么；
- 更新已有 Workshop 项目时是否覆盖 Steam 页面上手动调整过的标签。

需要标准 Workshop 分类时，应优先原样使用页面已有的标签名称；只有用户明确要求自定义标签时才自行填写其他字符串。
## `ItemDescription`

官方帮助确认这是可选的 Mod 描述，用于 Steam 展示（原文 `for the Steam store`），要求 **under 8000 characters**。不再仅凭字段名推测其用途；保守按少于 8000 个字符处理。

旧范本提示 `8000 characters or less`，与帮助中的 `under 8000` 存在端点措辞差异；恰好 8000 字符是否被接受仍未验证。中文、换行、转义及格式标记如何计数，以及上传更新是否覆盖／清空已手动编辑的描述、空元素与省略是否等效，仍未知。不要套用打折 Buff 的 128 字符位计数。

没有当前用户的描述编写需求时可保留现有内容或空值，不擅自编造简介。

## `PublishedFileId`

`project.xml` 中的 `PublishedFileId` 对应该 Mod 在 Steam Workshop 中的发布项目 ID，例如：

```xml
<PublishedFileId>某个 Steam Workshop 数字 ID</PublishedFileId>
```

首次真正上传以前，应当不写该项或将其留空；如果未写，真上传时上传器会自动生成并写入对应 ID。强行预填一个 ID 会发生什么，目前未知。`dont_submit` 通常称为“假上传”，观察上它好像会把该字段写成 `0`，但这一点尚未完全确认。

该字段不属于日常手动修改项。上传前必须检查它不应被手动写成 `0`；已经成功发布的 Mod 应保留上传器记录的现有 ID。若成功上传后删除该字段，再由同一上传者上传，观察上好像仍会生成同一段 ID；不同上传者是否相同以及上传器依靠什么信息恢复该 ID，均未知，不得依赖这一行为。

### 与编译后 `loc2` 文件名前缀的关系

XML 本地化文件被编译为 `loc2` 后，生成文件通常以该 Steam Workshop ID 作为文件名前缀。一个从未真上传、只进行过 `dont_submit` 假上传的 Mod，其 `loc2` 文件名前缀会是 `0`。因此必须检查本地化目录中是否存在以下高风险命名：

```text
0_<语言名>.loc2
<语言名>.loc2
```

例如 `0_schinese.loc2` 或无前缀的 `schinese.loc2`。这类过于通用的文件名可能与其他 Mod 或原版文件同名并发生文件覆盖，严重时会使原版对应语言的大量本地化消失。

若 Mod 尚未获得真实 Workshop ID，应将生成的 `loc2` 文件改为具有唯一、非 `0` 前缀的名称，避免与其他内容重名。这里修改的是编译产物的**文件名前缀**，不是伪造或手动填写 `PublishedFileId`。

当本地化因覆盖或缺失而失效时，游戏内绝大多数文本会直接显示 XML 中本应引用的 `entry` ID，并呈蓝色，例如：





排查大范围蓝字时，应同时检查 `PublishedFileId`、是否只进行过假上传，以及 `loc`／`loc2` 文件是否使用 `0_` 前缀、无前缀通用文件名或与其他文件重名。
## `ItemDescriptionShort`

官方帮助确认该字段可选，是**游戏内 Mod 选择界面中鼠标悬停时显示的短简介**，要求 **under 512 chars**，保守按少于 512 个字符处理。

具体字符计数方式、恰好 512 是否接受、超长时的处理、换行／本地化支持，以及空元素与省略是否等效仍未知。不能继续把用途、可选性和声明的长度要求一概写为未知，也不能照搬打折 Buff 的字符位规则。

## Mod 文件夹名中的 `error` 禁用片段

当 Mod **根文件夹名称**中包含连续字符串 `error` 时，游戏将无法正常识别该 Mod。这里限制的是承载 `project.xml`、`preview_icon.png` 等内容的 Mod 文件夹本身，而不是 `project.xml` 中的显示标题或普通子文件名。

当前观察疑似表明该判断不区分大小写，即 `error`、`Error`、`ERROR` 等写法都可能触发同一问题；大小写行为尚未完全确认。创建或重命名 Mod 根文件夹时，应直接避免在任何位置、以任何大小写组合使用 `error` 这一连续字符片段，不要依赖大小写差异规避。

若一个目录结构看似完整、根部已有 `project.xml` 和 `preview_icon.png`，但游戏仍完全不能正常识别，应把“Mod 根文件夹名是否包含 `error`”列为优先排查项。

官方范本内容如下：

```xml
<?xml version="1.0" encoding="utf-8"?>
<project>
    <ItemDescriptionShort/>
    <ModDataPath>c:/absolute_path_to_your_mod_folders_data_directory/data</ModDataPath>
    <Title>Your Mod Title here</Title>
    <Language>english</Language>
    <UpdateDetails>When you update your mod, this is where you would describe your latest changes</UpdateDetails>
    <Visibility>private</Visibility>
    <UploadMode>direct_upload</UploadMode>
    <VersionMajor>0</VersionMajor>
    <VersionMinor>0</VersionMinor>
    <TargetBuild>0</TargetBuild>
    <Tags>
        <Tags>tag1</Tags>
        <Tags>tag2</Tags>
    </Tags>
    <ItemDescription>Describe your mod in 8000
characters or less here!</ItemDescription>
</project>
```

## 每种文件的路径与文件名都是必查项

读取、创建、修改或引用任何一种 Mod 文件时，不能只检查文件内部语法；还必须先核对：

1. 文件应位于哪个功能目录；
2. 文件名必须采用什么格式，前缀是否可以差分或自定义；
3. 文件名、父目录名与定义内部 ID 是否存在对应关系；
4. 引用的图片、动画、音频、本地化或其他配置是否位于引擎实际扫描的位置；
5. 当前知识是否已经确认这些要求是硬性规则、常规安全格式，还是仅有实例支持。

知识库若尚未记录某种文件的路径或命名要求，Agent 不得仅凭扩展名合法就随意创建，也不得把“内容可写在该文件中”误当成“文件放在任何位置、使用任何名称都会被加载”。应优先检查原版和官方 DLC 的同类结构；仍无法确认且该文件是实现所必需时，必须向用户说明缺口或询问，而不是脑补。

### Size-0 仍属于怪物

Size-0 虽是特殊单位，但首先仍是怪物，并具有通用怪物性质。除非某条机制明确排除 Size-0 或记载其专门例外，否则本文及知识库其他内容泛称“怪物”时均包含 Size-0；不得把“怪物”默认解释成“非 Size-0 怪物”。

### 战斗中怪物侧的 Size 总量上限

当前用户于 2026-09-30 明确补充：战斗中，Size 1 及以上的怪物总数不可能高于 4；整个怪物侧所有单位的 Size 之和必定小于等于 4。这里的“怪物侧”总量规则包含 Size-0，但 Size-0 的 Size 为 0，因此不会增加该总和。

- 对 Size 1 及以上单位，不能只按“单位数量”判断是否超出容量，还必须把每个单位的实际 Size 相加。
- Size-0 可以作为中间单位存在，不占用这条 Size 总量，但仍属于怪物并可能带来碰撞箱、目标筛选、死亡清理和时序负担；不能因为不占 Size 容量就把它当成没有战斗对象。
- 设计召唤、变身、复活、尸体替换或多单位生成时，必须检查生成后怪物侧全部 Size 的总和；如果会使总和超过 4，不能视为可正常容纳的战斗状态。
- “Size 1 及以上怪物总数不高于 4”是由 Size 总和小于等于 4 推出的数量边界；不要把它误写成 Size-0 也最多只能有 4 个。Size-0 的数量仍须按其自身机制、场上对象限制、碰撞箱和性能风险单独检查。

### 怪物定义文件的常规安全结构



```text
monsters\<怪物大类ID>\
├─ anim\
│  ├─ <怪物大类ID>.sprite.<动画中缀>.atlas
│  ├─ <怪物大类ID>.sprite.<动画中缀>.png
│  └─ <怪物大类ID>.sprite.<动画中缀>.skel
└─ <怪物小类ID>\
   ├─ <怪物小类ID>.info.darkest
   └─ <怪物小类ID>.art.darkest
```

例如：

```text
monsters\com_lp_trinketSS_Summon\com_lp_trinketSS_Summon_A\com_lp_trinketSS_Summon_A.info.darkest
monsters\com_lp_trinketSS_Summon\com_lp_trinketSS_Summon_A\com_lp_trinketSS_Summon_A.art.darkest
```

同一个大类可以复用多个差分：

```text
monsters\mod_size0\anim\mod_size0.sprite.combat.skel
monsters\mod_size0\mod_size0_A\mod_size0_A.info.darkest
monsters\mod_size0\mod_size0_B\mod_size0_B.info.darkest
monsters\mod_size0\mod_size0_1\mod_size0_1.info.darkest
```

这表示一个 `mod_size0` 大类，下面有 `_A`、`_B`、`_1` 三个小类；动画资源只需在该大类的 `anim` 下维护一套，除非某个小类确实需要不同动画资源。

- `<怪物大类ID>` 是目录、动画资源和小类文件名前缀的组织 ID；它**不强制等于** `enemy_type: .id`。`enemy_type` 可以任意书写，也可以在同一怪物定义中写多个 ID；把大类 ID 也写成 `enemy_type` 只是部分作者为了方便采用的习惯写法，不是引擎要求。
- `<怪物小类ID>` 必须采用 `<怪物大类ID>_<单字符差分>`：下划线后必须恰好一个字符，多字符后缀一律不合法，如 `_AA`、`_10`。目前明确确认可用的是大写字母 `A`–`Z` 与数字 `0`–`9`；`@`、`#` 疑似可用但尚待确认，不能写成确定合法或确定非法；其他字符形式也待确认。
- **怪物大类名不得超过 30 个字符；怪物小类 ID／小类文件夹名不得超过 32 个字符**。小类长度计数包含完整小类名中的大类 ID、下划线和差分后缀（例如 `_A`）。这两个上限按当前用户明确更正分别记录，不再通过后缀长度相减推导另一项。超过对应上限会导致游戏产生截断，进而无法正确识别相关怪物；创建或审查普通怪物、Size-0 时必须分别检查大类名和完整小类名。

- **大类复用优先**：如果多个怪物或 size-0 只需要不同的差分、标签、Stats 或 Info 内容，而可以共用同一套 `anim`、Art 结构和兼容边界，应使用一个大类，在其下创建多个小类。不要为每个小类默认新建一个只有 `_A` 的大类；
- 只有在动画/Art、对象侧、enemy_type 语义、加载覆盖、Info 兼容性或其他已确认边界确实不兼容时，才拆分新的怪物大类。大类数量越多，游戏加载成本越高；
- 小类文件夹名与其中 `.info.darkest`、`.art.darkest` 的文件名前缀必须完全相同，包括大小写；允许使用大写，不能把小类名强制转小写后要求文件匹配。知识库编写者2026-11-05明确纠正；检查器诊断 `KB-MONSTER-FILENAME-MISMATCH` 按原始名称精确比较。
- 同一大类的动画通常放在大类目录下的 `anim`，由各小类的 Art 定义引用；
- Info 与 Art Header 在语法上可以跨 `*.info.darkest`、`*.art.darkest`、`*.override.darkest` 书写，不等于可以忽略上述引擎扫描目录与常规文件命名。

目前尚未完整验证：怪物大类目录、小类目录和文件名前缀的目录层级/扫描要求是否每一项都属于绝对不可改变的硬性要求。小类差分长度已明确要求恰好一个字符；哪些字符已经确认、哪些仍待确认，按上文记录。

### 怪物 AI（monster brain）定义文件

- 怪物 Info 中的 `monster_brain: .id <AI_ID>` 用于引用另一处怪物 AI 定义的 `id`。
- 定义文件放在 `raid\ai\` 下，安全文件名格式为 `*.monster_brains.json`。
- 文件顶层使用 `monster_brains` 数组，一个文件可以定义多个带有独立 `id` 的 AI 条目。
- 原版 `raid\ai\base.monster_brains.json` 中实际定义了 `id` 为 `default` 的条目，因此 `monster_brain: .id default` 不是无定义的占位字符串。
- 官方文件存在 `base.monster_brains.json`、`arena.monster_brains.json`、`shieldbreaker.monster_brains.json`、`color_of_madness.monster_brains.json` 和 `additional.color_of_madness.monster_brains.json` 等命名，说明 `*` 前缀可有不同名称，甚至可以包含点号；但创作时仍建议使用稳定且能够追溯到本 Mod 的前缀。
- 对于 Size 0 中间单位，`monster_brain:` 只有保证怪物定义完整的意义；Size 0 不受 AI 干涉。非 Size-0 的普通怪物则必须继续检查被引用条目中的技能选择、目标选择、冷却等完整配置，不能只根据 AI ID 猜测行为。

## 内容较完整的职业 Mod
以玩家可游玩的内容完整性而言，一个较完整的职业 Mod 往往包含：

```text
audio
campaign
effects
heroes
localization
panels
raidshared
trinkets
upgrades
```

这份列表描述常见的完整配置，不是判定 Mod 文件夹是否合法的固定清单。较精简的职业 Mod 可以缺少其中若干目录；某个可选功能一旦被使用，其对应资源和定义仍必须存在。

## 职业本体的核心内容
- `heroes` 目录及其内部的角色动画、`art` 定义和 `info` 定义属于职业本体的核心内容。
- `art` 与 `info` 指定义内容，不要求必须按文件名机械分开。两类定义可以写在同一个文件中，例如统一放进 `info`、`art` 或其他文件名的文件；社区习惯仍是将 `info` 与 `art` 分开，便于阅读和维护。
- 当前资料仅有“`upgrades` 也必须存在”的转述，尚未得到确认。为保证常规职业 Mod 的完整性，建议保留 `upgrades`，但 Agent 不得将其描述为已经证实的引擎识别条件。
- 除职业核心内容外，其余目录相对于最小职业本体可视为按功能选用；它们仍可能是音频、技能 Effect、本地化、界面、共用资源、饰品或升级系统正常工作的必要组成。

## Agent 判断顺序
1. 检查 Mod 根文件夹名是否包含任意大小写形式的连续字符串 `error`；如有，应先重命名并完全避开该片段。
2. 判断文件夹根部是否同时存在 `project.xml` 与符合尺寸要求的 `preview_icon.png`。
3. 检查 `project.xml` 是否保留官方范本结构。
4. 检查 `ModDataPath` 是否为独立 Mod 数据目录的绝对路径；项目文件与数据同目录只是常规布局；若上传器无法识别而游戏内本地游玩正常，应优先排查该字段。不要把反斜杠和末尾斜杠的观察性行为写成已确认硬规则。
5. 若存在 `PreviewIconFile`，确认其作为合法 Mod 封面字段保留；普通情况下维持指向根目录 `preview_icon.png`，不要擅自改名、改路径或断言其必写。
6. 检查 `Language` 是否使用游戏 `localization` 目录中的语言内部名称；不要把其实际影响范围或省略行为说成已确认。
7. `UpdateDetails` 没有明确的更新说明需求时可保持为空；不要将其推测用途写成已完整验证的机制，也不要自行编造更新日志。
8. 检查 `Visibility` 是否符合用户对上传后公开状态的要求；使用官方列出的 `public`、`friends` 或 `private`，且不得推断更新时一定会覆盖现有可见性。
9. 检查 `UploadMode` 是否符合用户要求：`direct_upload` 会直接上传，`dont_submit` 只编译而不上传。
10. 修改 Mod 后删除旧 `modfiles.txt`；若包含依赖该文件的已知特例，或需要发布，再在所有修改完成后重新生成匹配当前内容的新文件。不得用直接覆盖游戏根目录绕过问题。
11. `VersionMajor` 与 `VersionMinor` 是否正确组成用户要求的游戏内显示版本号？未经要求不得擅自改动；不要编造异常参数行为。
12. `TargetBuild` 声明目标游戏构建版本；具体校验行为与 `0` 的意义仍未知。
13. `Tags` 是否保持外层列表与内层同名项的范本结构？是否只把实际标签写入参数，而没有把 `GENERAL`、`CLASS MODS` 分组标题或括号中的项目数量写进去？
14. `ItemDescription` 没有专门需求时是否保持为空？若填写，是否按官方 Steam 描述用途与少于 8000 字符的保守限制填写，并保留计数和上传覆盖行为未知？
15. `PublishedFileId` 是否保留上传器生成的现有 Steam Workshop ID？首次上传前不得手动写 `0`；同时检查编译后的 `loc2` 文件是否使用 `0_` 或无前缀通用名称。
16. `ItemDescriptionShort` 没有专门需求时是否保持为空，并避免把其具体用途、必写性或显示位置说成已确认？
17. 若目标是职业 Mod，再检查 `heroes` 内的动画、`art` 与 `info` 定义。
18. 根据实际功能检查 `audio`、`campaign`、`effects`、`localization`、`panels`、`raidshared`、`trinkets`、`upgrades`，不要因为目录被称为“可选”就遗漏已被代码引用的内容。

英雄升级树、初始补给和名册容量文件见：[英雄升级树、初始补给与名册容量](26-英雄升级树、初始补给与名册容量.md)。
