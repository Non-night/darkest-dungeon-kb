using System.Text;
using System.Text.Json;

namespace BuffGrammarChecker.Core;

internal sealed class JsonSourceMap
{
    private readonly Dictionary<string, (int Line, int Column)> _locations = new(StringComparer.Ordinal);

    private JsonSourceMap()
    {
    }

    public static JsonSourceMap Build(string json)
    {
        var map = new JsonSourceMap();
        var utf8 = Encoding.UTF8.GetBytes(json);
        var reader = new Utf8JsonReader(utf8, new JsonReaderOptions
        {
            AllowTrailingCommas = false,
            CommentHandling = JsonCommentHandling.Disallow
        });
        var stack = new Stack<ContainerFrame>();

        while (reader.Read())
        {
            switch (reader.TokenType)
            {
                case JsonTokenType.PropertyName:
                {
                    if (stack.TryPeek(out var objectFrame))
                    {
                        objectFrame.PendingProperty = reader.GetString() ?? string.Empty;
                        var propertyPath = AppendProperty(objectFrame.Path, objectFrame.PendingProperty);
                        map.TryAdd(propertyPath, utf8, reader.TokenStartIndex);
                    }

                    break;
                }
                case JsonTokenType.StartObject:
                case JsonTokenType.StartArray:
                {
                    var valuePath = ResolveNextValuePath(stack);
                    map.TryAdd(valuePath, utf8, reader.TokenStartIndex);
                    stack.Push(new ContainerFrame(
                        reader.TokenType == JsonTokenType.StartObject ? ContainerKind.Object : ContainerKind.Array,
                        valuePath));
                    break;
                }
                case JsonTokenType.EndObject:
                case JsonTokenType.EndArray:
                    if (stack.Count > 0)
                    {
                        stack.Pop();
                    }
                    break;
                default:
                {
                    var valuePath = ResolveNextValuePath(stack);
                    map.TryAdd(valuePath, utf8, reader.TokenStartIndex);
                    break;
                }
            }
        }

        return map;
    }

    public (int? Line, int? Column) Find(string path)
    {
        if (_locations.TryGetValue(path, out var location))
        {
            return (location.Line, location.Column);
        }

        return (null, null);
    }

    public static string AppendProperty(string parentPath, string propertyName)
    {
        if (propertyName.Length > 0 && (char.IsLetter(propertyName[0]) || propertyName[0] == '_') &&
            propertyName.All(character => char.IsLetterOrDigit(character) || character == '_'))
        {
            return $"{parentPath}.{propertyName}";
        }

        return $"{parentPath}['{propertyName.Replace("'", "\\'")}']";
    }

    private static string ResolveNextValuePath(Stack<ContainerFrame> stack)
    {
        if (stack.Count == 0)
        {
            return "$";
        }

        var parent = stack.Peek();
        if (parent.Kind == ContainerKind.Array)
        {
            return $"{parent.Path}[{parent.NextArrayIndex++}]";
        }

        var property = parent.PendingProperty ?? string.Empty;
        parent.PendingProperty = null;
        return AppendProperty(parent.Path, property);
    }

    private void TryAdd(string path, byte[] utf8, long tokenStartIndex)
    {
        if (_locations.ContainsKey(path))
        {
            return;
        }

        var limit = (int)Math.Min(tokenStartIndex, utf8.Length);
        var line = 1;
        var column = 1;
        for (var index = 0; index < limit; index++)
        {
            if (utf8[index] == (byte)'\n')
            {
                line++;
                column = 1;
            }
            else if ((utf8[index] & 0b1100_0000) != 0b1000_0000)
            {
                // UTF-8 continuation bytes do not advance the user-visible character column.
                column++;
            }
        }

        _locations[path] = (line, column);
    }

    private enum ContainerKind
    {
        Object,
        Array
    }

    private sealed class ContainerFrame(ContainerKind kind, string path)
    {
        public ContainerKind Kind { get; } = kind;
        public string Path { get; } = path;
        public int NextArrayIndex { get; set; }
        public string? PendingProperty { get; set; }
    }
}

