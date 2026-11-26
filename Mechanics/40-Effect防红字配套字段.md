# Effect 防红字配套字段

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 非零 `.stun` 与 `.queue true`
当 Effect 写有 `.stun`，且其参数不为 `0` 时，通常需要同时写：

```darkest
.queue true
```

否则会产生红字报错。由于 `.queue` 省略时默认是 `false`，所以不能认为“没有填写 `.queue`”会自动获得适合眩晕的时序。

安全写法示意：

```darkest
// 非零眩晕通常放在 queue true
effect: .name "aaa_stun" .target "target" .chance 100% .stun 1 .on_hit true .on_miss false .queue true
```

这条规则描述眩晕 Effect 的常规防红字配套。`.stun 0` 不属于“参数不为 0”的情况。若特殊机制明确要求 AWR 或 `queue false` 眩晕，可以刻意不写 `.queue true`，但需要接受由此产生的红字；不能为了消除红字而擅自改变设计所需时序。

## 加减光 Effect 默认使用 queue true

知识库编写者确认（2026-09-20）：Effect 的 `.torch_increase` 与 `.torch_decrease` 若不在 `queue true` 时序执行，会产生红字报错。没有专门的时序设计要求时，两者都应显式写 `.queue true`；省略 `.queue` 默认是 false，不能省略来规避此要求。

若设计明确要求其他时序，应保留所需时序并说明红字代价，不能为消除报错而破坏依赖链。该结论针对 Effect 的直接加减光，不是 `torch_increase_percent`／`torch_decrease_percent` Buff 的图标规则；也不额外断言 spawn 等调用方中 queue 能建立与技能相同的阶段。

## DOT、击退/拉前与 `.can_apply_on_death true`
写有以下效果的 Effect，通常需要同时写 `.can_apply_on_death true`，否则会产生红字报错：

- 有效 DOT；例如流血、腐蚀、压力 DOT、燃烧等；
- 击退；通常由 `.push` 表示；
- 拉前；通常由 `.pull` 表示。

安全写法示意：

```darkest
// DOT 的常规防红字配套
effect: .name "aaa_bleed" .target "target" .chance 100% .dotBleed 3 .on_hit true .on_miss false .can_apply_on_death true

// 击退的常规防红字配套
effect: .name "aaa_push" .target "target" .chance 100% .push 1 .on_hit true .on_miss false .can_apply_on_death true

// 拉前的常规防红字配套
effect: .name "aaa_pull" .target "target" .chance 100% .pull 1 .on_hit true .on_miss false .can_apply_on_death true
```

`.can_apply_on_death true` 的机制含义仍是：攻击技能在自身结算窗口内击杀目标后，允许相应 Effect 延续到新生成的尸体。将它作为 DOT、击退或拉前的防红字配套，并不意味着 DOT 触发被改成了原技能内即时击杀。

## Agent 实现检查
1. `.stun` 参数是否不为 `0`？若是，常规情况是否明确写了 `.queue true`；若刻意使用 AWR/`queue false`，是否保留所需时序并明确接受红字？
2. Effect 是否包含有效 DOT？若是，是否明确写了 `.can_apply_on_death true`？
3. Effect 是否包含 `.push` 或 `.pull`？若是，是否明确写了 `.can_apply_on_death true`？
4. 是否没有因为添加 `.can_apply_on_death true`，就错误改变对 DOT 击杀时点的理解？
