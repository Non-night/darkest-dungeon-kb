# Buff 知识库

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- [buffs.json 结构、标准必写项与可选项](buff_schema.md)
- [stat_type 存档数字 ID 与 amount 默认增益/减益分类](stat_type_amount_classification.md)
- `rule_type`：55 条
- `stat_type`：101 条
- `duration_type`：12 条

## 创作默认规范
- 每条 Buff 通常都要显式填写 `rule_type`、`is_false_rule`、`rule_data.float` 与 `rule_data.string`；无条件 Buff 也写 `rule_type: "always"`。
- `remove_if_not_active` 默认显式写为 `false`；只有设计明确要求条件失效立即移除，或特定 Buff 类型已有证据要求使用 `true` 时才可改为 `true`。
- 有明显玩家可读意义的常规 Buff（如眩晕抗性、减压量）默认写 `has_description: true`；纯寄存器／逻辑门／自清理等辅助 Buff 才可默认写 `false`，用户明确要求时除外。
- 完整字段分级、标准骨架与例外见 `buff_schema.md`。

每个词条采用与 Effect.name 相同的字段化结构，适合精确检索。
