# 音效制作与 FMOD 事件、Bank 接入

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 证据入口与版本默认值

本专题根据本地提供的 `darkest_audio_framework` 工程内嵌教程整理。原始材料根为 `D:\darkestdungeon_audio_mod_materials`，只用于历史定位，不是接收方必须具有的运行路径。可迁移证据在 `Sources/audio_integration_20261108.json`：`tutorials[]` 保存九个原始 `.event` XML、`note`、对象 GUID 与 SHA-256；`files[]` 保存 README、两份示例 JSON、Bank 定义；`example_events[]` 保存十二个事件的 XML 与映射。构建不访问原盘符，不改写 FMOD 工程。

`READ_ME_FIRST.txt` 署名 Kevin Regamey / Power Up Audio，指向 `MODDERS_READ_ME_FIRST` 中各事件的 Properties Pane。按官方随附资料记录；来源包未经官方签名或在线原包哈希认证，不冒称本地包与某个在线归档逐字相同。九个教程的精确文件名及对象 ID 均在快照中。

历史教程 `01_intro` 指定 FMOD Studio **1.06.07**。知识库编写者于2026-11-08在维护会话修正：最旧版本已不是必须要求，但因长期历史要求，仍将1.06.07作为默认／参考版本。这条修正不等于任意新版构建的 Bank 均兼容，也没有给出完整兼容版本清单。旧教程的菜单和目录是该工程环境的步骤；新版操作须核对对应版本，不能把现代 Unity/Unreal 接入步骤直接当成地牢规则。

## 内置官方框架副本：仅保留 hero_zzz 示例

知识库内置路径为 `Sources/audio_framework_hero_zzz/darkest_audio_framework/darkest_audio_framework.fspro`。先将 `Sources/audio_framework_hero_zzz` 整目录复制到目标工作目录，再用FMOD打开工程，参照教程创建自己的事件、Bank和Mixer路由。内置工程供学习及模板使用，不能将整个Build目录直接覆盖到游戏；实际部署仍遵守下文 `audio/secondary_banks` 与campaign配置规则。

当前用户于2026-11-08明确说明，本地材料中除hero_zzz以外的自制内容是此前制作Mod的残留。入库副本保留框架原版事件目录、文件夹、Mixer／VCA／Snapshot等结构，保留九段教程及hero_zzz的十二个事件、十二份WAV和Audio Bin引用、Bank定义、预构建hero_zzz.bank及随附说明／JSON。`master_bank`工程XML定义和Master文件夹是原框架结构，保留不表示提供或建议部署自制主Bank。

已排除NONIGHT_Unique_Monster_Trinket的Bank定义、三个所属事件及其三个Mixer Input，另排除五份非zzz素材及对应Audio Bin记录；缓存、Profiler、hero_zzz之外的构建产物及旧GUIDs.txt也不入库。不能按 `trinket_` 前缀删除原版事件，排除以残留Bank成员关系和素材依赖为依据。精确文件及哈希见 `Sources/audio_framework_hero_zzz_manifest.json`；`python tools/portable_kb.py check` 校验副本哈希及排除项未混入，迁移打包会携带此目录。

所有复制文件保留原始字节；原始D盘材料不变。静态检查已闭合十二份示例事件至素材的引用，保留对象没有指向被排除对象的引用；未启动FMOD验证打开、重建或游戏播放。该副本由本地材料筛选，未与发布方未修改原始包校验，不能声称是已认证的原始发行包。历史load_order保留原文，部署前仍需修正到secondary_banks。

## 自制声音：新事件、Bank 与 Mixer 的制作顺序

