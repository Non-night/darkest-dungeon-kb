# `combat_skill:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄特有。
- **用途**：定义英雄主动战斗技能。
- **官方实例分布**：英雄 8285 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.id` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 技能代码名 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.dmg` | 一个数字；支持整数、小数、百分号 | 英雄特有。 | 英雄技能的基础伤害修正：一个数字，可写小数或百分号。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.atk` | 一个数字，支持小数及百分号 | 英雄特有。 | 精准修正(一个数字，支持小数及百分号) | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.def` | 一个数字，支持小数及百分号 | 英雄特有。 | 闪避修正(一个数字，支持小数及百分号) | 静态合法字段表、Oni 术语表 |
| `.move` | 两个数字；参数至多 2 个 | 英雄特有。 | 技能造成的施术者自身位移，参数为后退量、前进量；不进行位移抗性判定。官方移动技能中可表示可选位移范围。知识库编写者于2026-10-22确认：第一次伤害结算（Buff、防御等，不含易伤）→技能.move自带位移→AWR→第二次伤害结算（计算易伤并应用最终伤害）。一号位时+50%伤害的英雄使用后退1的攻击技能，本次攻击仍享受该加成。两次结算为描述术语，不套用Effect推拉时序；不外推到反击、友方技能或非技能调用。详见 Mechanics/04-queue与AWR.md。 | 静态合法字段表、时序与站位伤害例子：知识库编写者2026-10-22明确确认；非原版代码阶段命名、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.crit` | 一个数字，支持小数及百分号 | 英雄特有。 | 暴击修正(一个数字，支持小数及百分号) | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.level` | 一个数字 | 按 Header 区分；`riposte_skill:` 的官方英雄与怪物实例均可出现 | 英雄技能等级。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.type` | 固定候选：`melee`、`ranged`、`move`、`teleport`；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 英雄技能类型。合法值为 melee、ranged、move、teleport。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.starting_cooldown` | 一个整数；仅怪物侧行为有资料支持 | 怪物技能特有 | 战斗开始时的技能冷却剩余回合（只对怪物侧有用） | 静态合法字段表、Oni 术语表 |
| `.per_battle_limit` | 一个数字 | 英雄特有。 | 每场战斗限制使用次数 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.per_turn_limit` | 一个数字 | 英雄特有。 | 每回合限制使用次数 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.is_continue_turn` | 布尔值：`true` 或 `false` | 英雄特有。 | 使用技能后继续行动（不结束回合）；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.launch` | 支持‘~’及数字 | 英雄特有。 | 人物技能释放站位 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.target` | 支持‘~’，‘@’，‘？’及数字 | 英雄特有。 | 英雄技能目标站位。完全不写该字段或参数为空时，技能必定成为指向英雄自身的友方技能；参数带 `@` 时指向友方。使用无等级共用分行且目标不为自身时，每个等级第一条定义必须写非空.target；同等级后续行或无等级行不能补救首行缺失。其余分行无须重复填写；下方无等级行可覆盖已建立的目标站位。友方技能无论怎样填写 `.is_stall_invalidating` 都无法阻止增援。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.self_target_valid` | 布尔值：`true` 或 `false` | 英雄特有。 | 友方目标技能是否允许选择施术者自身。true：允许；false：不允许。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.extra_targets_chance` | 一个数字，支持小数及百分号 | 怪物技能特有 | 怪物技能的额外目标概率；必须与 `.extra_targets_count` 同时存在。 | 静态合法字段表、Oni 术语表 |
| `.extra_targets_count` | 一个数字 | 怪物技能特有 | 怪物技能的额外目标数量；必须与 `.extra_targets_chance` 同时存在。 | 静态合法字段表、Oni 术语表 |
| `.is_crit_valid` | 布尔值：`true` 或 `false` | 英雄特有。 | 控制技能直伤是否允许暴击。`true`：允许；`false`：不允许。当前用户测试确认友方技能不可暴击，至少不会获得暴击带来的20% Effect概率加成；不能将该字段或技能暴击与治疗暴击混同。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.effect` | 后跟最多8个effect id，每个不超过64个字符；字符串参数至多 8 个；每个至多 64 字符 | 英雄特有。 | 技能公共 Effect 列表，不区分模式。单个字段至多 8 个 Effect ID，每个不超过 64 字符；模式专用 Effect 使用动态的 `.<mode_id>_effects`。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.valid_modes` | 后跟最多4个valid_mode id，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 英雄特有。 | 允许该技能在哪个模式使用，全模式使用就全写 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.ignore_stealth` | 布尔值：`true` 或 `false` | 英雄特有。 | 无视潜行；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.ignore_guard` | 布尔值：`true` 或 `false` | 英雄特有。 | 无视守护；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.can_miss` | 布尔值：`true` 或 `false` | 英雄特有。 | 技能是否可以被闪避（false则为必中）；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.can_be_riposted` | 布尔值：`true` 或 `false` | 英雄特有。 | 控制技能能否被反击。`true`：可以被反击；`false`：不可被反击，即无视反击。 | 静态合法字段表、Oni 术语表 |
| `.ignore_protection` | 布尔值：`true` 或 `false` | 英雄特有。 | 完全穿甲；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.required_performer_hp_range` | 两个数字，支持小数及百分号；参数至多 2 个 | 英雄特有。 | 当前生命值在某个范围内才可以使用这个技能 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.rank_damage_modifiers` | 最多四个数字，支持小数；参数至多 4 个 | 英雄特有。 | 按目标所在站位追加技能伤害修正。四个参数依次对应目标的 4、3、2、1 号位，而不是 1、2、3、4 号位；命中的目标处于哪个站位，就读取对应位置的参数，并与技能 `.dmg` 伤害修正加算。例如参数为 `0 -0.1 0.1 -0.05` 时，目标位于 2 号位会额外获得 `+10%` 伤害修正。该字段的数值不会自动显示在技能描述中，需要设计者自行决定是否补充可见说明。 | 静态合法字段表、Oni 术语表 |
| `.heal` | 两个数字；参数至多 2 个 | 英雄特有。 | 治疗 （最小值 最大值） | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.can_crit_heal` | 布尔值：`true` 或 `false` | 英雄特有。 | 治疗可以暴击，不写默认可暴击（true）；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.generation_guaranteed` | 布尔值：`true` 或 `false` | 英雄技能特有 | 保证英雄生成时携带该技能。该字段最多只能有效作用于一个技能；若多个技能都写 `.generation_guaranteed true`，应该只有书写顺序中的第一个生效。该必带技能不计入 `generation:` 的 `.number_of_random_combat_skills` 随机技能数量。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.is_user_selected_targets` | 布尔值：`true` 或 `false` | 怪物技能特有 | 目标可以选择技能承受者（参考老祖的回归造物主技能）；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.is_knowledgeable` | 布尔值：`true` 或 `false` | 怪物技能特有 | 是否可被玩家知晓怪物技能(玩家见过怪物技能第一次被使用后，是否显示该技能名称在怪物面板上)；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.is_monster_rerank_valid_on_attack` | 布尔值：`true` 或 `false` | 怪物技能特有 | 攻击时怪物重新排列有效？；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.is_monster_rerank_valid_on_friendly_presentation_end` | 布尔值：`true` 或 `false` | 怪物技能特有 | 友方技能结束时怪物重新排序有效？；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.is_monster_rerank_valid_on_friendly_post_result` | 布尔值：`true` 或 `false` | 怪物技能特有 | 友方技能判定结果时怪物重新排序有效？；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.is_stall_invalidating` | 布尔值：`true` 或 `false` | 英雄侧技能特有；不得用于怪物技能 | 控制英雄攻击技能是否能计入防增援次数，不要求技能造成伤害。该字段是英雄侧特有，默认值为 `true`；省略等同于写 `true`。写 `false` 时不能拖延增援。友方技能是例外：无论写 `true`、写 `false` 或省略该字段，都无法阻止增援。英雄 `combat_skill:` 未写有效 `.target` 时指向自身，`.target` 带 `@` 时指向友方，这两类友方技能都不因本字段改变增援结果。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.refresh_after_each_wave` | 布尔值：`true` 或 `false` | 英雄特有。 | 每波后刷新（农场无尽本的波次）；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.damage_heal_base_class_ids` | 后跟最多4个字符串 ID，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 英雄特有。 | 启用真吸血并列出获得回复的英雄或怪物 base class ID。基础回复等于最终直伤跳字，计算过量伤害和尸体直伤，不计算技能附带真伤；多个 ID 可同时回血。相同真吸血代码重复分行会导致翻倍，按每个技能等级最终合并后的定义避免重复；可各等级分别写一次，正确的无等级共用分行则共用部分整体写一次，不要两处重复。依据第88条P1422及当前用户2026-11-04确认，非本轮实机测试。AOE 合并方式尚未确认。 | 静态合法字段表、Oni 术语表 |
| `.ignore_deathsdoor` | 布尔值：`true` 或 `false` | 怪物技能特有 | 怪物技能是否跳过英雄死门判定。`true`：跳过；`false`：不跳过。 | 静态合法字段表、Oni 术语表 |
| `.icon` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 技能图标标识。值 `one` 通常对应职业根目录 `<hero_id>.ability.one.png`；`two` 等同理。`generic_move` 是通用移动图标。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.anim` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 填写基础动画名，不是 `.skel/.atlas/.png` 文件名。Skeleton 可提供 `<动画名>_<mode_id>` 作为模式专用变体，调用时仍只写基础动画名；无模式后缀的基础动画可由多个模式共用。三大基础动画 `idle`、`combat`、`walk` 无需在 Art 中指定，名称与资源路径正确时由游戏自动识别。完整边界见 Mechanics/33-英雄美术资源部署与识别边界.md。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.fx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 引用施术者侧 FX Skeleton 内部的动画名，不是资源文件名。职业自定义资源通常位于 `heroes/<hero_id>/fx/<hero_id>.sprite.<中缀>.*`。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.targfx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 命中时在目标 `fxskill` 锚点播放指定 FX 动画名；优先查职业 fx，也可引用游戏提供的全局共用 FX。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.targheadfx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 命中时目标身上出现的特效，特效的起点为目标的fxhead骨骼处 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.targchestfx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 命中时在目标 `fxchest` 锚点播放指定 FX 动画名；`blood_splatter`、`mark_target` 等可来自游戏全局共用 FX。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.misstargfx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 未命中时在目标 `fxskill` 锚点播放指定 FX 动画名。 | 静态合法字段表、Oni 术语表 |
| `.misstargheadfx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 未命中时目标身上出现的特效，特效的起点为目标的fxhead骨骼处 | 静态合法字段表、Oni 术语表 |
| `.misstargchestfx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 未命中时在目标 `fxchest` 锚点播放指定 FX 动画名。 | 静态合法字段表、Oni 术语表 |
| `.area_pos_offset` | 两个数字，支持小数；参数至多 2 个 | 英雄特有。 | 用于调整该技能演出动画的位置偏移。当前只确认它影响演出，不改变技能的实际启动站位、目标合法性或结算逻辑；两个数值各自对应的轴、正负方向、单位尺度，以及它偏移的准确演出对象，目前均未知。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.target_area_pos_offset` | 两个数字，支持小数；参数至多 2 个 | 英雄特有。 | 用于调整目标一侧的技能演出位置偏移。当前只能确认它属于目标侧演出偏移；究竟偏移目标单位自身、目标区域、目标身上的动画或目标胸口 FX，两个数值对应的坐标轴、正负方向和单位尺度，均尚不明确。不得把它解释为改变实际目标站位、可选范围或结算对象。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.reset_source_stance` | 布尔值：`true` 或 `false` | 英雄特有。 | 释放技能后自身还原成战斗形态，不写默认为true；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.reset_target_stance` | 布尔值：`true` 或 `false` | 英雄特有。 | 释放技能后目标还原成战斗形态，不写默认为true；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.can_display_selection` | 布尔值：`true` 或 `false` | 英雄特有。 | 是否显示目标选取光标；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.hide_performer_health` | 布尔值：`true` 或 `false` | 英雄特有。 | 是否隐藏自身血量；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.condensed_tooltip_effects` | 布尔值：`true` 或 `false` | 英雄特有。 | 2026-11-17字段函数证据：true写内部N=8，false／省略不清零旧N；显式per_line后应用可覆盖。type和stats为独立布尔。折叠按展开描述项、共享计数和分类重排，不保证减少字节；详见技能描述专题第8节，不据此概括所有Info/Art合并。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.condensed_tooltip_stats` | 布尔值：`true` 或 `false` | 英雄特有。 | 折叠技能描述的stats描述部分（基础精准 伤害修正 暴击修正等）；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.condensed_tooltip_type` | 布尔值：`true` 或 `false` | 英雄特有。 | 折叠技能描述的type描述部分（近战 远程）；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.condensed_tooltip_effects_per_line` | 一个数字 | 英雄特有。 | 2026-11-17技能消费者研究：本字段独立设置每行项数N，后应用会覆盖effects true写入的8，无须额外依赖true。N=0用LF并可用Buff增益／减益专用桶；N非零改普通分类，按展开描述项共用计数器，非每N个Effect或最终物理行硬上限。追加非空桶才计数，N倍数用LF，其余用SPACE/SPACE。负数可写入不等于推荐，异常值安全性未保证；完整分类、39桶重排及公式见Mechanics/100-技能描述容量拼接排版与面板战斗可见性.md第8节。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.nil` | 布尔值：`true` 或 `false` | 英雄特有。 | 隐藏技能统计数据（基础精准 伤害修正 暴击修正）和每次战斗使用的东西，比如前进后退等；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.custom_target_anim` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 强制目标播放指定名称的动画。 | 静态合法字段表、Oni 术语表 |
| `.has_crit_vo` | 布尔值：`true` 或 `false` | 英雄特有。 | 疑似控制暴击时的特殊旁白。`true`：启用；`false`：不启用；具体旁白行为尚未完全确认。 | 静态合法字段表、Oni 术语表 |
| `.custom_idle_anim_name` | 当前资料仅确认字段可写，参数类型/范围尚未整理 | 资料未证明绝对专用；官方当前仅怪物技能有实例 | 宫廷BOSS男爵使用该组参数进行动画模型的临时变身 | 静态合法字段表、Oni 术语表 |
| `.custom_idle_round_duration` | 当前资料仅确认字段可写，参数类型/范围尚未整理 | 资料未证明绝对专用；官方当前仅怪物技能有实例 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、Oni 术语表 |
| `.can_display_skill_name` | 布尔值：`true` 或 `false` | 怪物技能特有 | 是否显示技能名称（怪物侧）；布尔取值：`true` 启用上述行为，`false` 不启用上述行为。 | 静态合法字段表、Oni 术语表 |
| `.can_display_performer_selection_after_turn` | 布尔值：`true` 或 `false` | 英雄特有。 | 控制行动结束后是否保留施术者选择光标。`true`：保留；`false`：不保留。友方技能通常写 `false`，用于避免行动结束后残留选择光标。 | 静态合法字段表、Oni 术语表、游戏本体/官方 DLC 实例 |
| `.requires_burning` | 布尔值：`true` 或 `false` | 技能字段；官方当前仅英雄 `combat_skill:` 有实例，怪物侧行为尚未确认 | true：仅燃烧目标可被选中；false：不启用该燃烧目标限制。 | 静态合法字段表、Fire's Edge 无夜译注表、游戏本体/官方 DLC 实例 |
| `.dmg_per_burn_stack` | 一个浮点数 | 技能字段；官方当前仅英雄 `combat_skill:` 有实例，怪物侧行为尚未确认 | 目标每层燃烧增加对应比例伤害。例如 0.25 且目标有 10 层燃烧时，增加 250% 伤害。 | 静态合法字段表、Fire's Edge 无夜译注表、游戏本体/官方 DLC 实例 |
| `.copy_burn_behind` | 布尔值：`true` 或 `false` | 技能字段；官方当前仅英雄 `combat_skill:` 有实例，怪物侧行为尚未确认 | true：把目标后方单位一并加入攻击，将第一目标燃烧复制给第二目标，并清除第一目标燃烧；false：不启用。 | 静态合法字段表、Fire's Edge 无夜译注表、游戏本体/官方 DLC 实例 |
| `.ai_valid` | 布尔值：true 或 false；文档未说明省略默认值 | 英雄特有。 | false排除Act-Out与心控/魅惑调用。所有翻页技能及无限使用且不结束回合技能都应设置false。 | 新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json；新增字段，不冒称旧插件或官方实例已有 |
| `.counts_towards_skill_limit` | 布尔值：true 或 false；文档未说明省略默认值 | 英雄特有。 | false使该技能不占用英雄可装备技能数量上限。 | 新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json；新增字段，不冒称旧插件或官方实例已有 |
| `.skill_visible` | 布尔值：true 或 false；文档未说明省略默认值 | 英雄特有。 | false隐藏角色面板与升级菜单中的该技能，仅在战斗中可见。可用于特定状态下出现且无需升级的技能；需要升级效果时另行迂回。 | 新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json；新增字段，不冒称旧插件或官方实例已有 |
| `.force_selection` | 布尔值：true 或 false；文档未说明省略默认值 | 英雄特有。 | true使这一技能不能被取消装备；这是技能级装备选择锁定，不是强制点击某个战斗目标或强制本回合施放。 | 新版功能文档2026-11-05；Sources/modding_update_20261105_remaining.json；新增字段，不冒称旧插件或官方实例已有 |

