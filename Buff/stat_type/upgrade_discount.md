# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

upgrade_discount
# 分类
Buff `stat_type`
# 参数类型
固定字符串；配套 `amount` 为数值，`stat_sub_type` 为字符串。
# 参数约束
- `stat_sub_type` 可自由填写，但仍应使用稳定、可追踪的 ID。
- 可用 rule 分类仍应结合具体 stat_sub_type 和引擎上下文判断。
# 固定值 / 参数候选
- 无固定副类型候选。
# 语义
- 被称为【打折】类buff，因为其作用是在进行装备和技能升级时打折
## 存档数字 ID 与 amount 默认分类
- 存档 `stat_type` 数字 ID：`23`。
- `amount` 正值：增益；负值：减益；零值：减益。
- 这是默认增益/减益分类，不直接说明效果对游戏玩家有益或有害；Buff 型 DOT 的分类边界见[完整数字 ID 与 amount 分类表](../stat_type_amount_classification.md)。
# 作用范围
- `.buff_type upgrade_discount` 与 buffs.json 的 `"stat_type":"upgrade_discount"` 对应。
# 引擎行为（重要）
- 可用于制作自定义文本，因为此buff在使用并不实际存在的sub_type时，不会崩溃或弹出自定义子类型的错误，因此利用自定义sub_type实现自定义描述
  通常用于在文本不需要包含可变数值（可加算显示的数值）的自定义文本时使用它（不可变数值直接固化写进文本词条本身里）
  由于此类buff在显示时会自动根据amount的正负在文本前端添加正负号（举例打八折的是-80%即文本自带了会造成干扰的负号），
  因此如果需要显示浮动可变数值，则请不要使用这个buff，而是使用quirk_tag_evolution_duration制作自定义文本
- 这是常见的自定义 Buff 描述方案：通过 `stat_sub_type` 拼接 `buff_stat_tooltip_upgrade_discount_<自定义后缀>`，实际本地化对象是该副类型对应的 ID，而不是 Buff 的主 ID。社区习惯上常让自定义 Buff ID 与副类型后缀保持一致，便于追踪，但这只是命名约定。
- 若格式中使用 `%d` 等数值参数，显示值前可能自动带有负号；这会影响需要无符号数值的文本，但并不等于完全不能用于可叠加数值。文本本来需要负号时可以直接利用；也可以人工额外书写两个负号，把显示效果当作破折号使用。具体组合细节待补充。
- 副本中英雄／怪物 Buff 栏详情，仅在 Buff 原本能合并的前提下：本类型不携带附魔时纯文本和计数文本均可合并；文本 Buff 自身携带附魔时不合并。暴击源可与技能源合并且覆盖其普通图标，事件源与技能源不合并；不以原本图标相同为前提，特殊源内部规则本次未测。暂按所有附魔类型处理，未逐类确认；其他界面不作结论。需逐条显示时可直接在附魔 Buff 上写文本。九封2026-11-17报告及知识库编写者长期使用确认，见 Mechanics/16-loc与loc2本地化覆盖优先级.md 与 Sources/buff_tooltip_merge_20261117.json。
- 2026-11-17具名技能消费者：upgrade_discount正文在格式化后保留127字节，再追加SPACE；现代Buff／Effect自定义项255，模式汇总255，公共及最终511。历史128／256口径不再作跨消费者硬上限，饰品与Buff栏未由该研究重测。
- 按消费者保留UTF-8字节计，颜色头9、尾4，源CRLF2、原生LF1；数值展开后计数，%%仅实际格式化为单%时计1。upgrade_discount具名样本为round(-100*amount)，不能推广全部格式参数。
- 完整实机、隔离执行、条件推导和配方范围见Mechanics/100-技能描述容量拼接排版与面板战斗可见性.md及Sources/skill_tooltip_research_20261117.json。
- Rule 不可能直接控制这条自定义文本是否显示；Rule 只影响 Buff/Effect 的实际生效或生命周期，不能把 Rule 结果当作本地化显示开关。需要条件化文本时，必须通过不同 Buff/Effect 的存在与清理等间接路径实现。
- Buff承载的技能自定义文本须保留描述显示；这不适用于新版Effect自身.description_tooltip_id，后者即使Effect.has_description false仍显示。实际挂载且不需进入技能描述的Buff可按用途隐藏。
- 不要仅为隐藏自动描述而把有明显玩家可读意义的普通 Buff 默认写成 `has_description: false`；本方案属于有明确自定义文本引用时的例外设计。
# 常见错误
- 百分比型 amount 忘记使用小数（例如 30% 常写作 `0.3`）。
- 固定加减与倍率乘除顺序不同，极端负值可能出现反向增长等异常结果。
- `stat_sub_type` 缺失、误拼或错误地填写了不属于该主类型的值。
# 代码案例
```json
{"stat_type":"upgrade_discount","stat_sub_type":"","amount":0.1}
```

# 来源与可信度
- 当前知识库的结构化字段表：主类型及主副类型关系。
- `Sources/buff_stat_type_amount_classification.tsv`：存档主类型数字 ID 与 amount 正、负、零的默认增益/减益分类；Buff 型 DOT 不归入这两类。
- 主术语表 `Buff Types`：社区语义、运算与边界备注。
