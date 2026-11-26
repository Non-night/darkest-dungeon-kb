"""Focused integration tests for the read-only local syntax checker."""
from __future__ import annotations

import json
import os
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).with_name("checker.py")


class CheckerIntegrationTests(unittest.TestCase):
    def test_project_workshop_id_is_optional_in_every_upload_mode(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-project-metadata-") as temp:
            root = Path(temp)
            for mode in ("dont_submit", "direct_upload", "copy_and_upload", "strip_and_upload"):
                for workshop_id in ("", "<PublishedFileId/>", "<PublishedFileId>123456789</PublishedFileId>"):
                    with self.subTest(mode=mode, workshop_id=workshop_id):
                        (root / "project.xml").write_text(
                            "<project><Title>Local test</Title><VersionMajor>1</VersionMajor>"
                            "<VersionMinor>0</VersionMinor><TargetBuild>28385</TargetBuild>"
                            f"<UploadMode>{mode}</UploadMode>{workshop_id}</project>",
                            encoding="utf-8",
                        )
                        code, result = self.run_checker(root)
                        self.assertEqual(code, 0)
                        self.assertEqual(result["diagnostics"], [])

    def test_project_still_reports_missing_title_and_malformed_xml(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-project-invalid-") as temp:
            root = Path(temp)
            project = root / "project.xml"
            project.write_text(
                "<project><VersionMajor>1</VersionMajor><VersionMinor>0</VersionMinor>"
                "<TargetBuild>28385</TargetBuild></project>", encoding="utf-8",
            )
            _, result = self.run_checker(root)
            self.assertEqual(len(result["diagnostics"]), 1, result["diagnostics"])
            self.assertEqual(result["diagnostics"][0]["code"], "PROJECT-FIELD-MISSING")
            self.assertIn("Title", result["diagnostics"][0]["message"])
            project.write_text("<project><Title>Broken</project>", encoding="utf-8")
            code, result = self.run_checker(root)
            self.assertEqual(code, 1)
            self.assertEqual([item["code"] for item in result["diagnostics"]], ["PROJECT-XML-MALFORMED"])

    def test_new_buff_types_and_dynamic_subtypes_are_accepted(self) -> None:
        import re
        no_subtypes = ["crit_dmg_multiply", "crit_dmg_add", "heal_crit_chance_add",
                       "heal_crit_chance_multiply", "hp_heal_amount_received"]
        dynamic = [("effect_chance", "PROBE_EFFECT"), ("disable_combat_skill", "PROBE_SKILL")]
        with tempfile.TemporaryDirectory(prefix="dd-new-buff-types-") as temp:
            root = Path(temp)
            (root / "effects").mkdir()
            lines = [
                f'effect: .name "PROBE_{index}" .target performer .chance 100% .buff_type {stat} .buff_amount 0.1'
                for index, stat in enumerate(no_subtypes)
            ]
            lines.extend(
                f'effect: .name "PROBE_DYNAMIC_{index}" .target performer .buff_type {stat} .buff_sub_type "{subtype}" .buff_amount 1'
                for index, (stat, subtype) in enumerate(dynamic)
            )
            (root / "effects" / "probe.effects.darkest").write_text("\n".join(lines)+"\n", encoding="utf-8")
            _, result = self.run_checker(root)
            self.assertEqual(result["error_count"], 0, result["diagnostics"])
            source = (PROJECT.parent / "vendor" / "BuffGrammarChecker.Core" / "BuffStatTypeRules.cs").read_text(encoding="utf-8")
            block = re.search(r"ValidStatTypes\s*=.*?\{(.*?)\};", source, re.S)
            self.assertIsNotNone(block)
            known = set(re.findall(r'"([^"]+)"', block.group(1)))
            self.assertTrue(set(no_subtypes + [stat for stat, _ in dynamic]).issubset(known))

    def test_new_buff_types_keep_subtype_and_unknown_value_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-new-buff-invalid-") as temp:
            root = Path(temp)
            (root / "effects").mkdir()
            (root / "effects" / "probe.effects.darkest").write_text(
                'effect: .name "BAD_HEAL" .target performer .buff_type heal_crit_chance_add .buff_sub_type "bad" .buff_amount 1\n'
                'effect: .name "MISSING_EFFECT" .target performer .buff_type effect_chance .buff_amount 1\n'
                'effect: .name "EMPTY_SKILL" .target performer .buff_type disable_combat_skill .buff_sub_type "" .buff_amount 1\n'
                'effect: .name "TYPO" .target performer .buff_type heal_crit_chance_typo .buff_amount 1\n'
                'effect: .name "NO_NEW_STEAL" .target performer .steal_buff_stat_type heal_crit_chance_add\n',
                encoding="utf-8",
            )
            _, result = self.run_checker(root)
            codes = {issue["code"] for issue in result["diagnostics"]}
            self.assertIn("VSIX-EFFECT-BUFF-SUBTYPE-UNEXPECTED", codes)
            self.assertIn("VSIX-EFFECT-BUFF-SUBTYPE-REQUIRED", codes)
            invalid = [issue for issue in result["diagnostics"] if issue["code"] == "VSIX-EFFECT-INVALID-VALUE"]
            self.assertTrue(any("heal_crit_chance_typo" in issue["message"] for issue in invalid))
            self.assertTrue(any(".steal_buff_stat_type" in issue["message"] for issue in invalid))

    def test_compiled_checker_accepts_new_buff_json_types(self) -> None:
        import shutil
        runtime = shutil.which("dotnet")
        assembly = PROJECT.parent / "bin" / "Debug" / "net8.0" / "LocalModSyntaxChecker.dll"
        if runtime is None or not assembly.is_file():
            self.skipTest("需要已构建的 .NET 检查器及 dotnet 运行时")
        with tempfile.TemporaryDirectory(prefix="dd-new-buff-json-") as temp:
            root = Path(temp)
            (root / "shared" / "buffs").mkdir(parents=True)
            definitions = [
                ("crit_dmg_multiply", ""), ("crit_dmg_add", ""),
                ("heal_crit_chance_add", ""), ("heal_crit_chance_multiply", ""),
                ("hp_heal_amount_received", ""), ("effect_chance", "PROBE_EFFECT"),
                ("disable_combat_skill", "PROBE_SKILL")
            ]
            buffs = [
                {"id": f"PROBE_{index}", "stat_type": stat, "stat_sub_type": subtype,
                 "amount": 0.1, "rule_type": "always", "is_false_rule": False,
                 "remove_if_not_active": False, "rule_data": {"float": 0, "string": ""}}
                for index, (stat, subtype) in enumerate(definitions)
            ]
            target = root / "shared" / "buffs" / "probe.buffs.json"
            target.write_text(json.dumps({"buffs": buffs}), encoding="utf-8")
            (root / "effects").mkdir()
            effect_lines = [
                f'effect: .name "PROBE_EFFECT_{index}" .target performer .buff_type {stat} .buff_amount 0.1'
                + (f' .buff_sub_type "{subtype}"' if subtype else "")
                for index, (stat, subtype) in enumerate(definitions)
            ]
            (root / "effects" / "probe.effects.darkest").write_text("\n".join(effect_lines)+"\n", encoding="utf-8")
            result = subprocess.run([runtime, str(assembly), "--root", str(root), "--json"],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for buff in buffs:
                buff["stat_sub_type"] = "unexpected" if buff["stat_type"] not in {"effect_chance", "disable_combat_skill"} else ""
            target.write_text(json.dumps({"buffs": buffs}), encoding="utf-8")
            result = subprocess.run([runtime, str(assembly), "--root", str(root), "--json"],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("UNEXPECTED_STAT_SUB_TYPE", result.stdout)
            self.assertIn("MISSING_STAT_SUB_TYPE_VALUE", result.stdout)
            self.assertNotIn("UNKNOWN_STAT_TYPE", result.stdout)

    def run_checker(self, root: Path, *extra: str) -> tuple[int, dict]:
        args = [sys.executable, str(PROJECT), "--root", str(root), "--json", *extra]
        game = Path(os.environ.get("DD_GAME_ROOT", str(Path(__file__).resolve().parents[2] / "DarkestDungeon")))
        if game.is_dir() and "--reference-root" not in args:
            args[4:4] = ["--reference-root", str(game)]
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 1 if json.loads(result.stdout)["error_count"] else 0, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def make_mod(self, root: Path) -> None:
        (root / "localization").mkdir(parents=True)
        (root / "heroes" / "hero").mkdir(parents=True)
        (root / "effects").mkdir()
        (root / "colours").mkdir()
        (root / "shared" / "buffs").mkdir(parents=True)
        (root / "localization" / "project_paths.txt").write_text("..", encoding="utf-8")
        (root / "colours" / "base.colours.darkest").write_text('colour: .id "TEST_COLOUR" .rgba 255 255 255 255\n', encoding="utf-8")
        long_id = "a" * 16 + " " + "b" * 15
        (root / "localization" / "local.string_table.xml").write_text(
            """<strings>
  <language id="english"><entry id="amount">{?count}%d {colour_start|TEST_COLOUR}cats{colour_end}</entry></language>
  <language id="schinese"><entry id="amount">{?count}%s {colour_start|MISSING_COLOUR}只猫{colour_end}</entry></language>
</strings>""",
            encoding="utf-8",
        )
        (root / "heroes" / "hero" / "hero.info.darkest").write_text(
            f"""mode: .id "stance"
mode: .id "stance" "extra"
combat_skill: .id "hit" .level 0 .valid_modes "stance" .condensed_tooltip_effects true .effect "EF_OK" "EF_MISSING" .stance_effects "EF_MISSING" .ghost_effects "MISSING" .stance_effects "EF_OK" "EF_OK" "EF_OK" "EF_OK" "EF_OK" "EF_OK" "EF_OK" .damage_heal_base_class_ids A B C D E .unknown_field true
spawn: .effects "{long_id}"
""",
            encoding="utf-8",
        )
        (root / "effects" / "test.effects.darkest").write_text(
            'effect: .name "EF_OK" .target performer .buff_ids BUFF_X BUFF_Y\n' +
            f'effect: .name "{long_id}" .target performer\n' +
            'effect: .name "BAD" .not_a_real_keyword true\n' +
            'effect: .name "DOT" .dotBleed 1 .dotPoison 1\n' +
            'effect: .name "SET" .target performer .set_mode "stance"\n',
            encoding="utf-8",
        )
        (root / "shared" / "buffs" / "broken.buffs.json").write_text("{", encoding="utf-8")
        (root / "shared" / "buffs" / "refs.buffs.json").write_text(
            '{"buffs":[{"id":"BUFF_X","attack_additional_effect_ids":["BUFF_EFFECT_MISSING"]},{"id":"BUFF_Y","attack_additional_effect_ids":[]}]}', encoding="utf-8"
        )
        (root / "heroes" / "hero" / "bom.info.darkest").write_bytes(
            bytes([0xEF, 0xBB, 0xBF]) + 'mode: .id "bom"\n'.encode("utf-8")
        )

    def test_reports_localization_mode_effect_buff_and_encoding_findings(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-syntax-test-") as temp:
            root = Path(temp)
            self.make_mod(root)
            _, result = self.run_checker(root)
            codes = [item["code"] for item in result["diagnostics"]]
            self.assertIn("LOC-PLACEHOLDER-MISMATCH", codes)
            self.assertIn("LOC-COLOR-NOT-FOUND", codes)
            self.assertIn("KB-REF-MODE-NOT-FOUND", codes)
            self.assertIn("KB-REF-EFFECT-NOT-FOUND", codes)
            self.assertTrue(any(item["code"] == "KB-REF-EFFECT-NOT-FOUND" and "EF_MISSING" in item["message"] and "当前用户" in item["source"] for item in result["diagnostics"]))
            self.assertIn("BUFF-INVALID_JSON", codes)
            self.assertIn("BUFF-MISSING-REQUIRED-FIELD", codes)  # linked Buff core validates valid-JSON semantics too
            self.assertIn("KB-SPAWN-EFFECT-ID-LENGTH-CONSERVATIVE", codes)
            self.assertIn("KB-SPAWN-EFFECT-ID-LENGTH-CONSERVATIVE", codes)
            self.assertIn("VSIX-EFFECT-INVALID-KEYWORD", codes)
            self.assertIn("VSIX-INFO-INVALID-KEYWORD", codes)
            self.assertIn("VSIX-INFO-SINGLE-ARG-COUNT", codes)
            self.assertNotIn("KB-REF-BUFF-NOT-FOUND", codes)
            self.assertFalse(any(item["code"] == "KB-REF-MODE-NOT-FOUND" and "stance" in item["message"] for item in result["diagnostics"]))
            self.assertIn("KB-ENC-UTF8-BOM", codes)
            # This static boolean field ends with _effects but is not a mode-specific Effect list.
            self.assertFalse(any(item["code"] == "KB-REF-MODE-NOT-FOUND" and "condensed_tooltip" in item["message"] for item in result["diagnostics"]))

    def test_strict_references_promote_unresolved_ids(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-syntax-strict-") as temp:
            root = Path(temp)
            self.make_mod(root)
            _, result = self.run_checker(root, "--strict-references")
            unresolved = [item for item in result["diagnostics"] if item["code"] in {"KB-REF-MODE-NOT-FOUND", "KB-REF-EFFECT-NOT-FOUND"}]
            self.assertTrue(unresolved)
            self.assertTrue(all(item["severity"] == "error" for item in unresolved))

    def test_reference_root_closes_mode_and_effect_ids(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-syntax-refs-") as temp:
            root = Path(temp) / "mod"
            refs = Path(temp) / "refs"
            root.mkdir()
            refs.mkdir()
            self.make_mod(root)
            ref_dlc=refs / "dlc" / "999999_test" / "features" / "sample"
            (ref_dlc / "heroes" / "external").mkdir(parents=True)
            (ref_dlc / "heroes" / "external" / "external.info.darkest").write_text('mode: .id "ghost"\n', encoding="utf-8")
            long_id = "a" * 16 + " " + "b" * 15
            (ref_dlc / "effects").mkdir()
            (ref_dlc / "effects" / "external.effects.darkest").write_text(
                'effect: .name "MISSING" .target performer\n'
                'effect: .name "EF_MISSING" .target performer\n'
                f'effect: .name "{long_id}" .target performer\n'
                , encoding="utf-8"
            )
            _, result = self.run_checker(root, "--strict-references", "--reference-root", str(refs))
            unresolved = [item for item in result["diagnostics"] if item["code"] in {"KB-REF-MODE-NOT-FOUND", "KB-REF-EFFECT-NOT-FOUND"}]
            self.assertFalse(unresolved, [item["message"] for item in unresolved])

    def test_xml_reader_honors_declared_encoding_and_requires_english(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-loc-xml-encoding-") as temp:
            root = Path(temp)
            loc = root / "localization"
            loc.mkdir(parents=True)
            xml = '<?xml version="1.0" encoding="utf-16"?><strings><language id="schinese" /></strings>'
            (loc / "table.string_table.xml").write_bytes(xml.encode("utf-16"))
            _, result = self.run_checker(root)
            codes = [item["code"] for item in result["diagnostics"]]
            self.assertIn("LOC-ENGLISH-BASELINE-MISSING", codes)
            self.assertNotIn("LOC-XML-MALFORMED", codes)


    def test_trinket_and_monster_layout_checks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-layout-") as temp:
            root = Path(temp) / "Mod"
            (root / "trinkets").mkdir(parents=True)
            bad_monster = root / "monsters" / "brigand" / "brigand_AA"
            bad_monster.mkdir(parents=True)
            (bad_monster / "brigand_AA.info.darkest").write_text("enemy_type: .id bad\n", encoding="utf-8")
            nested_monster = root / "monsters" / "cultist" / "cultist_A" / "nested"
            nested_monster.mkdir(parents=True)
            (nested_monster / "cultist_A.info.darkest").write_text("enemy_type: .id bad\n", encoding="utf-8")
            (root / "trinkets" / "mod.entries.trinkets.json").write_text(
                '{"entries":[{"id":"t","buffs":["MISSING_BUFF"],"rarity":"missing_rarity","visual_rarity":"missing_rarity"}]}',
                encoding="utf-8",
            )
            (root / "trinkets" / "mod.rarities.trinkets.json").write_text('{"rarities":[]}', encoding="utf-8")
            _, result = self.run_checker(root)
            codes = {item["code"] for item in result["diagnostics"]}
            self.assertIn("KB-MONSTER-SUBCLASS-NAME", codes)
            self.assertIn("KB-MONSTER-EXTRA-DIRECTORY", codes)
            self.assertIn("KB-REF-BUFF-NOT-FOUND", codes)
            self.assertIn("KB-REF-RARITY-NOT-FOUND", codes)
            self.assertIn("TRINKET-VISUAL-RARITY-SAME", codes)


    def test_vsix_effect_diagnostic_families_are_retained(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-vsix-parity-") as temp:
            root = Path(temp)
            effects = root / "effects"
            effects.mkdir(parents=True)
            lines = [
                'bad: .name "bad"',
                'plain_text_without_effect',
                'effect: .name "E" .cure 1 .cure_burn 1 .heal 1 .healstress 1 .dotBleed 1 .dotPoison 1',
                'effect: .name "E2" .target performer .spawn_target_actor_base_class_id base',
                'effect: .name "E3" .skill_instant true .target target',
                'effect: .name "E4" .use_item_id item',
                'effect: .name "E5" .buff_type combat_stat_add .buff_amount 1',
                'effect: .name "E6" .guard 1 .on_hit true .chance 0.5',
                'effect: .name "E7" .daze 1 .affliction_blockable_chance 1',
                'effect: .name "E8" .item true .cure "1" .cure_disease 1 .buff_source_type custom_source',
                'effect: .name "E9" .buff_duration_type none .steal_buff_source_type custom_source .steal_buff_stat_type unknown',
                'effect: .name "E10" .target performer .gain_trinket 1',
                'effect: .name "E11" .target performer .steal_buff_source_type bsrc_skill',
                'effect: .name "' + 'n'*65 + '" .target performer',
                'effect: .name "E12" .buff_ids ' + ' '.join('B'+str(i) for i in range(9)),
            ]
            (effects / "parity.effects.darkest").write_text("\n".join(lines) + "\n", encoding="utf-8")
            _, result = self.run_checker(root)
            codes = {item["code"] for item in result["diagnostics"]}
            expected = {
                "VSIX-EFFECT-INVALID-HEADER", "VSIX-EFFECT-OUTSIDE-BLOCK", "VSIX-EFFECT-CURE-CONFLICT",
                "VSIX-EFFECT-HEAL-ORDER", "VSIX-EFFECT-CURE-DISEASE-ORDER", "VSIX-EFFECT-DOT-CONFLICT", "VSIX-EFFECT-SPAWN-TARGET-ORDER",
                "VSIX-EFFECT-UNSAFE-TARGET", "VSIX-EFFECT-USE-ITEM-TYPE-REQUIRED",
                "VSIX-EFFECT-BUFF-SUBTYPE-REQUIRED", "VSIX-EFFECT-GUARD-CHANCE",
                "VSIX-EFFECT-DAZE-SUGGESTION", "VSIX-EFFECT-AFFLICTION-CHANCE",
                "VSIX-EFFECT-INVALID-VALUE", "VSIX-EFFECT-QUOTED-NUMERIC-BOOL",
                "VSIX-EFFECT-CUSTOM-SOURCE", "VSIX-EFFECT-DURATION-NONE",
                "VSIX-EFFECT-STEAL-SOURCE-RISK", "VSIX-EFFECT-STEAL-STAT-RISK",
                "VSIX-EFFECT-TRINKET-TARGET", "VSIX-EFFECT-NAME-TOO-LONG", "VSIX-EFFECT-TOO-MANY-LIST-ARGS",
            }
            self.assertTrue(expected.issubset(codes), sorted(expected-codes))

    def test_dot_conflict_matches_vsix_same_line_scope(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-vsix-dot-scope-") as temp:
            root = Path(temp); effects = root / "effects"; effects.mkdir(parents=True)
            (effects / "scope.effects.darkest").write_text(
                'effect: .name "E" .dotBleed 1\n.dotPoison 1\n', encoding="utf-8"
            )
            _, result = self.run_checker(root)
            self.assertNotIn("VSIX-EFFECT-DOT-CONFLICT", {x["code"] for x in result["diagnostics"]})

    def test_vsix_info_diagnostic_families_are_retained(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-vsix-info-parity-") as temp:
            root = Path(temp)
            (root / "heroes" / "x").mkdir(parents=True)
            info = root / "heroes" / "x" / "x.info.darkest"
            info.write_text(
                """display_modifier: .disabled_popup_text_types actor_dot_complete actor_dot_complete // inline
skill: .id "x" .type bad
skill_reaction: .was_killed_effects "E"
""",
                encoding="utf-8",
            )
            _, result = self.run_checker(root)
            codes = {item["code"] for item in result["diagnostics"]}
            expected = {"VSIX-INFO-DUPLICATE-ARG", "VSIX-INFO-WAS-KILLED-EFFECTS", "VSIX-INFO-INLINE-COMMENT", "VSIX-INFO-CUSTOM-SKILL-TYPE"}
            self.assertTrue(expected.issubset(codes), sorted(expected-codes))


    def test_vsix_info_parameter_rules_and_cross_line_scope(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-vsix-info-rules-") as temp:
            root=Path(temp)
            (root / "heroes" / "x").mkdir(parents=True)
            (root / "heroes" / "x" / "x.info.darkest").write_text(
                'display_modifier: .disabled_popup_text_types actor_dot_complete actor_dot_complete unknown\n'
                'spawn: .effects A B C\nD\n'
                'mode: .id "' + ('x'*65) + '"\n'
                'display_modifier: .unknown_effects "E"\n', encoding="utf-8")
            _, result=self.run_checker(root)
            codes={x["code"] for x in result["diagnostics"]}
            expected={"VSIX-INFO-DUPLICATE-ARG","VSIX-INFO-INVALID-VALUE","VSIX-INFO-SPAWN-EFFECTS-LONG","VSIX-INFO-STRING-TOO-LONG","VSIX-INFO-DYNAMIC-EFFECT-CONTEXT"}
            self.assertTrue(expected.issubset(codes), sorted(expected-codes))

    def test_vsix_ignores_keywords_inside_quoted_effect_values(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-vsix-quoted-keyword-") as temp:
            root=Path(temp); (root/"effects").mkdir()
            (root/"effects"/"quoted.effects.darkest").write_text(
                'effect: .name "contains .not_a_keyword" .target performer\n', encoding="utf-8")
            _, result=self.run_checker(root)
            self.assertNotIn("VSIX-EFFECT-INVALID-KEYWORD", {x["code"] for x in result["diagnostics"]})


    def test_vsix_mode_name_warning_boundary_matches_plugin(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-vsix-mode-limit-") as temp:
            root=Path(temp)
            long_mode="m"*33
            (root/"heroes"/"x").mkdir(parents=True)
            (root/"heroes"/"x"/"x.info.darkest").write_text(f'skill: .id "x" .valid_modes "{long_mode}"\n',encoding="utf-8")
            _,result=self.run_checker(root)
            codes={item["code"] for item in result["diagnostics"]}
            self.assertIn("VSIX-INFO-STRING-LONG",codes)
            self.assertNotIn("VSIX-INFO-STRING-TOO-LONG",codes)


    def test_vsix_info_special_multi_value_rules(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-vsix-info-special-") as temp:
            root=Path(temp)
            (root/"heroes"/"x").mkdir(parents=True)
            (root/"heroes"/"x"/"x.info.darkest").write_text(
                'display_modifier: .disabled_popup_text_types actor_dot_complete actor_dot_complete bad\n'
                'battle_modifier: .disabled_act_out_combat_start_turn_types nothing nothing bad\n'
                'combat_skill: .damage_heal_base_class_ids A B C D E\n', encoding="utf-8")
            _,result=self.run_checker(root)
            codes={x["code"] for x in result["diagnostics"]}
            expected={"VSIX-INFO-DUPLICATE-ARG","VSIX-INFO-INVALID-VALUE","VSIX-INFO-TOO-MANY-ARGS"}
            self.assertTrue(expected.issubset(codes), sorted(expected-codes))
            self.assertTrue(any(x["code"]=="VSIX-INFO-TOO-MANY-ARGS" and x["severity"]=="warning" for x in result["diagnostics"]))


    def test_mode_effect_requires_same_line_valid_modes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-mode-effect-valid-") as temp:
            root=Path(temp)
            (root/"heroes"/"x").mkdir(parents=True)
            (root/"heroes"/"x"/"x.info.darkest").write_text(
                'mode: .id "stance"\n'
                'combat_skill: .id "bad" .stance_effects "E"\n'
                'combat_skill: .id "good" .valid_modes "stance" .stance_effects "E"\n', encoding="utf-8")
            _,result=self.run_checker(root)
            issues=[x for x in result["diagnostics"] if x["code"]=="KB-INFO-MODE-EFFECT-NOT-VALID"]
            self.assertEqual(len(issues),1)
            self.assertIn('"bad"', (root/"heroes"/"x"/"x.info.darkest").read_text(encoding="utf-8"))


    def test_empty_effect_reference_resolves_against_game_root(self) -> None:
        game=Path(os.environ.get("DD_GAME_ROOT", str(Path(__file__).resolve().parents[2] / "DarkestDungeon")))
        candidates=list(game.rglob("*.effects.darkest")) if game.is_dir() else []
        if not candidates:
            self.skipTest("本机没有游戏本体 effects.darkest 样本")
        sample=candidates[0].read_text(encoding="utf-8-sig")
        import re
        match=re.search(r'\.name\s+"([^"]+)"',sample)
        if not match:self.skipTest("本机首个 Effect 文件没有可提取的 .name")
        with tempfile.TemporaryDirectory(prefix="dd-game-ref-") as temp:
            root=Path(temp); (root/"effects").mkdir()
            (root/"heroes"/"ref").mkdir(parents=True)
            (root/"heroes"/"ref"/"ref.info.darkest").write_text(f'combat_skill: .id "s" .effect "{match.group(1)}"\n',encoding="utf-8")
            _,result=self.run_checker(root)
            self.assertNotIn("KB-REF-EFFECT-NOT-FOUND",{x["code"] for x in result["diagnostics"]})


    def test_unloadable_known_file_reports_info_and_skips_content_checks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-unloadable-path-") as temp:
            root=Path(temp)
            (root/"other").mkdir()
            (root/"other"/"bad.effects.darkest").write_text('bad: .not_a_keyword\n',encoding="utf-8")
            (root/"other"/"bad.entries.trinkets.json").write_text('{"bad": true}',encoding="utf-8")
            _,result=self.run_checker(root)
            diagnostics=result["diagnostics"]
            infos=[x for x in diagnostics if x["code"]=="KB-FILE-UNREADABLE-PATH"]
            self.assertEqual(len(infos),2)
            self.assertNotIn("VSIX-EFFECT-INVALID-KEYWORD",{x["code"] for x in diagnostics})
            self.assertNotIn("TRINKET-MISSING-ENTRIES",{x["code"] for x in diagnostics})


    def test_original_dlcs_use_their_real_wrapped_function_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-dlc-layout-") as temp:
            root=Path(temp)
            dlc=root/"dlc"/"580100_crimson_court"/"features"/"crimson_court"/"modes"/"bloodmoon"
            monster=dlc/"monsters"/"brigand_sapper"/"brigand_sapper_D"
            monster.mkdir(parents=True)
            (monster/"brigand_sapper_D.info.darkest").write_text('enemy_type: .id "brigand"\n',encoding="utf-8")
            (dlc/"effects").mkdir(parents=True)
            (dlc/"effects"/"mode.effects.darkest").write_text('effect: .name "DLCEffect" .target performer\n',encoding="utf-8")
            (dlc/"trinkets").mkdir()
            (dlc/"trinkets"/"mod.entries.trinkets.json").write_text('{"entries":[]}',encoding="utf-8")
            _,result=self.run_checker(root)
            codes=[x["code"] for x in result["diagnostics"]]
            self.assertNotIn("KB-FILE-UNREADABLE-PATH",codes)
            self.assertNotIn("KB-MONSTER-SUBCLASS-NAME",codes)

    def test_monster_filenames_preserve_matching_case(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-monster-case-") as temp:
            root = Path(temp)
            layouts = (root, root / "DLC" / "TestDlc" / "Features" / "TestFeature" / "Modes" / "TestMode")
            for layout in layouts:
                for base in ("Example_Hook_Summon", "Example_Reel_Summon", "lowercase"):
                    subclass = base + "_A"
                    folder = layout / "monsters" / base / subclass
                    folder.mkdir(parents=True)
                    for suffix in (".info.darkest", ".art.darkest"):
                        (folder / (subclass + suffix)).write_text('', encoding="utf-8")
            _, result = self.run_checker(root)
            codes = {diagnostic["code"] for diagnostic in result["diagnostics"]}
            self.assertNotIn("KB-MONSTER-FILENAME-MISMATCH", codes)
            self.assertNotIn("KB-MONSTER-SUBCLASS-NAME", codes)
            self.assertNotIn("KB-FILE-UNREADABLE-PATH", codes)

    def test_monster_filenames_reject_case_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-monster-case-mismatch-") as temp:
            root = Path(temp)
            for base, filename_base in (("MixedCase", "mixedcase"), ("lowercase", "LOWERCASE")):
                subclass = base + "_A"
                folder = root / "monsters" / base / subclass
                folder.mkdir(parents=True)
                for suffix in (".info.darkest", ".art.darkest"):
                    (folder / (filename_base + "_A" + suffix)).write_text('', encoding="utf-8")
            _, result = self.run_checker(root)
            mismatches = [diagnostic for diagnostic in result["diagnostics"] if diagnostic["code"] == "KB-MONSTER-FILENAME-MISMATCH"]
            self.assertEqual(len(mismatches), 4)
            self.assertTrue(all("包括大小写" in diagnostic["message"] for diagnostic in mismatches))

    def test_monster_base_and_complete_subclass_name_lengths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-monster-name-length-") as temp:
            root=Path(temp)
            base="b"*31
            subclass=base+"_A"
            folder=root/"monsters"/base/subclass
            folder.mkdir(parents=True)
            (folder/f"{subclass}.info.darkest").write_text('enemy_type: .id "test"\n',encoding="utf-8")
            _,result=self.run_checker(root)
            codes={x["code"] for x in result["diagnostics"]}
            self.assertIn("KB-MONSTER-BASE-NAME-TOO-LONG",codes)
            self.assertIn("KB-MONSTER-SUBCLASS-NAME-TOO-LONG",codes)


    def test_dlc_effects_are_scanned_with_or_without_feature_and_mode_wrappers(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-dlc-wrappers-") as temp:
            root = Path(temp)
            direct = root / "dlc" / "crimson_court" / "effects"
            featured = root / "dlc" / "crimson_court" / "features" / "crimson_court" / "effects"
            mode_only = root / "modes" / "bloodmoon" / "effects"
            for directory in (direct, featured, mode_only):
                directory.mkdir(parents=True)
                (directory / f"{directory.parent.name}.effects.darkest").write_text(
                    'effect: .name "WRAPPER_OK" .target performer\n', encoding="utf-8"
                )
            _, result = self.run_checker(root)
            self.assertNotIn("KB-FILE-UNREADABLE-PATH", {d["code"] for d in result["diagnostics"]})

    def test_default_game_index_excludes_local_mods_but_explicit_reference_can_include_one(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-game-root-mods-") as temp:
            game = Path(temp) / "DarkestDungeon"
            root = Path(temp) / "target-mod"
            self.make_mod(root)
            (root / "heroes" / "hero" / "hero.info.darkest").write_text(
                'combat_skill: .id "hit" .level 0 .effect "ONLY_IN_OTHER_MOD"\n', encoding="utf-8"
            )
            other_mod = game / "mods" / "other" 
            effects = other_mod / "effects"
            effects.mkdir(parents=True)
            (game / "effects").mkdir(parents=True)
            (game / "effects" / "base.effects.darkest").write_text(
                'effect: .name "BASE_GAME_EFFECT" .target performer\n', encoding="utf-8"
            )
            (effects / "other.effects.darkest").write_text(
                'effect: .name "ONLY_IN_OTHER_MOD" .target performer\n', encoding="utf-8"
            )
            import sys
            sys.path.insert(0, str(PROJECT.parent))
            try:
                from checker import Checker
            finally:
                sys.path.pop(0)
            checker = Checker(root, [], default_game=game)
            checker.index()
            self.assertNotIn("ONLY_IN_OTHER_MOD", checker.effect_ids)
            self.assertIn("BASE_GAME_EFFECT", checker.effect_ids)

            checker = Checker(root, [other_mod], default_game=game)
            checker.index()
            self.assertIn("ONLY_IN_OTHER_MOD", checker.effect_ids)

    def test_original_dlc_path_wrappers_and_monster_id_length_limits(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dd-dlc-layout-limits-") as temp:
            root=Path(temp)
            dlc=root/"dlc"/"580100_crimson_court"/"features"/"crimson_court"/"modes"/"bloodmoon"
            base="b"*31
            subclass=base+"_A"
            monster=dlc/"monsters"/base/subclass
            monster.mkdir(parents=True)
            (monster/f"{subclass}.info.darkest").write_text('enemy_type: .id "test"\n',encoding="utf-8")
            (dlc/"effects").mkdir(parents=True)
            (dlc/"effects"/"mode.effects.darkest").write_text('effect: .name "DLC_E" .target performer\n',encoding="utf-8")
            (dlc/"trinkets").mkdir()
            (dlc/"trinkets"/"mod.entries.trinkets.json").write_text('{"entries":[]}',encoding="utf-8")
            _,result=self.run_checker(root)
            codes={x["code"] for x in result["diagnostics"]}
            self.assertNotIn("KB-FILE-UNREADABLE-PATH",codes)
            self.assertIn("KB-MONSTER-BASE-NAME-TOO-LONG",codes)
            self.assertIn("KB-MONSTER-SUBCLASS-NAME-TOO-LONG",codes)



if __name__ == "__main__":
    unittest.main()