1. 在自制声音路线中，为新增或替换的素材创建新的 FMOD 事件。教程 `04_integration_intro` 明确指出，仅往既有 `event:/char/ally/vestal_divine_grace` 事件塞入新音频并构建，并不是此 Mod 接入方案；应新建事件，再配置游戏期望路径到新事件 GUID 的映射。单纯复用原版已有事件声音的路线见下方社区教程，不要求再造事件或Bank。
2. 按 `02_creating_sounds_in_fmod`，右键新事件，使用 `Assign to Bank` → `New Bank...`，将事件分配到自有 Bank。音频素材、事件、Bank 是不同对象；只导入 WAV 不等于完成事件和 Bank 接入。
3. 使用 Mixer（旧版快捷键 `Ctrl+2`），参照同类事件的 Mixer Routing 安置新事件。教程明确指出这关系到声音是否遵从游戏的各类音量滑块。不要为所有类型臆造一个通用总线名；以实际工程同类事件路由为证据。
4. 需要时在 Banks 页签选择 Bank，调整播放质量。采样率、声道、压缩格式的地牢通用硬性要求，本次来源未给出，不能补写猜测值。
5. 按 `05_bank_prep_and_placement` 执行 `File` → `Build...`，该旧工程的输出目录为 `Build\Desktop\`。应确认事件确已分配给本次构建的 Bank，并检查构建产物；XML 成员关系及 Bank 文件存在不等于实机播放已验证。

证据：`tutorials[]` 的 `02_creating_sounds_in_fmod`、`04_integration_intro`、`05_bank_prep_and_placement`，各 Event 对象的 `property[@name='note']/value`。上述是教程步骤，不是 Agent 自行游戏实测。

## 游戏期望路径与新事件 GUID 的映射

教程 `03_code_and_fmod_communication` 说明：新英雄、怪物或地牢会有引擎自动寻找的事件；新英雄 `zzz` 的示意前缀为 `/char/ally/zzz_*`，举例 `event:/char/ally/zzz_test1`。它没有定义所有技能、命中／未命中、脚步或动画时间轴的完整命名算法。不能由此断言任意 `.id` 或 `.anim` 都自动按某个公式播放。

教程 `04_integration_intro` 与 `06_guids` 明确：新事件可以放在与默认事件不同的层级位置，游戏通过默认路径到新事件 GUID 的覆盖关系接入。FMOD 自动给新建事件分配 GUID；右键**事件**执行 `Copy GUID`，不要把 Bank GUID 或音频素材 GUID 填入 `guid_override`。

`event_id` 是游戏原本期望调用的事件路径；`guid_override` 是实际要播放的新 FMOD 事件 GUID。同一事件可以包含多轨、随机或参数化内容，因此多个路径共享 GUID 只说明调用同一事件，不保证每次采样相同。不要把更改映射误解为新增游戏触发点或改变 Spine 触发时间。

## 不同模式使用不同技能音效

知识库编写者于2026-11-12在维护会话明确补充：“技能音效可以在不同模式不同，event id后面加上_模式id即可”。技能需要按模式区分音效时，在原技能事件路径末尾追加 `_<模式ID>`，得到对应模式的 `event_id`，再分别映射到要播放的真实FMOD事件GUID。普通英雄战斗技能的模式路径为 `event:/char/ally/<职业ID>_<技能ID>_<模式ID>`；这里的模式ID使用实际模式内部ID，不使用显示名。此格式由已收录的普通英雄技能基础路径和本次模式后缀规则组合得到。

模式后缀加在JSON中的 `event_id` 路径上，不加到 `guid_override` 或Bank文件名上；不同模式可分别指向不同音效事件，仍沿用既有Bank分配、Mixer路由和部署流程。来源：`Sources/audio_integration_20261108.json` 的 `mode_skill_audio_clarification`，证据为知识库编写者明确说明，非本轮Agent实机验证。

未命中分支使用 `<原技能事件路径>_miss_<模式ID>`，即 `_miss` 在模式后缀之前。普通英雄对应 `event:/char/ally/<职业ID>_<技能ID>_miss_<模式ID>`。当前用户随后明确补充该顺序，并提供Ambertley于11-12 21:32的聊天截图作为社区案例：`event:/char/ally/Roland_riposte1_Roland_mode_A` 与 `event:/char/ally/Roland_riposte1_miss_Roland_mode_A`，其他模式同样按此排列。截图副本见 `Sources/audio_evidence/20261112_mode_skill_audio.png`。截图中不同模式指向同一GUID，只佐证配置写法，不把它说成不同模式已播放不同声音的实测。缺少模式专用事件时的回退行为，以及扎营／道具事件是否沿用此后缀，本次未说明。原社区教程未证明模式规则的限制仍是其来源边界，不影响本次独立补充的已确认结论。

## campaign 配置、文件位置与路径差异

教程 `07_json_explanation` 明确要求该接入方案提供两类文件，前缀可自定，但保留以下结尾：

| 文件结尾 | 顶层字段 | 教程明确的职责 |
|---|---|---|
| `.campaign.load_order.json` | `load_order`，路径字符串数组 | 在开始 campaign 时加载所列 Bank |
| `.campaign.guid_overrides.json` | `event_guid_overrides`，对象数组 | 通过 `event_id`、`guid_override` 将默认路径映射到新事件 |

两份 JSON 的字段结构由配套文件直接印证。教程 `08_json_prep_and_placement` 要求把它们放在 `DarkestDungeon\audio`，`05_bank_prep_and_placement` 要求 Bank 放在 `DarkestDungeon\audio\secondary_banks`。这些是原教程写法，不授权 Agent 直接改游戏安装目录。用于独立目标 Mod 时，遵循目标 Mod 的 `audio\` 布局，按真实部署位置同步配置路径；Mod 加载边界同时见专题24和33。

**AUD-PATH-01（已澄清：构建输出与游戏部署分层）：**知识库编写者于2026-11-08在维护会话明确纠正：材料／工程的输出位置不代表已经接入游戏；真正接入游戏时，Bank 必须放在目标音频目录的 `secondary_banks` 内，即 `audio\secondary_banks\<bank>.bank`，`load_order` 对应填写 `secondary_banks/<bank>.bank`。随附 JSON 的 `mod_banks/hero_zzz.bank` 原文作为历史材料保留，不将其当作游戏支持任意 Bank 子目录的证据，也不再把这个问题悬置为部署目录二选一。工程 `Build\Desktop\hero_zzz.bank` 只是构建产物位置；将其部署到游戏或目标 Mod 是另一步。这里没有授权修改材料或游戏文件。

两类 campaign 配置是官方教程要求的方案组成；不应继续一概写为“好像要成对”。不过教程未证明每个作用域都必须成对、两文件前缀必须相同、已有 Bank 复用时必须重复声明，或缺文件的确切报错。作为生成规范可采用相同 Mod 自有前缀，不能把该保守规范冒称引擎硬性要求。

## zzz 示例映射的静态闭包

随附 JSON 覆盖十字军的六个技能事件及相应 `_miss` 事件，共十二项；这些 GUID 在工程中逐项对应到 `zzz_test1` 至 `zzz_test6` 及其 `_miss` 事件。十二个事件的 `relationship[@name='banks']` 均包含 `hero_zzz` 的 Bank GUID `{aa824c52-ee06-4963-a82a-458ee89e9536}`。因此，“十字军默认路径 → zzz 新事件”是演示替换，不是名称不一致错误。读取实际 XML 和 JSON 关系，不能只看教程08的“zzz示例”文字猜测覆盖对象。

| 检查项 | 已核对值与边界 |
|---|---|
| 默认路径 | `event:/char/ally/crusader_smite` |
| 新事件 | `zzz_test1`，Event 对象 GUID `{655cec79-c502-47a9-b9a4-c4b13cfc2067}` |
| Bank 定义 | `Banks/hero_zzz {aa824c52-ee06-4963-a82a-458ee89e9536}.bank`，这是工程 XML 定义，不是构建后的二进制 |
| 构建产物 | `Build/Desktop/hero_zzz.bank`，本次检查大小289760字节；SHA-256在证据快照 `built_bank` 中 |
| 输出与部署 | 随附 `mod_banks/hero_zzz.bank` 保留为材料原文；实际游戏接入须部署到 `audio\secondary_banks` 并使用 `secondary_banks/hero_zzz.bank`，见已澄清的 AUD-PATH-01 |
| 验证范围 | JSON映射、XML事件、Bank成员关系及构建文件存在；未反编译验证二进制Bank内容，未执行游戏播放测试 |

本表是已核对的来源案例，不是建议新 Mod 复用十字军路径、示例 GUID 或原有 Bank。需要新增或替换自己的技能时，必须先确定游戏实际调用路径，再使用自己创建的事件 GUID 与实际构建产物。这里不提供声称可直接运行的虚构技能配置。

## 接入排查与仍未知的边界

按依赖顺序检查：游戏是否真的会调用目标路径 → 映射是否使用正确的事件 GUID → 事件是否分配到本次构建的 Bank → 部署文件是否与 `load_order` 路径一致 → campaign 配置是否位于目标 Mod 的音频目录 → Mixer 路由是否符合相应音量控制。该顺序是由教程依赖整理的排查建议，不声称证明引擎内部加载顺序。教程将 campaign Bank 加载定位于开始 campaign 时，不能预设运行中热更新或重建 Bank 后无需重新加载。

仍未知：其他作用域精确定义；多个 Mod 的事件冲突优先级；同名文件合并规则；缺失／错误 GUID 和 Bank 的错误行为；Bank 列表顺序；所有技能及脚步的事件命名；Spine 时间轴到音频的完整绑定；新版 FMOD 的完整兼容版本集合。已有怪物大类 `_aggro`／`_death` 和 size-0 空白音效结论继续见专题33，不能被这里的未知清单降级。

## 证据账本与未采纳教程

| 账本ID | 结论及定位 | 等级、状态及示例资格 |
|---|---|---|
| AUD-I01 | 历史1.06.07默认与非强制修正：`tutorials[01_intro].note`；`version_clarification` | 历史官方资料＋知识库编写者确认；已确认；不认证任意新版 |
| AUD-I02 | 新事件、分配Bank、Mixer和质量：教程02、04 | 官方随附资料；已确认教程流程；不等于实机实测 |
| AUD-I03 | Build及输出目录：教程05 | 官方随附资料；限该旧工程；具体产物存在已静态核对 |
| AUD-I04 | 自动GUID与Copy GUID：教程06，十二个Event对象 | 官方随附资料＋语法事实；已确认；不得填Bank GUID |
| AUD-I05 | 默认路径与新事件层级可分离：教程03、04、06 | 官方随附资料；已确认；任意技能命名算法未确认 |
| AUD-I06 | campaign两份JSON、文件后缀及职责：教程07、08与配套JSON | 官方随附资料＋语法事实；已确认教程方案；不推广所有作用域 |
| AUD-I07 | 十二项十字军到zzz映射及Bank归属：`example_events[]` | 工程静态案例；已确认XML引用；参考用途，非实机正确证明 |
| AUD-PATH-01 | 材料输出位置不等于部署位置：教程05、配套JSON和2026-11-08维护会话纠正 | 知识库编写者确认；已澄清；游戏接入Bank必须在audio/secondary_banks |

首次摄入时 Nexus 返回403、FMOD只取得页面外壳，未据此采纳未读正文。2026-11-08后续通过浏览器读到两者正文，见下列新增段落及证据快照 `web_tutorial_review`。B站视频尚未完成音轨／逐段审阅，只登记已见页面与画面。既有工作簿审计的待审变化与本次音频摄入无关，不因本次补充刷新审计基线。

## 社区教程：复用原版声音与英雄技能事件命名

来源：Nexus `https://www.nexusmods.com/darkestdungeon/mods/593`，Seta nagato，2018-03-01，标题 `Tutorial - Implementing sounds to your skills (manually)`；2026-11-08通过浏览器读到全部文字正文，18张正文原图已于2026-11-08逐张核对（独立图库封面不在此范围）。证据等级为**社区资料**，不是新的游戏实测。它针对复用已有声音，区别于随附工程中新建事件／Bank的路线：已有事件仍需其所在Bank可用，然后将新职业技能期望路径映射到原有事件GUID。并非每次接入都要新建音频事件或复制原版Bank进Mod。

