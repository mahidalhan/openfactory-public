from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "PUBLIC_FILES.txt"
SKILLS_ROOT = ROOT / ".agents" / "skills"

OWNER_SKILLS = {
    "factory-capital-efficiency",
    "sales-production-commitment",
    "demand-backward-production-planning",
    "bottleneck-capacity-mix",
    "material-availability-gate",
    "workforce-shift-coverage",
    "quality-rework-loop",
    "standard-cost-margin-bridge",
    "working-capital-cash-conversion",
    "daily-management-cadence",
}


def manifest_files() -> set[str]:
    return {
        line.strip()
        for line in MANIFEST.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def repository_files() -> set[str]:
    if (ROOT / ".git").exists():
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return set(result.stdout.splitlines())

    ignored_parts = {"__pycache__", ".openfactory-private", ".claude", ".entire"}
    return {
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file()
        and not ignored_parts.intersection(path.relative_to(ROOT).parts)
        and path.suffix not in {".pyc", ".pyo"}
        and path.name != ".DS_Store"
    }


class PublicReadinessTest(unittest.TestCase):
    def test_manifest_exactly_matches_repository_files(self) -> None:
        self.assertEqual(manifest_files(), repository_files())

    def test_public_tree_has_exactly_ten_skills(self) -> None:
        actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(OWNER_SKILLS, actual)
        for name in actual:
            self.assertTrue((SKILLS_ROOT / name / "SKILL.md").is_file())

    def test_lean_tree_excludes_private_and_duplicate_surfaces(self) -> None:
        tracked = manifest_files()
        forbidden_prefixes = (
            "docs/",
            "tools/",
            "lessons/",
            "reference/",
            ".codex/skills/",
        )
        for path in tracked:
            with self.subTest(path=path):
                self.assertFalse(path.startswith(forbidden_prefixes))

    def test_public_files_have_no_obvious_private_routes(self) -> None:
        private_patterns = {
            "absolute macOS user path": re.compile("/" + "Users/"),
            "Notion workspace URL": re.compile("notion" + r"\.(?:so|site|com)/", re.I),
            "Google workspace document": re.compile("docs" + r"\.google\.com/", re.I),
            "camera stream URL": re.compile(r"\b(?:rts" + "p|rts" + r"ps)://", re.I),
            "private network address": re.compile(
                r"\b(?:10\.\d{1,3}\.|192\.168\.\d{1,3}\.|"
                r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.)"
            ),
            "email address": re.compile(
                r"\b[A-Z0-9._%+-]+" + "@" + r"[A-Z0-9.-]+\.[A-Z]{2,}\b",
                re.I,
            ),
            "private implementation name": re.compile(
                r"\b(?:pra" + "xis|tan" + "nery|open" + r"robot)\b", re.I
            ),
        }

        scan_files = manifest_files() - {"tests/test_public_readiness.py"}
        for relative in scan_files:
            path = ROOT / relative
            text = path.read_text(errors="ignore")
            for label, pattern in private_patterns.items():
                with self.subTest(path=relative, pattern=label):
                    self.assertIsNone(pattern.search(text), f"{label} in {relative}")

    def test_beginner_readme_has_complete_local_route(self) -> None:
        readme = (ROOT / "README.md").read_text()
        for phrase in (
            "You do not need to write code",
            "Open The Folder In Codex",
            "Start a **Local** chat",
            "Paste This Starter Prompt",
            "Data And Approval Rules",
            ".agents/skills/",
            "Apache License 2.0",
            "https://github.com/mahidalhan/openfactory.git",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, readme)

    def test_local_markdown_links_resolve(self) -> None:
        markdown_files = {
            path for path in manifest_files() if path.endswith(".md")
        }
        missing: list[tuple[str, str]] = []
        for relative in markdown_files:
            source = ROOT / relative
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", source.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                clean = target.split("#", 1)[0]
                if not (source.parent / clean).resolve().exists():
                    missing.append((relative, target))
        self.assertEqual([], missing)

    def test_codex_project_config_disables_external_surfaces(self) -> None:
        config = (ROOT / ".codex" / "config.toml").read_text()
        for setting in (
            "apps = false",
            "computer_use = false",
            "enable_mcp_apps = false",
            "plugins = false",
        ):
            self.assertIn(setting, config)


if __name__ == "__main__":
    unittest.main()
