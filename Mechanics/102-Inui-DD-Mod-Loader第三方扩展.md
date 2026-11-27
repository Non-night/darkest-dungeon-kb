# Inui DD Mod Loader 第三方扩展

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

## 来源与适用范围

本区记录 InuiDame 的 Darkest Dungeon DLL Mod Loader 及其预制插件。条目按对应插件和版本适用。证据来自外部来源作者的发布说明与使用文档，本知识库未对这些运行时修复开展新增实机验证。

- [0.25 发布说明](https://github.com/InuiDame/Darkest-Dungeon-DLL-Mod-Loader/releases/tag/0.25)
- [预制功能说明固定快照](https://github.com/InuiDame/Darkest-Dungeon-DLL-Mod-Loader/blob/52e8e67856a4fb93cfda08f04b0f3de588785d57/%E9%A2%84%E5%88%B6%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E%20Built-in%20Features.txt)
- [加载器 README 固定快照](https://github.com/InuiDame/Darkest-Dungeon-DLL-Mod-Loader/blob/52e8e67856a4fb93cfda08f04b0f3de588785d57/README.md)

## 扩展语法与启用检测

| 预制插件 | 本知识库 Python 检查器适配的字段 |
|---|---|
| `buff_icon` | Buff 的字符串 `buff_icon`。 |
| `dd_immune` | 英雄或怪物 Info 的 `immune:`。Buff 的 `immune_kill`、`immune_control`、`immune_capture` 布尔字段。 |
| `custom_type_effects` | Buff 和饰品接受 `<type>_type_additional_effect_ids` 或 `<type>_type_additional_effects`，值为 Effect ID 字符串或其数组。实际触发还受该插件配置的 `blocked_types` 影响。 |
| `hero_level_cap` | 英雄 Info 的 `level_cap:`，支持裸整数、`.max`、`.cap`，插件把值夹到 1～20。 |

检查器逐项验证对应游戏进程已加载代理和预制插件 DLL，并检查本次启动的插件日志。只有该插件通过验证才启用对应字段规则。未能确认时沿用原版检查。具体日志判据与覆盖范围见 [检查器说明](../tools/local_mod_syntax_checker/README.md#inui-ddmodloader-扩展)。

## 0.25 英雄等级上限与配套资源

`hero_level_cap` 从英雄的 `heroes/<英雄>/<英雄>.info.darkest` 读取 `level_cap:`。部署说明称安装包提供 7～10 级的名册图标及中英称号。英雄详情页通过 `str_resolve_<等级>` 查找称号，使用 `.loc2` 的语言需要相应编译资源。等级、XP 和显示资源应分别核对。

文档说明安装器将 `campaign/roster/roster.variables.json` 的 `resolve_level_thresholds` 补到 8 项，末项 `60` 对应 7 级。插件可按最后一段经验步长继续外推，UI 可计算到的最高等级受阈值表长度限制。若 7 级以上面板显示仍有问题，同时检查阈值表和 `res<N>` 名册底图。修改职业配置后需要重启游戏。

## 0.25 等级上限与 max_resource_entries 兼容性

上游报告，大量 Mod 环境中调高 `shared/resource_manager.setup` 的 `max_resource_entries`，曾可能与旧实现的启动阶段 Mod 扫描冲突。典型表现是启动约一秒后闪退，`app.log` 停在 `Post-crash check saved timestamp`。0.25 将等级上限插件的扫描与补丁工作移到工作线程，据上游说明修复了此冲突。该修复属于 `hero_level_cap` 的版本变更。

## 0.25 实验性 SpineFix

SpineFix 处理当前 Sprite 的 Spine 2.1 `.skel`，支持 `attachment` 时间线切片显隐、`drawOrder` 时间线层级变更和按 slot 切换混合模式。部分资源的 `drawOrder` 效果仍可能与编辑器不同。slot 末尾 `additive` 字节的插件约定为 `0` 正常、`1` 加法、`2` 正片叠底、`3` 滤色。

配置位于游戏根目录的 `DDModLoader/cfg/SpineFix.cfg`，修改后需重启。`repair_timelines` 可设 `0` 关闭、`1` 修补（默认）、`2` 只记录差异。`blend_modes` 控制混合模式。上游说明 SpineFix 和 SpineCompat 使用同一渲染 Hook，两者不要同时安装。功能限于插件适配的游戏构建。
