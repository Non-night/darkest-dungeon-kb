# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.max_hp_multiply
# 分类
Buff/战斗属性
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- 主术语表未提供独立语义。该字段来自已收录字段目录或配置实例，需结合原版证据或实机验证。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版扫描未找到直接实例；下方案例来自 Mod，只能证明社区内容存在这种写法，仍需实机验证。
- 新版生命反馈size-0必须添加battle_modifier: .ignore_hp_scale true；可50血启动、最大HP提高至100不回血后继续，无需极小HP稀释。0.99/0.01空Effect sentinel仍须保留。
- 详见：[Mechanics/28-spawn、生命反馈与size0执行链.md](../../Mechanics/28-spawn、生命反馈与size0执行链.md)
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- Mod「无夜的原版饰品重置」：`effects\TR_hidden_trinkets.effects.darkest:6`
```darkest
effect: .name "NONTR_torch_of_flesh_qs0_hp_1" .target performer .combat_stat_buff 1 .max_hp_multiply 499900% .on_hit true .on_miss true
```
- Mod「「素质极高的正道骑士（+老祖强化）」」：`effects\STRANGE.effects.darkest:2145`
```darkest
effect: .name "ripper_max_hp" .target "performer" .chance 100% .combat_stat_buff 1 .max_hp_multiply 25% .duration -1 .on_hit true .on_miss false
```
- Mod「The Disgraced Knight Boss」：`effects\K.effects.darkest:108`
```darkest
effect: .name "JK_MHP_Debuff_A"  .target "target" .chance 120% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .max_hp_multiply -0.20 .on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例回退：原版未找到该字段时，优先从 Workshop `262060` 选择 Mod 实例；Workshop 无实例时再从本地 `mods` 回退选择。
- 可信度原则：Mod 只确认该 Mod 如此书写；原版未提供直接实例，不能据此宣称为已验证的引擎规范。
