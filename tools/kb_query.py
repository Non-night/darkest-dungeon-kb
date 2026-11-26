#!/usr/bin/env python3
"""Return a small, deterministic evidence pack for a DD Mod question.

This is intentionally lexical and dependency-driven. The knowledge base has
stable identifiers, so exact fields and route cards are a better first pass than
an unrestricted full-text/vector search.
"""
from __future__ import annotations
from kb_common import KB

import argparse
import json
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
RAG = ROOT / "RAG"


@lru_cache(maxsize=32)
def _load_jsonl_cached(path: str, mtime_ns: int, size: int) -> tuple[dict[str, Any], ...]:
    # Cache only parsed read-only rows; rebuilds invalidate by file stat.
    return tuple(json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip())


def load_jsonl(name: str) -> list[dict[str, Any]]:
    path = RAG / name
    if not path.is_file():
        return []
    stat = path.stat()
    return list(_load_jsonl_cached(str(path), stat.st_mtime_ns, stat.st_size))


def compact(value: Any, limit: int) -> str:
    if isinstance(value, list):
        value = "；".join(str(item) for item in value if item)
    if isinstance(value, dict):
        value = "；".join(f"{key}: {item}" for key, item in value.items())
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: max(0, limit - 1)].rstrip() + "…"


@lru_cache(maxsize=32768)
def canonical_phrase(value: str) -> str:
    return re.sub(r'\s+', '', value).replace('开始时', '开始').replace('结束时', '结束')


def contains(query: str, term: str) -> bool:
    term = term.strip().lower()
    if not term:
        return False
    # ASCII identifiers must be matched as complete tokens.  Without this,
    # the generic Info keyword `.type` matches `stat_type` and `rule_type`.
    bare = term.lstrip(".")
    if re.fullmatch(r"[a-z0-9_]+", bare):
        return bool(re.search(rf"(?<![a-z0-9_]){re.escape(bare)}(?![a-z0-9_])", query))
    # Chinese/mixed field phrases are often spaced differently by a caller.
    # This is spelling normalization, not semantic equivalence of negations.
    return canonical_phrase(term) in canonical_phrase(query)


def ranked(rows: Iterable[dict[str, Any]], score) -> list[tuple[int, dict[str, Any]]]:
    result = [(score(row), row) for row in rows]
    return sorted((item for item in result if item[0] > 0), key=lambda item: (-item[0], str(item[1].get("id", ""))))


def match_groups(query: str, row: dict[str, Any]) -> bool:
    """AND across groups, OR within each group; absent groups preserve old behavior."""
    return all(any(contains(query, str(term)) for term in group) for group in row.get("match_groups", []))


