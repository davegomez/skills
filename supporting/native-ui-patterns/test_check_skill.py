#!/usr/bin/env python3
"""Regression tests for the native-ui-patterns development check."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from check_skill import check_archive, check_runtime, load_mapping

REPO = Path(__file__).resolve().parents[2]
SOURCE_RUNTIME = REPO / "skills" / "native-ui-patterns"
SOURCE_ARCHIVE = REPO / "supporting" / "native-ui-patterns"
MAPPING = SOURCE_ARCHIVE / "screenshot-map.tsv"


class RuntimeEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.runtime = Path(self.temporary.name) / "native-ui-patterns"
        shutil.copytree(SOURCE_RUNTIME, self.runtime)

    def errors(self) -> list[str]:
        errors: list[str] = []
        check_runtime(self.runtime, load_mapping(MAPPING), errors)
        return errors

    def assert_rejected(self, expected: str) -> None:
        errors = self.errors()
        self.assertTrue(
            any(expected in error for error in errors),
            f"expected rejection containing {expected!r}; got {errors!r}",
        )

    def test_rejects_duplicate_capture_bytes(self) -> None:
        first = self.runtime / "assets/android/settings/root.png"
        second = self.runtime / "assets/android/settings/display-and-touch.png"
        second.write_bytes(first.read_bytes())
        self.assert_rejected("duplicate runtime PNG bytes")

    def test_rejects_missing_capture(self) -> None:
        (self.runtime / "assets/ios/calendar/event-empty.png").unlink()
        self.assert_rejected("missing expected runtime path")

    def test_rejects_modified_capture(self) -> None:
        image = self.runtime / "assets/android/settings/search-no-results.png"
        image.write_bytes(image.read_bytes() + b"modified")
        self.assert_rejected("runtime PNG hash mismatch")

    def test_rejects_invalid_png_header(self) -> None:
        image = self.runtime / "assets/ios/maps/location-permission.png"
        image.write_bytes(b"not a png")
        self.assert_rejected("invalid PNG header")

    def test_rejects_broken_runtime_link(self) -> None:
        reference = self.runtime / "references/ios/navigation.md"
        reference.write_text(
            reference.read_text(encoding="utf-8")
            + "\n[Broken](../../assets/ios/files/missing.png)\n",
            encoding="utf-8",
        )
        self.assert_rejected("broken link")

    def test_rejects_external_runtime_link(self) -> None:
        reference = self.runtime / "references/ios/navigation.md"
        reference.write_text(
            reference.read_text(encoding="utf-8")
            + "\n[External](https://example.com/example.png)\n",
            encoding="utf-8",
        )
        self.assert_rejected("runtime external link")

    def test_rejects_unreachable_capture(self) -> None:
        reference = self.runtime / "references/ios/editing.md"
        text = reference.read_text(encoding="utf-8")
        text = text.replace(
            "[event form](../../assets/ios/calendar/event-form.png)", "event form"
        )
        reference.write_text(text, encoding="utf-8")
        self.assert_rejected("runtime PNG has no conditional visual route")

    def test_rejects_wrong_platform_route(self) -> None:
        reference = self.runtime / "references/ios/navigation.md"
        reference.write_text(
            reference.read_text(encoding="utf-8")
            + "\n| Wrong platform | [Android](../../assets/android/settings/root.png) | inspect |\n",
            encoding="utf-8",
        )
        self.assert_rejected("runtime PNG linked from wrong platform reference")

    def test_requires_visual_before_implementation_instruction(self) -> None:
        skill = self.runtime / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8").replace(
                "Before implementing or reviewing visual appearance, open the matched screenshots.",
                "Use screenshots when convenient.",
            ),
            encoding="utf-8",
        )
        self.assert_rejected("lacks mandatory pre-implementation visual inspection")

    def test_requires_text_only_skip_instruction(self) -> None:
        skill = self.runtime / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8").replace(
                "For text-only behavioral requests, skip screenshots.",
                "Screenshots are optional.",
            ),
            encoding="utf-8",
        )
        self.assert_rejected("lacks truthful text-only screenshot skip")

    def test_requires_state_specific_visual_selection(self) -> None:
        skill = self.runtime / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8").replace(
                "A matching state capture itself counts as the overview",
                "Open an overview before the matching state",
            ),
            encoding="utf-8",
        )
        self.assert_rejected("lacks state-specific screenshot selection")

    def test_rejects_ios_value_control_gap(self) -> None:
        skill = self.runtime / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8").replace(
                "| Switches, filters, and value controls | [iOS editing](references/ios/editing.md) |",
                "| Switches, filters, and value controls | Record a coverage gap |",
            ),
            encoding="utf-8",
        )
        self.assert_rejected("SKILL.md still records the iOS value-control gap")

    def test_accepts_current_runtime(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_requires_observed_android_search_back_sequence(self) -> None:
        reference = self.runtime / "references/android/search.md"
        reference.write_text(
            reference.read_text(encoding="utf-8").replace(
                "system Back first dismissed keyboard UI; a subsequent Back exited search",
                "Back behavior varied",
            ),
            encoding="utf-8",
        )
        self.assert_rejected("Android search lacks observed Back sequence")

    def test_requires_settings_only_help_qualification(self) -> None:
        reference = self.runtime / "references/android/search.md"
        reference.write_text(
            reference.read_text(encoding="utf-8").replace(
                "this was a Settings-only suggestion, not a generic recommended help destination",
                "this is a recommended help destination",
            ),
            encoding="utf-8",
        )
        self.assert_rejected(
            "Android search generalizes the Settings-only help suggestion"
        )


class ArchiveEvidenceTests(unittest.TestCase):
    def test_rejects_png_left_in_supporting_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "native-ui-patterns"
            shutil.copytree(SOURCE_ARCHIVE, archive)
            (archive / "stray.png").write_bytes(
                (SOURCE_RUNTIME / "assets/ios/calendar/event-empty.png").read_bytes()
            )
            errors: list[str] = []
            check_archive(archive, SOURCE_RUNTIME, load_mapping(MAPPING), None, errors)
            self.assertTrue(
                any("supporting archive contains PNG" in error for error in errors),
                errors,
            )

    def test_rejects_pending_original_that_duplicates_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "native-ui-patterns"
            shutil.copytree(SOURCE_ARCHIVE, archive)
            pending = archive / "research/notes/ios/captures-2026-09-08"
            pending.mkdir(parents=True, exist_ok=True)
            (pending / "S-X00-copy.png").write_bytes(
                (SOURCE_RUNTIME / "assets/ios/calendar/event-empty.png").read_bytes()
            )
            errors: list[str] = []
            check_archive(archive, SOURCE_RUNTIME, load_mapping(MAPPING), None, errors)
            self.assertTrue(
                any("duplicates a runtime PNG" in error for error in errors),
                errors,
            )

    def test_accepts_unique_pending_original(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "native-ui-patterns"
            shutil.copytree(SOURCE_ARCHIVE, archive)
            pending = archive / "research/notes/ios/captures-2026-09-08"
            pending.mkdir(parents=True, exist_ok=True)
            original = (SOURCE_RUNTIME / "assets/ios/calendar/event-empty.png").read_bytes()
            mutated = original[:-1] + bytes([original[-1] ^ 0xFF])
            (pending / "S-X01-unique.png").write_bytes(mutated)
            errors: list[str] = []
            check_archive(archive, SOURCE_RUNTIME, load_mapping(MAPPING), None, errors)
            self.assertFalse(
                any("PNG" in error for error in errors),
                errors,
            )


if __name__ == "__main__":
    unittest.main()
