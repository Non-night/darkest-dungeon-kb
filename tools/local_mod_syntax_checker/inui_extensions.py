"""Detect documented Inui extensions from the current game session."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess


EXTENSIONS = ("buff_icon", "custom_type_effects", "dd_immune", "hero_level_cap")
IMMUNITIES = {"kill", "control", "capture"}
TYPE_FIELD = re.compile(r"(.+)_type_additional_effect(?:_ids|s)\Z")
JSON_STRING_OR_COMMENT = re.compile(r'"(?:[^"\\]|\\.)*"|//[^\r\n]*|/\*.*?\*/', re.S)


def strip_json_comments(text: str) -> str:
    # Keep diagnostic line and column numbers aligned with the source.
    return JSON_STRING_OR_COMMENT.sub(
        lambda m: m[0] if m[0].startswith('"') else re.sub(r"[^\r\n]", " ", m[0]), text
    )


def running_games() -> list[dict]:
    if os.name != "nt":
        return []
    script = r'''
$items = @(Get-Process -Name Darkest -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        if ($_.Path -and ([IO.Path]::GetFileName((Split-Path $_.Path))) -ieq 'win64') {
            [pscustomobject]@{
                executable = $_.Path
                started = [DateTimeOffset]::new($_.StartTime).ToUnixTimeMilliseconds()
                modules = @($_.Modules | Where-Object { $_.FileName } | ForEach-Object FileName)
            }
        }
    } catch {}
})
ConvertTo-Json -InputObject $items -Compress -Depth 3
'''
    try:
        powershell = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32/WindowsPowerShell/v1.0/powershell.exe"
        # Path strings in the process output can contain non-ASCII characters.
        script = "[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)\n" + script
        result = subprocess.run([str(powershell), "-NoProfile", "-NonInteractive", "-Command", script],
                                capture_output=True, encoding="utf-8", timeout=5, check=True)
        return json.loads(result.stdout)
    except (OSError, ValueError, UnicodeError, subprocess.SubprocessError):
        return []


def active_features(game: Path, sessions: list[dict]) -> set[str]:
    executables = {game / folder / "Darkest.exe" for folder in ("win64", "_windows/win64", "_windowsnosteam/win64")}
    sessions = [s for s in sessions if Path(s["executable"]).resolve() in executables]
    if len(sessions) != 1:
        return set()
    session = sessions[0]
    exe = Path(session["executable"]).resolve()
    modules = {Path(name).resolve() for name in session["modules"]}
    if exe.with_name("dbghelp.dll") not in modules:
        return set()
    started_ms = session["started"]
    active = set()
    for name in EXTENSIONS:
        plugin = game / "mods/DD Mod Lib" / f"{name}.dll"
        log = game / "DDModLoader/log" / f"{name}.log"
        try:
            if not plugin.is_file() or plugin.resolve() not in modules:
                continue
            stat = log.stat()
            birth_ns = getattr(stat, "st_birthtime_ns", stat.st_ctime_ns)
            if min(birth_ns, stat.st_mtime_ns) // 1_000_000 < started_ms or stat.st_size > 8_000_000:
                continue
            text = log.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if re.search(r"\[FAIL\]|incompatible game version|hooks? (?:are )?not installed", text, re.I):
            continue
        if name == "buff_icon" and "All hooks installed and enabled successfully." in text:
            active.add(name)
        elif name == "custom_type_effects" and "CollectEffects detour installed" in text:
            active.add(name)
        elif name == "dd_immune" and "[DIAG] immune detour hit:" in text:
            active.add(name)
        elif name == "hero_level_cap":
            # The manual identifies the install summary and four successful writes.
            install = text.partition("installed:")[2]
            writes = re.findall(r"\bwriteback=(true|false)\b", install)
            if writes == ["true"] * 4:
                active.add(name)
    return active


def detect(game: Path | None) -> set[str]:
    if game is None or not (game / "mods/DD Mod Lib").is_dir():
        return set()
    return active_features(game, running_games())


def check_info(header: str, tail: str, hero: bool) -> str | None:
    if header == "level_cap:" and hero:
        match = re.fullmatch(r"\s*(?:\.(?:max|cap)\s+)?([+-]?[0-9]+)\s*", tail)
        if match:
            return None
        return "level_cap: 需要一个整数，可用 .max 或 .cap。"
    tokens = iter(re.findall(r"[^\s,]+", tail.lower()))
    for token in tokens:
        if token in IMMUNITIES:
            continue
        if token.startswith(".") and token[1:] in IMMUNITIES and next(tokens, "") in {"true", "false", "1", "0"}:
            continue
        return f"immune: 不支持参数 {token}。"
    return None


def game_for_mod(mod: Path) -> Path | None:
    """Resolve only the installation enclosing this local/Workshop Mod."""
    for parent in mod.parents:
        if parent.name.casefold() == "darkestdungeon" and parent / "mods" in mod.parents:
            return parent
        if tuple(x.casefold() for x in parent.parts[-4:]) == ("steamapps", "workshop", "content", "262060"):
            game = parent.parents[2] / "common/DarkestDungeon"
            return game if game.is_dir() else None
    return None
