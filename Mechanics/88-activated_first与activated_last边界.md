# activated_first 与 activated_last 边界

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


`activated_first` 与 `activated_last` 只比较英雄行动顺序，不把怪物行动计入判定。单刷时，英雄的天然回合同时满足两个 Rule；该英雄获得额外回合后，`activated_first` 变为假，但 `activated_last` 仍为真。被心控并移动到怪物侧的英雄仍会计入这两个 Rule；战斗外不存在行动顺序，二者均不生效。

```json
{"rule_type":"activated_first","is_false_rule":false}
{"rule_type":"activated_last","is_false_rule":false}
```

由二者同时为真构造的“单刷”条件，准确含义是“单刷时的天然回合”，不是单刷期间的所有额外回合。怪物速度可能决定天然回合的实际先后，但不改变怪物不计入这两个 Rule 的范围。

以上为社区测试结论；不同回合来源、更多怪物天然回合和未列出的跨侧状态仍需专项验证。
