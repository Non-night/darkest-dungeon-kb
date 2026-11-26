using System.Text.RegularExpressions;
using System.Xml;
using System.Xml.Linq;

namespace LocalModSyntaxChecker;

internal static class LocalizationSyntax
{
    private static readonly Regex ColourStart = new(@"\{colour_start\|(?<id>[^{}|]+)\}", RegexOptions.Compiled);
    private static readonly Regex NamedMarker = new(@"\{\?(?<name>[^{}]+)\}", RegexOptions.Compiled);
    private sealed record Signature(IReadOnlyList<string> Named, IReadOnlyList<string> Unnamed)
    {
        public bool Matches(Signature other) => Named.SequenceEqual(other.Named,StringComparer.Ordinal) && Unnamed.SequenceEqual(other.Unnamed,StringComparer.Ordinal);
    }

    public static void Validate(string file,string modRoot,IReadOnlySet<string> colourIds,bool strictReferences,
        Action<string,int,int,string,string,string,string> add)
    {
        string relative = Path.GetRelativePath(modRoot,file).Replace('\\','/');
        if (!relative.StartsWith("localization/",StringComparison.OrdinalIgnoreCase))
            add(file,1,1,"warning","KB-LOC-WRONG-DIRECTORY","string_table.xml 通常应位于 Mod 根目录的 localization/ 下，避免编译器扫描不到。","Mechanics/16-loc与loc2本地化覆盖优先级.md");
        if (!File.Exists(Path.Combine(modRoot,"localization","project_paths.txt")))
            add(file,1,1,"warning","KB-LOC-PROJECT-PATHS-MISSING","未找到 localization/project_paths.txt；单独运行 localization.exe 时可能无法按预期扫描项目根目录。","Mechanics/16-loc与loc2本地化覆盖优先级.md");

        XDocument document;
        try { document = XDocument.Load(file,LoadOptions.SetLineInfo); }
        catch (XmlException e)
        {
            add(file,e.LineNumber,e.LinePosition,"error","LOC-XML-MALFORMED",$"XML 语法错误：{e.Message}","Mechanics/16-loc与loc2本地化覆盖优先级.md");
            return;
        }
        catch (Exception e)
        {
            add(file,1,1,"error","LOC-XML-READ",$"无法读取本地化 XML：{e.Message}","Mechanics/16-loc与loc2本地化覆盖优先级.md");
            return;
        }

        var languages = document.Root?.DescendantsAndSelf().Where(e => e.Name.LocalName == "language").ToList() ?? new List<XElement>().ToList();
        if (!languages.Any(e => (string?)e.Attribute("id") == "english"))
            add(file,1,1,"error","LOC-ENGLISH-BASELINE-MISSING","缺少必需的 <language id=\"english\"> 基准节点；该节点允许为空。","Mechanics/16-loc与loc2本地化覆盖优先级.md; anchor:localization-english-baseline");

        var byLanguage = new Dictionary<string,Dictionary<string,List<XElement>>>(StringComparer.Ordinal);
        foreach (var language in languages)
        {
            string languageId = (string?)language.Attribute("id") ?? string.Empty;
            int line = Line(language), col = Column(language);
            if (languageId.Length == 0)
            {
                add(file,line,col,"error","LOC-LANGUAGE-ID-MISSING","language 节点缺少 id 属性。","Mechanics/16-loc与loc2本地化覆盖优先级.md");
                continue;
            }
            var entries = new Dictionary<string,List<XElement>>(StringComparer.Ordinal);
            foreach (var entry in language.Descendants().Where(e => e.Name.LocalName == "entry"))
            {
                string id = (string?)entry.Attribute("id") ?? string.Empty;
                if (string.IsNullOrWhiteSpace(id))
                {
                    add(file,Line(entry),Column(entry),"error","LOC-ENTRY-ID-MISSING","entry 缺少非空 id 属性。","Mechanics/16-loc与loc2本地化覆盖优先级.md");
                    continue;
                }
                if (!entries.TryGetValue(id,out var sameId)) entries[id] = sameId = new List<XElement>();
                sameId.Add(entry);
                ValidateEntry(file,entry,id,colourIds,strictReferences,add);
            }
            byLanguage[languageId] = entries;
        }

        if (!byLanguage.TryGetValue("english",out var english)) return;
        foreach (var (id,baseEntries) in english)
        {
            // 本地化资料明确记录重复 Entry 可通过编译；重复项不作猜测式一对一配对。
            if (baseEntries.Count != 1 || string.IsNullOrWhiteSpace(baseEntries[0].Value)) continue;
            var expected = GetSignature(baseEntries[0].Value);
            foreach (var (languageId,entries) in byLanguage)
            {
                if (languageId == "english" || !entries.TryGetValue(id,out var translations) || translations.Count != 1) continue;
                if (expected.Matches(GetSignature(translations[0].Value))) continue;
                add(file,Line(translations[0]),Column(translations[0]),"warning","LOC-PLACEHOLDER-MISMATCH",
                    $"Entry '{id}' 在 {languageId} 中的格式参数数量、类型或具名参数与 english 不一致。",
                    "Mechanics/16-loc与loc2本地化覆盖优先级.md");
            }
        }
    }

