using System.Globalization;
using System.Text;
using System.Text.Json;

namespace BuffGrammarChecker.Core;

public sealed class BuffFileValidator
{
    private const string RequiredSuffix = ".buffs.json";

    private static readonly IReadOnlyDictionary<string, ExpectedValueType> BuffFields =
        new Dictionary<string, ExpectedValueType>(StringComparer.Ordinal)
        {
            ["id"] = ExpectedValueType.String,
            ["stat_type"] = ExpectedValueType.String,
            ["stat_sub_type"] = ExpectedValueType.String,
            ["amount"] = ExpectedValueType.Number,
            ["remove_if_not_active"] = ExpectedValueType.Boolean,
            ["rule_type"] = ExpectedValueType.String,
            ["is_false_rule"] = ExpectedValueType.Boolean,
            ["rule_data"] = ExpectedValueType.Object,
            ["duration"] = ExpectedValueType.Number,
            ["duration_type"] = ExpectedValueType.String,
            ["remove_on_battle_complete"] = ExpectedValueType.Boolean,
            ["is_clear_debuff_valid"] = ExpectedValueType.Boolean,
            ["fx"] = ExpectedValueType.String,
            ["has_description"] = ExpectedValueType.Boolean,
            ["description_tooltip_id"] = ExpectedValueType.String,
            ["attack_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["friendly_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["move_skill_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["attack_crit_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["melee_attack_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["ranged_attack_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["riposte_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["riposte_crit_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["on_dodge_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["was_hit_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["was_hit_all_heroes_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["was_hit_all_monsters_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["kill_performer_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["kill_all_heroes_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["kill_all_monsters_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["riposte_kill_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["was_killed_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["was_killed_all_heroes_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["was_killed_all_monsters_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["quest_start_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["combat_start_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["turn_start_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["turn_end_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["round_end_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["battle_finished_successfully_additional_effect_ids"] = ExpectedValueType.StringArray,
            ["suppress_apply_poptext"] = ExpectedValueType.Boolean,
            ["consume_on_rule_active"] = ExpectedValueType.Boolean,
            ["force_positive"] = ExpectedValueType.Boolean,
            ["force_negative"] = ExpectedValueType.Boolean,
            ["clear_buffs_on_rule_active"] = ExpectedValueType.StringArray
        };

    private static readonly string[] RequiredBuffFields =
    [
        "id",
        "stat_type",
        "stat_sub_type",
        "amount",
        "rule_type",
        "is_false_rule",
        "rule_data"
    ];

    private static readonly IReadOnlyDictionary<string, ExpectedValueType> RuleDataFields =
        new Dictionary<string, ExpectedValueType>(StringComparer.Ordinal)
        {
            ["float"] = ExpectedValueType.Number,
            ["string"] = ExpectedValueType.String
        };

    private static readonly IReadOnlySet<string> NeverEffectiveIssueCodes =
        new HashSet<string>(StringComparer.Ordinal)
        {
            "INVERTED_ALWAYS_RULE",
            "INVALID_RULE_STRING_VALUE",
            "INVALID_RULE_FLOAT_VALUE",
            "INVALID_STAT_SUB_TYPE",
            "MISSING_STAT_SUB_TYPE_VALUE",
            "UNEXPECTED_STAT_SUB_TYPE",
            "UNKNOWN_STAT_TYPE",
            "INVALID_RULE_TYPE",
            "NON_GENERAL_RULE_FOR_NON_COMBAT_EFFECT",
            "HAS_BUFF_INVALID_VALUE",
            "HAS_BUFF_UNMATCHABLE_VALUE"
        };

    public ValidationResult ValidateFile(string filePath)
    {
        var fileName = Path.GetFileName(filePath);
        if (!IsValidFileName(fileName))
        {
            return InvalidFileNameResult(fileName);
        }

        try
        {
            return ValidateText(fileName, File.ReadAllText(filePath));
        }
        catch (Exception exception) when (exception is IOException or UnauthorizedAccessException)
        {
            return new ValidationResult(fileName,
            [
                new ValidationIssue(
                    ValidationSeverity.Error,
                    "FILE_READ_ERROR",
                    $"无法读取文件：{exception.Message}")
            ], true, false);
        }
    }

    public ValidationResult ValidateText(string fileName, string json)
    {
        if (!IsValidFileName(fileName))
        {
            return InvalidFileNameResult(fileName);
        }

        var issues = new List<ValidationIssue>();
        JsonDocument document;
        try
        {
            document = JsonDocument.Parse(json, new JsonDocumentOptions
            {
                AllowTrailingCommas = false,
                CommentHandling = JsonCommentHandling.Disallow,
                MaxDepth = 128
            });
        }
        catch (JsonException exception)
        {
            var zeroBasedLine = checked((int)(exception.LineNumber ?? 0));
            var zeroBasedBytePosition = checked((int)(exception.BytePositionInLine ?? 0));
            issues.Add(new ValidationIssue(
                ValidationSeverity.Error,
                "INVALID_JSON",
                $"文件内容不是合法 JSON：{CleanJsonExceptionMessage(exception.Message)}",
                string.IsNullOrWhiteSpace(exception.Path) ? "$" : exception.Path!,
                zeroBasedLine + 1,
                GetCharacterColumn(json, zeroBasedLine, zeroBasedBytePosition)));
            return new ValidationResult(fileName, issues, true, false);
        }

        using (document)
        {
            var sourceMap = JsonSourceMap.Build(json);
            ValidateRoot(document.RootElement, sourceMap, issues);
            AttachBuffIdentities(document.RootElement, issues);
        }

        return new ValidationResult(fileName, issues, true, true);
    }


    private static void AttachBuffIdentities(JsonElement root, List<ValidationIssue> issues)
    {
        if (root.ValueKind != JsonValueKind.Object ||
            !root.TryGetProperty("buffs", out var buffs) ||
            buffs.ValueKind != JsonValueKind.Array)
        {
            return;
        }

        for (var issueIndex = 0; issueIndex < issues.Count; issueIndex++)
        {
            var issue = issues[issueIndex];
            if (!TryGetBuffIndex(issue.JsonPath, out var buffIndex) || buffIndex >= buffs.GetArrayLength())
            {
                continue;
            }

            var buff = buffs[buffIndex];
            string? buffId = null;
            if (buff.ValueKind == JsonValueKind.Object &&
                buff.TryGetProperty("id", out var idElement) &&
                idElement.ValueKind == JsonValueKind.String)
            {
                buffId = idElement.GetString();
            }

            issues[issueIndex] = issue with
            {
                BuffId = string.IsNullOrWhiteSpace(buffId) ? null : buffId,
                BuffIndex = buffIndex
            };
        }
    }

    private static bool TryGetBuffIndex(string jsonPath, out int buffIndex)
    {
        const string prefix = "$.buffs[";
        buffIndex = default;
        if (!jsonPath.StartsWith(prefix, StringComparison.Ordinal))
        {
            return false;
        }

        var closingBracket = jsonPath.IndexOf(']', prefix.Length);
        return closingBracket > prefix.Length &&
               int.TryParse(
                   jsonPath.AsSpan(prefix.Length, closingBracket - prefix.Length),
                   NumberStyles.None,
                   CultureInfo.InvariantCulture,
                   out buffIndex) &&
               buffIndex >= 0;
    }

    public static bool TryResolveIssueLocation(
        string json,
        ValidationIssue issue,
        out int line,
        out int column)
    {
        ArgumentNullException.ThrowIfNull(json);
        ArgumentNullException.ThrowIfNull(issue);
        line = 0;
        column = 0;

        if (json.Length == 0)
        {
            return false;
        }

        try
        {
            using var document = JsonDocument.Parse(json, new JsonDocumentOptions
            {
                AllowTrailingCommas = false,
                CommentHandling = JsonCommentHandling.Disallow,
                MaxDepth = 128
            });
            var sourceMap = JsonSourceMap.Build(json);
            var candidatePaths = new List<string>();

            if (TryFindCurrentBuffIndex(document.RootElement, issue, out var currentBuffIndex))
            {
                var pathWithinBuff = GetPathWithinBuff(issue.JsonPath);
                if (pathWithinBuff is not null)
                {
                    candidatePaths.Add($"$.buffs[{currentBuffIndex}]{pathWithinBuff}");
                }

                candidatePaths.Add($"$.buffs[{currentBuffIndex}].id");
                candidatePaths.Add($"$.buffs[{currentBuffIndex}]");
            }
            else if (string.IsNullOrWhiteSpace(issue.BuffId) || GetPathWithinBuff(issue.JsonPath) is null)
            {
                candidatePaths.Add(issue.JsonPath);
            }

            foreach (var candidatePath in candidatePaths.Distinct(StringComparer.Ordinal))
            {
                var (resolvedLine, resolvedColumn) = sourceMap.Find(candidatePath);
                if (resolvedLine is > 0 && resolvedColumn is > 0)
                {
                    line = resolvedLine.Value;
                    column = resolvedColumn.Value;
                    return true;
                }
            }
        }
        catch (JsonException)
        {
            // The user may be in the middle of an edit. Fall back to an ID/property text search below.
        }

        return TryResolveIssueLocationByText(json, issue, out line, out column);
    }

    private static bool TryFindCurrentBuffIndex(JsonElement root, ValidationIssue issue, out int buffIndex)
    {
        buffIndex = default;
        if (root.ValueKind != JsonValueKind.Object ||
            !root.TryGetProperty("buffs", out var buffs) ||
            buffs.ValueKind != JsonValueKind.Array)
        {
            return false;
        }

        if (issue.BuffIndex is >= 0 && issue.BuffIndex.Value < buffs.GetArrayLength())
        {
            var indexedBuff = buffs[issue.BuffIndex.Value];
            if (string.IsNullOrWhiteSpace(issue.BuffId) || BuffHasId(indexedBuff, issue.BuffId))
            {
                buffIndex = issue.BuffIndex.Value;
                return true;
            }
        }

        if (!string.IsNullOrWhiteSpace(issue.BuffId))
        {
            var index = 0;
            foreach (var buff in buffs.EnumerateArray())
            {
                if (BuffHasId(buff, issue.BuffId))
                {
                    buffIndex = index;
                    return true;
                }

                index++;
            }
        }

        // If the old diagnostic has a concrete Buff ID, never fall back to its previous array index.
        // A rename or deletion would otherwise send the caret to an unrelated buff after an edit.
        if (string.IsNullOrWhiteSpace(issue.BuffId) &&
            issue.BuffIndex is >= 0 && issue.BuffIndex.Value < buffs.GetArrayLength())
        {
            buffIndex = issue.BuffIndex.Value;
            return true;
        }

        return false;
    }

    private static bool BuffHasId(JsonElement buff, string expectedId) =>
        buff.ValueKind == JsonValueKind.Object &&
        buff.TryGetProperty("id", out var idElement) &&
        idElement.ValueKind == JsonValueKind.String &&
        string.Equals(idElement.GetString(), expectedId, StringComparison.Ordinal);

    private static string? GetPathWithinBuff(string jsonPath)
    {
        const string prefix = "$.buffs[";
        if (!jsonPath.StartsWith(prefix, StringComparison.Ordinal))
        {
            return null;
        }

        var closingBracket = jsonPath.IndexOf(']', prefix.Length);
        return closingBracket >= 0 ? jsonPath[(closingBracket + 1)..] : null;
    }

    private static bool TryResolveIssueLocationByText(
        string json,
        ValidationIssue issue,
        out int line,
        out int column)
    {
        line = 0;
        column = 0;
        if (string.IsNullOrWhiteSpace(issue.BuffId))
        {
            return false;
        }

        var idPropertyIndex = FindIdProperty(json, issue.BuffId, 0);
        if (idPropertyIndex < 0)
        {
            return false;
        }

        var targetIndex = idPropertyIndex;

        if (TryFindContainingObjectBounds(json, idPropertyIndex, out var objectStart, out var objectEnd) &&
            TryFindPathWithinObject(json, objectStart, objectEnd, GetPathWithinBuff(issue.JsonPath), out var pathIndex))
        {
            targetIndex = pathIndex;
        }

        GetLineAndColumn(json, targetIndex, out line, out column);
        return true;
    }

    private static int FindIdProperty(string json, string? expectedId, int startIndex)
    {
        var propertyIndex = Math.Max(0, startIndex);
        while ((propertyIndex = FindProperty(json, "id", propertyIndex, json.Length)) >= 0)
        {
            if (expectedId is null)
            {
                return propertyIndex;
            }

            var cursor = propertyIndex + 4;
            SkipWhitespace(json, ref cursor);
            if (cursor >= json.Length || json[cursor] != ':')
            {
                propertyIndex += 4;
                continue;
            }

            cursor++;
            SkipWhitespace(json, ref cursor);
            var serializedId = JsonSerializer.Serialize(expectedId);
            if (cursor + serializedId.Length <= json.Length &&
                json.AsSpan(cursor, serializedId.Length).SequenceEqual(serializedId.AsSpan()))
            {
                return propertyIndex;
            }

            propertyIndex += 4;
        }

        return -1;
    }

    private static bool TryFindContainingObjectBounds(string json, int characterIndex, out int objectStart, out int objectEnd)
    {
        objectStart = -1;
        objectEnd = -1;
        var objectStack = new Stack<int>();
        var inString = false;
        var escaped = false;
        var limit = Math.Clamp(characterIndex, 0, json.Length);

        for (var index = 0; index < limit; index++)
        {
            var character = json[index];
            if (inString)
            {
                if (escaped)
                {
                    escaped = false;
                }
                else if (character == '\\')
                {
                    escaped = true;
                }
                else if (character == '"')
                {
                    inString = false;
                }

                continue;
            }

            if (character == '"')
            {
                inString = true;
            }
            else if (character == '{')
            {
                objectStack.Push(index);
            }
            else if (character == '}' && objectStack.Count > 0)
            {
                objectStack.Pop();
            }
        }

        if (objectStack.Count == 0)
        {
            return false;
        }

        objectStart = objectStack.Peek();
        objectEnd = FindMatchingObjectEnd(json, objectStart);
        if (objectEnd < 0)
        {
            objectEnd = json.Length;
        }

        return true;
    }

    private static int FindMatchingObjectEnd(string json, int objectStart)
    {
        var depth = 0;
        var inString = false;
        var escaped = false;
        for (var index = objectStart; index < json.Length; index++)
        {
            var character = json[index];
            if (inString)
            {
                if (escaped)
                {
                    escaped = false;
                }
                else if (character == '\\')
                {
                    escaped = true;
                }
                else if (character == '"')
                {
                    inString = false;
                }

                continue;
            }

            if (character == '"')
            {
                inString = true;
            }
            else if (character == '{')
            {
                depth++;
            }
            else if (character == '}' && --depth == 0)
            {
                return index + 1;
            }
        }

        return -1;
    }

    private static bool TryFindPathWithinObject(
        string json,
        int objectStart,
        int objectEnd,
        string? pathWithinBuff,
        out int propertyIndex)
    {
        propertyIndex = -1;
        if (string.IsNullOrWhiteSpace(pathWithinBuff))
        {
            return false;
        }

        var properties = pathWithinBuff
            .Split('.', StringSplitOptions.RemoveEmptyEntries)
            .Select(segment =>
            {
                var arrayStart = segment.IndexOf('[');
                return arrayStart >= 0 ? segment[..arrayStart] : segment;
            })
            .Where(segment => segment.Length > 0)
            .ToArray();
        if (properties.Length == 0)
        {
            return false;
        }

        var searchStart = objectStart;
        var searchEnd = Math.Min(json.Length, objectEnd);
        for (var index = 0; index < properties.Length; index++)
        {
            propertyIndex = FindProperty(json, properties[index], searchStart, searchEnd);
            if (propertyIndex < 0)
            {
                return false;
            }

            if (index == properties.Length - 1)
            {
                return true;
            }

            var valueStart = propertyIndex + properties[index].Length + 2;
            SkipWhitespace(json, ref valueStart);
            if (valueStart >= searchEnd || json[valueStart] != ':')
            {
                return false;
            }

            valueStart++;
            SkipWhitespace(json, ref valueStart);
            if (valueStart >= searchEnd || json[valueStart] != '{')
            {
                return false;
            }

            var nestedEnd = FindMatchingObjectEnd(json, valueStart);
            searchStart = valueStart;
            searchEnd = nestedEnd > valueStart ? Math.Min(searchEnd, nestedEnd) : searchEnd;
        }

        return false;
    }

    private static int FindProperty(string json, string propertyName, int startIndex, int endIndex)
    {
        var token = $"\"{propertyName}\"";
        var index = Math.Max(0, startIndex);
        var limit = Math.Min(json.Length, endIndex);
        while (index < limit)
        {
            index = json.IndexOf(token, index, StringComparison.Ordinal);
            if (index < 0 || index >= limit)
            {
                return -1;
            }

            var cursor = index + token.Length;
            SkipWhitespace(json, ref cursor);
            if (cursor < limit && cursor < json.Length && json[cursor] == ':')
            {
                return index;
            }

            index += token.Length;
        }

        return -1;
    }

    private static void SkipWhitespace(string text, ref int index)
    {
        while (index < text.Length && char.IsWhiteSpace(text[index]))
        {
            index++;
        }
    }

    private static void GetLineAndColumn(string text, int characterIndex, out int line, out int column)
    {
        line = 1;
        column = 1;
        var limit = Math.Clamp(characterIndex, 0, text.Length);
        for (var index = 0; index < limit; index++)
        {
            if (text[index] == '\r')
            {
                if (index + 1 < limit && text[index + 1] == '\n')
                {
                    index++;
                }

                line++;
                column = 1;
            }
            else if (text[index] == '\n')
            {
                line++;
                column = 1;
            }
            else
            {
                if (char.IsHighSurrogate(text[index]) && index + 1 < limit && char.IsLowSurrogate(text[index + 1]))
                {
                    index++;
                }

                column++;
            }
        }
    }
    public static bool IsValidFileName(string? fileName)
    {
        if (string.IsNullOrWhiteSpace(fileName) || !fileName.EndsWith(RequiredSuffix, StringComparison.OrdinalIgnoreCase))
        {
            return false;
        }

        return fileName.Length > RequiredSuffix.Length;
    }

    private static ValidationResult InvalidFileNameResult(string fileName) =>
        new(fileName,
        [
            new ValidationIssue(
                ValidationSeverity.Error,
                "INVALID_FILE_NAME",
                $"文件名“{fileName}”不符合要求。文件名必须为 *.buffs.json，且 * 部分不能为空。")
        ], false, false);

    private static void ValidateRoot(JsonElement root, JsonSourceMap sourceMap, List<ValidationIssue> issues)
    {
        if (root.ValueKind != JsonValueKind.Object)
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "ROOT_NOT_OBJECT",
                "JSON 根节点必须是对象，整体结构应为 { \"buffs\": [] }。", "$", "$" );
            return;
        }

        var rootProperties = root.EnumerateObject().ToList();
        var validatedRootProperties = rootProperties.Where(property => !ContainsChineseCharacter(property.Name)).ToList();
        ReportDuplicateProperties(validatedRootProperties, "$", sourceMap, issues);

        foreach (var property in validatedRootProperties.Where(property => property.Name != "buffs"))
        {
            var path = JsonSourceMap.AppendProperty("$", property.Name);
            AddIssue(issues, sourceMap, ValidationSeverity.Warning, "UNKNOWN_ROOT_FIELD",
                $"根节点中存在不支持的字段“{property.Name}”；根节点只应包含 buffs。", path, path);
        }

        if (!root.TryGetProperty("buffs", out var buffs))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "MISSING_BUFFS",
                "根节点缺少必需字段“buffs”。", "$", "$");
            return;
        }

        if (buffs.ValueKind != JsonValueKind.Array)
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "BUFFS_NOT_ARRAY",
                "字段“buffs”的值必须是对象数组。", "$.buffs", "$.buffs");
            return;
        }

        var index = 0;
        foreach (var buff in buffs.EnumerateArray())
        {
            ValidateBuff(buff, index, sourceMap, issues);
            index++;
        }
    }

    private static void ValidateBuff(JsonElement buff, int index, JsonSourceMap sourceMap, List<ValidationIssue> issues)
    {
        var buffPath = $"$.buffs[{index}]";
        var issueStartIndex = issues.Count;
        if (buff.ValueKind != JsonValueKind.Object)
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "BUFF_NOT_OBJECT",
                $"buffs 数组中的第 {index + 1} 项必须是对象。", buffPath, buffPath);
            return;
        }

        var properties = buff.EnumerateObject().ToList();
        var validatedProperties = properties.Where(property => !ContainsChineseCharacter(property.Name)).ToList();
        ReportDuplicateProperties(validatedProperties, buffPath, sourceMap, issues);
        var propertyNames = validatedProperties.Select(property => property.Name).ToHashSet(StringComparer.Ordinal);

        foreach (var requiredField in RequiredBuffFields.Where(requiredField => !propertyNames.Contains(requiredField)))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "MISSING_REQUIRED_FIELD",
                $"第 {index + 1} 个 buff 缺少必需字段“{requiredField}”。", buffPath, buffPath);
        }

        foreach (var property in validatedProperties)
        {
            var propertyPath = JsonSourceMap.AppendProperty(buffPath, property.Name);
            if (!BuffFields.TryGetValue(property.Name, out var expectedType))
            {
                ReportUnknownField(property.Name, BuffFields.Keys, propertyPath, sourceMap, issues);
                continue;
            }

            ValidateValueType(property.Value, expectedType, property.Name, propertyPath, sourceMap, issues);
        }

        if (buff.TryGetProperty("rule_data", out var ruleData) && ruleData.ValueKind == JsonValueKind.Object)
        {
            ValidateRuleData(ruleData, buffPath, sourceMap, issues);
        }

        ValidateStatTypeRelation(buff, buffPath, sourceMap, issues);
        ValidateRuleType(buff, buffPath, sourceMap, issues);
        ValidateRuleSemantics(buff, buffPath, sourceMap, issues);
        ValidateSpecialBuffIdBehavior(buff, buffPath, sourceMap, issues);
        ValidateRuleCategoryCompatibility(buff, buffPath, sourceMap, issues);
        SuppressNeverEffectiveDiagnosticsForTooltipOnlyBuff(buff, issues, issueStartIndex);
    }

    private static void SuppressNeverEffectiveDiagnosticsForTooltipOnlyBuff(
        JsonElement buff,
        List<ValidationIssue> issues,
        int issueStartIndex)
    {
        if (!buff.TryGetProperty("description_tooltip_id", out var tooltipElement) ||
            tooltipElement.ValueKind != JsonValueKind.String ||
            !buff.TryGetProperty("remove_if_not_active", out var removeIfNotActiveElement) ||
            removeIfNotActiveElement.ValueKind != JsonValueKind.False)
        {
            return;
        }

        var hasNeverEffectiveDiagnostic = issues
            .Skip(issueStartIndex)
            .Any(issue => NeverEffectiveIssueCodes.Contains(issue.Code));
        if (!hasNeverEffectiveDiagnostic)
        {
            return;
        }

        for (var issueIndex = issues.Count - 1; issueIndex >= issueStartIndex; issueIndex--)
        {
            var issue = issues[issueIndex];
            if (issue.Severity is ValidationSeverity.Error or ValidationSeverity.Warning &&
                NeverEffectiveIssueCodes.Contains(issue.Code))
            {
                issues.RemoveAt(issueIndex);
            }
        }
    }

    private static void ValidateSpecialBuffIdBehavior(
        JsonElement buff,
        string buffPath,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        if (!buff.TryGetProperty("id", out var idElement) || idElement.ValueKind != JsonValueKind.String)
        {
            return;
        }

        var buffId = idElement.GetString() ?? string.Empty;
        var idPath = $"{buffPath}.id";

        if (buffId.StartsWith(BuffSpecialIdRules.ClearOnDodgePrefix, StringComparison.Ordinal))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Info, "SPECIAL_CLEAR_ON_DODGE_ID",
                $"特殊 Buff ID 前缀“{BuffSpecialIdRules.ClearOnDodgePrefix}”：该 buff 会在持有者闪避时被清除。前缀后的内容可作为编号或其他标识，不要求固定写成字面量 N。",
                idPath, idPath);
        }

        if (buffId.StartsWith(BuffSpecialIdRules.AttacksAnyLaunchRankPrefix, StringComparison.Ordinal))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Info, "SPECIAL_ANY_LAUNCH_RANK_ID",
                $"特殊 Buff ID 前缀“{BuffSpecialIdRules.AttacksAnyLaunchRankPrefix}”：持有者的所有技能将忽略启动站位限制；该特殊行为无视 rule_type 和 is_false_rule。",
                idPath, idPath);
        }

        if (buffId.StartsWith(BuffSpecialIdRules.AttacksAnyTargetRankPrefix, StringComparison.Ordinal))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Info, "SPECIAL_ANY_TARGET_RANK_ID",
                $"特殊 Buff ID 前缀“{BuffSpecialIdRules.AttacksAnyTargetRankPrefix}”：持有者的非 AoE 技能将忽略目标站位限制；该特殊行为无视 rule_type 和 is_false_rule，对 AoE 技能无效。",
                idPath, idPath);
        }
    }

    private static void ValidateRuleCategoryCompatibility(
        JsonElement buff,
        string buffPath,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        if (!buff.TryGetProperty("stat_type", out var statTypeElement) ||
            statTypeElement.ValueKind != JsonValueKind.String ||
            !buff.TryGetProperty("stat_sub_type", out var statSubTypeElement) ||
            statSubTypeElement.ValueKind != JsonValueKind.String ||
            !buff.TryGetProperty("rule_type", out var ruleTypeElement) ||
            ruleTypeElement.ValueKind != JsonValueKind.String)
        {
            return;
        }

        var statType = statTypeElement.GetString() ?? string.Empty;
        var statSubType = statSubTypeElement.GetString() ?? string.Empty;
        var ruleType = ruleTypeElement.GetString() ?? string.Empty;
        if (!BuffRuleTypeRules.TryGetCategory(ruleType, out var category) ||
            category == BuffRuleCategory.General ||
            (statSubType != "speed_rating" && !BuffRuleSemantics.GeneralRuleOnlyStatTypes.Contains(statType)))
        {
            return;
        }

        var effectName = statSubType == "speed_rating"
            ? "stat_sub_type“speed_rating”"
            : $"stat_type“{statType}”";
        var ruleTypePath = $"{buffPath}.rule_type";
        AddIssue(issues, sourceMap, ValidationSeverity.Error, "NON_GENERAL_RULE_FOR_NON_COMBAT_EFFECT",
            $"{effectName}不能使用{BuffRuleTypeRules.GetCategoryDisplayName(category)} rule“{ruleType}”。这些效果不能在战斗过程中发生/不能瞬时生效，因此 rule_type 必须是通用型（条件型）。",
            ruleTypePath, ruleTypePath);
    }

    private static void ValidateRuleType(
        JsonElement buff,
        string buffPath,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        if (!buff.TryGetProperty("rule_type", out var ruleTypeElement) ||
            ruleTypeElement.ValueKind != JsonValueKind.String)
        {
            return;
        }

        var ruleType = ruleTypeElement.GetString() ?? string.Empty;
        if (BuffRuleTypeRules.AllowedValueSet.Contains(ruleType))
        {
            return;
        }

        var path = $"{buffPath}.rule_type";
        var suggestion = FindClosestValue(ruleType, BuffRuleTypeRules.AllowedValues);
        var suggestionText = suggestion is null ? string.Empty : $" 是否应为“{suggestion}”？";
        AddIssue(issues, sourceMap, ValidationSeverity.Error, "INVALID_RULE_TYPE",
            $"rule_type“{ruleType}”不是允许的值。{suggestionText}允许的 {BuffRuleTypeRules.AllowedValues.Count} 个值：{string.Join("、", BuffRuleTypeRules.AllowedValues)}。",
            path, path);
    }
    private static void ValidateRuleSemantics(
        JsonElement buff,
        string buffPath,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        if (!buff.TryGetProperty("rule_type", out var ruleTypeElement) ||
            ruleTypeElement.ValueKind != JsonValueKind.String ||
            !buff.TryGetProperty("is_false_rule", out var isFalseRuleElement) ||
            isFalseRuleElement.ValueKind is not (JsonValueKind.True or JsonValueKind.False) ||
            !buff.TryGetProperty("rule_data", out var ruleDataElement) ||
            ruleDataElement.ValueKind != JsonValueKind.Object ||
            !ruleDataElement.TryGetProperty("float", out var floatElement) ||
            !TryGetFloat(floatElement, out var floatValue) ||
            !ruleDataElement.TryGetProperty("string", out var stringElement) ||
            stringElement.ValueKind != JsonValueKind.String)
        {
            return;
        }

        var ruleType = ruleTypeElement.GetString() ?? string.Empty;
        var isFalseRule = isFalseRuleElement.GetBoolean();
        var stringValue = stringElement.GetString() ?? string.Empty;
        var buffId = buff.TryGetProperty("id", out var idElement) && idElement.ValueKind == JsonValueKind.String
            ? idElement.GetString() ?? string.Empty
            : string.Empty;
        var ignoresRule = BuffSpecialIdRules.IgnoresRule(buffId);
        var falseRulePath = $"{buffPath}.is_false_rule";
        var floatPath = $"{buffPath}.rule_data.float";
        var stringPath = $"{buffPath}.rule_data.string";

        if (ruleType == "always" && isFalseRule && !ignoresRule)
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Warning, "INVERTED_ALWAYS_RULE",
                "该buff将始终无效", falseRulePath, falseRulePath);
        }

        if (!isFalseRule && ruleType is "actorStatus" or "is_actor_status" &&
            !BuffRuleSemantics.ActorStatuses.Contains(stringValue))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "INVALID_RULE_STRING_VALUE",
                $"rule_type“{ruleType}”未取反时，rule_data.string 必须是 {string.Join("、", BuffRuleSemantics.ActorStatuses)} 之一，否则该 buff 将无效。",
                stringPath, stringPath);
        }

        if (ruleType == "has_buff")
        {
            if (!BuffStatTypeRules.ValidStatTypes.Contains(stringValue))
            {
                var suggestion = FindClosestValue(stringValue, BuffStatTypeRules.ValidStatTypes);
                var suggestionText = suggestion is null ? string.Empty : $" 是否应为“{suggestion}”？";
                AddIssue(issues, sourceMap, ValidationSeverity.Warning, "HAS_BUFF_INVALID_VALUE",
                    $"rule_type“has_buff”的 rule_data.string“{stringValue}”不是合法的 buff 主类型。{suggestionText}",
                    stringPath, stringPath);
            }
            else if (BuffStatTypeRules.CanSpecifySubType(stringValue))
            {
                AddIssue(issues, sourceMap, ValidationSeverity.Warning, "HAS_BUFF_UNMATCHABLE_VALUE",
                    $"rule_type“has_buff”的值“{stringValue}”对应的 buff 主类型可以使用 stat_sub_type，因此 has_buff 将始终无法检测到该类型的 buff。",
                    stringPath, stringPath);
            }
        }

        if (!isFalseRule && ruleType == "in_activity" &&
            !BuffRuleSemantics.Activities.Contains(stringValue))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "INVALID_RULE_STRING_VALUE",
                $"rule_type“in_activity”未取反时，rule_data.string 必须是 {string.Join("、", BuffRuleSemantics.Activities)} 之一，否则该 buff 将无效。",
                stringPath, stringPath);
        }

        if (!isFalseRule && ruleType == "in_rank" && !BuffRuleSemantics.Ranks.Contains(floatValue))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "INVALID_RULE_FLOAT_VALUE",
                "该站位无法使buff生效", floatPath, floatPath);
        }

        switch (ruleType)
        {
            case "hpbelow":
            case "target_hpbelow":
                if ((!isFalseRule && floatValue < 0f) || (isFalseRule && floatValue >= 1f))
                {
                    var requirement = isFalseRule ? "小于 1" : "大于或等于 0";
                    AddInvalidRuleFloatIssue(ruleType, requirement, isFalseRule, floatPath, sourceMap, issues);
                }
                break;

            case "hpabove":
            case "target_hpabove":
                if ((!isFalseRule && floatValue > 1f) || (isFalseRule && floatValue <= 0f))
                {
                    var requirement = isFalseRule ? "大于 0" : "小于或等于 1";
                    AddInvalidRuleFloatIssue(ruleType, requirement, isFalseRule, floatPath, sourceMap, issues);
                }
                break;

            case "lightbelow":
                if ((!isFalseRule && floatValue <= 0f) || (isFalseRule && floatValue > 100f))
                {
                    var requirement = isFalseRule ? "小于或等于 100" : "大于 0";
                    AddInvalidRuleFloatIssue(ruleType, requirement, isFalseRule, floatPath, sourceMap, issues);
                }
                break;

            case "lightabove":
                if ((!isFalseRule && floatValue >= 100f) || (isFalseRule && floatValue < 0f))
                {
                    var requirement = isFalseRule ? "大于或等于 0" : "小于 100";
                    AddInvalidRuleFloatIssue(ruleType, requirement, isFalseRule, floatPath, sourceMap, issues);
                }
                break;

            case "monster_type_count_min" when !isFalseRule && floatValue < 1f:
                AddIssue(issues, sourceMap, ValidationSeverity.Error, "INVALID_RULE_FLOAT_VALUE",
                    "rule_type“monster_type_count_min”要求 rule_data.float 大于或等于 1，否则该 buff 无法生效。",
                    floatPath, floatPath);
                break;
        }
    }

    private static void AddInvalidRuleFloatIssue(
        string ruleType,
        string requirement,
        bool isFalseRule,
        string path,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        var inversionText = isFalseRule ? "取反" : "未取反";
        AddIssue(issues, sourceMap, ValidationSeverity.Error, "INVALID_RULE_FLOAT_VALUE",
            $"rule_type“{ruleType}”{inversionText}时，rule_data.float 必须{requirement}，否则该 buff 无法生效。",
            path, path);
    }

    private static bool TryGetFloat(JsonElement value, out float number)
    {
        number = default;
        return value.ValueKind == JsonValueKind.Number &&
               float.TryParse(value.GetRawText(), NumberStyles.Float, CultureInfo.InvariantCulture, out number) &&
               !float.IsInfinity(number) &&
               !float.IsNaN(number);
    }
    private static void ValidateStatTypeRelation(
        JsonElement buff,
        string buffPath,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        if (!buff.TryGetProperty("stat_type", out var statTypeElement) ||
            statTypeElement.ValueKind != JsonValueKind.String ||
            !buff.TryGetProperty("stat_sub_type", out var statSubTypeElement) ||
            statSubTypeElement.ValueKind != JsonValueKind.String)
        {
            return;
        }

        var statType = statTypeElement.GetString() ?? string.Empty;
        var statSubType = statSubTypeElement.GetString() ?? string.Empty;
        var statTypePath = $"{buffPath}.stat_type";
        var statSubTypePath = $"{buffPath}.stat_sub_type";

        if (!BuffStatTypeRules.ValidStatTypes.Contains(statType))
        {
            var suggestion = FindClosestValue(statType, BuffStatTypeRules.ValidStatTypes);
            var suggestionText = suggestion is null ? string.Empty : $" 是否应为“{suggestion}”？";
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "UNKNOWN_STAT_TYPE",
                $"stat_type“{statType}”不是已知的 buff 类型。{suggestionText}", statTypePath, statTypePath);
            return;
        }

        if (BuffStatTypeRules.FreeFormSubType.Contains(statType))
        {
            if (BuffStatTypeRules.RequiredFreeFormSubType.Contains(statType) &&
                string.IsNullOrWhiteSpace(statSubType))
            {
                AddIssue(issues, sourceMap, ValidationSeverity.Error, "MISSING_STAT_SUB_TYPE_VALUE",
                    $"stat_type“{statType}”必须指定非空的 stat_sub_type。",
                    statSubTypePath, statSubTypePath);
            }

            return;
        }

        if (BuffStatTypeRules.StatTypeToSubTypes.TryGetValue(statType, out var allowedSubTypes))
        {
            if (string.IsNullOrEmpty(statSubType))
            {
                if (BuffStatTypeRules.MustHaveSubType.Contains(statType))
                {
                    AddIssue(issues, sourceMap, ValidationSeverity.Error, "MISSING_STAT_SUB_TYPE_VALUE",
                        $"stat_type“{statType}”必须指定非空的 stat_sub_type。允许值：{string.Join("、", allowedSubTypes.OrderBy(value => value, StringComparer.Ordinal))}。",
                        statSubTypePath, statSubTypePath);
                }

                return;
            }

            if (!allowedSubTypes.Contains(statSubType))
            {
                var suggestion = FindClosestValue(statSubType, allowedSubTypes);
                var suggestionText = suggestion is null ? string.Empty : $" 是否应为“{suggestion}”？";
                AddIssue(issues, sourceMap, ValidationSeverity.Error, "INVALID_STAT_SUB_TYPE",
                    $"stat_sub_type“{statSubType}”不属于 stat_type“{statType}”。{suggestionText}允许值：{string.Join("、", allowedSubTypes.OrderBy(value => value, StringComparer.Ordinal))}。",
                    statSubTypePath, statSubTypePath);
            }

            return;
        }

        if (!string.IsNullOrEmpty(statSubType))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "UNEXPECTED_STAT_SUB_TYPE",
                $"stat_type“{statType}”没有 stat_sub_type；由于该字段在 buffs.json 中必须存在，请将其值写为空字符串“”。",
                statSubTypePath, statSubTypePath);
        }
    }

    private static void ValidateRuleData(JsonElement ruleData, string buffPath, JsonSourceMap sourceMap, List<ValidationIssue> issues)
    {
        var ruleDataPath = $"{buffPath}.rule_data";
        var properties = ruleData.EnumerateObject().ToList();
        var validatedProperties = properties.Where(property => !ContainsChineseCharacter(property.Name)).ToList();
        ReportDuplicateProperties(validatedProperties, ruleDataPath, sourceMap, issues);
        var propertyNames = validatedProperties.Select(property => property.Name).ToHashSet(StringComparer.Ordinal);

        foreach (var requiredField in RuleDataFields.Keys.Where(requiredField => !propertyNames.Contains(requiredField)))
        {
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "MISSING_RULE_DATA_FIELD",
                $"rule_data 缺少必需字段“{requiredField}”。", ruleDataPath, ruleDataPath);
        }

        foreach (var property in validatedProperties)
        {
            var propertyPath = JsonSourceMap.AppendProperty(ruleDataPath, property.Name);
            if (!RuleDataFields.TryGetValue(property.Name, out var expectedType))
            {
                ReportUnknownField(property.Name, RuleDataFields.Keys, propertyPath, sourceMap, issues);
                continue;
            }

            ValidateValueType(property.Value, expectedType, $"rule_data.{property.Name}", propertyPath, sourceMap, issues);
        }
    }

    private static void ValidateValueType(
        JsonElement value,
        ExpectedValueType expectedType,
        string fieldName,
        string path,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        var isValid = expectedType switch
        {
            ExpectedValueType.String => value.ValueKind == JsonValueKind.String,
            ExpectedValueType.Boolean => value.ValueKind is JsonValueKind.True or JsonValueKind.False,
            ExpectedValueType.Object => value.ValueKind == JsonValueKind.Object,
            ExpectedValueType.StringArray => IsStringArray(value),
            ExpectedValueType.Number => IsFloatCompatibleNumber(value),
            _ => false
        };

        if (isValid)
        {
            return;
        }

        var expectedText = expectedType switch
        {
            ExpectedValueType.String => "带双引号的字符串",
            ExpectedValueType.Boolean => "布尔值 true 或 false",
            ExpectedValueType.Object => "JSON 对象",
            ExpectedValueType.StringArray => "字符串数组",
            ExpectedValueType.Number => "可转换为 float 的数字",
            _ => "正确类型的值"
        };

        AddIssue(issues, sourceMap, ValidationSeverity.Error, "INVALID_FIELD_TYPE",
            $"字段“{fieldName}”必须是{expectedText}，当前值类型为{GetKindText(value.ValueKind)}。", path, path);
    }

    private static bool IsStringArray(JsonElement value)
    {
        return value.ValueKind == JsonValueKind.Array &&
               value.EnumerateArray().All(item => item.ValueKind == JsonValueKind.String);
    }

    private static bool IsFloatCompatibleNumber(JsonElement value)
    {
        if (value.ValueKind != JsonValueKind.Number)
        {
            return false;
        }

        return float.TryParse(value.GetRawText(), NumberStyles.Float, CultureInfo.InvariantCulture, out var number) &&
               !float.IsInfinity(number) && !float.IsNaN(number);
    }

    private static void ReportUnknownField(
        string actualName,
        IEnumerable<string> candidates,
        string path,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        var match = candidates
            .Select(candidate => new { Name = candidate, Distance = DamerauLevenshteinDistance(actualName, candidate) })
            .OrderBy(item => item.Distance)
            .ThenBy(item => item.Name, StringComparer.Ordinal)
            .First();

        var message = IsPlausibleTypo(actualName, match.Name, match.Distance)
            ? $"发现未知字段“{actualName}”，疑似拼写错误。是否应为“{match.Name}”？"
            : $"发现不支持的字段“{actualName}”。请确认字段名是否正确。";

        AddIssue(issues, sourceMap, ValidationSeverity.Warning, "UNKNOWN_FIELD", message, path, path);
    }

    private static void ReportDuplicateProperties(
        IReadOnlyList<JsonProperty> properties,
        string parentPath,
        JsonSourceMap sourceMap,
        List<ValidationIssue> issues)
    {
        foreach (var duplicate in properties.GroupBy(property => property.Name, StringComparer.Ordinal).Where(group => group.Count() > 1))
        {
            var path = JsonSourceMap.AppendProperty(parentPath, duplicate.Key);
            AddIssue(issues, sourceMap, ValidationSeverity.Error, "DUPLICATE_FIELD",
                $"字段“{duplicate.Key}”重复出现了 {duplicate.Count()} 次。", path, path);
        }
    }

    private static void AddIssue(
        List<ValidationIssue> issues,
        JsonSourceMap sourceMap,
        ValidationSeverity severity,
        string code,
        string message,
        string path,
        string locationPath)
    {
        var (line, column) = sourceMap.Find(locationPath);
        issues.Add(new ValidationIssue(severity, code, message, path, line, column));
    }

    private static string? FindClosestValue(string actualValue, IEnumerable<string> candidates)
    {
        var closest = candidates
            .Select(candidate => new { Value = candidate, Distance = DamerauLevenshteinDistance(actualValue, candidate) })
            .OrderBy(item => item.Distance)
            .ThenBy(item => item.Value, StringComparer.Ordinal)
            .FirstOrDefault();

        return closest is not null && IsPlausibleTypo(actualValue, closest.Value, closest.Distance)
            ? closest.Value
            : null;
    }

    private static bool IsPlausibleTypo(string actualValue, string candidate, int distance)
    {
        var maximumLength = Math.Max(actualValue.Length, candidate.Length);
        if (maximumLength == 0)
        {
            return false;
        }

        var maximumDistance = maximumLength switch
        {
            <= 4 => 1,
            <= 12 => 2,
            _ => 3
        };
        var minimumSimilarity = maximumLength switch
        {
            <= 4 => 0.65,
            <= 12 => 0.75,
            _ => 0.85
        };
        var similarity = 1d - (double)distance / maximumLength;
        return distance <= maximumDistance && similarity >= minimumSimilarity;
    }

    private static int DamerauLevenshteinDistance(string source, string target)
    {
        var distances = new int[source.Length + 1, target.Length + 1];
        for (var sourceIndex = 0; sourceIndex <= source.Length; sourceIndex++)
        {
            distances[sourceIndex, 0] = sourceIndex;
        }

        for (var targetIndex = 0; targetIndex <= target.Length; targetIndex++)
        {
            distances[0, targetIndex] = targetIndex;
        }

        for (var sourceIndex = 1; sourceIndex <= source.Length; sourceIndex++)
        {
            for (var targetIndex = 1; targetIndex <= target.Length; targetIndex++)
            {
                var cost = source[sourceIndex - 1] == target[targetIndex - 1] ? 0 : 1;
                var distance = Math.Min(
                    Math.Min(distances[sourceIndex - 1, targetIndex] + 1, distances[sourceIndex, targetIndex - 1] + 1),
                    distances[sourceIndex - 1, targetIndex - 1] + cost);

                if (sourceIndex > 1 && targetIndex > 1 &&
                    source[sourceIndex - 1] == target[targetIndex - 2] &&
                    source[sourceIndex - 2] == target[targetIndex - 1])
                {
                    distance = Math.Min(distance, distances[sourceIndex - 2, targetIndex - 2] + 1);
                }

                distances[sourceIndex, targetIndex] = distance;
            }
        }

        return distances[source.Length, target.Length];
    }

    private static bool ContainsChineseCharacter(string text)
    {
        foreach (var rune in text.EnumerateRunes())
        {
            var value = rune.Value;
            if (value is >= 0x3400 and <= 0x4DBF or
                >= 0x4E00 and <= 0x9FFF or
                >= 0xF900 and <= 0xFAFF or
                >= 0x20000 and <= 0x2FA1F or
                >= 0x30000 and <= 0x323AF)
            {
                return true;
            }
        }

        return false;
    }
    private static string GetKindText(JsonValueKind kind) => kind switch
    {
        JsonValueKind.String => "字符串",
        JsonValueKind.Number => "数字",
        JsonValueKind.True or JsonValueKind.False => "布尔值",
        JsonValueKind.Object => "对象",
        JsonValueKind.Array => "数组",
        JsonValueKind.Null => "null",
        _ => kind.ToString()
    };

    private static int GetCharacterColumn(string json, int zeroBasedLine, int zeroBasedBytePosition)
    {
        var lineStart = 0;
        for (var line = 0; line < zeroBasedLine && lineStart < json.Length; line++)
        {
            var nextLine = json.IndexOf('\n', lineStart);
            lineStart = nextLine < 0 ? json.Length : nextLine + 1;
        }

        var remainingBytes = Math.Max(0, zeroBasedBytePosition);
        var characterCount = 0;
        for (var index = lineStart; index < json.Length && json[index] != '\r' && json[index] != '\n';)
        {
            var characterLength = char.IsHighSurrogate(json[index]) && index + 1 < json.Length && char.IsLowSurrogate(json[index + 1]) ? 2 : 1;
            var byteCount = Encoding.UTF8.GetByteCount(json.AsSpan(index, characterLength));
            if (byteCount > remainingBytes)
            {
                break;
            }

            remainingBytes -= byteCount;
            characterCount++;
            index += characterLength;
        }

        return characterCount + 1;
    }
    private static string CleanJsonExceptionMessage(string message)
    {
        var separatorIndex = message.IndexOf(" LineNumber:", StringComparison.Ordinal);
        return separatorIndex >= 0 ? message[..separatorIndex] : message;
    }

    private enum ExpectedValueType
    {
        String,
        Number,
        Boolean,
        Object,
        StringArray
    }
}









