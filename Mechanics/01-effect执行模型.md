# Effect 执行模型

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


Effect 文件格式、注释、必填 `.name` 与常见定义骨架见：[Effect 定义基础](../Effect/README.md)。

## Update 的统一含义

知识库各处作为游戏机制术语使用的 `Update` 指同一个游戏状态更新机制，包括模型更新、`bsrc_instantSkill` 来源清除及真光环的 Any Update 清除；不能按所在章节将其拆成彼此独立的机制。当前用户于2026-11-03明确统一该术语；非本轮新增实机测试。具体条目所述触发动作和结果仍按其记录理解，不据术语统一补造尚未记录的结果。

## 最小心智模型
一次 effect 不是孤立运行的。至少要同时考虑：

1. **定义**：`effect:` 行通过 `.name` 建立可被引用的 Effect。
2. **调用方**：技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等。
3. **调用方提供的目标**：例如技能选中的一个或多个单位。
4. **effect 的 `.target`**：对调用方目标再次映射，可能改为施术者、双方群体或全局。
5. **执行次数**：群攻会逐个调用目标执行；`.apply_once` 可阻止后续重复。
6. **结算时序**：`.queue`、`.apply_with_result`、死亡、行动结束、战斗结束等。
7. **后续反应**：ActorDot、hp_reaction、spawn、buff rule 可能晚于原 effect。

## 创作检查清单
- Effect 是否已在 `effects\*.effects.darkest` 中定义，并具有唯一、正确的 `.name`？
- 谁引用该 effect？
- 调用方提供几个目标？
- `.target` 把最终目标改成谁？
- effect 会执行一次还是按目标重复？
- 是否要求在直伤前、行动结束前或战斗胜利前完成？
- effect 杀死目标后，还期待哪些 ActorDot/hp_reaction 执行？

## 安全原则
先做单目标、queue 默认值、无回合外改动的最小版本，再逐项加入群体、AWR、spawn、initiative。复杂功能应拆成多个命名清晰的 effect，并给每个中间 effect 写明时序职责。
