# Info / Art / Override 定义知识库

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


本层整理单位 `Info` 体系的 67 个 Header、静态可写字段、参数限制、适用对象和官方实例。

## 文件与语法

- 常见文件：`*.info.darkest`、`*.art.darkest`、`*.override.darkest`。
- Info 与 Art 内容可以写在同一文件；社区习惯通常仍把逻辑和美术定义分开。
- 每个定义块以 Header 开始，字段以点号开头：

```darkest
combat_skill: .id "skill_id" .level 0 .type "melee" .launch 1234 .target 12
```

- `//` 为注释。
- 同一 Header 可换行继续书写；示例代码不使用 `...` 作为省略号。
- 英雄 `combat_skill:` 还支持同 ID 分行及不写 `.level` 的“无等级共用分行”；其中 `.target` 有特殊合并规则，详见对应 Header 文档与 Mechanics 专题。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。

## 同文件名整体覆盖

`*.info.darkest`、`*.art.darkest`、`*.override.darkest` 在相同相对路径／文件名下整体覆盖，不按写出的 Header 增量补丁。英雄、怪物及其他 Info 类对象均须保留未修改部分；修改指定技能时应复制完整原文件后只替换目标定义。文件内部同 ID 分行不改变该跨来源覆盖边界。依据知识库编写者纠正，详见[文件覆盖](../Mechanics/13-文件覆盖、逆序覆盖与同ID合并.md)与[Mod目录](../Mechanics/24-Mod识别与职业Mod目录结构.md)。

## Info 非注释行长度上限

知识库编写者更正（2026-11-01）：Info 文件中的**非注释内容**单行保留前 511 个字符，仅大于 511 字符的部分被截断；恰好 511 字符不会因该长度限制被截断。空格、引号及其他已知参与该行的原始字符均计入长度，不能只计算可见的非空白内容。若 combat_skill: 行的前 511 个字符已经占满，其后追加的完整 Effect 引用 "aaa" 会被截断，视同未写；若截断点落在字段或引用内部，则可能使其不完整，不可依赖这种解析结果。换行符、制表符和中文字符是否以及如何参与底层计数，仍未确认。 若 `app.log` 随后出现 `Could not find effect "<ID>"`，还需按[该报错的查找失败边界](../Mechanics/12-报错类型与日志.md)区分表现与根因。

## 对象边界

- `skill:` 是怪物主动技能；`combat_skill:`、`combat_move_skill:` 是英雄技能。
- `riposte_skill:` 为英雄/怪物共用，部分字段的参数格式会随单位侧变化。
- `death_class:`、`life_time:`、`initiative:`、`enemy_type:` 属于怪物定义；英雄职业 Mod 仅可在 `corpse` 等特殊怪物实体中使用，不是普通英雄本体字段。
- “官方当前仅某一侧有实例”不等于已证实该字段绝对为该侧专用；文档会区分“特有”和“实例分布”。

## 检索顺序

1. 先到 [Header 索引](index.md) 选择对象与 Header。
2. 在对应 Header 文档中查字段参数、对象限制和官方实例。
3. 小模型/RAG 按 `header + keyword` 精确查 `RAG/info_fields.jsonl`。
4. 涉及 Effect 时序、Buff、ActorDot、spawn、生命反馈、真吸血、升级树、区域建筑、城镇事件、英雄外围标签或美术资源时，再加载对应 `Effect/`、`Buff/`、`Mechanics/` 文档；美术引用要区分动画名、资源文件名和 Atlas PNG 页面名。

## 证据边界

- 字段与固定候选来自静态合法字段表；知识库使用时不依赖任何外部插件或辅助软件。
- 行为说明优先采用游戏本体/官方 DLC 实例与已有社区文档。
- 仅有字段形式、没有行为证据时，明确写为“尚未确认”，不得由字段英文名补造机制。
- Fire's Edge 新增的 Info 内容已经并入对应 Header：`mode:.battle_start_effect_ids`、技能的 `.requires_burning` / `.dmg_per_burn_stack` / `.copy_burn_behind`、`death_class:.is_valid_on_burn_dot`。
