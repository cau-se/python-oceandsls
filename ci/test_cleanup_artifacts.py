#  Copyright (c) 2026.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Tests of the artifact cleanup used by the scheduled CI pipeline."""

import contextlib
import io
import json
import threading
import unittest
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from parameterized import parameterized

from cleanup_artifacts import main, select_for_deletion, select_logs_for_erasure

NOW = datetime(2026, 11, 2, 12, tzinfo=timezone.utc)
ARCHIVE = ({"file_type": "archive"}, {"file_type": "trace"})
LOG = ({"file_type": "trace"},)


def job(job_id, days_old, ref="main", name="pylint", artifacts=ARCHIVE, status="success"):
    return {"id": job_id, "name": name, "ref": ref, "artifacts": artifacts, "status": status,
            "created_at": (NOW - timedelta(days=days_old)).isoformat().replace("+00:00", "Z")}


def ids(jobs):
    return sorted(j["id"] for j in jobs)


class TestSelection(unittest.TestCase):

    @parameterized.expand([
        ("newest_five_on_default_branch_kept_regardless_of_age", [job(i, days_old=100 + i) for i in range(1, 9)],
         [1, 2, 3, 4, 5], [6, 7, 8]),
        # The newest five jobs on the default branch keep their artifacts however old they are
        # Input: eight jobs on main, all older than 30 days
        # Expected Result: the newest five kept, the other three deleted

        ("recent_artifacts_kept_beyond_newest_five", [job(i, days_old=i) for i in range(1, 9)],
         list(range(1, 9)), []),
        # Artifacts younger than 30 days are kept beyond the newest five
        # Input: eight jobs on main, all younger than 30 days
        # Expected Result: all kept

        ("other_branches_expire_by_age_only", [job(1, 40, ref="feature"), job(2, 10, ref="feature"), job(3, 50)],
         [2, 3], [1]),
        # On other branches only the age counts
        # Input: feature jobs 40 and 10 days old, a main job 50 days old
        # Expected Result: the 40 day old feature job deleted

        ("other_jobs_and_jobs_without_artifacts_ignored",
         [job(1, 90, name="tests"), job(2, 90, artifacts=[{"file_type": "trace"}]), job(3, 90, artifacts=[]),
          job(4, 90, ref="old-branch")], [], [4]),
        # Only jobs of the selected name with an artifact archive are considered
        # Input: an old tests job, pylint jobs with a log only or no artifacts, an old job on another branch
        # Expected Result: only the job on the other branch deleted, nothing kept

        ("fewer_than_five_on_default_branch", [job(i, days_old=100 + i) for i in range(1, 4)], [1, 2, 3], []),
        # Fewer than five jobs on the default branch are all kept
        # Input: three old jobs on main
        # Expected Result: all kept

        ("maximum_age_is_inclusive", [job(1, 29, ref="feature"), job(2, 30, ref="feature"),
                                      job(3, 31, ref="feature")], [1, 2], [3]),
        # Artifacts expire after more than 30 days
        # Input: feature jobs 29, 30 and 31 days old
        # Expected Result: the 31 day old job deleted

        ("no_jobs", [], [], []),
        # A project without jobs
        # Input: no jobs
        # Expected Result: nothing kept or deleted
    ])
    def test_select_for_deletion(self, test_name, jobs, expected_keep, expected_delete):
        keep, delete = select_for_deletion(jobs, "pylint", "main", 5, 30, NOW)
        self.assertEqual(expected_keep, ids(keep), test_name)
        self.assertEqual(expected_delete, ids(delete), test_name)

    @parameterized.expand([
        ("old_log_on_default_branch", [job(1, 200, artifacts=LOG)], [1]),
        # A finished job older than six months with nothing but a log is erased
        # Input: a successful pylint job on main, 200 days old, only a log
        # Expected Result: erased

        ("old_failed_log_on_other_branch", [job(2, 200, ref="feature", artifacts=LOG, status="failed")], [2]),
        # The branch and the result do not matter
        # Input: a failed pylint job on a feature branch, 200 days old, only a log
        # Expected Result: erased

        ("younger_than_six_months", [job(3, 100, artifacts=LOG)], []),
        # Younger logs are kept
        # Input: a pylint job 100 days old with only a log
        # Expected Result: not erased

        ("still_has_artifacts", [job(4, 200)], []),
        # Jobs with an artifact archive are handled by the artifact deletion
        # Input: a pylint job 200 days old with an archive
        # Expected Result: not erased

        ("already_erased", [job(5, 200, artifacts=[])], []),
        # Erased jobs have no artifacts left
        # Input: a pylint job 200 days old without artifacts
        # Expected Result: not erased

        ("other_job", [job(6, 200, artifacts=LOG, name="tests")], []),
        # Only jobs of the selected name are erased
        # Input: a tests job 200 days old with only a log
        # Expected Result: not erased

        ("running_job", [job(7, 200, artifacts=LOG, status="running")], []),
        # Unfinished jobs are not erased
        # Input: a running pylint job with only a log
        # Expected Result: not erased

        ("canceled_job", [job(8, 200, artifacts=LOG, status="canceled")], [8]),
        # Canceled jobs are finished
        # Input: a canceled pylint job 200 days old with only a log
        # Expected Result: erased

        ("maximum_age_is_inclusive", [job(9, 182, artifacts=LOG), job(10, 183, artifacts=LOG),
                                      job(11, 184, artifacts=LOG)], [11]),
        # Logs expire after more than 183 days
        # Input: pylint jobs 182, 183 and 184 days old with only a log
        # Expected Result: the 184 day old job erased
    ])
    def test_select_logs_for_erasure(self, test_name, jobs, expected_ids):
        erase = select_logs_for_erasure(jobs, "pylint", 183, NOW)
        self.assertEqual(expected_ids, [j["id"] for j in erase], test_name)


