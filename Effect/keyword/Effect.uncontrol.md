# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.uncontrol
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 当前知识库收录下列 2 个固定候选值；生成代码时应优先使用这些原样值。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- 合法参数为 `0`、`1`（数字布尔）；不得改用 `true`/`false`。字段控制：解除魅惑（也就是解除心控）
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版扫描未找到直接实例；下方案例来自 Mod，只能证明社区内容存在这种写法，仍需实机验证。
- 对被控制者使用，而非对控制者
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- Mod「浊心斯卡蒂--Skadi the corrupting heart」：`effects\red_sikadi.effects.darkest:156`
```darkest
effect: .name "uncontrol 1" .target "target" .chance 500% .uncontrol 1 .on_hit true .on_miss true
```
- Mod「「刻俄柏」Ceobe Class」：`effects\Ceobe.effects.darkest:91`
```darkest
effect: .name "Ceobe Uncontrol" .target "performer" .chance 10000% .uncontrol 1 .on_hit true .on_miss true .queue false .has_description false .apply_once true
```
- Mod「「森蚺」Eunectes Class」：`effects\Eunectes.effects.darkest:93`
```darkest
effect: .name "Eunectes Uncontrol" .target "performer" .chance 10000% .uncontrol 1 .on_hit true .on_miss true .queue false .has_description false .apply_once true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例回退：原版未找到该字段时，优先从 Workshop `262060` 选择 Mod 实例；Workshop 无实例时再从本地 `mods` 回退选择。
- 可信度原则：Mod 只确认该 Mod 如此书写；原版未提供直接实例，不能据此宣称为已验证的引擎规范。
