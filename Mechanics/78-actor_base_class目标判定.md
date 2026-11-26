# actor_base_class 的目标判定

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 已确认结论

`actor_base_class` 是进攻型（施术）Rule。它检查当前 Effect 的实际作用目标，而不是技能 Header 声明的目标集合；因此同一技能对友方施加的 Effect，也会按该友方的职业/怪物内部 ID 判定。非技能调用（如 size-0、act_out、饰品触发）同样可以使用，但必须以该 Effect 的实际目标为准。

```json
{
  "rule_type":"actor_base_class",
  "is_false_rule":false,
  "rule_data":{"float":0.0,"string":"hero_id"}
}
```

## 限制

该 Rule 不能在防御型（受术者）Buff 上生效；不能因为技能目标栏写了敌方站位，就把所有同技能的友方 Effect 都当作敌方目标判定。`true/false/null` 三态及取反规则仍按通用 Rule 语义处理。
