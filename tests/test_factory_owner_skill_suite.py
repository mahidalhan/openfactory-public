from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"

OWNER_SKILLS = (
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
)

REMOVED_PRIVATE_SKILLS = (
    "balance-sheet-roic-analysis",
    "camera-cycle-counting",
    "factory-camera-inventory",
    "pra" + "xis-old-erp-extraction",
    "extend",
)


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise AssertionError("missing YAML frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip()
    return values


class FactoryOwnerSkillSuiteTest(unittest.TestCase):
    def test_suite_has_exactly_ten_unique_members(self) -> None:
        directories = sorted(
            path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()
        )
        self.assertEqual(10, len(OWNER_SKILLS))
        self.assertEqual(10, len(set(OWNER_SKILLS)))
        self.assertEqual(sorted(OWNER_SKILLS), directories)

    def test_each_skill_has_valid_identity_and_complete_contract(self) -> None:
        required_sections = (
            "Source Trust",
            "Minimum Inputs",
            "Eval Gates",
            "Human Approval",
            "Completion Standard",
        )

        for skill_name in OWNER_SKILLS:
            with self.subTest(skill=skill_name):
                skill_file = SKILLS_ROOT / skill_name / "SKILL.md"
                self.assertTrue(skill_file.is_file(), skill_file)
                text = skill_file.read_text()
                metadata = frontmatter(text)

                self.assertEqual(skill_name, metadata.get("name"))
                self.assertTrue(metadata.get("description", "").startswith("Use when"))
                self.assertLessEqual(len(metadata["description"]), 1024)
                for section in required_sections:
                    self.assertIn(f"## {section}", text)

    def test_suite_index_lists_each_member_once_and_in_order(self) -> None:
        index = (SKILLS_ROOT / "README.md").read_text()
        numbered_members = re.findall(r"^\d+\. `([^`]+)`$", index, flags=re.MULTILINE)
        self.assertEqual(list(OWNER_SKILLS), numbered_members)

    def test_shared_status_and_handoff_contract_is_documented(self) -> None:
        index = (SKILLS_ROOT / "README.md").read_text()
        for status in (
            "ready",
            "blocked_missing_input",
            "infeasible",
            "needs_approval",
            "complete",
        ):
            self.assertIn(f"`{status}`", index)
        for field in (
            "goal",
            "scope",
            "as_of",
            "sources",
            "status",
            "decision",
            "economic_value",
            "assumptions",
            "next_action",
            "owner",
            "due_at",
        ):
            self.assertIn(field, index)

    def test_skills_do_not_depend_on_removed_private_skills(self) -> None:
        combined = "\n".join(
            (SKILLS_ROOT / name / "SKILL.md").read_text() for name in OWNER_SKILLS
        )
        for removed in REMOVED_PRIVATE_SKILLS:
            with self.subTest(skill=removed):
                self.assertNotIn(f"`{removed}`", combined)

    def test_public_skill_references_resolve(self) -> None:
        known = set(OWNER_SKILLS)
        domain_prefixes = (
            "factory-",
            "sales-",
            "demand-",
            "bottleneck-",
            "material-",
            "workforce-",
            "quality-",
            "standard-",
            "working-",
            "daily-",
            "balance-",
            "camera-",
            "pra" + "xis-",
        )

        for skill_name in OWNER_SKILLS:
            text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text()
            tokens = set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", text))
            references = {token for token in tokens if token.startswith(domain_prefixes)}
            with self.subTest(skill=skill_name):
                self.assertTrue(references <= known, references - known)

    def test_no_skill_routes_to_docs_or_legacy_skill_locations(self) -> None:
        combined = "\n".join(
            (SKILLS_ROOT / name / "SKILL.md").read_text() for name in OWNER_SKILLS
        )
        self.assertNotIn("docs/", combined)
        self.assertNotIn(".codex/skills", combined)


if __name__ == "__main__":
    unittest.main()
