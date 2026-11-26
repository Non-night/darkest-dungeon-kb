# 进攻向 Rule 不适用于防御向 Buff

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 已确认结论

这些 Rule 都是**进攻型（施术）Rule**：带 Rule 的 Buff 位于施术者身上，Rule 在被修饰的技能或 Effect 处理时检查受术者／目标上下文；它们不是贴在受术者身上、持续读取受术者状态的防御向 Rule。对 `actorStatus` 而言，`rule_data.string` 是要在受术者身上查找的状态。目标上下文必须按被修饰的属性区分：技能层百分比加伤、穿甲等读取当前技能目标；腐蚀概率等依靠具体 Effect 结算的属性读取该 Effect 的最终目标。群体目标按每个最终目标分别判定，不能把两种目标上下文混写。`monsterType`、`monsterSize`、`actor_base_class` 同属目标型 Rule，但各自的目标类型和取值仍须按对应词条核对；`meleeonly`、`rangedonly`、`skill` 则检查当前技能元数据，不是受术者状态。

`actorStatus`、`monsterType`、`monsterSize`、`actor_base_class` 不必依附于技能固有目标：适配的进攻向属性在非技能调用的 Effect 中也可受它们修饰，按该次调用和 Effect 实际目标判定。这是四种 Rule 的一般适用性，不表示任意 `stat_type` 都能在非技能调用中生效，也不保证任意配置均无干扰；技能层与 Effect 层的目标解析仍须分开，防御向 Buff 仍不能使用这四种 Rule。证据：迂回表第62条 P1204/X1411；当前用户于2026-11-03确认，非本轮新增实机测试。

```json
{
  "rule_type":"actorStatus",
  "is_false_rule":false,
  "rule_data":{"float":0.0,"string":"stunned"}
}
```

### 示例一：技能层穿甲读取技能目标

下面的 Buff 定义放在**施术者**身上。它修饰技能层的 `ignore_protection`，因此 `actorStatus` 检查当前技能的目标是否具有 `stunned`，而不是检查施术者自身：

```json
{
  "id": "KB_actorStatus_stunned_skill_pen",
  "stat_type": "ignore_protection",
  "stat_sub_type": "",
  "amount": 0.5,
  "remove_if_not_active": false,
  "rule_type": "actorStatus",
  "is_false_rule": false,
  "rule_data": {"float": 0.0, "string": "stunned"},
  "is_clear_debuff_valid": false,
  "has_description": true
}
```

该 Buff 已经位于施术者身上时，技能的 `.target 1234` 提供被检查的技能目标：

```darkest
combat_skill: .id "KB_attack" .level 0 .type "melee" .atk 100% .dmg 3 5 .crit 5% .launch 4321 .target 1234
```

目标眩晕时，该技能层穿甲 Buff 才干涉这次技能；目标没有眩晕时，该 Rule 不成立。

### 示例二：Effect 层腐蚀概率读取 Effect 目标

下面的 Buff 同样放在**施术者**身上，但它修饰 `poison_chance`，该属性在具体腐蚀 Effect 结算时才读取目标。因此 Rule 检查的是该 Effect 的最终 `.target`：

```json
{
  "id": "KB_actorStatus_stunned_poison_chance",
  "stat_type": "poison_chance",
  "stat_sub_type": "",
  "amount": 0.5,
  "remove_if_not_active": false,
  "rule_type": "actorStatus",
  "is_false_rule": false,
  "rule_data": {"float": 0.0, "string": "stunned"},
  "is_clear_debuff_valid": false,
  "has_description": true
}
```

该 Buff 已经位于施术者身上时，下面的 Effect 以自身最终目标进行 `actorStatus` 判定：

```darkest
effect: .name "KB_poison" .target "target" .chance 100% .poison 3 .duration 3 .on_hit true .on_miss false
```

因此不能因为这两个 Buff 都由施术者持有，就把腐蚀概率的判定对象改写成技能 Header 的目标集合；必须读取实际执行该腐蚀 Effect 的最终目标。

## 常驻负修正与近战、远程正修正的三 Buff 组合

可用三条 Buff 形成这样的净值组合：一条常驻降低减益施加率，另两条分别以 `meleeonly`、`rangedonly` 为条件提供等量正修正。在自身对应技能的 Rule 有效判定期间，匹配的正修正抵消常驻负修正；被敌方近战或远程攻击时，这两条进攻向 Rule 不激活，因而保留常驻负修正。三条 Buff 仍各自存在，数值抵消不是移除实体，也不是在一条 Buff 中并列两个 Rule。

原表用常驻 −500000%、近战条件 +500000%、远程条件 +500000% 演示减益施加率抵消；这些极值只是原表示例，不是必需值或通用安全数值。组合要求对应属性及结算路径确能等量抵消，不能据此把任意属性或未被近战／远程条件覆盖的技能类型都认定为已覆盖。

这里使用“对应 Rule 有效判定期间”，不能简化为“仅在实际释放技能之后”：知识库已确认 `meleeonly`／`rangedonly` 在选中技能、尚未释放时就进入判定期。该组合也不保证任意 ActorDot、`act_out`、反击、饰品反馈等调用都不受干扰，具体上下文仍须核对。减益施加率只在实际使用该属性的概率路径中影响效果；同侧 Buff 及已确认特殊目标的不过抗边界仍按 [Buff 概率专题](95-Buff同侧异侧与减益概率判定.md) 处理。

证据：迂回表第51条 P1117/X1300–P1123/X1307，原表称受 sasiji 蘑菇人饰品启发；当前用户于2026-11-03确认按上述组合及判定范围补入，非本轮新增实机测试。不将“非自身使用技能时”的原表概括扩大为对所有额外调用方的无干扰保证；此处记录机制组合，不补造具体 Mod 实现。

## 未知边界

四种目标型进攻 Rule 可在非技能 Effect 中使用，但反击、饰品、ActorDot、act_out 等具体调用中的施术者归属、属性读取层、目标解析及其他交互仍须逐项核对；不因一般适用性就认定这些来源的每种配置均按上述两个技能示例运行。
