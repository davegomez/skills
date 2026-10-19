#!/usr/bin/env python3
"""Validate the native-ui-patterns runtime skill and preserved source evidence."""

from __future__ import annotations

import argparse
import hashlib
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

EXPECTED_SCREENSHOTS = (109, 41_819_305)
EXPECTED_DUMPS = (57, 1_134_708)
EXPECTED_ROUTES = {
    f"references/{platform}/{operation}.md"
    for platform in ("ios", "android")
    for operation in (
        "navigation",
        "search",
        "editing",
        "content-states",
        "onboarding-permissions",
        "accessibility",
    )
}
ARCHIVE_ROOT = Path(__file__).resolve().parent
MAPPING_PATH = ARCHIVE_ROOT / "screenshot-map.tsv"
SCENARIOS = {
    "iOS edit form": (["SKILL.md", "references/ios/editing.md"], 1_400),
    "Android no-results search": (["SKILL.md", "references/android/search.md"], 1_300),
    "cross-platform peer navigation": (
        [
            "SKILL.md",
            "references/ios/navigation.md",
            "references/android/navigation.md",
        ],
        1_700,
    ),
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
WORD_RE = re.compile(r"\b[\w’'-]+\b")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@dataclass(frozen=True)
class Capture:
    original_path: str
    runtime_path: str
    sha256: str
    width: int
    height: int
    byte_count: int


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", header[16:24])


def load_mapping(path: Path) -> tuple[Capture, ...]:
    lines = path.read_text(encoding="utf-8").splitlines()
    expected_header = "original_path\truntime_path\tsha256\twidth\theight\tbytes"
    if not lines or lines[0] != expected_header:
        raise ValueError("screenshot mapping has an invalid header")
    captures = []
    for number, line in enumerate(lines[1:], 2):
        fields = line.split("\t")
        if len(fields) != 6:
            raise ValueError(
                f"screenshot mapping row {number} has {len(fields)} fields"
            )
        original, runtime, digest, width, height, byte_count = fields
        captures.append(
            Capture(original, runtime, digest, int(width), int(height), int(byte_count))
        )
    if len(captures) != EXPECTED_SCREENSHOTS[0]:
        raise ValueError(f"screenshot mapping has {len(captures)} rows")
    if len({capture.original_path for capture in captures}) != len(captures):
        raise ValueError("screenshot mapping repeats an original path")
    if len({capture.runtime_path for capture in captures}) != len(captures):
        raise ValueError("screenshot mapping repeats a runtime path")
    if sum(capture.byte_count for capture in captures) != EXPECTED_SCREENSHOTS[1]:
        raise ValueError("screenshot mapping byte total changed")
    return tuple(captures)


def slug(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def local_links(path: Path) -> list[str]:
    return LINK_RE.findall(path.read_text(encoding="utf-8"))


def link_target(source: Path, raw: str) -> Path | None:
    target_text = raw.strip().split(maxsplit=1)[0].strip("<>")
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target_text):
        return None
    if target_text.startswith("#"):
        return source.resolve()
    path_text = target_text.partition("#")[0]
    return (source.parent / unquote(path_text)).resolve()


def check_links(
    roots: tuple[Path, ...], markdown: list[Path], errors: list[str], label: str
) -> None:
    resolved_roots = tuple(root.resolve() for root in roots)
    display_root = roots[0]
    for source in markdown:
        for raw in local_links(source):
            target_text = raw.strip().split(maxsplit=1)[0].strip("<>")
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target_text):
                fail(
                    errors,
                    f"{label} external link: {source.relative_to(display_root)} -> {raw}",
                )
                continue
            target = link_target(source, raw)
            if target is None:
                fail(
                    errors,
                    f"unresolvable link: {source.relative_to(display_root)} -> {raw}",
                )
                continue
            if not any(target.is_relative_to(root) for root in resolved_roots):
                fail(
                    errors,
                    f"link escapes allowed roots: {source.relative_to(display_root)} -> {raw}",
                )
                continue
            if not target.exists():
                fail(
                    errors, f"broken link: {source.relative_to(display_root)} -> {raw}"
                )
                continue
            fragment = target_text.partition("#")[2]
            if fragment and target.is_file() and target.suffix == ".md":
                headings = {
                    slug(heading)
                    for heading in HEADING_RE.findall(
                        target.read_text(encoding="utf-8")
                    )
                }
                if unquote(fragment) not in headings:
                    fail(
                        errors,
                        f"broken anchor: {source.relative_to(display_root)} -> {raw}",
                    )