- 在 `Starting with loading the sound of the skill Dank Meme` 中，先用原版 `base.heroes.load_order.json` 查所需英雄Bank；示例复用 `secondary_banks/hero_vestal.bank`。不要凭显示名猜Bank归属。
- 在 `Adding the sound for the skill Dank Meme` 中，作者按职业ID与 `combat_skill` 的技能ID组成普通英雄技能事件路径 `event:/char/ally/<职业ID>_<技能ID>`，未命中分支追加 `_miss`。例子是 `event:/char/ally/meme_lord_dank_meme`。这是普通英雄技能接入的社区规则；模式后缀另由知识库编写者补充，见“不同模式使用不同技能音效”；反击、脚步、ActorDot与Spine时间轴等特殊调用不由本教程证明。
- 查得已有事件GUID后，用它覆盖新技能的期望事件；正常分支与 `_miss` 分别核对。作者在一条 `_miss` 说明里漏写示例后缀，不能复制该笔误，也不将其“治疗不会失败”的旁述升级为通用引擎规则。
- 在 `Doing the same for Mlg trick shot but with enemies sounds` 中，作者提醒：应取技能ID，不取 `.fx` 动画名；示例恰好同名只是偶合。怪物声音可能在共享Bank，不能由出现场景推定归属。作者曾用加载一批Bank兜底，本库不将它推荐为默认做法；只加载已定位的必要依赖，不采纳其加载成本可忽略的泛化说法。