    private static void ValidateEntry(string file,XElement entry,string entryId,IReadOnlySet<string> colourIds,bool strict,
        Action<string,int,int,string,string,string,string> add)
    {
        int line=Line(entry),column=Column(entry);
        foreach (Match colour in ColourStart.Matches(entry.Value))
        {
            string id=colour.Groups["id"].Value;
            if (colourIds.Contains(id)) continue;
            add(file,line,column,strict ? "error" : "warning","LOC-COLOR-NOT-FOUND",
                $"Entry '{entryId}' 引用的颜色 ID '{id}' 未在 Mod/引用目录的 *.colours.darkest 中找到。",
                "Mechanics/16-loc与loc2本地化覆盖优先级.md");
        }
        foreach (Match marker in NamedMarker.Matches(entry.Value))
        {
            int formatStart=marker.Index+marker.Length;
            if (TryFormat(entry.Value,formatStart,out _,out _)) continue;
            add(file,line,column,"error","LOC-NAMED-PARAM-MALFORMED",
                $"Entry '{entryId}' 的具名参数标记 '{{?{marker.Groups["name"].Value}}}' 后没有合法格式参数。",
                "Mechanics/16-loc与loc2本地化覆盖优先级.md");
        }
    }

    private static Signature GetSignature(string text)
    {
        var names=NamedMarker.Matches(text).Cast<Match>().ToDictionary(m=>m.Index+m.Length,m=>m.Groups["name"].Value);
        var named=new List<string>(); var unnamed=new List<string>();
        for(int i=0;i<text.Length;i++)
        {
            if(text[i]!='%') continue;
            if(i+1<text.Length && text[i+1]=='%') { i++; continue; }
            if(!TryFormat(text,i,out int end,out string type)) continue;
            if(names.TryGetValue(i,out var name)) named.Add(name+":"+type); else unnamed.Add(type);
            i=end-1;
        }
        named.Sort(StringComparer.Ordinal);
        return new Signature(named,unnamed);
    }

    private static bool TryFormat(string text,int start,out int end,out string type)
    {
        end=start; type=string.Empty;
        if(start>=text.Length || text[start]!='%') return false;
        int i=start+1;
        while(i<text.Length && (text[i] is '+' or '-' or '#' or '0' or ' ' or '.' || char.IsDigit(text[i]))) i++;
        // Knowledge base confirms at least these conversion letters; do not reject unfamiliar compiler extensions.
        const string conversions="dfuisc";
        if(i>=text.Length || !conversions.Contains(text[i])) return false;
        type=text[i].ToString(); end=i+1; return true;
    }
    private static int Line(XObject element) => element is IXmlLineInfo info && info.HasLineInfo() ? info.LineNumber : 1;
    private static int Column(XObject element) => element is IXmlLineInfo info && info.HasLineInfo() ? info.LinePosition : 1;
}
