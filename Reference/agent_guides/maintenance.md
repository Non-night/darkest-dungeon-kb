# 维护与源文件地图

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 一条知识怎样进入知识库

先查已有内容，区分补充、纠错、撤回、合并、索引调整。证据记录保留原话、对象/调用方/目标、条件、时序、版本、来源定位、确认状态与未知项。历史“用户”指知识库编写者，当前授权只来自当前用户。

| 要改什么 | 可编辑入口 | 生成内容 |
|---|---|---|
| 机制正文 | `Sources/mechanics/<原专题名>.md` | `Mechanics/`、`RAG/mechanics.jsonl` |
| Buff 源表与 AI 原表 | `tools/mechanics_tables.py`、`tools/monster_ai_source_topic.py` 及冻结工作簿 | 专题15内表与专题94；不要改生成表格 |
| 自动机制卡 | 正文对应章节；卡的 ID/选择器在 `Sources/navigation/cards/` | `RAG/mechanic_cards.jsonl`，每节有定位与哈希 |
| 定制机制摘要 | `Sources/navigation/cards/` 内 `summary_mode=curated` 的条目 | 同上；正文改变时核对定制摘要 |
| 锚点、路由、关系 | `Sources/navigation/anchors/`、`routes.json`、`relations.json` | `RAG/agent_*.jsonl`；`Sources/agent_index_source.json` 仅为生成的兼容视图 |
| 入口协议与实现检查 | `Sources/protocol/` | `AGENT_USAGE.md`、`README.md`、`Reference/agent_guides/` |
| Effect / Buff 字段 | `tools/generate_effect_buff.py`，新版增补另见 `tools/modding_update_remaining.py` | `Effect/`、`Buff/` 与对应 JSONL |
| Info / Art / Override | `tools/generate_info.py`、`tools/info_schema_data.json` | `Info/` 与对应 JSONL |
| 原版速查、本地化索引 | 相应 `generate_vanilla_index.py`、`generate_description_index.py` 与冻结输入 | `Reference/` 与对应 JSONL |
| 原版副本数值表 | `Sources/vanilla_raid_tables.md` | `Reference/vanilla_raid_tables.md` |
| 逐条证据 | `Sources/` 下来源账本、原文与快照 | 供正文与索引引用，不能用摘要取代 |

原版专属数值、默认分布和固定实例归入原版速查表。Mod 可复用的路径、文件命名、字段结构、加载条件与配置机制归入机制专题。混合条目拆开放置并互相链接。

来源地图是职责说明，不自动授权写所有目录。机制标题、路径、ID 尽量稳定；确需合并时保留跳转和历史，不让旧链接失效。正常修改无需在 Python 里追加 `replace()` 链。

## 最小维护闭包

1. 修改正文与证据。纠错要说明旧说法的状态和新依据；不要仅加相反摘要来掩盖旧正文。
2. 查相关锚点及定制摘要。普通章节摘要自动更新；定制摘要的来源指纹改变会显示 `summary_drift`。核对后同步摘要和 `source_snapshot_sha256`，不要只刷新指纹隐藏旧结论。迁移指纹仅表示快照，不代表重新实测。只有新增可复用的跨字段结论时才加锚点，不必每次加路由。
3. 有帮助的关系可显式记录，不需要给所有可能推论预先建边。维护联想入口时写清关系类型、条件与来源。
4. 重建并运行结构、检索、细节保留和迁移检查。新增字段必须完整重建 Effect/Buff/Info；纯机制/导航可用增量重建。

```powershell
python tools/build_knowledge_base.py --mechanics-only
python tools/validate_knowledge_base.py
python tools/test_kb_query.py
python tools/test_kb_organization.py
python tools/audit_reorganization.py
python tools/portable_kb.py check
```

新增/变化外部资料另运行 `audit_coverage.py --dry-run`，逐项处理候选；不能刷新基线来隐藏未处理内容。没有 Git 时以备份、文件清单与哈希检查改动范围。代码校验与游戏实测分开报告。

## 2026-11-11 整理保留策略

98个专题从原生成器的最终正文迁出，原 Python、索引、协议和正文备份于 `Review/reorganization_20261111/before_sources.zip`。正文细节、原始来源与旧 ID 保留。普通机制卡改为按原节生成；定制摘要继续保留其证据边界。一个残留旧版推拉文件改为兼容跳转，历史全文仍在备份。

所有已登记的差异、回归结果与未决项见 `Review/reorganization_20261111/report.md`。结构全量覆盖不等于对全部来源重新进行实机验证。