原图补充核对：`593-1519907311-131784963.png` 与 `593-1519907828-921088579.png` 展示路径数组及 `secondary_banks/hero_vestal.bank`；`593-1519911472-938939770.png` 展示正常与 `_miss` 两条映射均已填入事件GUID。中间步骤图中的全零GUID只是待填写占位，不能当成可运行的静音配置。末四张图展示从 `skeleton_arbalist_A.art.darkest` 的技能 `.id "crossbow_shot"` 查到目录中的 `event:/char/enemy/skeleton_arbalist_crossbow_shot` 及 `_miss`，用于给英雄复用怪物声音。这只证明该教程的来源查找案例，不把英雄侧 `ally` 目标路径改成 `enemy`，也不推广为所有怪物事件的命名规则。18张原图精确文件名及分组定位保存在证据快照 `AUD-W07.figure_review`。

教程末尾关于任填 `PublishedFileId` 的旧建议与现有知识库规则不一致，未采纳。音频资料只用于其覆盖到的音频机制，不覆盖专题24及本地化规则。原版Bank查表实例已在维护时读取 `DarkestDungeon\audio\base.heroes.load_order.json`，证实 `hero_vestal.bank` 路径；未凭文中对骷髅弩手的叙述认证当前所有版本的敌人Bank分配。

