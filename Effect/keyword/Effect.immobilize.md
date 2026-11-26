# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.immobilize
# 分类
扩展/专项字段
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 只把本条记录的时序结论用于 `.pull` / `.push`；不要外推到扰乱。
- 死亡和召唤造成的位置变化是否属于本字段阻止范围之外，现有资料记为无视定身。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- 合法参数为 `0`、`1`（数字布尔）；`1` 表示定身，阻止目标位置变化，包括官方移动按钮等常规移动方式，但不是禁用位移技能本身。
- 定身状态不写入存档；重新读档后会消失。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 与 `.pull` / `.push` 处于同一时序时，定身无视文本顺序优先于推拉；若需要先推拉后定身，必须使用不同大时序。
- 定身阻止推拉会触发相邻单位被错误推拉的目标错乱 Bug；该结论不外推到扰乱。
- 详见：[Mechanics/04-queue与AWR.md](../../Mechanics/04-queue与AWR.md)
- 与 `.pull` / `.push` 同层时，无论文本顺序，定身都先于推拉。
- 定身阻止推拉时会发生目标错乱：击退错向目标后方相邻单位，拉前错向目标前方相邻单位；相邻单位无法继续移动时表现为无事发生。
- 死亡和召唤造成的位置变化无视定身的阻止效果。
- 详见：[queue、AWR 与暴击特效时序](../../Mechanics/04-queue与AWR.md)。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2078`
```darkest
effect: .name "immobilize" .target "target" .chance 100% .immobilize 1 .on_hit true .on_miss false	.queue true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:104`
```darkest
effect: .name "Scarecrow Immobilize" .target "target" .chance 100% .immobilize 1 .duration 2 .on_hit true .on_miss false	.queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
