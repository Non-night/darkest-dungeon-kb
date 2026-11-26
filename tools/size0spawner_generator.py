from __future__ import annotations

"""Generate a local Size-0 template from the Size0Spawner resource template.

This utility deliberately generates the resource/base-Info template only. It does
not invent spawn, hp_reaction, max-HP expansion, sentinel, or death-gate logic.
Those behaviors remain documented in Mechanics/05-size0召唤物.md and related pages.
"""

import argparse
import json
import re
import shutil
import sys
from xml.sax.saxutils import quoteattr
from pathlib import Path


DEFAULT_TEMPLATE_ROOT = Path(__file__).resolve().parent / "size0spawner_template"
RACE_RE = re.compile(r"^[A-Z0-9]$")
FORBIDDEN_NAME_CHARS = set('<>:"/\\|?*')
TEXT_SUFFIXES = {".darkest", ".atlas"}


def fail(message: str) -> "NoReturn":
    raise ValueError(message)


def validate_identifier(value: str, label: str) -> str:
    item = value.strip()
    if not item:
        fail(f"{label} 不能为空。")
    if any(ch.isspace() for ch in item):
        fail(f"{label} 不能包含空白。")
    if any(ch in FORBIDDEN_NAME_CHARS for ch in item):
        fail(f"{label} 包含 Windows 路径或文件名非法字符：{item!r}")
    if item in {".", ".."}:
        fail(f"{label} 不能是 . 或 ..。")
    return item


def validate_size0_name(value: str) -> str:
    return validate_identifier(value, "size0 名称")


def parse_races(values: list[str]) -> list[str]:
    races: list[str] = []
    for raw in values:
        for item in raw.replace(",", " ").split():
            race = item.strip().upper()
            if not RACE_RE.fullmatch(race):
                fail(f"此生成工具目前只接受已确认的单个 A-Z 或 0-9 差分；多字符后缀不合法，@/# 仍待确认：{item!r}")
            if race not in races:
                races.append(race)
    if not races:
        fail("至少需要一个差分，默认差分为 A。")
    return races


def parse_enemy_types(values: list[str] | None) -> list[str] | None:
    if values is None:
        return None
    result: list[str] = []
    for raw in values:
        for item in raw.replace(",", " ").split():
            enemy_type = validate_identifier(item, "enemy_type")
            if enemy_type not in result:
                result.append(enemy_type)
    if not result:
        fail("--enemy-types 至少需要一个 enemy_type ID。")
    return result