class FakeGitLab(BaseHTTPRequestHandler):
    jobs = []
    deleted = []
    erased = []
    tokens = set()

    def log_message(self, *args):  # pylint: disable=arguments-differ
        pass

    def do_GET(self):  # pylint: disable=invalid-name
        FakeGitLab.tokens.add(self.headers.get("PRIVATE-TOKEN"))
        page = int(parse_qs(urlparse(self.path).query)["page"][0])
        batch = FakeGitLab.jobs[(page - 1) * 3: page * 3]  # 3 jobs per page to exercise pagination
        self.send_response(200)
        self.send_header("X-Next-Page", str(page + 1) if page * 3 < len(FakeGitLab.jobs) else "")
        self.end_headers()
        self.wfile.write(json.dumps(batch).encode())

    def do_DELETE(self):  # pylint: disable=invalid-name
        FakeGitLab.deleted.append(int(self.path.split("/jobs/")[1].split("/")[0]))
        self.send_response(204)
        self.end_headers()

    def do_POST(self):  # pylint: disable=invalid-name
        assert self.path.endswith("/erase")
        FakeGitLab.erased.append(int(self.path.split("/jobs/")[1].split("/")[0]))
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"{}")


class TestMain(unittest.TestCase):
    """main() against a fake GitLab API with pylint jobs 10 to 70 days old on main, a 60 day old feature job and
    jobs 200 (main), 300 (feature) and 100 days old with only a log left."""

    def setUp(self):
        FakeGitLab.jobs = ([job(i, days_old=10 * i) for i in range(1, 8)] + [job(20, 60, ref="feature")]
                           + [job(30, 200, artifacts=LOG), job(31, 300, ref="feature", artifacts=LOG),
                              job(32, 100, artifacts=LOG)])
        FakeGitLab.deleted, FakeGitLab.erased, FakeGitLab.tokens = [], [], set()
        server = HTTPServer(("127.0.0.1", 0), FakeGitLab)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        self.environ = {"CI_API_V4_URL": f"http://127.0.0.1:{server.server_port}/api/v4", "CI_PROJECT_ID": "42",
                        "CI_DEFAULT_BRANCH": "main", "ARTIFACT_CLEANUP_TOKEN": "secret"}

    @parameterized.expand([
        ("delete_old_artifacts", {}, 0, [6, 7, 20], [], ["3 older than 30 days to delete",
                                                          "set ARTIFACT_CLEANUP_ERASE_LOGS=true to erase them"]),
        # Old artifacts are deleted through the API; erasing logs is off by default
        # Input: the default settings
        # Expected Result: jobs 6, 7 (60, 70 days) and the 60 day old feature job deleted, no logs erased

        ("erase_old_logs", {"ARTIFACT_CLEANUP_ERASE_LOGS": "true"}, 0, [6, 7, 20], [30, 31],
         ["2 job(s) with only a log left older than 183 days to erase"]),
        # Logs older than six months are erased when enabled
        # Input: ARTIFACT_CLEANUP_ERASE_LOGS=true
        # Expected Result: the artifacts deleted and the logs of jobs 30 and 31 erased (job 32 is younger)

        ("dry_run", {"ARTIFACT_CLEANUP_DRY_RUN": "true", "ARTIFACT_CLEANUP_ERASE_LOGS": "true"}, 0, [], [],
         ["would delete"] * 3 + ["would erase"] * 2),
        # A dry run deletes and erases nothing
        # Input: ARTIFACT_CLEANUP_DRY_RUN=true and ARTIFACT_CLEANUP_ERASE_LOGS=true
        # Expected Result: nothing deleted or erased, three deletions and two erasures reported

        ("keep_more", {"ARTIFACT_CLEANUP_KEEP": "7"}, 0, [20], [], ["the newest 7 on main are always kept"]),
        # The number of kept jobs is configurable
        # Input: ARTIFACT_CLEANUP_KEEP=7
        # Expected Result: only the feature job deleted

        ("longer_maximum_age", {"ARTIFACT_CLEANUP_MAX_AGE_DAYS": "100"}, 0, [], [],
         ["0 older than 100 days to delete"]),
        # The maximum age is configurable
        # Input: ARTIFACT_CLEANUP_MAX_AGE_DAYS=100
        # Expected Result: nothing deleted
    ])
    def test_main(self, test_name, settings, expected_code, expected_deleted, expected_erased, expected_output):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main({**self.environ, **settings}, NOW)

        self.assertEqual(expected_code, code, test_name)
        self.assertEqual(expected_deleted, sorted(FakeGitLab.deleted), test_name)
        self.assertEqual(expected_erased, sorted(FakeGitLab.erased), test_name)
        self.assertEqual({"secret"}, FakeGitLab.tokens, test_name)
        output = out.getvalue()
        for part in set(expected_output):
            self.assertEqual(expected_output.count(part), output.count(part), f"{test_name}: {part}\n{output}")

    @parameterized.expand([
        ("missing_token", {}, ["ARTIFACT_CLEANUP_TOKEN is not set", "'Job: Read' and 'Job Artifact: Delete'"],
         "'Job: Delete'"),
        # A missing token is reported with the required permissions
        # Input: no ARTIFACT_CLEANUP_TOKEN
        # Expected Result: exit code 2, the permissions Job: Read and Job Artifact: Delete named

        ("missing_token_erase_logs", {"ARTIFACT_CLEANUP_ERASE_LOGS": "true"},
         ["ARTIFACT_CLEANUP_TOKEN is not set", "and 'Job: Delete'"], None),
        # Erasing logs needs another permission
        # Input: no ARTIFACT_CLEANUP_TOKEN, ARTIFACT_CLEANUP_ERASE_LOGS=true
        # Expected Result: exit code 2, the permission Job: Delete named as well

        ("empty_token", {"ARTIFACT_CLEANUP_TOKEN": ""}, ["ARTIFACT_CLEANUP_TOKEN is not set"], None),
        # An empty token counts as missing
        # Input: an empty ARTIFACT_CLEANUP_TOKEN
        # Expected Result: exit code 2
    ])
    def test_missing_token(self, test_name, settings, expected_parts, unexpected_part):
        environ = {**self.environ, **settings}
        if "ARTIFACT_CLEANUP_TOKEN" not in settings:
            del environ["ARTIFACT_CLEANUP_TOKEN"]
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = main(environ, NOW)

        self.assertEqual(2, code, test_name)
        for part in expected_parts:
            self.assertIn(part, err.getvalue(), test_name)
        if unexpected_part:
            self.assertNotIn(unexpected_part, err.getvalue(), test_name)
        self.assertEqual(([], []), (FakeGitLab.deleted, FakeGitLab.erased), test_name)


if __name__ == "__main__":
    unittest.main()
