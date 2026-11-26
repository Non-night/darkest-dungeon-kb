# JSON 与 Darkest 文件的 UTF-8 无 BOM 硬性要求

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


## 硬性规则

Darkest Dungeon Mod 中所有扩展名为 `*.json` 和 `*.darkest` 的文本配置文件，只要采用 UTF 编码保存，就必须统一保存为：

```text
UTF-8 without BOM
```

即 **UTF-8 无 BOM**。不得保存为 UTF-8 with BOM，也不得使用会主动写入 BOM 的 `utf-8-sig` 等输出方式。

这不是排版建议，而是文件可识别性的硬性要求。UTF-8 BOM 的字节序列为：

```text
EF BB BF
```

若该字节序列出现在文件开头，游戏可能无法正常识别首个 Header、首个 JSON 字段或整个文件，表现为内容仿佛“没写”、解析失败或其他异常。

## Agent 写文件要求

1. 新建任何 `*.json` 或 `*.darkest` 文件时，必须直接以 UTF-8 无 BOM 写入。
2. 修改已有 `*.json` 或 `*.darkest` 文件时，应检查文件开头是否带 BOM；若带有 BOM，保存结果时必须移除。
3. 不得因为编辑器界面只显示“UTF-8”，就假定文件一定无 BOM；应使用明确标为 `UTF-8 without BOM`、`UTF-8 无 BOM` 的保存模式，或检查文件开头字节。
4. Python 写入时使用 `encoding="utf-8"`，不得使用 `encoding="utf-8-sig"`。
5. 使用其他脚本或编辑器时，也必须确认其输出不会写入 BOM。尤其不能依赖不同 PowerShell 版本中可能不同的默认文本编码行为。
6. 只改变编码时不得顺带改变换行、缩进、字段顺序或其他无关内容；但只要目标 `*.json`／`*.darkest` 文件被创建或重写，最终文件就必须无 BOM。

## 生成前／交付前检查

- 所有新建或改写的 `*.json` 文件，开头是否不是 `EF BB BF`？
- 所有新建或改写的 `*.darkest` 文件，开头是否不是 `EF BB BF`？
- 写入 API 是否明确使用 UTF-8 无 BOM，而非依赖系统默认编码？
- 若游戏反馈文件首段、首行或整份配置仿佛未被读取，是否优先检查 BOM？
