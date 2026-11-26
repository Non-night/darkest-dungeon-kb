# Buff rule 存档内 ID 与 `rule_type` 对照

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 结论

存档中的 Buff 对象使用数值字段 `rule` 保存 Buff Rule ID。对当前用户提供的存档文本进行读取时，在 `actor.buff_group[*].rule` 中发现 **64 个 Buff 实例**；其中去重后的数值完整覆盖 `0` 至 `54`，共 **55 个存档内 Rule ID**。

下表按知识库当前 `rule_type` 顺序给出存档内 ID 对照。ID 是零基编号；原《Buff Rules》术语表的序号从 1 开始，因此通常可理解为“术语表序号 - 1”。

## 对照表

| 存档内 `rule` ID | `rule_type` |
|---:|---|
| `0` | `always` |
| `1` | `skill` |
| `2` | `riposte` |
| `3` | `rangedonly` |
| `4` | `meleeonly` |
| `5` | `actorStatus` |
| `6` | `monsterSize` |
| `7` | `firstroundonly` |
| `8` | `in_camp` |
| `9` | `in_dungeon` |
| `10` | `in_activity` |
| `11` | `in_room` |
| `12` | `in_corridor` |
| `13` | `at_deaths_door` |
| `14` | `in_rank` |
| `15` | `hpbelow` |
| `16` | `hpabove` |
| `17` | `lightbelow` |
| `18` | `lightabove` |
| `19` | `torch_setting` |
| `20` | `stress_below` |
| `21` | `stress_above` |
| `22` | `virtued` |
| `23` | `afflicted` |
| `24` | `monsterType` |
| `25` | `attacking_monster_type` |
| `26` | `monster_type_count_min` |
| `27` | `is_vampire` |
| `28` | `target_is_vampire` |
| `29` | `has_quirk` |
| `30` | `walking_backwards` |
| `31` | `actor_base_class` |
| `32` | `in_mode` |
| `33` | `is_guarded` |
| `34` | `target_is_guarded` |
| `35` | `is_guarding` |
| `36` | `target_is_guarding` |
| `37` | `is_stealthed` |
| `38` | `target_is_stealthed` |
| `39` | `has_item_id` |
| `40` | `has_item_type` |
| `41` | `is_actor_status` |
| `42` | `no_trinkets` |
| `43` | `target_hpabove` |
| `44` | `target_hpbelow` |
| `45` | `activated_last` |
| `46` | `activated_first` |
| `47` | `ondeathsdoorenter` |
| `48` | `target_in_rank` |
| `49` | `is_target_corpse` |
| `50` | `any_is_burning` |
| `51` | `negative_quirk_above` |
| `52` | `quest_uses_remaining_above` |
| `53` | `has_buff` |
| `54` | `target_is_burning` |

## 存档字段与证据边界

- 存档字段路径：`actor.buff_group.<buff_guid>.rule`。
- 存档中同时存在对应的 `is_false_rule`、`ruledata_number` 与 `ruledata_string` 字段；Rule ID 本身只表示 Rule 类型，不包含这些参数。
- 本表的数值 ID 直接来自当前用户提供的存档数据；`rule_type` 名称与顺序依据知识库当前 Buff Rule 记录整理。
- 当前用户提供的存档文本中，`rule` 数值覆盖 0–54，但该文本本身没有同时保存 Rule 名称。因此，“存档数字 ID 与知识库 `rule_type` 顺序的对应关系”属于基于存档完整 ID 覆盖与知识库 Rule 顺序的对照整理；若要达到反编译级确认，仍需带有 Rule 枚举名称或程序结构的独立来源。

## 来源

1. 当前用户提供的存档文本：`Sources/portable_evidence/d0/d022971a425b5861ee1e35c1d8272cded38aab8f8448e389315cba545ad484dd.txt`，读取 `actor.buff_group[*].rule`。
2. 《暗黑地牢代码（基于Oni术语表）……xlsx》的 `Buff Rules` 工作表：传统 Rule 顺序与名称。
3. Fire's Edge Modding Features 中文译注表 `Buffs` 工作表第 17–25 行：知识库后续收录的新增 Rule 类型。
4. 知识库当前结构化 Rule 记录：`RAG/buff_rule_types.jsonl`。

## 证据等级

- 存档中出现哪些数值：**当前用户提供的存档数据，直接观察**。
- 每个数值对应的名称：**知识库 Rule 顺序对照，当前资料下的整理结果**；不是仅凭存档字段名称直接读取出的名称。
- 本页只记录字段映射，不额外推断各 Rule 的目标、时序、真假判定或 `is_false_rule` 行为；这些内容仍以各 `Buff/rule_type/*.md` 词条为准。
