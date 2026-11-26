# Size-0 召唤物

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## effect_chance 定向替代与 size-0 精简（2026-11-05）

知识库编写者明确补充：`effect_chance` + `actor_base_class` + 对群 Effect 可逐最终目标筛选生效对象，模拟类似 Spawn 定向。若生命反馈二段式二号机仅负责定向，可省去二号机；仅为 Spawn 定向而使用的单个 size-0 大概率也可替换。实际目标为自身时 `actor_base_class` 失效；自身目标直接用 `effect_chance` 制约最终 Effect，无需 size-0 定向。

须按实际施术者和最终目标核对概率门、抗性及原载体的其他职责；该替换不自动省去状态、时序、分支或战斗开始切模式所需流程。完整说明见[模拟定向](07-spawn定向.md)，来源：`Sources/effect_chance_directed_filter_20261105.json`。Agent未自行运行游戏测试。

## 推拉与 size-0：现行结论与早期观察

知识库编写者后续实测确认：**size-0 已不再与常规怪物产生旧版推拉交互，不再需要安全拉前／击退迂回；按需求直接填写拉前／击退数值即可。** 与大体型的具体拉前／击退规则疑似有变化，仍未确认，不能据此给出统一的新位移公式。此处“交互”限推拉，不撤销 size-0 碰撞箱遮挡、计数、召唤或生命反馈等独立结论。

### 2026-11-05 的早期观察（非现行待确认状态）

知识库编写者2026-11-05连续实测：目标起始4号位，前方有一个size1和一个size2，且已在1号位提前召唤size0。拉前2到2号位；拉前3、拉前4均到1号位。前方size1与size2先后顺序未提供。按过往版本的末次交换size0退至队尾模型，此类拉前本应到4号位；现有结果与该旧模型不符，不能继续把它作为当前可靠预测。

当时“推拉与 size-0 的问题可能已修复、尚未证明击退”的状态已被后续明确实测结论取代。3+1 组合的具体落点及大体型通则仍未测试／确认。旧版按实体交换数量、途经 size-0 扣位移、末次交换 size-0 退至队尾及 sentinel 安全推拉代码仅作历史参考，不能继续作为现行创作要求。独立的 AWR／queue 时序与 Rule 语义不因空间模型纠正而撤销。

来源：`Sources/reorganization_corrections_20261111.json` / `REORG-SIZE0-MOVEMENT`；早期记录为 `Sources/movement_size0_uncertainty_20261105.json`。完整历史方案见[推拉专题](90-怪物推拉与size0站位边界.md)。

## 2026-11-05 新版更新

新版要求：所有生命反馈size-0必须加入 battle_modifier: .ignore_hp_scale true，忽略狱火/NG+难度加血。可直接50血启动、最大生命扩展到100且不回血，再执行后续；不再要求极小初始HP与极大倍率稀释。仍需先放0.99向下/0.01向上空Effect sentinel，再放对应方向真实反馈。

详见[新版字段与修复](96-新版Modding更新Buff技能地牢饰品怪癖.md)及`Sources/modding_update_20261105_remaining.json`。

## Size-0 与怪物的关系
Size-0 是一种特殊怪物。它也可能在设计中充当中间载体，但这不会使它脱离怪物类别：知识库或设计说明中不带明确排除条件、泛称“怪物”及通用怪物性质时，必须把 Size-0 包含在范围内。只有某条机制明确说明 Size-0 不适用或有专门例外时，才按该例外处理。

## 必需骨架
Size-0 指 `.size 0` 的怪物或中间对象。常用骨架：

```darkest
display: .size 0
initiative: .number_of_turns_per_round 0
battle_modifier: .can_be_summon_rank false
```

其中 `.can_be_summon_rank false` 是关键安全项，Size-0 必须显式声明，否则存在 rank 溢出崩溃风险。此风险边界来自迂回表第 3 条 P369/X392，经当前用户于 2026-11-02 确认；不扩大为每次省略都必定立即崩溃，也不补造底层触发条件。本条为风险确认，非本轮新增实机测试。

