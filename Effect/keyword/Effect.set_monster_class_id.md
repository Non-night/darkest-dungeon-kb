# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.set_monster_class_id
# 分类
扩展/专项字段
# 参数类型
当前资料未限定完整值域；查阅参数说明和已收录案例
# 参数约束
- 当前资料未形成完整固定值域；应结合参数说明、原版实例和调用上下文填写。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `怪物 【小类id】`：俗称set变身，本质是将自己变化为另一个怪物了
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 术语边界：知识库中“set 变身”专指 `.set_monster_class_id` 或 `.set_monster_class_ids`；`.set_mode` 是模式切换，与 set 变身无关。
- 当前用户于2026-09-30补充：set 目标处于死而不僵状态时通常被阻断；但 set Effect 同时显式写 `.can_apply_on_death true .can_apply_on_corpse true` 可突破该限制，少任一项均不行。set 获准后，`.set_monster_class_reset_hp` 省略／false／0 会继承血量并继承死而不僵状态；显式 true/1 则重置为满血正常状态。治疗能否使继承而来的死而不僵状态解除仍未知。
- 知识库编写者2026-09-19补充：死亡且死而不僵的size-0对自身set会被阻断，类似此时不能有效召唤；此旧结论现限定为未同时显式写出两个放行字段的常规情况。普通spawn后续项继续不代表set可用。
- 连续set后的size-0绝大多数情况下无法被monster_type_count_min正常检测；黑圣物有生效个例但他人无法复刻，条件未知。不要升级为绝对失效或普遍可靠。
- 知识库编写者于2026-09-19补充：size-0 A 的 spawn 中 set 成 B 后，不启动 B 的 spawn，而继续 A 剩余的 spawn 列表；后续自身操作由 B 承接，生命反馈只使用 B 的 hp_reaction。
- spawn 列表延续不等于无条件继承生命/Buff；需核对 set_monster_class_reset_hp、set_monster_class_reset_buffs 及相关生命继承配置，未提供默认值或通用 DOT 继承规则。
- 社区迂回资料记录：同一怪物连续 set，从第二次起 spawn 对英雄跨侧 Buff 异常按同侧处理；另有 spawn 定向失效问题，其精确起始次数未单独确认。参见专题28的精确证据定位。
- 详见：[Mechanics/28-spawn、生命反馈与size0执行链.md](../../Mechanics/28-spawn、生命反馈与size0执行链.md)
- 除了与英雄侧共通的利用模式名改变模型的变身方式之外，怪物侧具有四种专属的变身方式：
  Death变身：死亡变身，即death class .monster_class_id，常用于亡语写法和多阶段BOSS，如先祖、沉睡者。
  Set变身：即.set_monster_class_id，常用于自身变化为相同size0的怪物，如女伯爵、邀请函的血裔怪物。
  shifter变身：即shape_shifter: .monster_class_ids，原版用于无形血肉。
  最后还有一种在art文件里使用.custom_idle_anim_name和.custom_idle_round_duration实现临时的模型改变，原版用于宫廷DLC男爵。
  
  上述方式中，
  Death变身最常见，可继承生命值，变身前后的size无限制，但变身后会有免疫AD的BUG
  Set变身不但可继承生命值，甚至可以继承增减益状态和AI冷却，但size只能不变或变小，无法变大
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:335`
```darkest
effect: .name "To Seed Red" .target "target" .chance 100% .set_monster_class_id seed_red_D .set_monster_class_reset_hp true .set_monster_class_reset_buffs false .on_hit true .on_miss true .queue true .apply_once true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:127`
```darkest
effect: .name "Syco Swap A" .target "performer" .chance 100% .set_monster_class_id sycophant_A .set_monster_class_reset_hp true .set_monster_class_reset_buffs true .on_hit true .on_miss true .queue true .apply_once true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:136`
```darkest
effect: .name "xform coccoon A" .target "target" .chance 100% .set_monster_class_id cocoon_A .set_monster_class_reset_hp true .set_monster_class_reset_buffs true .on_hit true .on_miss true .queue true .apply_once true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
