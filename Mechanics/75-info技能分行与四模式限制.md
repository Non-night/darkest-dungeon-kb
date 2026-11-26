# info 技能分行与四模式限制

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 已确认结论

同 ID 的 `skill` 分行可使用新版精简写法：首行提供完整参数，后续行提供新增或覆盖字段。已观察到的字段包括 `level`、`valid_modes`、公共 Effect 和子模式 Effect。

### 模式差分的同行 `valid_modes` 前置条件

当前用户补充（2026-09-29）：已知技能的模式差分必须依附于同一行存在的可用模式定义。若某字段写成 `.<mode_id>_effects`，则该行必须写有 `.valid_modes`，且其中必须包含对应的 `<mode_id>`；否则该模式差分视为没有写入，不应按可用模式 Effect 处理。

```text
// 有效：同行声明了 aaa，并提供 aaa 的模式 Effect
skill: .id "example" .valid_modes "aaa" .aaa_effects "example_mode_effect"

// 无效：没有同行 valid_modes，aaa 差分视为未写
skill: .id "example" .aaa_effects "example_mode_effect"

// 无效：同行 valid_modes 没有 aaa，aaa 差分视为未写
skill: .id "example" .valid_modes "bbb" .aaa_effects "example_mode_effect"
```

这里的“同行”指同一条最终被解析的技能定义行／分行组合中，实际提供该模式差分的那一行；等级分行、无等级共用分行及字段覆盖仍需按对应 Header 的分行继承规则逐项核对，不要把另一条无关技能行的 `.valid_modes` 借来满足条件。

`valid_modes` 也可以作为无等级共用分行内容使用：如果所有技能等级允许的模式集合完全相同，应在所有等级行之后只写一次不带 `.level` 的同 ID `skill:` 行；只有模式集合随等级变化时，才在各等级行分别书写。这样可以避免无意义的逐级重复，不改变 `.valid_modes` 单行最多 4 个模式的既有边界。

```text
skill: .id "example" .level 1 .valid_modes "0 1" .effect "base"
skill: .id "example" .level 2 .valid_modes "2 3" .effect "upgrade"
```

单行 `valid_modes` 实测上限为 4 个模式，超过 4 个应继续分行。第二行哪些字段继承、哪些覆盖，必须按对应 Header 和原版实例逐字段确认，不能笼统假定未重复字段全部继承。

## 未知边界

怪物技能也观察到同类写法，但不同 Header 的解析和重复参数优先级尚未完全测完。

## 模式名与 Effect ID 冲突

社区实测发现，**不要直接把 Effect 的 ID 命名为模式名**。当技能引用与模式名完全相同的 Effect 时，即使技能的 `.valid_modes` 未包含该模式，技能也可能被无条件视为处于该模式下，导致模式限制失效；该现象与 `.target` 是否省略、引用是否加引号、使用公共 Effect 还是子模式 Effect，以及 32/64 位主程序无关。

```text
// 不安全：Effect ID 与模式名完全相同
effect: .name "Rajang_E" .set_mode Rajang_E
skill: .id "Rajang_SK5" .valid_modes Rajang_Pre .effect Rajang_E

// 安全命名：避免与任何模式名完全相同
effect: .name "set_mode_Rajang_E" .set_mode Rajang_E
skill: .id "Rajang_SK5" .valid_modes Rajang_Pre .effect set_mode_Rajang_E
```

创作时应为模式切换 Effect 使用不会与任一模式 ID 完全相同的专用命名。该结论来自特定版本黑箱测试；其他会触发模式解析的 ID 碰撞形式尚未穷举。
