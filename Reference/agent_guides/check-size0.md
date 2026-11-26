# size0、行动与生命反馈

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


只在当前任务涉及本组时展开。若本页历史维护建议与现行专题或当前用户明确约束冲突，先核对适用范围；不要机械执行所有检查。

- queue/AWR 是否改变死亡、ActorDot、hp_reaction 的窗口？

- 是否有 size-0、回合外加动、最后一杀软锁风险？

- Size-0 首先是怪物，具有通用怪物性质；泛称“怪物”及描述通用怪物机制时必须包含 Size-0，只有明确记载的例外才可排除。怪物定义采用 `monsters\<大类ID>\<大类ID>_<差分>\<大类ID>_<差分>.info.darkest` 与同名前缀的 `.art.darkest`；差分后缀必须恰好一个字符，多字符后缀禁止。大写字母 `A`–`Z` 和数字 `0`–`9` 已确认可用；`@`、`#` 疑似可用但待确认。大类动画位于 `monsters\<大类ID>\anim\`。创建时严格遵循。

4a. 只要任务涉及生成、解释或修复 size-0，必须先读取 `Mechanics/05-size0召唤物.md`、`Mechanics/08-hp_reaction.md` 与 `Mechanics/28-spawn、生命反馈与size0执行链.md`，并默认采用 `size0Spawner` 模板：基础骨架；生命反馈size-0必须写 `.ignore_hp_scale true`，可50血启动→最大HP升到100且不回血→后续流程，保留0.99向下/0.01向上空Effect sentinel。不要只写一个自定义 size-0 骨架。

4a-asset. 生成 size-0 时还必须读取 `Mechanics/05-size0召唤物.md` 中的 `size0Spawner` Info/Art/动画资源模板；优先整体复制 `info.darkest`、`art.darkest` 和 `anim\` 下的 combat/defend `.skel/.atlas/.png` 资源，再统一替换 `monster_xxx` 占位符。不得只生成逻辑 Info 而遗漏 Art 或动画资源。

4a-tool. 若另外使用知识库编写者历史外部 Size0Spawner GUI 工具，只能把它视为资源/基础 Info-Art 生成工具；生成后必须额外检查生命反馈所需 `.ignore_hp_scale true`、50→100不回血的初始化、0.99/0.01 sentinel、死亡门和资源最小化，不能把工具输出直接当成完整 size0Spawner 逻辑。

4a-generator. 需要快速生成基础 size-0 模板时，优先在本机调用 `python tools\size0spawner_generator.py --name <id> --output <dir> --races A`；可先加 `--dry-run`。该工具只生成资源/基础 Info-Art 模板，不代替 size0Spawner 生命反馈和死亡门逻辑。

4a-audio-required. 只要生成或维护 size-0，必须检查并加入对应的 `*.narration.json` 空旁白屏蔽；原版通用召唤/死亡音效覆盖属于推荐项，若实际加入必须在回复中告知当前用户，除非当前用户已经明确要求该覆盖。

4a-class. 生成多个怪物或 size-0 小类时，优先复用同一个大类 ID，用 `_A` 至 `_Z` 或 `_0` 至 `_9` 差分；只有动画、Art、enemy_type 语义或加载兼容性不兼容时才新建大类。不要默认生成多个只有 `_A` 的大类。

4e. 设计 `spawn: .effects` 时，所有被引用的 Effect ID 按不超过 31 个字符检查；空格按当前用户实测计入、代码引号不计入但底层引号边界未知。优先使用短 ASCII ID，不要把技能 Effect 的名称长度规则套到 spawn。
