import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "application-tracker" / "scripts" / "manage_applications.py"


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True
    )


class TestManageApplications(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump({"schema_version": 1, "as_of": "2026-07-03", "applications": [], "notes": []}, self.tmp)
        self.tmp.close()
        self.path = self.tmp.name

    def load(self):
        with open(self.path) as f:
            return json.load(f)

    def add(self, company="Goldman Sachs", role="IB Spring Insight", **kw):
        args = [
            "--applications", self.path, "add",
            "--company", company, "--role", role,
            "--source", kw.get("source", "trackr"),
            "--url", kw.get("url", "https://example.com/job"),
        ]
        if "deadline" in kw:
            args += ["--deadline", kw["deadline"]]
        if "date_found" in kw:
            args += ["--date-found", kw["date_found"]]
        return run(*args)

    def test_add_assigns_first_id(self):
        result = self.add()
        self.assertEqual(result.returncode, 0, result.stderr)
        data = self.load()
        self.assertEqual(len(data["applications"]), 1)
        self.assertEqual(data["applications"][0]["id"], "APP-0001")
        self.assertEqual(data["applications"][0]["status"], "targeted")

    def test_second_add_increments_id(self):
        self.add(company="Goldman Sachs", role="IB Spring Insight")
        self.add(company="Morgan Stanley", role="S&T Spring Insight")
        data = self.load()
        ids = [a["id"] for a in data["applications"]]
        self.assertEqual(ids, ["APP-0001", "APP-0002"])

    def test_duplicate_company_role_rejected(self):
        self.add(company="Goldman Sachs", role="IB Spring Insight")
        result = self.add(company="Goldman Sachs", role="IB Spring Insight")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stderr)
        data = self.load()
        self.assertEqual(len(data["applications"]), 1)

    def test_invalid_source_rejected(self):
        result = self.add(source="glassdoor")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--source must be one of", result.stderr)

    def test_update_status_and_history(self):
        self.add()
        result = run("--applications", self.path, "update", "--id", "APP-0001",
                      "--status", "submitted", "--date", "2026-07-10")
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = self.load()["applications"][0]
        self.assertEqual(entry["status"], "submitted")
        self.assertEqual(entry["date_submitted"], "2026-07-10")
        statuses = [h["status"] for h in entry["status_history"]]
        self.assertEqual(statuses, ["targeted", "submitted"])

    def test_update_corrects_role_and_location(self):
        self.add(role="2027 Summer Analyst")
        result = run("--applications", self.path, "update", "--id", "APP-0001",
                      "--role", "2027 Real Estate Debt Strategies Summer Analyst",
                      "--location", "London")
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = self.load()["applications"][0]
        self.assertEqual(entry["role"], "2027 Real Estate Debt Strategies Summer Analyst")
        self.assertEqual(entry["location"], "London")

    def test_update_role_alone_counts_as_a_change(self):
        self.add()
        result = run("--applications", self.path, "update", "--id", "APP-0001", "--role", "Renamed")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("role -> Renamed", result.stdout)

    def test_update_role_leaves_status_untouched(self):
        self.add()
        run("--applications", self.path, "update", "--id", "APP-0001", "--status", "interview")
        run("--applications", self.path, "update", "--id", "APP-0001", "--role", "Renamed")
        entry = self.load()["applications"][0]
        self.assertEqual(entry["status"], "interview")
        self.assertEqual([h["status"] for h in entry["status_history"]], ["targeted", "interview"])

    def test_update_invalid_status_rejected(self):
        self.add()
        result = run("--applications", self.path, "update", "--id", "APP-0001", "--status", "ghosted")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--status must be one of", result.stderr)

    def test_update_unknown_id_rejected(self):
        result = run("--applications", self.path, "update", "--id", "APP-9999", "--status", "submitted")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no application with id", result.stderr)

    def test_update_no_fields_rejected(self):
        self.add()
        result = run("--applications", self.path, "update", "--id", "APP-0001")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no fields supplied", result.stderr)

    def test_notes_append_preserves_existing(self):
        self.add()
        run("--applications", self.path, "update", "--id", "APP-0001", "--notes-append", "first note")
        run("--applications", self.path, "update", "--id", "APP-0001", "--notes-append", "second note")
        entry = self.load()["applications"][0]
        self.assertIn("first note", entry["notes"])
        self.assertIn("second note", entry["notes"])

    def test_find_matches_existing_company(self):
        self.add(company="Goldman Sachs", role="IB Spring Insight")
        result = run("--applications", self.path, "find", "--company", "Goldman Sachs")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("APP-0001", result.stdout)

    def test_find_is_case_insensitive_and_substring_tolerant(self):
        self.add(company="Goldman Sachs", role="IB Spring Insight")
        result = run("--applications", self.path, "find", "--company", "goldman")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("APP-0001", result.stdout)

    def test_find_narrows_by_role_when_company_has_multiple(self):
        self.add(company="GSA Capital", role="Quantitative Researcher - Intern")
        self.add(company="GSA Capital", role="Women in Trading Insight Programme")
        result = run("--applications", self.path, "find", "--company", "GSA Capital", "--role", "Women in Trading")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("APP-0002", result.stdout)
        self.assertNotIn("APP-0001", result.stdout)

    def test_find_no_match_exits_nonzero(self):
        self.add(company="Goldman Sachs", role="IB Spring Insight")
        result = run("--applications", self.path, "find", "--company", "Blackstone")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no application found", result.stderr)


if __name__ == "__main__":
    unittest.main()