## FMOD 官方教程：制作概念、构建产物与游戏部署

来源：FMOD Studio User Manual **2.03.15（2026-09-21）**，浏览器2026-11-08已读 Quick Start 全文及 Getting Events into Your Game 全文。定位与链接见证据快照 `web_tutorial_review`；这是FMOD版本限定的官方资料，不自动认证地牢的新版支持范围。

`Quick Start Tutorial` 的第5～16步演示创建事件、导入素材、建立音轨与multi instrument、加入播放列表及试听；multi instrument可以从列表随机选择素材。因此“多个路径映射同一事件GUID”不等于每次播放同一个采样。第17～29步演示参数和音高自动化；参数存在不代表地牢会为自定义参数赋值。第30～32步演示分配Bank、Build与默认 `Build/Desktop` 输出。这是通用教学示例，不能据其分配Master Bank的简化步骤要求地牢Mod替换主Bank。

`Getting Events into Your Game` 第8.1节明确：普通事件未分配Bank就不会因一次Build自动进入产物；8.1.1另有referenced event的默认随父事件入Bank规则，不把普通事件结论误写成没有例外。8.3区分当前平台Build、所有平台Build和单个Bank构建。

第8.4节明确构建输出目录可设置；`.bank`为运行时产物，且启用拆分构建时可能另有 `.assets.bank`／`.streams.bank`。因此不能只看工程文件存在便判定已部署，或把单一 `.bank` 视为任何设置下都完整。拆分构建在地牢中的接入能力本次未验证，不能直接生成该方案。

