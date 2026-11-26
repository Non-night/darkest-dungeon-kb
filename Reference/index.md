# 领域参考索引

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


本层不替代精确词条，而是告诉小模型“某类问题应去哪里找”。

| 领域 | 首选结构化内容 | 深入来源 |
|---|---|---|
| Effect | `Effect/keyword/`、`Mechanics/01~10` | 原版/官方 DLC 案例、主术语表 `Effects`、筛选后的 Mod effect 行 |
| Buff | `Buff/` | 主术语表 `Buff Types/Rules/Durations` 与结构化 Buff 词条 |
| Info / Art / Override | `Info/headers/`、`RAG/info_fields.jsonl` | 对应 Header 文档、游戏本体/官方 DLC 实例；工作簿行仅作补充 |

| initiative | `Mechanics/09-initiative行动点.md` | initiative 测试工作簿、主术语表 Effect 行 |
| Size-0 / spawn / hp_reaction | `Mechanics/05、07、08` | 已收录模板、Mod 案例与迂回代码 DOCX |

| 怪物 AI | `暗黑地牢怪物AI代码表` 各 Sheet | 原版怪物配置与已收录 Mod 的 monster AI 配置 |
| 城镇事件 | `暗黑地牢城镇事件效果代码表` | 原版事件 JSON/XML 案例 |
| 全局规则 | `全局规则整理` 工作簿 | 对应原版 rules 文件与实机测试 |

| 地图生成 | 主术语表 `maps` Sheet | 原版地图教程与生成文件 |

## 检索规则
- 先用 `RAG/domain_catalog.jsonl` 找到 workbook/sheet。



