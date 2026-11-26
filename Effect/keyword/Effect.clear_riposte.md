# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.clear_riposte
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔 `0` 或 `1`。
- 只有参数为 `1` 时才清除目标的反击；参数为 `0` 时等同于未填写该关键字。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.clear_riposte 1`：清除当前 Effect 目标的反击。
- `.clear_riposte 0`：不产生清除反击的效果。
# 作用范围
- 清除对象是当前 Effect 的最终目标。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 只对 Effect 形式建立的反击有效；对由 Buff 三要素建立的反击无效。
# 常见错误
- 将 `.clear_riposte 0` 当作会清除反击。
- 认为该字段可以清除由 Buff 三要素建立的反击。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2145`
```darkest
effect: .name clear_riposte_target .target "target" .chance 100% .clear_riposte 1 .on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2146`
```darkest
effect: .name clear_riposte_performer .target "performer" .chance 100% .clear_riposte 1 .on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 Effect：`DarkestDungeon\effects\base.effects.darkest:2145-2146`。
- 用户补充的 `.clear_riposte` 参数语义说明。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