同节区分主Bank的工程路由数据与 `.strings.bank` 的名称／路径／GUID查询信息；缺strings时可按GUID查找是FMOD通用说明，不等于地牢Mod要复制或覆盖自己的 `Master.bank`、`Master.strings.bank`。原版运行时已有的主Bank依赖不能随意替换。

同节说明Bank兼容性取决于Studio与Engine版本关系。地牢实际内置Engine版本及支持组合本次未查明，因此仍保留“1.06.07默认、非强制；不能保证任意新版兼容”的边界。FMOD可配置的构建输出路径与地牢游戏接入目录是两层规则：后者按知识库编写者确认必须使用 `audio\secondary_banks`。

## 单条音效混音与游戏音量总控的操作

**调单条声音：**在 Mixer 的 Routing 页选择自己的事件；若 Mixing Desk 未显示该事件，切换到 `Selected Buses` 视图，显示所选事件的通道条。确认推子当前控制的是 Volume，再调整该事件的音量并试听；0 dB 表示该级不增减音量。修改原版共享Group Bus会同时影响其下其他事件，调整自己这一条声音时应选择自己的事件。FMOD官方操作依据：`AUD-OP01`，Mixing 9.1.2、9.5。

**调整音色：**选择要处理的轨道或总线，在下方 Deck 查看其信号链，调整链中已有的EQ等效果参数并试听。信号从左向右经过效果，先后次序会改变结果；需要比较处理前后时，右键效果切换 `Bypass`。修改轨道影响该轨道，修改整个事件输出或共享总线会扩大处理范围。不要为地牢工程臆造固定EQ、压缩或响度数值。依据：`AUD-OP01`，Mixing 9.8。

**让声音跟随游戏音量设置：**

1. 在地牢随附工程中按 `Ctrl+2` 打开 Mixer（旧版快捷键），进入 Routing 页。
2. 找到一个原版同类事件，查看它所在的Group Bus及上级路由；制作英雄技能音效就参照同类英雄技能事件。
3. 在Routing树中，将自己的新事件拖到同一个既有Group Bus下面。不要只在Events浏览器移动文件夹；也不要只将事件加入某个Mixer View，后者只是视图组织，不改变游戏内行为。
4. 保留原版的上级控制关系。若检查发现相关总线使用VCA，还应参照原版既有归属；FMOD中可右键选择 `Assign to VCA`，或在VCAs页拖入已有VCA。这里只说明检查和操作方法，地牢各滑块实际控制的总线／VCA名称尚无完整核对表，不能自己新建同名对象就认定已接上游戏控制。
5. 保存后重新构建自有Bank，按前述流程部署到 `audio/secondary_banks` 并核对加载表。该步骤沿用地牢随附教程的接入方式，不要求替换游戏Master Bank。

地牢随附教程02直接说明Mixer位置关系到声音是否服从游戏音量滑块；`AUD-OP01`的Mixing 9.1.1、9.1.2、9.2、9.6补充拖动路由、视图与VCA操作。不要把FMOD里的Master Bus、单个事件的音量推子、游戏设置中的总音量滑块混为同一对象；调低单个事件不会自动建立游戏控制关系。新建Group Bus／VCA也不会自行让地牢代码控制它。