def route_score(query: str, route: dict[str, Any]) -> int:
    if not match_groups(query, route):
        return 0
    score = sum(3 + min(4, len(signal) // 8) for signal in route.get("signals", []) if contains(query, signal))
    return score + int(route.get("priority", 0)) if score else 0


def anchor_score(query: str, anchor: dict[str, Any]) -> int:
    if not match_groups(query, anchor):
        return 0
    matched = [term for term in anchor.get('triggers',[]) if contains(query,term)]
    score = sum(2 + min(4, len(term) // 8) for term in matched)
    score += max((min(12,len(re.sub(r'\s+','',term))//4) for term in matched if len(term)>=8), default=0)
    return score + min(60, int(anchor.get("priority", 0))) if score else 0


EXCLUDED_MECHANISMS = {
    "size0": r"(?<![a-z0-9_])size[\s-]*0(?![a-z0-9_])|零体积|零体型",
    "ActorDot": r"(?<![a-z0-9_])(?:actordot|actor_dot|ad)(?![a-z0-9_])",
}


def task_constraints(query: str) -> tuple[str, list[str]]:
    """Keep prohibitions visible, but never route a forbidden carrier as requested work."""
    excluded: set[str] = set()
    def strip_clause(match: re.Match[str]) -> str:
        clause = match.group(0)
        negative = re.search(r"(?:不使用|不能使用|不能用|不允许使用|不允许|不得使用|不用|禁止|禁用|不借助|不采用|无需使用|无需|排除)", clause)
        if not negative:
            return clause
        prefix, tail = clause[:negative.start()], clause[negative.start():]
        # A contrast starts a positive instruction, not another prohibited item.
        contrast = re.search(r"(?:但(?:是)?|而)(?=允许|使用|可以|要|用)", tail)
        suffix = ""
        if contrast:
            tail, suffix = tail[:contrast.start()], tail[contrast.start():]
        for name, pattern in EXCLUDED_MECHANISMS.items():
            if re.search(pattern, tail, flags=re.I):
                excluded.add(name)
                tail = re.sub(pattern, " ", tail, flags=re.I)
        return prefix + tail + suffix
    positive = re.sub(r"[^，,。；;\n]+", strip_clause, query.lower())
    return positive, sorted(excluded)


def exact_field_ids(query: str) -> set[str]:
    return {field.lower() for field in re.findall(r"\.[A-Za-z_][A-Za-z0-9_]*", query)}


GENERIC_INFO_FIELDS = {".type"}

# Small, explicit mappings for common user-facing Buff concepts.
BUFF_ALIASES = {
    "精准": {"subtype": "attack_rating"},
    "命中": {"subtype": "attack_rating"},
    "accuracy": {"subtype": "attack_rating"},
    "闪避": {"subtype": "defense_rating"},
    "dodge": {"subtype": "defense_rating"},
    "回合数": {"duration_type": "round"},
    "三回合": {"duration_type": "round"},
    "持续三回合": {"duration_type": "round"},
}


def round_duration_mentioned(query: str) -> bool:
    """Recognize an explicit numeric or labelled round-duration phrase."""
    return bool(re.search(r"(?:持续\s*)?\d+\s*回合", query)) or ("持续" in query and "回合" in query)


def effect_score(query: str, fields: set[str], row: dict[str, Any]) -> int:
    keyword = str(row.get("keyword", "")).lower()
    if keyword in fields:
        return 100
    search_terms = row.get("search_terms", [])
    if any(contains(query, str(term)) for term in search_terms):
        return 95
    return 20 if keyword and contains(query, keyword) else 0


def info_score(query: str, fields: set[str], row: dict[str, Any]) -> int:
    keyword = str(row.get("keyword", "")).lower()
    header = str(row.get("header", "")).lower()
    header_hit = bool(header and contains(query, header.rstrip(":")))
    # `.type` is shared by many unrelated Headers.  Require its Header in
    # the query; otherwise an explicit generic field would fan out globally.
    if fields and keyword not in fields:
        return 0
    if keyword in fields and (keyword not in GENERIC_INFO_FIELDS or header_hit):
        score = 90
    elif not fields and "_" in keyword and contains(query, keyword):
        # A named Info field is also a valid exact lookup without its dot.
        score = 85
    else:
        score = 0
    if header_hit and score:
        score += 40
    return score


def buff_score(query: str, row: dict[str, Any]) -> int:
    score = 0
    id_context = any(term in query.lower() for term in ("存档", "数字id", "数字 id", "stat_type id", "主类id", "主类 id"))
    if id_context and row.get("save_stat_type_id") is not None:
        if re.search(rf"(?<!\d){int(row['save_stat_type_id'])}(?!\d)", query):
            score = 98
    for key in ("stat_type", "rule_type", "duration_type"):
        value = str(row.get(key, "")).lower()
        if value and contains(query, value):
            score = max(score, 90)
    subtypes = {str(value).lower() for value in row.get("subtypes", [])}
    for alias, selector in BUFF_ALIASES.items():
        alias_hit = alias in query
        if selector.get("duration_type") == "round":
            alias_hit = alias_hit or round_duration_mentioned(query)
        if not alias_hit:
            continue
        if selector.get("subtype") in subtypes:
            score = max(score, 78)
        if selector.get("duration_type") == str(row.get("duration_type", "")).lower():
            score = max(score, 78)
    return score


def card_score(
    query: str,
    route_ids: set[str],
    row: dict[str, Any],
    preferred_sources: set[str] | None = None,
    semantic_terms: Iterable[str] | None = None,
    source_weights: dict[str, int] | None = None,
) -> int:
    title = str(row.get("title", "")).lower()
    heading = str(row.get("heading", "")).lower()
    doc_path = str(row.get("doc_path", "")).replace("\\", "/").lower()
    preferred_sources = preferred_sources or set()
    source_weights = source_weights or {}
    matched_weights = [weight for source, weight in source_weights.items() if source in doc_path]
    intended_doc = bool(matched_weights) or any(source in doc_path for source in preferred_sources)
    score = 0
    lexical_hits = 0
    tokens = set(re.findall(r"[a-z_]{3,}|[\u4e00-\u9fff]{2,}", query))
    tokens.update(
        str(term).lower()
        for term in (semantic_terms or ())
        if term and contains(query, str(term))
    )
    for term in row.get("search_terms", []):
        if contains(query, str(term)):
            score += 30
            lexical_hits += 1
    generic_topic_terms = {"buff", "饰品", "trinket", "effect", "技能", "skill"}
    for token in tokens:
        if token in heading:
            score += 12
            lexical_hits += 1
        elif token in title and token not in generic_topic_terms:
            score += 8
            lexical_hits += 1
    # Chinese questions rarely insert word boundaries. Compare informative
    # character fragments and exact identifiers with section prose as well as
    # titles, so "时序" alone cannot promote unrelated push/pull sections.
    features = retrieval_features(query)
    body = (heading + ' ' + str(row.get('abstract',''))).lower()
    matched_features = [term for term in features if term in body]
    coverage = sum(features[t] for t in matched_features) / max(1,sum(features.values()))
    if len(matched_features)>=2 or any('_' in t for t in matched_features):
        lexical_hits += 2
        score += int(320*coverage)
    # Anchor and route source paths are stronger than loose lexical overlap.
    # A card from an intended source is useful even when its heading uses a
    # different term; unrelated one-word matches are discarded.
    # A source path alone must not pull an unrelated card into a precise
    # field query. Require at least one query/semantic token hit for every
    # mechanic card; intended sources then break ties among those hits.
    if lexical_hits == 0:
        return 0
    if intended_doc:
        score += 80 + min(60, max(matched_weights, default=0))
    elif lexical_hits < 2:
        return 0
    for route_id in route_ids:
        route_no = route_id.rsplit(":", 1)[-1].replace(".", "-")
        if route_no in doc_path:
            score += 20
    return score


@lru_cache(maxsize=128)
def retrieval_features(query: str) -> dict[str, int]:
    generic = {'effect','buff','skill','queue','true','false','awr','技能','效果','触发','时序','当前','这个','是否','可以','一个'}
    result = {}
    for term in re.findall(r'[a-z_][a-z0-9_]+|\d+%',query.lower()):
        if term not in generic:
            result[term]=8 if '_' in term else 3
    for run in re.findall(r'[\u4e00-\u9fff]+',query):
        for width in (2,3):
            for start in range(len(run)-width+1):
                term=run[start:start+width]
                if term not in generic:
                    result[term]=width
    return result


def query_excerpt(value: Any, query: str, limit: int) -> str:
    """Keep a matching later conclusion visible; exact full text remains expandable."""
    text = str(value or '')
    if len(text) <= limit:
        return compact(text, limit)
    terms = set(re.findall(r'[a-z_]{3,}|[\u4e00-\u9fff]{2}', query.lower()))
    chunks = re.split(r'(?<=[。；])|\n\n', text)
    scored = [(sum(len(t) for t in terms if t in chunk.lower()), index, chunk) for index,chunk in enumerate(chunks)]
    selected = []
    total = 0
    for score,index,chunk in sorted(scored, key=lambda item:(-item[0],item[1])):
        if not score:
            continue
        if total and total+len(chunk)>limit-12:
            continue
        selected.append((index,chunk)); total+=len(chunk)
        if total>=limit-12:
            break
    if not selected:
        return compact(text,limit)
    return compact('…'+' '.join(c for _,c in sorted(selected))+' [摘录；完整条件见原条目]',limit)


def source_fragments(sources: Iterable[Any]) -> set[str]:
    """Return normalized path fragments suitable for mechanic-card matching."""
    fragments: set[str] = set()
    for source in sources:
        if not source:
            continue
        path = str(source).replace("\\", "/").lower()
        if path.endswith(".md"):
            fragments.add(path)
            fragments.add(path.rsplit("/", 1)[-1])
    return fragments


def effect_summary(row: dict[str, Any]) -> str:
    details = [
        row.get("parameter_type"),
        row.get("argument_semantics"),
        row.get("constraints"),
        row.get("engine_behavior"),
    ]
    return compact([item for item in details if item], 520)


def info_summary(row: dict[str, Any]) -> str:
    # Info records use the compact schema emitted by the generator. Keep the
    # summary useful without serializing the full official example.
    details = [
        row.get("parameter"),
        row.get("scope"),
        row.get("description"),
        row.get("evidence"),
    ]
    return compact([item for item in details if item], 500)


def buff_summary(row: dict[str, Any]) -> str:
    details = [
        f"stat_type={row['stat_type']}" if row.get("stat_type") else None,
        f"rule_type={row['rule_type']}" if row.get("rule_type") else None,
        f"duration_type={row['duration_type']}" if row.get("duration_type") else None,
        f"subtypes={row['subtypes']}" if row.get("subtypes") else None,
        row.get("meaning"),
        row.get("category"),
        row.get("constraints"),
        row.get("semantics"),
        row.get("notes"),
        row.get("engine_behavior"),
        f"save_stat_type_id={row['save_stat_type_id']}" if row.get("save_stat_type_id") is not None else None,
        row.get("raw_amount_classification"),
        row.get("classification_note"),
    ]
    return compact([item for item in details if item], 700)


def vanilla_matches(query: str) -> list[dict[str, Any]]:
    hits = []
    vanilla_rows = load_jsonl("vanilla_content.jsonl")
    for row in vanilla_rows:
        aliases = [a["name"] for a in row.get("aliases", [])]
        terms = row.get("name_zh", []) + row.get("name_en", []) + aliases + [row.get("game_id", "")]
        matched = [term for term in terms if len(term) >= 2 and term.lower() not in {"move", "skill", "buff", "stress", "heal", "attack", "pass", "移动", "攻击", "治疗"} and contains(query.lower(), term)]
        if row.get("header")=="riposte_skill" and any(term in query.lower() for term in ("反击", "riposte")):
            hero_rows=vanilla_rows
            owner_names=[term for hero in hero_rows if hero.get("kind")=="hero" and hero.get("game_id")==row.get("owner") for term in hero.get("name_zh",[])+hero.get("name_en",[])+[hero["game_id"]]+[a["name"] for a in hero.get("aliases",[])]]
            if row.get("owner")=="bounty_hunter": owner_names.append("赏金")
            if any(contains(query.lower(),term) for term in owner_names): matched.append(row["owner"]+"反击")
        if matched:
            score=max(map(len, matched)) - (100 if row.get("lookup_priority")=="low" else 0)
            if any(term.lower()==query.strip().lower() for term in matched): score += 50
            if row.get("kind") in ("character", "party"):
                score += 20
            hits.append((score, row))
    return [row for _, row in sorted(hits, key=lambda x: (-x[0], x[1]["id"]))[:6]]


def make_pack(query: str, budget: int, max_records: int, include_history: bool = False) -> dict[str, Any]:
    normalized, excluded_mechanisms = task_constraints(query)
    fields = exact_field_ids(normalized)
    routes = load_jsonl("agent_routes.jsonl")
    anchors = load_jsonl("agent_anchor_cards.jsonl")
    if not include_history:
        anchors = [r for r in anchors if r.get('retrieval_status') not in ('historical','withdrawn','superseded')]
    anchor_by_id = {str(row["id"]): row for row in anchors}
    selected_routes = [row for _, row in ranked(routes, lambda row: route_score(normalized, row))[:2]]
    if not selected_routes:
        selected_routes = [next(row for row in routes if row.get("id") == "route:research-fallback")]

    # Direct trigger matches must precede broad route-required anchors.  Otherwise
    # a route with many generic required checks can consume the six-anchor pack
    # before the exact mechanism requested by the query is returned.
    direct_anchor_ids: list[str] = [
        str(anchor["id"])
        for _, anchor in ranked(anchors, lambda row: anchor_score(normalized, row))
    ]
    selected_anchor_ids = list(direct_anchor_ids)
    for route in selected_routes:
        conditional = set(route.get("conditional_anchors", []))
        selected_anchor_ids.extend(
            anchor_id for anchor_id in route.get("required_anchors", [])
            if anchor_id not in conditional or anchor_score(normalized, anchor_by_id.get(anchor_id, {})) > 0
        )
    # One controlled dependency hop, preserving the order that made the card relevant.
    for anchor_id in list(selected_anchor_ids):
        anchor = anchor_by_id.get(anchor_id)
        if anchor:
            selected_anchor_ids.extend(anchor.get("requires", []))
    selected_anchors = []
    for anchor_id in selected_anchor_ids:
        anchor = anchor_by_id.get(anchor_id)
        if anchor and anchor not in selected_anchors:
            selected_anchors.append(anchor)
    selected_anchors = selected_anchors[:6]

    info_headers = load_jsonl("info_headers.jsonl")
    has_info_header = any(
        str(row.get("header", "")).rstrip(":").lower() in normalized
        for row in info_headers
    )
    info_route_selected = any(row.get("id") == "route:info.definition" for row in selected_routes)
    info_enabled = info_route_selected or bool(fields - GENERIC_INFO_FIELDS) or has_info_header

    exact: list[dict[str, str]] = []
    effects = ranked(load_jsonl("effect_keywords.jsonl"), lambda row: effect_score(normalized, fields, row))[:3]
    for _, row in effects:
        exact.append({"kind": "effect", "id": str(row.get("id")), "path": str(row.get("doc_path")), "summary": effect_summary(row)})
    infos = ranked(
        load_jsonl("info_fields.jsonl"),
        lambda row: info_score(normalized, fields, row) if info_enabled else 0,
    )[:3]
    for _, row in infos:
        exact.append({"kind": "info_field", "id": str(row.get("id")), "path": str(row.get("doc_path", "RAG/info_fields.jsonl")), "summary": info_summary(row)})
    buff_route_selected = any(row.get("id") == "route:buff.create" for row in selected_routes)
    buff_enabled = buff_route_selected or any(
        term in normalized for term in (
            "buff", "增益", "stat_type", "rule_type", "duration_type",
            "存档", "数字 id", "数字id", "默认分类", "正值", "负值", "零值",
            "增益减益分类", "amount 分类", "amount分类",
        )
    )
    for file_name in ("buff_stat_types.jsonl", "buff_rule_types.jsonl", "buff_duration_types.jsonl"):
        limit = 2 if buff_enabled and any(alias in normalized for alias in BUFF_ALIASES) else 1
        rows = ranked(
            load_jsonl(file_name),
            lambda row: buff_score(normalized, row) if buff_enabled else 0,
        )[:limit]
        for _, row in rows:
            exact.append({"kind": "buff", "id": str(row.get("id")), "path": str(row.get("doc_path", file_name)), "summary": buff_summary(row)})

    # Exact localization Entry or normalized-format lookup, not broad keyword inventory loading.
    if any(token in normalized for token in ('tooltip_', 'effect_', 'skill_name_', 'clear_guard', 'description_entries')):
        for row in load_jsonl("description_entries.jsonl") if (KB / "RAG/description_entries.jsonl").exists() else []:
            fmt = row["format"]
            if fmt.lower() not in normalized:
                continue
            ev = next((e for e in row["evidence"] if e["tier"] != "local_mod" and e["language"] == "english"), row["evidence"][0])
            exact.append({"kind": "description_entry", "id": row["id"], "path": "RAG/description_entries.jsonl", "summary": str({"format": fmt, "status": row["status"], "vanilla_present": row["vanilla_present"], "local_mod_present": row["local_mod_present"], "example": ev})})
            if sum(x["kind"] == "description_entry" for x in exact) >= 3:
                break

    route_ids = {str(row["id"]) for row in selected_routes}
    preferred_sources = set()
    source_weights: dict[str, int] = {}

    def add_preferred_sources(sources: Iterable[Any], weight: int = 0) -> None:
        for fragment in source_fragments(sources):
            preferred_sources.add(fragment)
            source_weights[fragment] = max(source_weights.get(fragment, 0), weight)

    for route in selected_routes:
        route_weight = route_score(normalized, route)
        add_preferred_sources(route.get("exact_sources", []), route_weight)
        for condition, target in route.get("expand_when", {}).items():
            # Conditional source expansion must actually match this question.
            if contains(normalized, str(condition)) or target in {a["id"] for a in selected_anchors}:
                add_preferred_sources([target], route_weight)
        for anchor_index, anchor_id in enumerate(route.get("required_anchors", [])):
            required = anchor_by_id.get(anchor_id)
            if required and required in selected_anchors:
                matched_anchor_score = anchor_score(normalized, required)
                # Later required anchors are generally the route's more
                # specific risk check (for example AOE repetition after
                # generic target scope), so let them break shared-source ties
                # only when that specific check is present in this query.
                anchor_weight = (
                    route_weight
                    + 4
                    + matched_anchor_score * 4
                    + (anchor_index * 30 if matched_anchor_score else 0)
                )
                add_preferred_sources(required.get("source_refs", []), anchor_weight)
    for anchor in selected_anchors:
        add_preferred_sources(anchor.get("source_refs", []), anchor_score(normalized, anchor))
    semantic_terms = [
        signal
        for route in selected_routes
        for signal in route.get("signals", [])
    ] + [
        trigger
        for anchor in selected_anchors
        for trigger in anchor.get("triggers", [])
    ]
    cards = [
        row
        for _, row in ranked(
            [r for r in load_jsonl("mechanic_cards.jsonl") if include_history or r.get('retrieval_status') not in ('historical','withdrawn','superseded')],
            lambda row: card_score(
                normalized,
                route_ids,
                row,
                preferred_sources,
                semantic_terms,
                source_weights,
            ),
        )[:3]
    ]
    records: list[dict[str, Any]] = []
    for row in vanilla_matches(query):
        refs = "; ".join(f"{s['path']}:{s['line']}" for s in row["source_refs"][:3])
        records.append({"type": "vanilla_content", "id": row["id"], "text": compact([row.get("name_zh"), row.get("name_en"), row.get("aliases"), row["summary"]], 900), "path": "RAG/vanilla_content.jsonl | " + refs})

    # Task-specific conclusions and exact fields must survive small budgets.
    focused = [anchor for anchor in selected_anchors if anchor['id'] in direct_anchor_ids]
    def append_anchor(anchor: dict[str, Any]) -> None:
        path = compact(anchor.get("source_refs"), 240)
        sections = anchor.get("source_sections", [])
        if sections:
            path += " | 定位: " + "; ".join(str(section) for section in sections)
        records.append({"type": "anchor", "id": anchor["id"], "text": query_excerpt(anchor.get("claim"), normalized, 550), "path": path,
                        "evidence_level":anchor.get('evidence_level'), "requires":anchor.get('requires',[]),
                        "excerpted":len(str(anchor.get('claim',''))) > 550})
    # A typed dotted field is an explicit lookup. Natural-language mechanism
    # questions get their decisive conclusions before generic field skeletons.
    if not fields:
        for anchor in focused:
            append_anchor(anchor)
    for row in exact:
        records.append({"type": row["kind"], "id": row["id"], "text": row["summary"], "path": row["path"]})
    if fields:
        for anchor in focused:
            append_anchor(anchor)
    for row in cards:
        span = row.get('source_span',{})
        summary = query_excerpt(row.get('abstract'),normalized,580)
        if row.get('summary_drift'):
            summary = '[定制摘要的来源正文已变化；先核对原节] ' + summary
        records.append({"type":"mechanic_card", "id":row['id'], "text":summary,
                        "path":row['doc_path'] + (f":{span['start_line']}" if span else ''),
                        "source_span":span, "excerpted":row.get('full_characters',0)>580})
    for anchor in selected_anchors:
        if anchor not in focused:
            append_anchor(anchor)
    for route in selected_routes:
        records.append({"type":"route", "id":route['id'], "text":compact(route.get('intent'),180), "path":"RAG/agent_routes.jsonl"})

    kept: list[dict[str, Any]] = []
    used = 0
    for record in records:
        size = len(record["text"]) + len(record["id"]) + len(record["path"]) + 30
        if len(kept) >= max_records or used + size > budget:
            continue
        kept.append(record)
        used += size
    return {
        "query": query,
        "explicit_fields": sorted(fields),
        "excluded_mechanisms": excluded_mechanisms,
        "routes": [row["id"] for row in selected_routes],
        "records": kept,
        "used_characters": used,
        "budget_characters": budget,
        "related":related_records([r['id'] for r in kept], limit=6),
        "next_step":"Read decisive records first; expand their exact sections or --record ID --related when needed. Distinguish confirmed premises, deductions, and engine hypotheses; links do not limit possible associations. Missing hits are not unknown facts.",
    }


def related_records(ids: Iterable[str], limit: int = 12) -> list[dict[str, Any]]:
    selected = set(ids)
    result = []
    seen = set()
    # Required predecessors before optional cross-links; no automatic text load.
    edges = sorted(load_jsonl('agent_relation_edges.jsonl'), key=lambda r:({'requires':0,'source':1,'section_of':2,'see_also':3}.get(r.get('relation'),4),str(r.get('to'))))
    for edge in edges:
        if edge.get('from') in selected and edge.get('to') not in selected:
            key=(edge.get('to'),edge.get('relation'))
            if key not in seen:
                seen.add(key); result.append(edge)
    return result[:limit]


def lookup_record(ident: str, related: bool = False) -> dict[str, Any]:
    if ident.startswith('document:'):
        relative = ident.removeprefix('document:')
        path = (ROOT/relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError('Document not found: '+ident)
        return {'id':ident,'doc_path':relative,'text':path.read_text(encoding='utf-8'),
                'related':related_records([ident]) if related else []}
    files=('agent_anchor_cards','mechanic_cards','agent_routes','effect_keywords','info_fields',
           'buff_stat_types','buff_rule_types','buff_duration_types','mechanics','vanilla_content')
    for file in files:
        row = next((r for r in load_jsonl(file+'.jsonl') if r.get('id')==ident),None)
        if row:
            result=dict(row)
            if row.get('source_span'):
                span=row['source_span']
                lines=(ROOT/row['doc_path']).read_text(encoding='utf-8').splitlines()
                result['section_text']='\n'.join(lines[span['start_line']-1:span['end_line']])
            if related:
                result['related']=related_records([ident])
            return result
    raise ValueError('Record not found: '+ident)


def main() -> None:
    # The desktop shell may decode subprocess output as UTF-8 even when
    # Python inherited a legacy Windows code page.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Return a compact, route-first DD knowledge pack.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--query", help="Task summary, preferably with file type and explicit fields.")
    selector.add_argument('--record', help='Expand one stable ID, including exact section and metadata.')
    parser.add_argument('--related', action='store_true', help='Show one-hop relations for --record.')
    parser.add_argument('--include-history', action='store_true', help='Allow historical or withdrawn cards in search.')
    parser.add_argument("--budget", type=int, default=6000, help="Maximum output characters, default: 6000.")
    parser.add_argument("--max-records", type=int, default=10, help="Maximum returned records, default: 10.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()
    from kb_update import notify
    notify(ROOT)
    if args.record:
        print(json.dumps(lookup_record(args.record,args.related),ensure_ascii=False,indent=2))
        return
    pack = make_pack(args.query, max(800, args.budget), max(1, args.max_records),args.include_history)
    if args.json:
        print(json.dumps(pack, ensure_ascii=False, indent=2))
        return
    print(f"Query: {pack['query']}")
    if pack["explicit_fields"]:
        print("Exact fields: " + ", ".join(pack["explicit_fields"]))
    if pack["excluded_mechanisms"]:
        print("Excluded mechanisms (constraints, not requested implementations): " + ", ".join(pack["excluded_mechanisms"]))
    print("Routes: " + ", ".join(pack["routes"]))
    for record in pack["records"]:
        print(f"\n[{record['type']}] {record['id']}\n{record['text']}\nSource: {record['path']}")
    print(f"\nBudget: {pack['used_characters']}/{pack['budget_characters']} characters")
    if pack['related']:
        print('Related (optional, not loaded): '+ '; '.join(f"{r['relation']} -> {r['to']}" for r in pack['related']))
    print(pack["next_step"])


if __name__ == "__main__":
    main()
