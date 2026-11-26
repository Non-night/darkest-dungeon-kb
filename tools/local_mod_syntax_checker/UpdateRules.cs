using System.Globalization;
using System.Text.Json;
using For_the_Darkest_Dungeon.DefinitionDarkest;

namespace LocalModSyntaxChecker;

internal static class UpdateRules
{
    private static readonly JsonDocument Document = JsonDocument.Parse(
        typeof(UpdateRules).Assembly.GetManifestResourceStream("LocalModSyntaxChecker.update_rules.json")!);
    public static JsonElement Data => Document.RootElement;

    public static void Apply()
    {
        foreach (var header in Data.GetProperty("info_boolean_fields").EnumerateObject())
            foreach (var field in header.Value.EnumerateArray())
                if (!DarkestInfoData.InfoContextMap[header.Name].Contains(field.GetString()!))
                    DarkestInfoData.InfoContextMap[header.Name].Add(field.GetString()!);
        foreach (var field in Data.GetProperty("effect_arguments").EnumerateObject())
        {
            if (!DarkestEffectsData.AllKeywords.Contains(field.Name)) DarkestEffectsData.AllKeywords.Add(field.Name);
            DarkestEffectsData.KeywordToValuesMap.Remove(field.Name);
        }
        foreach (var target in Data.GetProperty("effect_targets").EnumerateArray())
            if (!DarkestEffectsData.TargetValues.Contains(target.GetString()!))
                DarkestEffectsData.TargetValues.Add(target.GetString()!);
    }

    public static bool IsInfoBoolean(string header, string keyword) =>
        Data.GetProperty("info_boolean_fields").TryGetProperty(header, out var fields) &&
        fields.EnumerateArray().Any(field => field.GetString() == keyword);

    public static bool IsValidArgument(string kind, string value) => kind switch
    {
        "boolean" => value.Equals("true", StringComparison.OrdinalIgnoreCase) || value.Equals("false", StringComparison.OrdinalIgnoreCase),
        "numeric_boolean" => value is "0" or "1",
        "integer" => System.Text.RegularExpressions.Regex.IsMatch(value, @"^[+-]?[0-9]+$"),
        "number" => double.TryParse(value, NumberStyles.Float, CultureInfo.InvariantCulture, out var number) && double.IsFinite(number),
        "string" => !string.IsNullOrWhiteSpace(value),
        _ => false
    };

    public static void ReportPartialCoverage(string file, string text,
        Action<string,int,int,string,string,string,string> add)
    {
        var parts = file.Replace('\\', '/').Split('/');
        var domain = Data.GetProperty("partial_domains").EnumerateObject()
            .FirstOrDefault(entry => parts.Contains(entry.Name, StringComparer.OrdinalIgnoreCase));
        if (domain.Value.ValueKind != JsonValueKind.Undefined && file.EndsWith(".json", StringComparison.OrdinalIgnoreCase))
        {
            add(file, 1, 1, "info", "KB-COVERAGE-PARTIAL", domain.Value.GetString()!, "tools/local_mod_syntax_checker/update_rules.json");
            try
            {
                using var document = JsonDocument.Parse(text);
                ValidateJsonNode(document.RootElement, domain.Name, "$", file, add);
            }
            catch (JsonException error)
            {
                add(file, (int)(error.LineNumber ?? 0) + 1, (int)(error.BytePositionInLine ?? 0) + 1,
                    "error", "JSON-INVALID", error.Message, "JSON");
            }
        }
    }

    private static bool IsValidJsonValue(string kind, JsonElement value) => kind switch
    {
        "boolean" => value.ValueKind is JsonValueKind.True or JsonValueKind.False,
        "string" => value.ValueKind == JsonValueKind.String && !string.IsNullOrWhiteSpace(value.GetString()),
        "integer" => value.ValueKind == JsonValueKind.Number && value.TryGetDouble(out var number) &&
            double.IsFinite(number) && number == Math.Truncate(number),
        "string_array" => value.ValueKind == JsonValueKind.Array && value.EnumerateArray().All(item => item.ValueKind == JsonValueKind.String),
        _ => value.ValueKind == JsonValueKind.String && Data.GetProperty("json_enums").TryGetProperty(kind, out var allowed) &&
            allowed.EnumerateArray().Any(item => item.GetString() == value.GetString())
    };

    private static void ValidateJsonNode(JsonElement node, string domain, string path, string file,
        Action<string,int,int,string,string,string,string> add)
    {
        if (node.ValueKind == JsonValueKind.Object)
        {
            var fields = Data.GetProperty("json_fields").GetProperty(domain).EnumerateObject()
                .ToDictionary(field => field.Name, field => field.Value.GetString()!);
            var required = new HashSet<string>();
            if (node.TryGetProperty("type", out var type) && type.ValueKind == JsonValueKind.String &&
                Data.GetProperty("json_required_by_type").TryGetProperty(domain, out var types) &&
                types.TryGetProperty(type.GetString()!, out var conditional))
                foreach (var field in conditional.EnumerateObject())
                {
                    fields[field.Name] = field.Value.GetString()!;
                    required.Add(field.Name);
                }
            foreach (var field in fields)
            {
                bool exists = node.TryGetProperty(field.Key, out var value);
                if (!exists && !required.Contains(field.Key)) continue;
                if (!exists || !IsValidJsonValue(field.Value, value))
                    add(file, 1, 1, "error", "KB-UPDATE-JSON-ARGUMENT", $"{path}.{field.Key} 要求 {field.Value}。", "tools/local_mod_syntax_checker/update_rules.json");
            }
            foreach (var field in node.EnumerateObject()) ValidateJsonNode(field.Value, domain, path + "." + field.Name, file, add);
        }
        else if (node.ValueKind == JsonValueKind.Array)
        {
            int index = 0;
            foreach (var item in node.EnumerateArray()) ValidateJsonNode(item, domain, $"{path}[{index++}]", file, add);
        }
    }
}