def check_frontmatter(skill: Path, errors: list[str]) -> str:
    if not skill.exists():
        fail(errors, "missing runtime SKILL.md")
        return ""
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, "SKILL.md has no YAML frontmatter")
        return text
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    if fields.get("name") != "native-ui-patterns":
        fail(errors, "frontmatter name must be native-ui-patterns")
    expected = (
        "Native UI patterns. Use when designing iOS or Android screens, reviewing "
        "platform fit, or adapting a flow between platforms."
    )
    if fields.get("description") != expected:
        fail(errors, "frontmatter description does not match approved trigger")
    if "disable-model-invocation" in fields:
        fail(errors, "runtime skill must remain model-invoked")
    return text


def check_runtime(
    runtime: Path, captures: tuple[Capture, ...], errors: list[str]
) -> dict[str, int]:
    text = check_frontmatter(runtime / "SKILL.md", errors)
    files = [path for path in runtime.rglob("*") if path.is_file()]
    symlinks = [path for path in runtime.rglob("*") if path.is_symlink()]
    if symlinks:
        fail(errors, "runtime contains symlinks: " + ", ".join(map(str, symlinks)))

    expected_files = {"SKILL.md", *EXPECTED_ROUTES, *(c.runtime_path for c in captures)}
    actual_files = {str(path.relative_to(runtime)) for path in files}
    for extra in sorted(actual_files - expected_files):
        fail(errors, f"unexpected runtime path: {extra}")
    for missing in sorted(expected_files - actual_files):
        fail(errors, f"missing expected runtime path: {missing}")

    route_links = {
        raw.partition("#")[0]
        for raw in local_links(runtime / "SKILL.md")
        if raw.startswith("references/")
    }
    if route_links != EXPECTED_ROUTES:
        fail(
            errors, "routing table does not contain exactly the 12 operation references"
        )
    if (
        "For cross-platform work, read the matching operation file in each platform column"
        not in text
    ):
        fail(errors, "SKILL.md lacks bounded cross-platform routing")
    if (
        "Before implementing or reviewing visual appearance, open the matched screenshots."
        not in text
    ):
        fail(errors, "SKILL.md lacks mandatory pre-implementation visual inspection")
    if "For text-only behavioral requests, skip screenshots." not in text:
        fail(errors, "SKILL.md lacks truthful text-only screenshot skip")
    if "A matching state capture itself counts as the overview" not in text:
        fail(errors, "SKILL.md lacks state-specific screenshot selection")
    if (
        "| Switches, filters, and value controls | [iOS editing](references/ios/editing.md) |"
        not in text
    ):
        fail(errors, "SKILL.md still records the iOS value-control gap")

    android_search_path = runtime / "references/android/search.md"
    android_search = (
        android_search_path.read_text(encoding="utf-8")
        if android_search_path.is_file()
        else ""
    )
    if (
        "system Back first dismissed keyboard UI; a subsequent Back exited search"
        not in android_search
        or "Whether Back clears a query is **Unconfirmed**" not in android_search
    ):
        fail(errors, "Android search lacks observed Back sequence or boundary")
    if (
        "this was a Settings-only suggestion, not a generic recommended help destination"
        not in android_search
    ):
        fail(errors, "Android search generalizes the Settings-only help suggestion")
    if (
        "Give the field, result items, Back, and Clear meaningful labels, and preserve focus when results change"
        not in android_search
    ):
        fail(errors, "Android search lacks semantic labels/focus guidance")

    for phrase in (
        "layout, alignment, spacing, control placement, and surrounding content",
        "Pixel measurements are estimates",
        "never iOS points, Android dp, or target-device dimensions",
        "state the visual-evidence gap instead of inventing a specification",
        "Use the target viewport and framework to validate the translation",
    ):
        if phrase not in text:
            fail(errors, f"SKILL.md lacks visual evidence guard: {phrase}")

    markdown = sorted(path for path in files if path.suffix == ".md")
    check_links((runtime,), markdown, errors, "runtime")
    for route in EXPECTED_ROUTES:
        route_text = (
            (runtime / route).read_text(encoding="utf-8")
            if (runtime / route).is_file()
            else ""
        )
        if (
            "## Visual references" not in route_text
            or "| Visual question / state |" not in route_text
        ):
            fail(errors, f"operation reference lacks task-based visual table: {route}")
        if "only" not in route_text.split("## Visual references", 1)[-1].lower():
            fail(
                errors,
                f"operation reference lacks narrow image-loading instruction: {route}",
            )

    pngs = sorted(runtime.rglob("*.png"))
    if (len(pngs), sum(path.stat().st_size for path in pngs)) != EXPECTED_SCREENSHOTS:
        fail(errors, "runtime PNG count/bytes changed")
    digests = [sha256(path) for path in pngs]
    if len(set(digests)) != len(digests):
        fail(errors, "duplicate runtime PNG bytes")

    by_path = {capture.runtime_path: capture for capture in captures}
    for relative, capture in by_path.items():
        path = runtime / relative
        if not path.is_file():
            continue
        dimensions = png_dimensions(path)
        if dimensions is None:
            fail(errors, f"invalid PNG header: {relative}")
            continue
        if dimensions != (capture.width, capture.height):
            fail(errors, f"runtime PNG dimensions mismatch: {relative}")
        if path.stat().st_size != capture.byte_count:
            fail(errors, f"runtime PNG byte count mismatch: {relative}")
        if sha256(path) != capture.sha256:
            fail(errors, f"runtime PNG hash mismatch: {relative}")

    routed: dict[str, set[str]] = {relative: set() for relative in by_path}
    for source in (runtime / "references").rglob("*.md"):
        source_relative = str(source.relative_to(runtime))
        source_platform = source_relative.split("/")[1]
        for line in source.read_text(encoding="utf-8").splitlines():
            for raw in LINK_RE.findall(line):
                target = link_target(source, raw)
                if target is None or not target.is_relative_to(runtime.resolve()):
                    continue
                relative = str(target.relative_to(runtime.resolve()))
                if relative not in routed:
                    continue
                asset_platform = relative.split("/")[1]
                if source_platform != asset_platform:
                    fail(
                        errors,
                        f"runtime PNG linked from wrong platform reference: {relative} -> {source_relative}",
                    )
                if line.lstrip().startswith("|"):
                    routed[relative].add(source_relative)
    for relative, routes in routed.items():
        if not routes:
            fail(errors, f"runtime PNG has no conditional visual route: {relative}")

    budgets: dict[str, int] = {}
    for scenario, (paths, budget) in SCENARIOS.items():
        if any(not (runtime / path).is_file() for path in paths):
            continue
        words = sum(
            len(WORD_RE.findall((runtime / path).read_text(encoding="utf-8")))
            for path in paths
        )
        budgets[scenario] = words
        if words > budget:
            fail(errors, f"{scenario} routing budget is {words} words, limit {budget}")
    return budgets