针对迂回表第 9 条 P444/X492，当前用户于 2026-11-02 进一步确认：尤其在连锁 spawn 与自灭流程中，未显式写 false 存在 rank 溢出崩溃并进一步导致存档循环卡死、无法正常继续的风险。不将其写成每次必现，也不推断存档永久损坏或具体恢复方法；非本轮新增实机测试。

## size0Spawner 可直接复制的 Info / Art / 动画资源模板

**知识库编写者提供的历史本地模板来源（非运行依赖）**：`D:\Size0Spawner\template`。该目录已经包含可以直接复制后替换占位符的 size-0 基础资源，不再只是抽象逻辑模板。

目录结构：

```text
template\
├─ anim\
│  ├─ monster_xxx.sprite.combat.atlas
│  ├─ monster_xxx.sprite.combat.png
│  ├─ monster_xxx.sprite.combat.skel
│  ├─ monster_xxx.sprite.defend.atlas
│  ├─ monster_xxx.sprite.defend.png
│  └─ monster_xxx.sprite.defend.skel
└─ monster_xxx_A\
   ├─ monster_xxx_A.info.darkest
   └─ monster_xxx_A.art.darkest
```

`monster_xxx`、`monster_xxx_A` 和 `monster_xxx.sprite.<中缀>` 是同一占位符族，实际创作时必须统一替换为目标怪物大类、差分和动画资源前缀。不要只改 Info ID 而保留动画文件的旧前缀。

### Atlas 文件的两条硬性检查

知识库编写者确认（2026-09-20）：size0Spawner 模板的 `.atlas` 文件第一行必须保留为空行，不能删除；第二行是第一页图片名称，必须与对应的 PNG 文件名逐字符完全一致，包括大小写、点号、下划线和扩展名。

模板示意：

```text
<第一行：必须为空>
monster_xxx.sprite.combat.png
size: 361,388
format: RGBA8888
```

复制并替换占位符后，`monster_xxx.sprite.combat.atlas` 的第二行必须变成 `目标大类.sprite.combat.png`，并且该 PNG 必须确实以同名文件存在。`defend` Atlas 同理。不能只修改 Atlas 文件名或只修改 PNG 文件名，也不能把第一行空行当作可删除的格式空白。



以下是模板中的可直接使用骨架；其中长的 `display_modifier` 列表是模板原样保留的表现层抑制配置：

```darkest
display: .size 0
enemy_type: .id "monster_xxx"

stats: .hp 1 .def 0% .prot 0 .spd 1 .stun_resist 500% .poison_resist 500% .bleed_resist 500% .debuff_resist 500% .move_resist 500%
personality: .prefskill -1

initiative: .number_of_turns_per_round 0

monster_brain: .id default

battle_modifier: .accelerate_stall_penalty False .disable_stall_penalty False .can_surprise false .can_be_surprised True .always_surprise False .always_be_surprised False .can_be_summon_rank False

commonfx: .deathfx death_medium
display_modifier: .disabled_popup_text_types actor_dot_complete pass hp_heal_dot_onset hp_heal_dot hp_heal_dot_crit miss no_damage crit_damage damage death_avoided deathblow hero_heal hero_heal_crit monster_heal monster_heal_crit stress_reduce stress_damage resist move_resist disease_resist buff debuff debuff_resist stun stun_resist stun_clear poison poison_resist bleed bleed_resist cured cure_failed tagged guard guard_failed riposte full heart_attack heal_failed vampire vampire_resist stress_dot stress_dot_resist shuffle_dot shuffle_dot_resist health_damage_block_onset health_damage_block tag_block damage_reflect control_resist refresh_skills daze daze_resist guard_break
```

这个 Info 模板已包含 size-0 必需的 `.size 0`、每轮 0 行动点和 `.can_be_summon_rank False`；`stats`、`monster_brain`、`commonfx`、`display_modifier` 也属于模板的直接组成部分，不要在生成时擅自删掉再自行补造另一套最小骨架。若目标设计需要不同血量、速度、抗性或表现抑制，必须明确写出差分并说明原因。

模板里的 `enemy_type: .id "monster_xxx"` 只是占位示例。`enemy_type` 可以改成任意实际 ID，也可以连续写多个 `enemy_type: .id "..."`；它不要求等于怪物大类 ID。生成时必须按实际的 `kill_enemy_types`、筛选、标签或其他机制需求显式选择，不要把大类 ID 自动当成唯一或必然的 enemy_type。

