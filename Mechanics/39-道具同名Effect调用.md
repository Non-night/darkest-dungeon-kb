# 道具使用与同名 Effect 调用

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 核心规则
道具被使用时，引擎会调用与该道具 ID 同名的 Effect。

例如，道具 ID 为 `aaa`，则其使用流程要求存在：

```darkest
// 道具 aaa 的使用 Effect
effect: .name "aaa" .item 1 .target "target" .on_hit true .on_miss true
```

这里的关键关系是：

- 道具 ID：`aaa`
- Effect 名称：`.name "aaa"`
- 道具标记：`.item 1`

三者必须一致配套。道具定义不需要依靠另一个不同名称的 Effect 来承接其基础使用效果。

## `.item` 的要求
- 道具使用所调用的同名 Effect 必须写 `.item 1`。
- `.item` 是数字布尔字段，应写 `1`，不能改写为 `true`。
- `.item 1` 同时使该 Effect 带出的 Buff 按道具源 `bsrc_item` 处理。
- 普通技能、饰品 Trigger、spawn 等非道具调用的 Effect，不应仅为模仿道具格式而添加 `.item 1`。

## 失败边界
当前尚未明确以下错误各自会表现为红字、无效果或其他问题：

- 道具存在，但不存在与其 ID 同名的 Effect；
- 存在同名 Effect，但漏写 `.item 1`；
- 道具 ID 与 Effect `.name` 仅部分相似而非完全同名。

因此写 Mod 时不得依赖这些未明确的失败行为；应直接保证“道具 ID 与 Effect 名称同名，且 Effect 写 `.item 1`”。这类未明确内容可以规避，不要求学习者重复测试。

## Agent 实现检查
1. 是否读取了道具的实际 ID？
2. 是否创建了 `.name` 与该 ID 同名的 Effect？
3. 该 Effect 是否明确写了 `.item 1`？
4. 是否避免误写 `.item true`？
5. 是否没有优先复用原版同名 Effect/Buff，以免分行或覆盖干扰当前 Mod？