def locate_template(root: Path) -> tuple[Path, Path]:
    anim = root / "anim"
    base_race = root / "monster_xxx_A"
    if not root.is_dir():
        fail(f"找不到模板目录：{root}")
    if not anim.is_dir():
        fail(f"模板缺少 anim 目录：{anim}")
    if not base_race.is_dir():
        fail(f"模板缺少 monster_xxx_A 目录：{base_race}")
    required = [
        base_race / "monster_xxx_A.info.darkest",
        base_race / "monster_xxx_A.art.darkest",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        fail("模板缺少基础文件：" + ", ".join(missing))
    return anim, base_race


def renamed_filename(filename: str, size0: str, race: str | None = None) -> str:
    result = filename
    if race is not None:
        result = result.replace("monster_xxx_A", f"{size0}_{race}")
    return result.replace("monster_xxx", size0)


def render_text(path: Path, size0: str) -> str:
    text = path.read_text(encoding="utf-8")
    return text.replace("monster_xxx", size0)


def render_info(path: Path, size0: str, enemy_types: list[str] | None) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    output: list[str] = []
    inserted = False
    for line in lines:
        if line.strip().startswith("enemy_type:"):
            if not inserted:
                if enemy_types is None:
                    # Keep the source placeholder visible so the caller must make
                    # an explicit enemy_type decision instead of inheriting a
                    # base-class naming habit silently.
                    output.append(line)
                else:
                    output.extend(f'enemy_type: .id "{enemy_type}"\n' for enemy_type in enemy_types)
                inserted = True
            continue
        output.append(line.replace("monster_xxx", size0))
    if not inserted and enemy_types is not None:
        output.extend(f'enemy_type: .id "{enemy_type}"\n' for enemy_type in enemy_types)
    return "".join(output)


def write_text_no_bom(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def copy_one(source: Path, target: Path, size0: str, enemy_types: list[str] | None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() in TEXT_SUFFIXES:
        if source.name.endswith(".info.darkest"):
            text = render_info(source, size0, enemy_types)
        else:
            text = render_text(source, size0)
        if source.suffix.lower() == ".atlas":
            atlas_lines = text.splitlines()
            expected_png = target.with_suffix(".png").name
            if not atlas_lines or atlas_lines[0] != "":
                fail(f"Atlas 第一行必须为空行：{source}")
            if len(atlas_lines) < 2 or atlas_lines[1].strip() != expected_png:
                actual = atlas_lines[1].strip() if len(atlas_lines) >= 2 else "<missing>"
                fail(f"Atlas 第二行必须严格匹配对应 PNG 文件名：期望 {expected_png!r}，实际 {actual!r}，文件 {source}")
        write_text_no_bom(target, text)
    else:
        shutil.copy2(source, target)


def collect_jobs(anim: Path, base_race: Path, target_root: Path, size0: str, races: list[str]) -> list[tuple[Path, Path]]:
    jobs: list[tuple[Path, Path]] = []
    for source in sorted(path for path in anim.rglob("*") if path.is_file()):
        relative = source.relative_to(anim)
        target = target_root / "anim" / renamed_filename(str(relative), size0)
        jobs.append((source, target))
    for race in races:
        race_root = target_root / f"{size0}_{race}"
        for source in sorted(path for path in base_race.rglob("*") if path.is_file()):
            relative = source.relative_to(base_race)
            target = race_root / renamed_filename(str(relative), size0, race)
            jobs.append((source, target))
    return jobs


def render_name_localization(size0: str, races: list[str]) -> str:
    lines = ['<?xml version="1.0" encoding="utf-8"?>', '<root>']
    for language in ("english", "schinese"):
        lines.append(f'  <language id="{language}">')
        for race in races:
            entry_id = quoteattr(f"str_monstername_{size0}_{race}")
            lines.append(f'    <entry id={entry_id}><![CDATA[]]></entry>')
        lines.append('  </language>')
    lines.append('</root>')
    return "\n".join(lines) + "\n"


def generate(
    size0: str,
    output: Path,
    template_root: Path,
    races: list[str],
    enemy_types: list[str] | None,
    dry_run: bool,
) -> dict[str, object]:
    anim, base_race = locate_template(template_root)
    target_root = output / size0
    if target_root.exists():
        fail(f"输出目录已存在，为避免覆盖请更换输出目录或 size0 名称：{target_root}")
    jobs = collect_jobs(anim, base_race, target_root, size0, races)
    if not jobs:
        fail("模板中没有可复制的文件。")
    name_file = target_root / "_mod_support" / "localization" / f"{size0}.size0.string_table.xml"
    if not dry_run:
        for source, target in jobs:
            copy_one(source, target, size0, enemy_types)
        name_file.parent.mkdir(parents=True, exist_ok=True)
        write_text_no_bom(name_file, render_name_localization(size0, races))
    return {
        "size0_base_class": size0,
        "races": races,
        "enemy_types": enemy_types if enemy_types is not None else ["<template placeholder: choose explicitly>"],
        "template_root": str(template_root),
        "output_root": str(target_root),
        "dry_run": dry_run,
        "files": [str(target.relative_to(target_root)) for _, target in jobs] + [str(name_file.relative_to(target_root))],
        "localization_deployment": "把 _mod_support/localization 内文件部署到 Mod 根目录 localization 并编译；此配套目录不是怪物资源目录。已提供 english、schinese；其他支持语言按设计补齐。",
        "cleanup_guidance": "size0 善后优先使用匹配实际 enemy_type 的 kill_enemy_types；只有确认该方式在具体调用环境失效或不适用时，才考虑 kill 1。",
        "next_step": "这是资源/基础 Info-Art 模板；仍需按 size0Spawner 专题补齐 spawn、hp_reaction、最大生命扩展、sentinel 和其他逻辑。",
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="从知识库内置模板生成本地 size-0 Info/Art/anim 基础模板。"
    )
    parser.add_argument("--name", required=True, help="目标怪物大类/资源分组 ID，例如 my_size0；它不等于 enemy_type 的强制值")
    parser.add_argument("--output", required=True, type=Path, help="生成根目录；工具会创建 <output>/<name>")
    parser.add_argument("--template-root", type=Path, default=DEFAULT_TEMPLATE_ROOT, help="模板目录，默认使用知识库内置模板")
    parser.add_argument("--races", nargs="+", default=["A"], help="单字符小类差分，例如 A B 1；本工具当前仅接收已确认的 A-Z/0-9，@/# 待确认；多字符禁止；默认 A")
    parser.add_argument("--enemy-types", nargs="+", default=None, help="显式写入一个或多个 enemy_type ID，例如 --enemy-types sz0_probe sz0_logic；省略时保留模板占位符")
    parser.add_argument("--dry-run", action="store_true", help="只检查并列出将生成的文件，不写入磁盘")
    args = parser.parse_args()
    try:
        result = generate(
            validate_size0_name(args.name),
            args.output.resolve(),
            args.template_root.resolve(),
            parse_races(args.races),
            parse_enemy_types(args.enemy_types),
            args.dry_run,
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