原版基础游戏已有普通怪物的多行实例：`DarkestDungeon\monsters\unclean_giant\unclean_giant_A\unclean_giant_A.info.darkest:2-3` 中，Unclean Giant A 连续写入 `man` 与 `beast` 两个 `enemy_type`：

```darkest
enemy_type: .id "man"
enemy_type: .id "beast"
```

该原版实例直接证明多行写法存在于原版怪物数据中，但不是 size-0 案例；size-0 纳入这一规则，是因为 size-0 首先是怪物，并由当前用户明确确认适用。

### Art 基础文件

模板中的 `monster_xxx_A.art.darkest` 为：

```darkest
commonfx: .deathfx death_medium
display_modifier: .disabled_popup_text_types actor_dot_complete pass hp_heal_dot_onset hp_heal_dot hp_heal_dot_crit miss no_damage crit_damage damage death_avoided deathblow hero_heal hero_heal_crit monster_heal monster_heal_crit stress_reduce stress_damage resist move_resist disease_resist buff debuff debuff_resist stun stun_resist stun_clear poison poison_resist bleed bleed_resist cured cure_failed tagged guard guard_failed riposte full heart_attack heal_failed vampire vampire_resist stress_dot stress_dot_resist shuffle_dot shuffle_dot_resist health_damage_block_onset health_damage_block tag_block damage_reflect control_resist refresh_skills daze daze_resist guard_break
```

该 Art 模板当前没有额外的 `.anim` 技能字段；动画资源由同目录约定的 Skeleton/Atlas/PNG 文件提供。不要因为 Art 文件看起来只有表现抑制字段，就删除它或把 Info 文件当成 Art 文件的替代品。

### 动画资源

模板提供两套资源组：

- `monster_xxx.sprite.combat.skel/.atlas/.png`
- `monster_xxx.sprite.defend.skel/.atlas/.png`

