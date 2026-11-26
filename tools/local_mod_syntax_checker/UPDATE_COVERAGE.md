# Build 28385 检查器适配账本

维护日期：2026-11-08。当前用户授权修复知识库内置检查器；不修改外部插件、独立 Buff 检查器、游戏或 Mod。

## 证据与范围

- 新版语法证据：`Review/2026-11-05-Modding-Update/vs_plugin_update_inventory.json` 的全部78项；`Sources/modding_update_20261105_remaining.json`；同目录 `source.md` 和 `translation_blocks.json`。这些是已采纳的社区资料/新版功能说明，不等同于本次实机测试。
- Header 语法：`RAG/info_fields.jsonl` 的 `battle_modifier:|.ignore_hp_scale` 与 `combat_skill:|.ai_valid/.counts_towards_skill_limit/.skill_visible/.force_selection`。仅在对应 Header 放行，不扩展到所有技能 Header。
- Buff 附魔数组：上述来源的 blocks 52–62；新饰品 Trigger：block 118；`specific_recruit`：block 95；怪癖新时间单位依原说明为 `combat_end` / `quest_end`，不得替换为 `quest_complete` 等猜测值。
- 既有结构参考：原版 `DarkestDungeon\raid\camping\default.camping_skills.json` 的 `skills[].effects[]`；原版 `DarkestDungeon\campaign\town_events\base.town_events.events.json` 的 `events[].data[]`；官方 DLC `DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\trinkets\crimson_court.entries.trinkets.json` 的 AdditionalEffects 字符串数组；原版 `DarkestDungeon\shared\quirk\quirk_library.json` 的 `quirks[]`。只读核对，没有修改这些文件。

## 逐类覆盖

| 清单类别 | 数量 | 本次后的状态 |
|---|---:|---|
| Effect 关键字 | 16 | 两入口共享单参数类型检查；含13项新关键字及既有 `dotShuffle`、`cure_burn`、`set_trigger_limit`。不推定未知字符串枚举。 |
| Effect 新目标 | 10 | 两入口接受；Python 不再以旧插件枚举覆盖较新值域。 |
| Buff 主类型 | 8 | 7项新增和既有燃烧衰减继续可识别；动态/无副类型约束保留，不扩展偷取列表。 |
| Buff Trigger 字段 | 25 | 两入口接受字符串数组，包括空数组；非法数组/元素仍报错。 |
| Buff `force_negative` | 1 | 两入口接受布尔值，字符串布尔不合法。 |
| Info 字段 | 5 | 两入口接受对应 Header 下的单一布尔值；缺参数、错误类型、错误 Header 均报错。 |
| JSON 扩展 | 9 | 4个饰品数组、扎营2项、指定新兵参数、怪癖时间单位有基础检查；事件付费组合仅记录未覆盖，不声称可验证组合运行行为。 |
| props/BGM/怪癖图片 | 4 | 仅保留已知语法/路径证据，不以静态检查证明加载与呈现效果。 |

## 修复根因

1. 旧 Info 原始表与新版知识文档脱节。新增共享 `update_rules.json`，Python 在旧表上加载经采纳的新规则，C# 构建时嵌入同一份规则。
2. Python 原先读取较新的 Effect 值域后又被旧插件表覆盖，导致10种合法目标误报。改为合并，新增参数由共享类型规则验证。
3. C# Buff 字段表漏24种附魔数组与 `force_negative`；Python 原先完全不检查这些字段类型。补齐 Core 字段表，并让 Python 读取这份表进行类型检查。
4. 删除“部分激活 Rule 必不能触发攻击附魔”的过期诊断；强制过抗的守护类 Effect 不再触发旧概率警告；`other_trinket` 不再被饰品目标建议误报。
5. Python/文档原先容易把“检查完成”误读为“完整 Core 已运行”。现在输出覆盖边界，README 明确说明 Python 不调用 C#，完整 Buff 专项语义需另运行内置 C# 入口。

## 测试与未覆盖边界

- `test_update_rules.py` 自动遍历全部78项，防止新清单项目未分类；分别对两个入口构造合法字段/目标、缺参数、错误值、未知字段、错误 Header、所有 Buff Trigger 类型错误，以及实际功能目录下的 JSON 扩展正反例。
- `test_checker.py` 保留旧诊断和引用闭包回归；新测试不是通过关闭未知字段检查或将错误统一降级实现。
- 不因删除过期诊断就宣称 daze/stun 所有组合已修复；保留既有实测风险边界。Effect 时序、概率共享、切模式、引擎加载、最终目标与新旧字段实际运算行为仍需实机证据。
- `KB-COVERAGE-PARTIAL` 表示对应 JSON 专题只有局部验证；`KB-COVERAGE-BUFF-PARTIAL` 表示 Python 未运行完整 Core 语义。它们是覆盖信息，不是游戏错误，也不代表已验证未覆盖部分。
- 本次新增 JSON 基础诊断使用文件级位置并在消息中提供 JSON 路径；完整 C# Buff 专项仍保留原有精确行列。
- 未修改 `tools/info_schema_data.json` 的历史插件快照，也未改写来源快照或原版实例。新版 overlay 是独立的已采纳增量，不冒充旧插件原本支持。