## 动态模式 Effect 字段

当本行包含 `.valid_modes` 时，可为对应模式写：

```darkest
.<mode_id>_effects "effect_id_1" "effect_id_2"
```

- `<mode_id>` 必须对应本行 `.valid_modes` 中的模式 ID；必须存在这个同行可用模式定义时，该模式差分才会生效。
- 如果同行没有 `.valid_modes`，或 `.valid_modes` 不包含该 `<mode_id>`，则 `.<mode_id>_effects` 视为未写入／不产生该模式差分，不要只因字段语法看起来合法就认为它会生效。
- 每个动态字段至多引用 6 个 Effect ID，每个 ID 不超过 64 字符。
- 这是动态字段模板，不是字面量关键字 `.<mode_id>_effects`。

## 单位侧差异

- 设计稿若以 `●`／`○` 标记站位，英雄侧通常从左到右按 `4321` 换算，怪物侧通常从左到右按 `1234` 换算；因此英雄启动 `●●●○` 为 `.launch 432`，英雄攻击技能的敌方目标 `●●●○` 为 `.target 123`。怪物设计稿的圆点方向不固定，必须先向用户确认。完整说明见 `Mechanics/20-站位参数表达式.md`。
- `.dmg` 必须按技能 Header 与单位侧解释，不能统一成一种参数格式。
- `.level` 不能绝对标为英雄专用：官方怪物 `riposte_skill:` 存在 `.level 0`。
- `.is_stall_invalidating` 是英雄侧特有字段；即使静态字段表将其列入怪物 `skill:` 文档，也不得用于怪物技能。默认值为 `true`，省略等同于 `true`；写 `false` 时不能拖延增援。友方技能无论写 `true`、写 `false` 或省略，都无法阻止增援。
- `.requires_burning`、`.dmg_per_burn_stack`、`.copy_burn_behind` 是 Fire's Edge 新技能字段；官方当前仅英雄 `combat_skill:` 有实例，怪物侧行为尚未确认。