`.skel` 是 Spine 2.1.27 二进制 Skeleton，不能按普通文本手改；`.atlas` 与 `.png` 使用同一资源前缀，Atlas 中当前可见区域名为 `combat`/`defend` 和 `shadow`。复制时必须保持 `.skel`、`.atlas`、`.png` 基名一致，并保持这些文件位于该怪物大类的 `anim\` 目录。当前模板未把 Skeleton 内部动画名完整反编译为文本，因此不能据文件名单独推断额外动画名；需要修改动画调用时仍应检查 Skeleton 实际内容。

这组文件现在属于 size0Spawner 的资源模板闭包：Info、Art 和动画资源应一起复制、统一替换占位符，再在其上追加实际 `spawn`、`hp_reaction` 和其他 Header；不能只复制其中一个部分。

## D:\Size0Spawner 生成工具与 size0Spawner 逻辑的边界

当前用户提供的 `D:\Size0Spawner\app.py` 是实际存在的 Tk GUI 生成工具。它与 `D:\Size0Spawner\template` 配套，但**不能把它等同于完整的 size0Spawner 逻辑实现**。

### 工具已经确认会做的事

根据 `app.py` 的 `generate`、`modify_atlas` 和 `modify_info_darkest`：

- 从内置或相邻的 `template` 目录复制 `anim\` 下的 combat/defend `.skel`、`.atlas`、`.png`；
- 将文件名中的 `monster_xxx` 替换为用户输入的 size0 名称；
- 修改 Atlas 第二行的 PNG 前缀；
- 按所选差分创建 `<size0>_<差分>` 目录，并复制/重命名 `info.darkest` 与 `art.darkest`；
- 修改 Info 中的 `stats` 和 `enemy_type` 标签；这里的 enemy_type 只是工具可写的目标标签，不代表必须等于大类 ID，也不限制为单个 ID。
- 将界面填写的 `spawn`、`loot`、`hp_reaction`、`death_reaction`、`life_time` 追加到 Info 文件。

### 工具不会自动完成的 size0Spawner 逻辑

当前 `app.py` 没有自动生成或验证以下流程：

- 生命反馈size-0必须.ignore_hp_scale true；可50血启动→最大HP升至100不回血；
- 向下 `0.99`、向上 `0.01` 的生命反馈 sentinel；
- 重启误触发保护、血月同乘区稀释、生命比例回传的完整时序；
- 死亡后召唤/set 生效层阻断与后续普通 Effect 继续调用的审查；
- 单个 size-0 优先、技能 Effect 引用最小化、多个载体复用同一怪物大类的资源优化。

因此，**工具的资源复制逻辑与 size0Spawner 模板一致，但工具本身不等于完整 size0Spawner 逻辑**。Agent 可以用它快速生成资源和基础 Info/Art，但生成后仍必须按本页的 size0Spawner、生命反馈、死亡门和资源最小化规则复核并补齐逻辑。不能因为工具成功生成文件，就断言生命反馈安全或整个 size0Spawner 已完成。

## 与 `D:\Size0Spawner\app.py` 的逐项对照审计（2026-09-20）

本次只读对照了外部 `D:\Size0Spawner\app.py` 与知识库内 `tools/size0spawner_generator.py`；外部工具和模板未修改。结论是：**两者不是完全相同的生成器**。当前用户此前要求知识库工具只负责本地快速生成模板，因此差异是有意保留的，不能继续把知识库工具描述为 `app.py` 的完整复刻。

### 在当前平面模板上的共同结果

- 都从 `template\anim` 复制 combat/defend 的 `.skel`、`.atlas`、`.png`；
- 都把 `monster_xxx` 替换为输入的 size0 大类/资源前缀；
- 都按 `_A` 等差分创建 `<size0>_<差分>` 目录，并替换 `monster_xxx_A` 文件名；
- 都保留 Atlas 的第一行空行，并把第二行的 PNG 前缀替换为目标前缀；当前模板没有额外嵌套资源时，资源文件集合和占位符替换结果等效；
- 两者都支持 A-Z 和 0-9 差分。`app.py` 的 GUI 直接列出这些差分，CLI 工具对输入做同样的单字符校验并统一转为大写。

CLI 工具另外对 Atlas 做了更严格的安全检查：第一行不是空行，或第二行不逐字符等于目标 PNG 文件名时直接拒绝生成；`app.py` 只替换第二行中的 `monster_xxx`，不主动校验这两个条件。

### 明确存在的功能差异

| 项目 | `D:\Size0Spawner\app.py` | 知识库 `size0spawner_generator.py` |
|---|---|---|
| 操作方式 | Tk GUI；每个差分单独填写配置 | 本地 CLI；只接收名称、输出目录、差分、可选 enemy_type |
| Stats | 可按差分填写并写回 `stats:` | 不改 Stats，保留模板内容 |
| 默认/自定义 enemy_type | GUI 默认可写入大类 ID，也可改为多条自定义标签 | 省略 `--enemy-types` 时保留模板占位符；显式参数才写入任意多条 ID，不把大类 ID强制当作 enemy_type |
| spawn | 可按行追加 `spawn:` | 不追加 |
| loot | 可配置并追加 `loot:` | 不追加 |
| hp_reaction | 可配置并追加 | 不追加 |
| death_reaction | 可配置并追加 | 不追加 |
| life_time | 可配置并追加 | 不追加 |
| 输出目录已存在 | `app.py` 会创建目录并可能覆盖已有同名文件 | CLI 为防止误改，目标目录已存在时直接拒绝 |
| 资源遍历 | `app.py` 当前按模板目录第一层文件复制 | CLI 递归复制，适配嵌套资源；平面模板下结果一致 |
| 怪物名称本地化 | `app.py` 不生成 | CLI 额外生成 `_mod_support/localization/<size0>.size0.string_table.xml`，提供各差分空名称条目；需手动部署到 Mod 的 `localization` 并编译 |

`app.py` 和 CLI 均不自动完成完整生命反馈流程：初始／最大生命配置、`.ignore_hp_scale true`、0.99/0.01 sentinel、死亡门及资源最小化仍须按实际设计补齐。旧版“小初始血量→大倍率扩展→回满→再次扩展不回血”不再是必须步骤；现行可采用50血启动并扩展最大生命到100、不回血。工具功能边界不等于要求继续使用旧数值方案。

因此，当前正确的描述是：知识库工具**复刻了当前模板的资源复制与占位符替换核心，并增加了安全校验和 size0 名称本地化配套**；它没有复刻 `app.py` 的 GUI 配置写回功能。若未来要求完全复刻 `app.py`，必须另行把每差分 Stats、enemy_type 默认标签、spawn、loot、hp_reaction、death_reaction、life_time 和 GUI 的复制配置逻辑加入 CLI，并重新审查“默认 enemy_type 写大类 ID”与当前用户已确认的任意 enemy_type 原则之间的取舍。

## 知识库内置的本地快速生成工具

知识库内有一个可由 Agent 在本机直接调用的命令行工具：[tools/size0spawner_generator.py](../tools/size0spawner_generator.py)。它不访问云端，也不修改 `D:\Size0Spawner\template`；默认从知识库内置 `tools/size0spawner_template` 读取资源，不依赖原维护者的外部目录，并把新模板写到当前用户指定的输出目录。

基本调用：

```powershell
python tools\size0spawner_generator.py --name mod_size0 --output ./generated --races A B 1 --enemy-types sz0_probe sz0_logic
```

`--name` 是大类/资源分组和文件前缀；`--races A B 1` 生成同一大类下的 `_A`、`_B`、`_1` 小类。差分后缀必须恰好一个字符，多字符后缀不合法。此生成工具目前只接受已确认的单个 A-Z 或 0-9；`@`、`#` 虽疑似可用但尚待确认，因此当前工具只实现已确认子集。`--enemy-types` 才是显式写入 Info 的一个或多个 `enemy_type` ID。省略 `--enemy-types` 时工具保留模板占位符，避免擅自把大类 ID 当成 enemy_type。

