# Buff 特殊 ID 前缀机制

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


以下机制由 Buff 的 `id` 前缀触发，不是 `stat_type`、`rule_type` 或 Buff 源类型。只要 Buff ID 具有指定前缀，就会继承对应行为。

## `DUELIST_TOUCHE_DODGE_`
- Buff ID 以 `DUELIST_TOUCHE_DODGE_` 开头时，Buff 会在持有者闪避后被清除。
- 英文资料写作 `DUELIST_TOUCHE_DODGE_N`，同时又明确说明以 `DUELIST_TOUCHE_DODGE_` 为前缀的 Buff 都会继承该行为。
- 因此应按前缀 `DUELIST_TOUCHE_DODGE_` 使用；末尾的 `N` 疑似表示任意数字，也可能是原文多写，当前资料不能确定其含义。

## `ATTACKS_ANY_LAUNCH_RANK`
- Buff ID 以 `ATTACKS_ANY_LAUNCH_RANK` 开头时，持有者的所有技能忽略启动站位限制。
- 该前缀机制无视该 Buff 的 rule：即使 rule 不满足，特殊 ID 行为仍会生效。

## `ATTACKS_ANY_TARGET_RANK`
- Buff ID 以 `ATTACKS_ANY_TARGET_RANK` 开头时，持有者的所有技能忽略目标站位选择限制。
- 对 AOE 技能无效。
- 该前缀机制无视该 Buff 的 rule：即使 rule 不满足，特殊 ID 行为仍会生效。

## 使用边界
- 这些字符串是 Buff `id` 的前缀，不要填写到 `stat_type`、`stat_sub_type`、`rule_type` 或 `buff_source_type`。
- 前缀后可以继续追加用于区分不同 Buff 的后缀；不得把“前缀继承行为”误写成“只有完全同名 ID 才有效”。
- “无视 rule”只说明特殊 ID 前缀带来的站位忽略行为不受 rule 限制，不代表该 Buff 的普通 `stat_type` 效果也必然无视 rule。

## 来源与可信度
- `Fire's Edge Modding Features翻译（无夜译注）.xlsx`，`Buffs` 工作表第 27～29 行。
- `DUELIST_TOUCHE_DODGE_N` 中 `N` 的具体含义未确认；“以 `DUELIST_TOUCHE_DODGE_` 为前缀会继承行为”是资料明确内容。
