# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.has_description
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 当前知识库收录下列 2 个固定候选值；生成代码时应优先使用这些原样值。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- 合法参数为 `true`、`false`（字符布尔）；不得改用 `0`/`1`。字段控制：允许effect显示描述，就是你在游戏里能不能看到这个效果的文字说明，不写默认为true
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1468`
```darkest
effect: .name "Clear Guard Target" .target "target" .chance 100% .clearguarding 1 .clearguarded 1 .on_hit true .on_miss true .has_description false
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:4`
```darkest
effect: .name "Clear Guard" .target "performer" .chance 100% .clearguard 1 .on_hit true .on_miss true .can_apply_on_death false .queue false .has_description false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:1470`
```darkest
effect: .name "Clear Guard Self" .target "performer" .chance 100% .clearguarding 1 .clearguarded 1 .on_hit true .on_miss true .has_description false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