def archived_patterns(archive: Path) -> set[str]:
    result: set[str] = set()
    for platform in ("ios", "android"):
        for path in (archive / "docs" / platform).glob("*.md"):
            result.update(HEADING_RE.findall(path.read_text(encoding="utf-8")))
    return result


def mapped_patterns(readme: Path) -> set[str]:
    if not readme.exists():
        return set()
    return {
        line.split("`", 2)[1]
        for line in readme.read_text(encoding="utf-8").splitlines()
        if line.startswith("| `")
    }


def check_baseline(
    baseline: Path,
    archive: Path,
    runtime: Path,
    captures: tuple[Capture, ...],
    errors: list[str],
) -> None:
    if not baseline.is_dir():
        fail(errors, f"baseline does not exist: {baseline}")
        return
    for capture in captures:
        original = baseline / capture.original_path
        current = runtime / capture.runtime_path
        if not original.is_file():
            fail(errors, f"baseline screenshot missing: {capture.original_path}")
        elif not current.is_file():
            fail(
                errors,
                f"runtime screenshot missing during baseline check: {capture.runtime_path}",
            )
        elif sha256(original) != sha256(current):
            fail(errors, f"baseline screenshot hash changed: {capture.original_path}")
    for original in sorted(path for path in baseline.rglob("*") if path.is_file()):
        relative = original.relative_to(baseline)
        if original.suffix == ".png" or ".ruff_cache" in relative.parts:
            continue
        preserved = archive / relative
        if not preserved.is_file():
            fail(errors, f"baseline non-image file missing: {relative}")
        elif (original.suffix == ".xml" or original.name == ".DS_Store") and sha256(
            original
        ) != sha256(preserved):
            fail(errors, f"baseline raw file hash changed: {relative}")


