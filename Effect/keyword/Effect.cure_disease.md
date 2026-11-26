# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.cure_disease
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔 `0` 或 `1`；只有 `.cure_disease 1` 才有效。
- 当同一逻辑 Effect 中同时出现 `.cure_disease 1` 与 `.cure 1` 时，必须把 `.cure_disease 1` 写在前面。
- 每次对一个目标执行 `.cure_disease 1` 时，从其现有疾病中随机治愈一种。疾病定义中的扎营移除、城镇活动治疗和顶替限制均拦不住该 Effect，血病（猩红诅咒）也可被抽中并治愈。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.cure_disease 1`：治愈目标的疾病。
- `.cure_disease 0`：无效。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版扫描未找到直接实例；下方案例来自 Mod，只能证明社区内容存在这种写法，仍需实机验证。
- 只有 `.cure_disease 1` 有效；与 `.cure 1` 同一逻辑 Effect 时必须先写它。
- 详见：[Mechanics/19-Effect性质不够确定.md](../../Mechanics/19-Effect性质不够确定.md)
- 单独出现且写为 `0` 时一定无效。
- 与 `.cure` 同时出现时的顺序要求已知，但该要求是否跨越同名分行或同一 Header 内换行保持不变，当前未确认。
- 疾病抽选的权重未知。迂回表第123条 P1882–P1883/X2415–X2416 记录了单病上限及绕过疾病防移除限制的行为。知识库编写者于 2026-11-24 补充为随机单病，并明确疾病定义参数无法拦截本字段。扎营技能 `remove_disease` 与疗养院分别使用自己的治疗规则。
# 常见错误
- 在 `.cure_disease 1` 之后写 `.cure 1`。
- 将 `.cure_disease 0` 当作会治愈疾病。
# 代码案例
- Mod「Farmstead Plus」：`effects\farmPlus.effects.darkest:161`
```darkest
effect: .name "trinket_cure_disease" .target "target" .chance 10%  .cure_disease 1	.on_hit true .on_miss false
```
- Mod「「芙洛丝」Floss Class」：`effects\Floss.effects.darkest:36`
```darkest
effect: .name "Floss_2" .target "performer" .item 1 .chance 100% .cure_disease 1 .on_hit true .on_miss true .queue true
```
- Mod「[小钟] Cimbalillo」：`effects\cimbalillo.effects.darkest:28`
```darkest
effect: .name "cimbalillo_loot1" .target "target" .chance 9000% .cure_disease 1 .healstress 5 .on_hit true .on_miss true .queue false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例回退：原版未找到该字段时，优先从 Workshop `262060` 选择 Mod 实例；Workshop 无实例时再从本地 `mods` 回退选择。
- 知识库编写者补充的 `.cure_disease` 参数、生效条件及与 `.cure` 的顺序说明。
- 迂回表第123条 P1882–P1883/X2415–X2416 及知识库编写者于 2026-11-24 补充的随机单病与防移除说明。
- 可信度原则：Mod 只确认该 Mod 如此书写；原版未提供直接实例，不能据此宣称为已验证的引擎规范。
