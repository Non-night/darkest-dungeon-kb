# 暗黑地牢 Mod 制作知识库

这是给《暗黑地牢》初代 Mod 作者用的参考库。想知道某个字段怎么写、一个 Effect 会在什么时候结算，或者原版是怎么做的，都可以从这里查起。也可以让能读本地文件的 AI 先查资料，再帮你写或修改 Mod。

## 手动查资料

直接在 GitHub 上就能看。按专题查时序、概率和副本机制，可以从[机制目录](Mechanics/index.md)开始。已经知道字段名，就查 [Effect](Effect/index.md)、[Buff](Buff/buff_schema.md) 或 [Info / Art / Override](Info/index.md)。要对照原版数据，可以看[原版副本数值表](Reference/vanilla_raid_tables.md)和[特殊配队名称](Reference/vanilla_party_names.md)。仓库也附有 Inui 整理的代码表（`暗黑地牢代码整合版2026.11.11版.xlsx`）。

想跨专题搜索，在仓库首页点 **Code → Download ZIP**，解压整个目录，然后在解压后的仓库根目录打开终端。检索脚本需要 Python 3.10 或更新版本。

```powershell
python tools/kb_query.py --query "force_resist_type effect_chance"
python tools/kb_query.py --query "回合开始附魔和流血结算谁先"
```

可以输入字段名，也可以直接用中文问。结果会给出相关条目的位置，顺着路径看正文就能核对适用条件、例外和证据。

## 让 AI 帮你写 Mod

把解压后的知识库和你的 Mod 目录交给能访问本地文件的 AI。给它 Mod 路径、想实现的行为和允许修改的范围。下面这段可以直接复制，替换方括号里的内容。

```text
知识库在「[知识库目录]」，Mod 在「[Mod 目录]」。
我要实现「[效果、目标、触发时机和持续时间]」。
请先读知识库的 AGENT_USAGE.md，用 tools/kb_query.py 查相关机制，再打开命中的正文核对字段用法。
只修改这个 Mod 里与需求有关的部分。完成后跑静态检查，告诉我改了哪些文件、查到了哪些结论，以及哪些行为需要进游戏验证。
```

公开版没有附带可安装的 AI Skill。一次性任务直接用上面的提示即可。如果经常让 AI 写地牢 Mod，可以让你用的客户端根据 [AGENT_USAGE.md](AGENT_USAGE.md) 和[实现检查目录](Reference/agent_guides/index.md)创建自己的 Skill。把知识库路径、什么时候该查库、怎么调用检索脚本，以及改完怎么做静态检查写进去，再补上你自己的项目习惯。

也可以自己运行[静态检查器](tools/local_mod_syntax_checker/README.md)。把路径替换成你的 Mod 根目录即可。

```powershell
python tools/local_mod_syntax_checker/checker.py --root "D:/Mods/MyMod"
```

## 更新提示

检索脚本只在运行时顺便检查更新，默认每天最多联网检查一次。发现新版时只提示，保留你的本地文件。想关闭联网检查，在知识库根目录创建 `.kb-local/update-settings.json`，写入 `{"automatic_update_checks": false}`。