只检查模板和列出将生成的文件，不写盘：

```powershell
python tools\size0spawner_generator.py --name my_size0 --output ./generated --dry-run
```

工具会复制并重命名：

- `anim\` 下的 combat/defend `.skel`、`.atlas`、`.png`；
- 每个差分目录中的 `.info.darkest` 与 `.art.darkest`；
- Info 中的 `monster_xxx` 占位符和 Atlas 前缀。

它默认拒绝覆盖已经存在的 `<output>\<name>` 目录，以免误改已有 Mod。生成结果只是资源和基础 Info/Art 模板；Agent 仍必须按本页其他章节补齐 spawn、hp_reaction、最大生命扩展、sentinel、死亡门和其他逻辑。`--template-root` 可在本机模板路径不同的情况下指定另一个同结构模板目录。

size-0 善后自灭默认优先使用匹配实际 `enemy_type` 的 `kill_enemy_types`；只有确认它在当前调用环境失效或不适用时，才考虑 `.kill 1`。

默认优先不适用于零血不死载体：迂回表第237条 P4331–P4338/X5664–X5672 记载，`.can_die_from_damage false` 的怪物不能被 `.kill_enemy_types` 真正消灭，并可能暂时丢失动画／可选中性；满 Captor 还可能崩溃。原表建议这类怪物用 `.kill 1`，但普通 size-0 又有 `.kill 1` 的独立时序风险，因此常规自灭模板不要把 size-0 配成零血不死后仍照搬默认清理。此为原表历史测试边界，未在本轮重测；特殊设计须一起核对零血不死、清理方式与调用时序，不能把两条建议单独当作无条件保证。
## size0Spawner 默认模板与生成逻辑

**当前用户本次补充（2026-09-19）**：知识库中的 size-0 生成默认统一采用 `size0Spawner` 模板和本节逻辑。`size0Spawner` 是通用知识库模板名，不是单个 Mod 专题；除非有明确的已证实特殊需求，不要为同一用途另起一套 size-0 骨架。

基础骨架使用已确认的三个字段：

```darkest
display: .size 0
initiative: .number_of_turns_per_round 0
battle_modifier: .can_be_summon_rank false
```

`spawn: .effects` 与 `hp_reaction:` 仍按各自 Header 写入同一怪物 Info，并引用独立定义的 Effect。下面是 size0Spawner 的**逻辑模板**；它是生成顺序和保护规则，不是可以直接复制而不替换 ID 的完整文件：

```text
size0Spawner
├─ 基础骨架：size 0、每轮 0 行动点、不可占用召唤站位
├─ 生命反馈size-0：必须设置.ignore_hp_scale true，50血启动
├─ 最大生命扩展到100
├─ 不回血，保持当前HP为50
├─ 不再需要旧版极大最大生命稀释步骤
├─ 第二次扩展后不回血，直接进入后续生命反馈流程
└─ hp_reaction：先写方向对应的无影响 sentinel，再写真正产生效果的 reaction
```

新版生命反馈size-0必须写 `.ignore_hp_scale true`，可直接50血启动、最大生命扩展到100不回血，后续照常；旧极小初始HP加极大倍率稀释流程已不再必要。空Effect sentinel要求不变。

## size0 名称本地化不可省略

每个 size0 小类都必须有 `str_monstername_<小类ID>` 名称条目，否则也会红字。名称不实际显示，可用空 CDATA；详见[怪物名称本地化](16-loc与loc2本地化覆盖优先级.md)。这与旁白 tags 使用大类 ID 不同。内置生成工具同时输出 `_mod_support/localization/<大类ID>.size0.string_table.xml`，逐小类提供 english、schinese 空名称。部署时把 `_mod_support/localization` 内文件复制到目标 Mod 的 `localization` 并编译；`_mod_support` 是工具输出配套目录，不是游戏扫描目录，也不要留在 `monsters` 内当作已部署。其他支持语言按设计补齐。

## size0 的旁白屏蔽与通用音效覆盖

**当前用户要求**：只要设计或生成了 size-0，就必须把死亡旁白屏蔽纳入实现闭包。Agent 应在目标 Mod 的 `audio` 目录中检查是否已有对应的 `*.narration.json`；没有时应创建或补齐自定义前缀的旁白文件，在 `entries[].id: "kill_monster"` 下使用空 `audio_event`，并为每个需要屏蔽的 size0/怪物标签分别写一个 audio event。一个 `tags` 数组只写一个目标 Tag；不要依赖同一数组中的多个 Tag 组合筛选。

详细结构和证据边界见：[Art、音频与 Size 0 旁白边界](33-英雄美术资源部署与识别边界.md)。旁白文件前缀可以自定义；`kill_monster` 旁白屏蔽的 Tag 必须写怪物大类 ID，不能写 `_A`、`_B`、`_1` 等小类/种族差分；同一大类下多个差分由同一个大类 Tag 覆盖。

原版通用召唤/死亡音效覆盖属于**推荐的演出优化**：在用户允许修改目标 Mod 的前提下，可以按该专题记录的多作用域 `guid_overrides`、`load_order` 和空白 secondary bank 方案覆盖 `event:/general/char/summon_enemy` 与 `event:/general/char/death_enemy`。它不是 size0 逻辑生效的条件，也不是所有版本的硬性文件白名单；使用它时必须在交付说明中明确告诉当前用户已经加入了原版通用音效覆盖。当前用户已经明确要求覆盖时，不需要再次询问是否允许，但仍要报告修改了哪些音频文件。

旁白屏蔽是 size0 输出闭包中的必需检查项；通用音效覆盖是默认建议项。二者都只改变演出，不改变 size0 的死亡状态、spawn 调用链或死亡门。

### size0Spawner 的资源最小化原则

- 先尝试用**一个** size-0 和它自己的 `hp_reaction`、relay 或多段生命比例编码完成逻辑。二段式、第二个载体或额外 size-0 只有在单个载体无法同时承载所需状态、时序或分支时才增加。
- 在保证效果成立的前提下，优先减少 size-0 数量；过多中间怪物可能增加运行时卡顿、碰撞箱和死亡清理负担。
- 优先减少技能中的 `.effect` 引用数量，并遵守技能单行最多 8 个引用、通常不超过 6 个的实践限制；引用过多可能导致 Info 溢出或截断。
- 必须使用多个 size-0 时，非必要情况下尽量让它们属于同一个怪物大类，通过差分或同类定义复用加载范围；怪物大类数量越多，游戏加载成本越高。目录、ID、差分和资源仍须按对象边界逐项核对，不能为了合并大类而混用不兼容的 Info/Art。
- `size0spawner_generator.py` 的 `--name` 只负责大类/资源分组和文件前缀；它不代表必须写入 `enemy_type`。需要时用 `--enemy-types type_a type_b` 显式写入一个或多个任意 `enemy_type`，不要把大类 ID 与 `enemy_type` 的习惯写法当成硬性绑定。
- 这些是设计资源约束，不改变 size-0 的死亡门、spawn 顺序、生命反馈阈值或目标映射；若减少载体会破坏时序或清理，必须保留足够的载体。
- size-0 的普通善后自灭，在没有遇到 `kill_enemy_types` 失效或不适用的具体调用环境时，优先使用匹配实际 `enemy_type` 的 `kill_enemy_types`；不要把 `.kill 1` 当作默认自灭方式。`.kill 1` 只在已确认前者失效、调用时序特殊或设计确实需要时作为后备，并单独复核该时序。

### size0Spawner 的概率门余量检查

使用 Buff、流血、腐蚀、眩晕或治愈流血/腐蚀/燃烧作为 size-0 概率门时，必须同时检查两层余量：

1. 门控 Buff 自身的正负数值：正向至少 `+1000%`，负向至多 `-1000%`，防止同类常规 Buff 干扰；
2. 最终施加率／成功率：普通 Buff、流血、腐蚀、眩晕的成功/失败最终施加率分别至少 `+1000%`、至多 `-1000%`；三种治愈门分别至少 `+100%`、至多 `0%`。

设计明确要求真实过抗概率时记录例外，不要把门控余量误写成通用 Effect 数值规则。

### size0Spawner 的生命反馈落点与 sentinel

正常生命反馈的真伤/治疗落点应按本页“生命反馈阈值的中点落点”设计：向下分支取当前阈值与更低阈值或 0 的中点，向上分支取当前阈值与更高阈值或满血的中点。不要让真伤/治疗刚好停在真实阈值上。

### size0Spawner 的生命反馈 sentinel

- 只要使用向下生命反馈（`.is_under true`），就必须在所有会产生实际效果的向下 reaction 之前，先写一个 `.hp_ratio 0.99 .is_under true` 的无影响 reaction。
- 只要使用向上生命反馈（`.is_under false`），就必须在所有会产生实际效果的向上 reaction 之前，先写一个 `.hp_ratio 0.01 .is_under false` 的无影响 reaction。
- 两个方向都使用时，两个 sentinel 都放在对应方向的实际 reaction 之前；同一次生命变化仍按 `hp_reaction` 的自上而下顺序只选择第一条匹配项。
- sentinel 的 Effect 可以是无效 Effect、无关紧要的 Buff 或其他不产生实际逻辑影响的操作。`.tag 0` 可以作为一种已收录的占位选择：它不施加标记，但被实际引用时可能产生红字报错；如果不接受这个诊断输出，应改用其他已确认的无影响 Effect。
- sentinel 不是可省略的装饰。它用于在重启误触发时抢先命中无影响 reaction，避免错误进入后面的真实分支。

## 常见用途
当前用户于 2026-11-02 复查迂回表第 3 条 P368/X390 时确认：**Size-0 仍不能使用常规技能**。保留这一使用限制，但去掉原表用“Size-0 固定处于 rank 0”推导该结论的旧解释；实际位置与遮挡关系见 [Size-0 实际位置与定身遮挡](60-size0实际位置与定身遮挡.md)。不要通过给 Size-0 配置 AI 常规技能来实现需求；其机制应通过下列非技能流程承载。模板中的 `monster_brain: .id default` 不证明它能使用常规技能，也不因此需要删除模板字段。本条为当前用户确认，非本轮新增实机测试；不补造不能使用技能的底层原因。

- 进入战场后通过 `spawn: .effects` 执行中间 Effect。
- 作为 hp_reaction、death_reaction、状态检测、概率门或技能等级传递载体；能用单个 size-0 完成时优先复用单个载体。
- 临时延迟战斗胜利，为最后一杀后的 ActorDot/反应争取时间。
- 通过生命值、最大生命值和治疗变化承载“生命反馈二段式”。

## 死亡后的 spawn 链：调用继续，死而不僵目标门及专项分支

- size-0 在自己的 spawn Effect 序列中被击杀后，后续 `spawn: .effects` Header 和后续列表项仍会继续**调用**。
- “spawn 不会因死亡被阻断”只表示列表继续调用，不表示每个被调用 Effect 都能成功改变游戏状态。
- 例如：

```text
spawn: .effects "a"
spawn: .effects "b"
spawn: .effects "c"
```

其中 `a` 使 size-0 自灭，`b` 尝试对一个目标召唤或执行 set，`c` 对英雄全体治疗。执行时 `a` 先调用并使 size-0 死亡；`b` 仍然会被调用，但若其最终目标处于死而不僵状态，召唤/set通常在生效层被阻断；若 `b` 同时显式写 `.can_apply_on_death true .can_apply_on_corpse true`，可突破该目标门；`c` 仍会被调用，并可按普通 Effect 规则生效。不要把该例写成“只要发起者死亡，召唤/set就必定失败”。
- 该目标死亡门同样适用于 `hp_reaction` 所带出的召唤和 set。调用来源或发起者死亡本身都不是阻断条件；检查的是 Effect 的最终目标状态及是否显式带齐双字段。
- **狗贼二段式例外**：该设计用一号机的死亡作为二号机召唤成功与否的判别信号，因此二号机召唤 Effect 必须将 `.can_apply_on_death` 与 `.can_apply_on_corpse` 两项都省略，或都显式写 `false`；不能同时显式写 `true` 绕过死亡门。该约束仅适用于以一号机死亡作为分支信号的狗贼二段式，不是所有召唤的通用写法。
- 常规设计中，自灭 Effect 应晚于仍需成功的召唤和 set 变身，包括生命反馈带出的操作。若确实要对死而不僵目标继续执行召唤/set，必须显式同时写两个放行字段；set还需决定是否用 `.set_monster_class_reset_hp true/1` 脱离死而不僵状态。始终区分“Effect 被调用”和“Effect 成功改变对象状态”。

## 风险
- size-0 无论仍然存活，还是已经死亡但处于“死而不僵”状态，其互动碰撞箱都会继续存在，并可能遮挡画面上“相同”位置怪物的互动碰撞箱，造成鼠标无法选中被遮挡的怪物。这里的“相同位置”不是简单的常规站位相同：存档数据中的位置并不完全相同，而且不能通过 `in_rank` Rule 判断这一重叠关系，具体底层位置机制仍未知。
- 被 size-0 遮挡的怪物仍可通过手柄选中，但会缺失正常选中时的 UI 高亮、鼠标悬停怪物简介等表现。因此应尽快用 `kill_enemy_types` 等方式处理 size-0，同时注意单纯令其进入“死而不僵”并不会立即解除鼠标遮挡。
- 多数动画不显示，死亡可能触发老祖语音。
- 不结束回合的技能中，即使逻辑上已自灭，画面/点击区域可能到行动结束才更新。
- 若依赖它延迟胜利，必须设计兜底自灭，避免永久不能结束战斗。
- 默认自灭优先选择 `kill_enemy_types`；只有确认该 Effect 在当前调用来源/时序失效或不适用时，才改用 `.kill 1` 或其他后备方式。反击饰品 AWR 等已知失效边界必须单独核对，不能把该例外推广到普通 spawn/hp_reaction。
- 召唤/死亡通用音效和老祖旁白的演出抑制，见[Art、音频与 Size 0 旁白边界](33-英雄美术资源部署与识别边界.md)；它们是表现优化，不替代自灭逻辑。
- 反击与饰品被命中 Trigger 中，size-0 配合 `.health_damage` 的组合可能导致游戏崩溃；此类流程优先使用治疗触发生命反馈。

size-0 的 spawn 内 set 可继续最初 spawn 剩余列表、不启动目的地 spawn，生命反馈则使用当前形态；连续 set 另有定向与同侧异常限制。知识库编写者补充与已有资料的精确范围见下述专题。

spawn、生命反馈、重启保护与执行嵌套见：[spawn、生命反馈与 size-0 执行链](28-spawn、生命反馈与size0执行链.md)。