## 友方目标与增援

- 最终没有有效 `.target`（完全不写或参数为空）时，该英雄技能必定指向英雄自身，并按友方技能处理。
- `.target` 参数带 `@` 时指向友方；例如 `@12` 表示友方一、二号位为可选范围，不等同于 AOE。
- 友方技能无论怎样填写 `.is_stall_invalidating` 都无法阻止增援。

完整说明见：[友方技能目标与增援判定](../../Mechanics/38-友方技能目标与增援判定.md)。

## 同 ID 分行与无等级共用分行

同一技能 ID 可以先按 `.level` 分别定义各等级，再在这些等级行下方书写不带 `.level` 的同 ID `combat_skill:`，把所有等级相同的字段追加到每个等级定义中。这种写法称为“无等级共用分行”。

- 共用行必须放在该技能所有等级行之后。知识库编写者2026-11-08确认：若写在所有有等级行之前，其中 `.effect` 必定不会发生；整行疑似视为未写，但其他字段是否也失效尚未确认。夹在等级行之间的行为本条未确认。来源：`Sources/skill_shared_line_order_20261108.json`。

- 同类单参数字段后写覆盖先写。
- `.effect` 等多值列表字段可以通过后续分行追加共用引用。
- `.target` 特殊：若目标不为自身，同一技能每个等级的第一条带 `.level` 的定义必须写参数非空的 `.target`；只在同等级后续分行或无等级共用行补写无效，会成为自身技能。其余分行不必重复写 `.target`；下方无等级行可用有效 `.target` 覆盖已建立的目标站位。来源：`Sources/skill_split_first_level_target_20261105.json`。
- `.target` 参数为空等同于未填写；须按每个等级分别核对第一条定义，不借用其他等级的首行目标。



`DarkestDungeon\dlc\4964110_fires_edge\features\runaway\heroes\runaway\runaway.info.darkest:43`

```darkest
combat_skill: .id "backdraft" .level 0 .type "ranged" .atk 95% .dmg -50% .crit 7% .launch 321 .target 12 .is_crit_valid True .ignore_guard true .requires_burning true .dmg_per_burn_stack 0.25 .copy_burn_behind true
```

## 官方实例

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.art.darkest:15`

```darkest
combat_skill: .id "aimed_shot" .icon "one" .anim "attack_rifle" .fx "aimed_shot" .targchestfx "aimed_shot_target" .area_pos_offset 100 0
```

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.info.darkest:13`

```darkest
combat_skill: .id "aimed_shot" .level 0 .type "ranged" .atk 95% .dmg 0% .crit 5% .launch 43 .target 234 .is_crit_valid True  .effect "Sniper Damage 1" .generation_guaranteed true
```

`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\heroes\duelist\duelist.info.darkest:20`

```darkest
combat_skill: .id "touche" .level 0 .type "melee" .atk 90%  .dmg 0% .crit 1% .move 1 0 .launch 4321 .target 12 .is_crit_valid True  .effect "Duelist Touche Buff 1" .valid_modes stance_defensive
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
