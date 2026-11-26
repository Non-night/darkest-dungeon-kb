# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.requires_not_burning_target
# 分类
扩展/专项字段
# 参数类型
字符布尔（合法值：`true`、`false`）
# 参数约束
- 参数类型为字符布尔；使用 `true` 或 `false`。
# 固定值 / 参数候选
- `false`
- `true`
# 语义
- 参数为 `true` 时，该 Effect 仅能对未处于燃烧状态的目标生效。
- 参数为 `false` 时，不启用上述非燃烧目标条件。
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 游戏本体、官方 DLC、本地 mods 与 Workshop 262060 均未找到直接 effect 定义实例。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 游戏本体、官方 DLC、Workshop `262060` 与本地 `mods` 中均未检索到可直接引用的 `effect:` 定义实例。

# 来源与可信度
- Fire’s Edge Modding Features 无夜译注表。
- 可信度原则：当前未找到可直接引用的原版或已安装 Mod 实例，但该行为来自已收录专项资料，可按词条中的明确结论使用；不得自行扩展未说明的边界。
