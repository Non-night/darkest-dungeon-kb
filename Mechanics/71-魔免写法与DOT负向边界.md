# 魔免写法与 DOT 负向边界

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 三类写法

- **假魔免**：把流血、腐蚀等抗性提高到已知上限附近；超过该抗性上限的施加率仍可能穿透，因此不是严格免疫。
- **真魔免弱魔免**：这是 `combat_stat_multiply` 的 `damage_received_percent` 硬减伤 Buff，不是 DOT“所受量”。`amount: -1.0` 时，满足 Rule 的伤害被压为 0。`rule_type: "skill"`、`rule_data.string: "aaa"`、`is_false_rule: true` 的精确含义是：在有效技能判定中，当前技能 ID 不是 `aaa` 时成立；当前技能 ID 是 `aaa` 时为普通 `false`；无有效技能判定时为 `null`，取反后仍不生效。“不存在的技能 ID＋取反”不等于 `always`。证据：迂回表第31条 P818/X950、P822/X954–P823/X955，当前用户2026-11-03确认。该 Rule 从玩家按下技能时进入判定期；对 ActorDot 的覆盖仍有调用者、受术者和残留时机边界。
- **真魔免强魔免**：同样是 `damage_received_percent` 硬减伤。`rule_type: "attacking_monster_type"`、指定怪物名并取反时，普通 false 的精确含义是：当前不是被该指定名字的怪物攻击时成立；但 Rule 返回 `null` 时无论取反与否都不成立。该 Buff 不仅抵消 DOT，还会抵消各种指向持有英雄自身的非直伤（例如队友技能指向自身的真伤、队友 act_out 攻击队友产生的生命百分比伤害、自己技能指向自身的真伤等）。只有在被任意怪物攻击或反击时，`attacking_monster_type` 的该 Rule 才进入例外判定，使对应直伤不被此 Buff 抵消。该 Rule 的稳定用法仅在英雄侧得到支持，怪物侧不可用。

弱魔免代码骨架（将 `aaa` 替换为实际技能 ID）：

```json
{
  "id": "ExampleWeakMagicImmunity",
  "stat_type": "combat_stat_multiply",
  "stat_sub_type": "damage_received_percent",
  "amount": -1.0,
  "remove_if_not_active": false,
  "rule_type": "skill",
  "is_false_rule": true,
  "rule_data": {"float": 1.0, "string": "aaa"},
  "is_clear_debuff_valid": false,
  "has_description": true
}
```

强魔免代码骨架（将怪物类型名替换为实际内部 ID；仅用于英雄侧）：

```json
{
  "id": "ExampleStrongMagicImmunity",
  "stat_type": "combat_stat_multiply",
  "stat_sub_type": "damage_received_percent",
  "amount": -1.0,
  "remove_if_not_active": false,
  "rule_type": "attacking_monster_type",
  "is_false_rule": true,
  "rule_data": {"float": 1.0, "string": "指定怪物类型"},
  "is_clear_debuff_valid": false,
  "has_description": true
}
```

**负量DOT存在性已修正（2026-11-05）**：Effect型与Buff型DOT正负量均可存在，最终负持续时间不可存在；旧“负量必定被抵抗”的禁用依据已撤回。负量存在不自动证明负量抵消、元素护盾和魔免整套方案可用，具体结算仍核对[专题66](66-负数DOT与不可治愈边界.md)。这不改变本页不依赖负量DOT的硬减伤规则。

知识库编写者此前记录过旧版本/早期观察：怪物侧硬减伤低于 `-100%` 时可能使生命值上升。当前用户于 2026-10-08 更正：在未知的某次更新之后，怪物侧现已与英雄侧表现一致，硬减伤低于 `-100%` 时只会把伤害压为 `0`，不会导致生命值上升；当前也不应再按“超量回血”或该路径触发向上生命反馈处理。更新发生的具体版本和时间未知。

以上为当前版本观察与历史边界的并列记录；不同版本、死门源和 ActorDot 组合的完整边界仍未全部确认。
