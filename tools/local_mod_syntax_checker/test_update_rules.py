"""Regression coverage for the accepted build 28385 syntax inventory."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from checker import Checker, KB

DIRECTORY = Path(__file__).parent
RULES = json.loads((DIRECTORY / "update_rules.json").read_text(encoding="utf-8"))


class UpdateRulesTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="dd-update-rules-")
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)

    def write(self, name, text):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def check(self, compiled=False, *extra):
        if compiled:
            runtime = shutil.which("dotnet")
            assembly = DIRECTORY / "bin/Debug/net8.0/LocalModSyntaxChecker.dll"
            if not runtime or not assembly.is_file():
                self.skipTest("需要已构建的内置 C# 入口")
            command = [runtime, str(assembly)]
        else:
            command = [sys.executable, str(DIRECTORY / "checker.py")]
        result = subprocess.run([*command, "--root", str(self.root), "--json", *extra],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertIn(result.returncode, (0, 1), result.stdout + result.stderr)
        data = json.loads(result.stdout)
        return [{key.lower(): value for key, value in issue.items()}
                for issue in data.get("diagnostics", data.get("Diagnostics", []))]

    def populate_valid(self):
        values = {"string": '"TEST_ID"', "number": "2", "numeric_boolean": "1",
                  "boolean": "true", "integer": "3"}
        lines = [f'effect: .name "FIELD_{index}" .target performer {field} {values[kind]}'
                 for index, (field, kind) in enumerate(RULES["effect_arguments"].items())]
        lines.extend(f'effect: .name "TARGET_{index}" .target {target}'
                     for index, target in enumerate(RULES["effect_targets"]))
        lines.extend([
            'effect: .name "GUARD" .target performer .chance -1 .guard 1 .on_hit true .force_resist_type poison',
            'effect: .name "TRINKET" .target other_trinket .trigger_limit_minimum_increase 1',
        ])
        self.write("effects/update.effects.darkest", "\n".join(lines))
        self.write("heroes/test/test.info.darkest", "\n".join(
            f"{header} {field} true" for header, fields in RULES["info_boolean_fields"].items()
            for field in fields))
        checker = Checker(self.root, [])
        buff = {"id": "TEST", "stat_type": "crit_dmg_add", "stat_sub_type": "", "amount": 1,
                "rule_type": "always", "is_false_rule": False, "remove_if_not_active": False,
                "rule_data": {"float": 0, "string": ""}, "force_negative": True}
        buff.update({field: [] for field in checker.buff_fields if field.endswith("_additional_effect_ids")})
        self.write("shared/buffs/update.buffs.json", json.dumps({"buffs": [buff]}))

    def assert_valid(self, compiled):
        self.populate_valid()
        issues = self.check(compiled)
        self.assertFalse([issue for issue in issues if issue["severity"] == "error"], issues)
        self.assertFalse([issue for issue in issues if issue["code"] in {
            "BUFF-UNKNOWN_FIELD", "VSIX-EFFECT-GUARD-CHANCE", "VSIX-EFFECT-TRINKET-TARGET"}], issues)

    def test_dot_paths_ignored_in_scan_and_reference_index(self):
        self.write("mod/.backups/snapshot/effects/old.effects.darkest",
                   '\ufeffeffect: .name "BACKUP" .target performer\n')
        self.write("mod/effects/.alternate/old.effects.darkest",
                   '\ufeffeffect: .name "LOCAL_DOT_DIR" .target performer\n')
        self.write("mod/effects/.draft.effects.darkest",
                   '\ufeffeffect: .name "LOCAL_DOT_FILE" .target performer\n')
        self.write("refs/.staging/effects/old.effects.darkest",
                   'effect: .name "REF_DOT_DIR" .target performer\n')
        self.write("refs/effects/.draft.effects.darkest",
                   'effect: .name "REF_DOT_FILE" .target performer\n')
        self.write("refs/effects/live.effects.darkest",
                   'effect: .name "LIVE" .target performer\n')
        self.write(".dot-ref/effects/old.effects.darkest",
                   'effect: .name "DOT_ROOT" .target performer\n')
        hidden_ids = ("BACKUP", "LOCAL_DOT_DIR", "LOCAL_DOT_FILE", "REF_DOT_DIR", "REF_DOT_FILE", "DOT_ROOT")
        references = ' '.join(f'"{effect_id}"' for effect_id in (*hidden_ids, "LIVE"))
        self.write("mod/heroes/probe/probe.info.darkest",
                   f'combat_skill: .id "probe" .level 0 .effect {references}\n')
        self.write("mod/effects/visible.effects.darkest",
                   '\ufeffeffect: .name "VISIBLE" .target performer\n')
        workspace = self.root
        self.root = workspace / "mod"
        for compiled in (False, True):
            with self.subTest(compiled=compiled):
                diagnostics = self.check(compiled, "--strict-references", "--reference-root", str(workspace / "refs"),
                                         "--reference-root", str(workspace / ".dot-ref"))
                bom_files = [item["file"] for item in diagnostics if item["code"] == "KB-ENC-UTF8-BOM"]
                self.assertEqual(bom_files, ["effects/visible.effects.darkest"], diagnostics)
                self.assertFalse(any(item["code"] == "KB-EFFECT-WRONG-DIRECTORY" for item in diagnostics), diagnostics)
                unresolved = [item["message"] for item in diagnostics if item["code"] == "KB-REF-EFFECT-NOT-FOUND"]
                self.assertEqual(len(unresolved), len(hidden_ids), diagnostics)
                for effect_id in hidden_ids:
                    self.assertTrue(any(f"'{effect_id}'" in message for message in unresolved), diagnostics)

    def test_python_accepts_inventory_fields_and_targets(self):
        self.assert_valid(False)

    def test_compiled_accepts_inventory_fields_and_targets(self):
        self.assert_valid(True)

    def assert_invalid(self, compiled):
        self.populate_valid()
        lines = [f'effect: .name "BAD_{index}" .target performer {field}'
                 for index, field in enumerate(RULES["effect_arguments"])]
        lines.extend([
            'effect: .name "BAD_BOOLEAN" .suppress_bark maybe',
            'effect: .name "BAD_NUMBER" .health_damage_percent nonsense',
            'effect: .name "BAD_INTEGER" .set_trigger_limit 1.5',
            'effect: .name "QUOTED_BOOLEAN" .cure_burn "1"',
            'effect: .name "BAD_TARGET" .target performer_adjacent_typo',
            'effect: .name "BAD_FIELD" .fake_update_keyword true',
        ])
        self.write("effects/invalid.effects.darkest", "\n".join(lines))
        self.write("heroes/test/test.info.darkest", "\n".join(
            [f"{header} {field} maybe" for header, fields in RULES["info_boolean_fields"].items()
             for field in fields] + ["weapon: .force_selection true", "combat_skill: .ignore_hp_scale true",
                                    "combat_skill: .ai_valid", "combat_skill: .skill_visible true false"]))
        buff_path = self.root / "shared/buffs/update.buffs.json"
        data = json.loads(buff_path.read_text(encoding="utf-8"))
        buff = data["buffs"][0]
        buff.update({field: 17 for field in buff if field.endswith("_additional_effect_ids")})
        buff["force_negative"] = "not_boolean"
        buff["unknown_update_field"] = True
        self.write("shared/buffs/update.buffs.json", json.dumps(data))
        issues = self.check(compiled)
        codes = {issue["code"] for issue in issues}
        self.assertTrue({"KB-UPDATE-EFFECT-ARGUMENT", "KB-UPDATE-INFO-ARGUMENT",
                         "VSIX-INFO-INVALID-KEYWORD", "VSIX-EFFECT-INVALID-VALUE",
                         "VSIX-EFFECT-INVALID-KEYWORD", "VSIX-EFFECT-QUOTED-NUMERIC-BOOL",
                         "BUFF-UNKNOWN_FIELD"}.issubset(codes), issues)
        invalid_buffs = [issue for issue in issues if issue["severity"] == "error" and issue["code"].startswith("BUFF-")]
        self.assertGreaterEqual(len(invalid_buffs), 26, invalid_buffs)

    def test_python_rejects_invalid_update_values(self):
        self.assert_invalid(False)

    def test_compiled_rejects_invalid_update_values(self):
        self.assert_invalid(True)

    def test_entire_update_inventory_has_explicit_coverage(self):
        checker = Checker(self.root, [])
        inventory = json.loads((KB / RULES["source"]).read_text(encoding="utf-8"))["items"]
        partial = {"specific_recruit", "event_cost + embark_party_buff", "effect", "has_description",
                   "evolution_duration_type", "move_skill_additional_effects", "quest_start_additional_effects",
                   "combat_start_additional_effects", "turn_start_additional_effects"}
        for item in inventory:
            field = item["identifier"]
            with self.subTest(field=field):
                if item["object"] == "effect_keyword":
                    self.assertIn(field, RULES["effect_arguments"])
                elif item["object"] == "effect_target":
                    self.assertIn(field, checker.effect_values[".target"])
                elif item["object"] == "buff_stat_type":
                    self.assertIn(field, checker.effect_values[".buff_type"])
                elif item["object"] == "buff_trigger_field" or field == "force_negative":
                    self.assertIn(field, checker.buff_fields)
                elif item["object"] in RULES["info_boolean_fields"]:
                    self.assertIn(field, RULES["info_boolean_fields"][item["object"]])
                else:
                    self.assertIn(field, partial | set(RULES["runtime_only"]))

    def test_partial_domains_are_not_silently_passed(self):
        for domain in RULES["partial_domains"]:
            self.write(f"{domain}/probe.json", "{}")
        for compiled in (False, True):
            issues = self.check(compiled)
            partial = [issue for issue in issues if issue["code"] == "KB-COVERAGE-PARTIAL"]
            self.assertEqual(len(partial), 4, issues)

    def test_buff_root_array_is_diagnostic_not_crash(self):
        self.write("shared/buffs/invalid.buffs.json", '{"buffs": 17}')
        issues = self.check()
        self.assertTrue(any(issue["code"] == "BUFF-MISSING-BUFFS" for issue in issues), issues)

    def test_new_json_fields_in_real_domain_paths(self):
        files = {
            "trinkets/update.entries.trinkets.json": {"entries": [{"id": "TEST", **{
                field: [] for field in RULES["json_fields"]["trinkets"]}}]},
            "raid/camping/update.camping_skills.json": {"skills": [{"effects": [
                {"type": "effect", "sub_type": "TEST", "has_description": False}]}]},
            "campaign/town_events/update.town_events.events.json": {"events": [{"data": [
                {"type": "specific_recruit", "string_data": "crusader", "number_data": 4}]}]},
            "shared/quirk/update.quirk_library.json": {"quirks": [
                {"evolution_duration_type": value} for value in ("combat_end", "quest_end")]},
        }
        for name, data in files.items():self.write(name, json.dumps(data))
        for compiled in (False, True):
            issues = self.check(compiled)
            self.assertFalse([issue for issue in issues if issue["severity"] == "error"], issues)
            self.assertEqual(sum(issue["code"] == "KB-COVERAGE-PARTIAL" for issue in issues), 4, issues)
        for name in files:
            self.write(name, json.dumps({
                "entries": [{"id": "TEST", "quest_start_additional_effects": 17}],
                "effects": [{"type": "effect", "has_description": "false"}],
                "data": [{"type": "specific_recruit", "string_data": "TEST", "number_data": True}],
                "evolution_duration_type": "quest_complete",
            }))
        for compiled in (False, True):
            issues = self.check(compiled)
            self.assertGreaterEqual(sum(issue["code"] == "KB-UPDATE-JSON-ARGUMENT" for issue in issues), 5, issues)

    def test_activated_rule_no_longer_blocks_additional_effects(self):
        self.write("shared/buffs/update.buffs.json", json.dumps({"buffs": [{
            "id": "TEST", "stat_type": "crit_dmg_add", "stat_sub_type": "", "amount": 1,
            "rule_type": "activated_first", "is_false_rule": False, "remove_if_not_active": True,
            "rule_data": {"float": 0, "string": ""}, "attack_additional_effect_ids": ["TEST"]}]}))
        issues = self.check(True)
        self.assertNotIn("BUFF-ACTIVATED_RULE_ADDITIONAL_EFFECTS_UNREACHABLE", {issue["code"] for issue in issues})


if __name__ == "__main__":
    unittest.main()