**接入排查建议（非本次实机测试）：**以同一条音效比较游戏音效分类滑块及总音量滑块调低、调到零和恢复后的变化；若只有原声变化，优先比对自制事件与原版同类事件的路由及既有VCA归属。若带混响Send，还要检查Return Bus的去向，避免复制信号走到受控分组之外。FMOD的Send会复制信号，前级Send可能不受后级推子／Mute影响；只看主路径不足以排除尾音残留。依据：`AUD-OP01`，Mixing 9.3、9.7。这个检查不替代已收录结论，也不表示本次已启动游戏验证。

教程阅读进度和视频抽查时间点保留在 `Sources/audio_integration_20261108.json`，正文以可执行操作、适用范围和必要边界为主。FMOD现代界面操作来源为2.04.00，不因此认证该版本构建的Bank兼容地牢；仍以1.06.07为默认参考版本。



## 扎营技能与道具使用音效的事件路径（AUD-CAMP-ITEM-01）

2026-11-08应当前用户要求补录。证据为本地原版程序字符串、原版音频工程的事件文件夹链及原版技能／物品 ID 的静态交叉核对，不是知识库编写者历史实测，也不是本轮实机播放验证。可迁移快照：`Sources/audio_camp_items_20261108.json`，含程序 SHA-256、字符串文件偏移、事件 XML、文件夹链、Mixer Input 和原版 ID 行号。

| 调用对象 | `event_id` 格式 | ID 来源与原版对应 |
|---|---|---|
| 扎营技能 | `event:/camp/skill/<扎营技能ID>` | `raid\camping\*.camping_skills.json` 的技能 `id`；`encourage`、`pep_talk`、`sanctuary` 与工程事件逐一对应 |
| 道具使用 | `event:/general/items/<物品ID>` | `inventory\*.inventory.items.darkest` 的 `.id`；`bandage`、`holy_water`、`antivenom` 与工程事件逐一对应 |

程序中分别有 `/camp/skill/%s`、`/general/items/%s` 格式串；FMOD 映射配置中的完整路径带 `event:` 前缀。扎营路径不额外拼英雄职业 ID，道具路径不额外拼 `supply` 等物品类型；不要套用战斗技能的 `event:/char/ally/<职业ID>_<技能ID>` 结构，也不要以 Effect ID 或 `.fx` 名替代技能／物品 ID。原版数据作为上述格式的静态佐证；仅存在格式字符串不能单独证明格式参数来自哪个函数、精确播放时机或所有特殊道具分支。

接入仍使用 `audio\<自有前缀>.campaign.guid_overrides.json` 的 `event_guid_overrides`，每项填写游戏期望的 `event_id` 和真实新事件 `guid_override`；新事件自身在 FMOD 中的文件夹可以不同。Bank 放 `audio\secondary_banks`，由配套 `.campaign.load_order.json` 加载；不要改原版事件或部署自制 Master Bank。继续沿用专题前述已确认的 GUID／Bank 构建与部署规则。

Mixer 路由也按原版同类事件选择：本次快照中三个扎营事件共享既有输出总线 `{adfa4f91-c65f-4fdc-8735-679dfcf0707d}`，三个物品事件共享另一既有输出总线 `{a4f11e9d-d837-4cc4-bd44-66ba3d8cb66b}`。这些 GUID 只定位所核对模板的既有对象；不能在别的工程新造同名／同 GUID 总线后声称已接上游戏音量控制。

**边界：**本轮未实测扎营、道具播放、声音重叠、音量滑块或事件缺失行为；没有认证所有物品类型及奇物交互、消耗失败、治疗派生事件。普通物品路径不能推导 `_miss` 等后缀。当前用户本次 Mod 要求“战斗只播放命中音效，未命中故意留空”，属于项目设计选择，不是知识库通用要求，不能据此要求其他 Mod 静音或省略未命中事件。