def check_runtime_baseline(
    baseline: Path,
    runtime: Path,
    archive: Path,
    captures: tuple[Capture, ...],
    errors: list[str],
) -> None:
    if not baseline.is_dir():
        fail(errors, f"runtime baseline does not exist: {baseline}")
        return
    expected_hashes = {capture.sha256 for capture in captures}
    original_pngs = list(baseline.rglob("*.png"))
    if len(original_pngs) != 8:
        fail(
            errors,
            f"pre-expansion runtime baseline has {len(original_pngs)} PNGs, expected 8",
        )
    for original in original_pngs:
        if sha256(original) not in expected_hashes:
            fail(
                errors,
                f"pre-expansion runtime PNG was not preserved: {original.relative_to(baseline)}",
            )
    metadata = archive / "preserved-runtime-metadata"
    original_metadata = list(baseline.rglob(".DS_Store"))
    if len(original_metadata) != 3:
        fail(
            errors,
            f"pre-expansion runtime baseline has {len(original_metadata)} .DS_Store files, expected 3",
        )
    for original in original_metadata:
        relative = original.relative_to(baseline)
        preserved = metadata / relative
        if not preserved.is_file() or sha256(original) != sha256(preserved):
            fail(
                errors, f"pre-expansion runtime metadata was not preserved: {relative}"
            )


def check_archive(
    archive: Path,
    runtime: Path,
    captures: tuple[Capture, ...],
    baseline: Path | None,
    errors: list[str],
) -> None:
    markdown = sorted(archive.rglob("*.md"))
    check_links((archive, runtime), markdown, errors, "supporting")
    source_patterns = archived_patterns(archive)
    mapped = mapped_patterns(archive / "README.md")
    if len(source_patterns) != 47:
        fail(
            errors,
            f"expected 47 archived pattern headings, found {len(source_patterns)}",
        )
    if mapped != source_patterns:
        fail(
            errors,
            "original pattern mapping no longer covers exactly the source headings",
        )
    pending = archive / "research/notes/ios/captures-2026-09-08"
    runtime_hashes = {capture.sha256 for capture in captures}
    for png in sorted(archive.rglob("*.png")):
        if png.parent != pending:
            fail(
                errors,
                f"supporting archive contains PNG outside the pending-originals folder: {png.relative_to(archive)}",
            )
        elif sha256(png) in runtime_hashes:
            fail(errors, f"pending iOS original duplicates a runtime PNG: {png.name}")
    dumps = list((archive / "research/notes/android/ui-dumps").glob("*.xml"))
    if (len(dumps), sum(path.stat().st_size for path in dumps)) != EXPECTED_DUMPS:
        fail(errors, "archived XML dump count/bytes changed")
    if baseline:
        check_baseline(baseline, archive, runtime, captures, errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline",
        type=Path,
        help="pre-migration supporting/native-ui-patterns or original corpus directory",
    )
    parser.add_argument(
        "--runtime-baseline",
        type=Path,
        help="pre-expansion runtime directory for selected-PNG and metadata preservation",
    )
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    runtime = repo / "skills/native-ui-patterns"
    archive = repo / "supporting/native-ui-patterns"
    errors: list[str] = []
    try:
        captures = load_mapping(MAPPING_PATH)
    except (OSError, ValueError) as exc:
        print(f"native-ui-patterns check: FAIL\n- {exc}")
        return 1
    budgets = check_runtime(runtime, captures, errors)
    check_archive(archive, runtime, captures, args.baseline, errors)
    if args.runtime_baseline:
        check_runtime_baseline(
            args.runtime_baseline, runtime, archive, captures, errors
        )
    if errors:
        print("native-ui-patterns check: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("native-ui-patterns check: PASS")
    print(f"- runtime files: {sum(1 for path in runtime.rglob('*') if path.is_file())}")
    print(
        "- runtime Markdown words: "
        + str(
            sum(
                len(WORD_RE.findall(path.read_text(encoding="utf-8")))
                for path in runtime.rglob("*.md")
            )
        )
    )
    print(f"- runtime images: {sum(1 for path in runtime.rglob('*.png'))}")
    print(
        f"- runtime evidence: {EXPECTED_SCREENSHOTS[0]} byte-unique, mapped PNGs"
        " with verified hashes and dimensions"
    )
    for scenario, words in budgets.items():
        print(
            f"- {scenario}: {words} words across {len(SCENARIOS[scenario][0])} Markdown files"
        )
    pending = archive / "research/notes/ios/captures-2026-09-08"
    pending_count = len(list(pending.glob("*.png"))) if pending.is_dir() else 0
    print(
        f"- supporting evidence: {pending_count} pending iOS originals, 0 runtime"
        " duplicates; 57 original XML dumps"
    )
    if args.baseline:
        print("- baseline: PNG/XML/.DS_Store hashes and non-image presence preserved")
    if args.runtime_baseline:
        print(
            "- runtime baseline: selected PNGs and relocated .DS_Store bytes preserved"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
