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

import json
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import pytest

from cleanup_artifacts import main, select_for_deletion, select_logs_for_erasure

NOW = datetime(2026, 11, 2, 12, tzinfo=timezone.utc)
ARCHIVE = [{"file_type": "archive"}, {"file_type": "trace"}]
LOG = [{"file_type": "trace"}]


def job(job_id, days_old, ref="main", name="pylint", artifacts=ARCHIVE, status="success"):
    return {"id": job_id, "name": name, "ref": ref, "artifacts": artifacts, "status": status,
            "created_at": (NOW - timedelta(days=days_old)).isoformat().replace("+00:00", "Z")}


def ids(jobs):
    return sorted(j["id"] for j in jobs)


def test_newest_five_on_default_branch_are_kept_regardless_of_age():
    jobs = [job(i, days_old=100 + i) for i in range(1, 9)]  # all older than 30 days
    keep, delete = select_for_deletion(jobs, "pylint", "main", 5, 30, NOW)
    assert ids(keep) == [1, 2, 3, 4, 5]
    assert ids(delete) == [6, 7, 8]


def test_recent_artifacts_are_kept_beyond_the_newest_five():
    jobs = [job(i, days_old=i) for i in range(1, 9)]  # all younger than 30 days
    keep, delete = select_for_deletion(jobs, "pylint", "main", 5, 30, NOW)
    assert ids(keep) == list(range(1, 9)) and delete == []


def test_other_branches_expire_by_age_only():
    jobs = [job(1, 40, ref="feature"), job(2, 10, ref="feature"), job(3, 50)]
    keep, delete = select_for_deletion(jobs, "pylint", "main", 5, 30, NOW)
    assert ids(delete) == [1]
    assert ids(keep) == [2, 3]


def test_other_jobs_and_jobs_without_artifacts_are_ignored():
    jobs = [job(1, 90, name="tests"), job(2, 90, artifacts=[{"file_type": "trace"}]), job(3, 90, artifacts=[]),
            job(4, 90, ref="old-branch")]
    keep, delete = select_for_deletion(jobs, "pylint", "main", 5, 30, NOW)
    assert ids(delete) == [4] and keep == []


def test_only_old_finished_jobs_with_nothing_but_a_log_are_erased():
    jobs = [job(1, 200, artifacts=LOG), job(2, 200, ref="feature", artifacts=LOG, status="failed"),
            job(3, 100, artifacts=LOG),  # younger than six months
            job(4, 200),  # still has artifacts: handled by the artifact deletion
            job(5, 200, artifacts=[]),  # already erased
            job(6, 200, artifacts=LOG, name="tests"), job(7, 200, artifacts=LOG, status="running")]
    erase = select_logs_for_erasure(jobs, "pylint", 183, NOW)
    assert [j["id"] for j in erase] == [1, 2]


class FakeGitLab(BaseHTTPRequestHandler):
    jobs = []
    deleted = []
    erased = []
    tokens = set()

    def log_message(self, *args):
        pass

    def do_GET(self):
        FakeGitLab.tokens.add(self.headers.get("PRIVATE-TOKEN"))
        page = int(parse_qs(urlparse(self.path).query)["page"][0])
        batch = FakeGitLab.jobs[(page - 1) * 3: page * 3]  # 3 jobs per page to exercise pagination
        self.send_response(200)
        self.send_header("X-Next-Page", str(page + 1) if page * 3 < len(FakeGitLab.jobs) else "")
        self.end_headers()
        self.wfile.write(json.dumps(batch).encode())

    def do_DELETE(self):
        FakeGitLab.deleted.append(int(self.path.split("/jobs/")[1].split("/")[0]))
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        assert self.path.endswith("/erase")
        FakeGitLab.erased.append(int(self.path.split("/jobs/")[1].split("/")[0]))
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"{}")


@pytest.fixture
def gitlab():
    FakeGitLab.jobs = ([job(i, days_old=10 * i) for i in range(1, 8)] + [job(20, 60, ref="feature")]
                       + [job(30, 200, artifacts=LOG), job(31, 300, ref="feature", artifacts=LOG),
                          job(32, 100, artifacts=LOG)])
    FakeGitLab.deleted, FakeGitLab.erased, FakeGitLab.tokens = [], [], set()
    server = HTTPServer(("127.0.0.1", 0), FakeGitLab)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield {"CI_API_V4_URL": f"http://127.0.0.1:{server.server_port}/api/v4", "CI_PROJECT_ID": "42",
           "CI_DEFAULT_BRANCH": "main", "ARTIFACT_CLEANUP_TOKEN": "secret"}
    server.shutdown()


def test_main_deletes_old_artifacts_through_the_api(gitlab):
    assert main(gitlab, NOW) == 0
    # jobs 1-5 are the newest on main; 6, 7 (60, 70 days) and the 60 day old feature job are deleted
    assert sorted(FakeGitLab.deleted) == [6, 7, 20]
    assert FakeGitLab.tokens == {"secret"}
    assert FakeGitLab.erased == []  # erasing logs is off by default


def test_main_erases_old_logs_when_enabled(gitlab, capsys):
    assert main({**gitlab, "ARTIFACT_CLEANUP_ERASE_LOGS": "true"}, NOW) == 0
    assert sorted(FakeGitLab.deleted) == [6, 7, 20]
    assert sorted(FakeGitLab.erased) == [30, 31]  # job 32 is younger than six months
    assert "2 job(s) with only a log left older than 183 days to erase" in capsys.readouterr().out


def test_dry_run_deletes_and_erases_nothing(gitlab, capsys):
    assert main({**gitlab, "ARTIFACT_CLEANUP_DRY_RUN": "true", "ARTIFACT_CLEANUP_ERASE_LOGS": "true"}, NOW) == 0
    assert FakeGitLab.deleted == [] and FakeGitLab.erased == []
    out = capsys.readouterr().out
    assert out.count("would delete") == 3 and out.count("would erase") == 2


def test_missing_token_is_reported(gitlab, capsys):
    environ = dict(gitlab)
    del environ["ARTIFACT_CLEANUP_TOKEN"]
    assert main(environ, NOW) == 2
    assert "ARTIFACT_CLEANUP_TOKEN" in capsys.readouterr().err
