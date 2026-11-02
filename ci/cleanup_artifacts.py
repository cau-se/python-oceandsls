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
"""Delete old job artifacts while keeping the newest ones on the default branch.

GitLab can only expire artifacts by age (artifacts:expire_in). This script implements "expire after N days, but
always keep the newest K artifacts on the default branch": the job's artifacts never expire (expire_in: never) and
this script, run from a scheduled pipeline, deletes the artifacts of all other jobs that are older than N days.

Configuration (environment variables):
    ARTIFACT_CLEANUP_TOKEN          access token, required: a fine-grained personal access token for the project
                                    with the permissions "Job: Read" (list jobs) and "Job Artifact: Delete"; its
                                    owner needs the Maintainer role. A legacy token with scope api works as well.
    ARTIFACT_CLEANUP_JOB            name of the job whose artifacts are cleaned up (default: pylint)
    ARTIFACT_CLEANUP_KEEP           number of newest artifacts on the default branch to keep (default: 5)
    ARTIFACT_CLEANUP_MAX_AGE_DAYS   other artifacts are deleted once they are older than this (default: 30)
    ARTIFACT_CLEANUP_DRY_RUN        "true": only report what would be deleted
    CI_API_V4_URL, CI_PROJECT_ID, CI_DEFAULT_BRANCH   provided by GitLab CI
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional, Tuple


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def has_artifacts(job: Dict) -> bool:
    """True if the job still has artifacts besides its log (trace), which is not deleted."""
    return any(a.get("file_type") != "trace" for a in job.get("artifacts") or [])


def select_for_deletion(
        jobs: Iterable[Dict], job_name: str, default_branch: str, keep: int, max_age_days: int, now: datetime
) -> Tuple[List[Dict], List[Dict]]:
    """Return (jobs to keep, jobs whose artifacts are deleted).

    The newest ``keep`` jobs with artifacts on the default branch are always kept; all other jobs with artifacts are
    deleted when they are older than ``max_age_days``.
    """
    candidates = sorted(
        (j for j in jobs if j.get("name") == job_name and has_artifacts(j)),
        key=lambda j: parse_time(j["created_at"]), reverse=True,
    )
    newest_on_default = [j for j in candidates if j.get("ref") == default_branch][:keep]
    kept_ids = {j["id"] for j in newest_on_default}
    limit = now - timedelta(days=max_age_days)
    delete = [j for j in candidates if j["id"] not in kept_ids and parse_time(j["created_at"]) < limit]
    keep_list = [j for j in candidates if j not in delete]
    return keep_list, delete


class GitLab:
    """Minimal GitLab REST client (standard library only, so the job needs no extra packages)."""

    def __init__(self, api_url: str, project_id: str, token: str):
        self.base = f"{api_url.rstrip('/')}/projects/{urllib.parse.quote(str(project_id), safe='')}"
        self.token = token

    def request(self, method: str, path: str, params: Optional[Dict] = None):
        url = self.base + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
        request = urllib.request.Request(url, method=method, headers={"PRIVATE-TOKEN": self.token})
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            return (json.loads(body) if body else None), response.headers

    def jobs(self) -> List[Dict]:
        """All jobs of the project (newest first), following the pagination headers."""
        jobs, page = [], "1"
        while page:
            batch, headers = self.request("GET", "/jobs", {"per_page": 100, "page": page})
            jobs.extend(batch)
            page = headers.get("X-Next-Page", "")
        return jobs

    def delete_artifacts(self, job_id: int) -> None:
        self.request("DELETE", f"/jobs/{job_id}/artifacts")


def main(environ: Optional[Dict[str, str]] = None, now: Optional[datetime] = None) -> int:
    env = os.environ if environ is None else environ
    token = env.get("ARTIFACT_CLEANUP_TOKEN")
    if not token:
        print("ARTIFACT_CLEANUP_TOKEN is not set: add a fine-grained personal access token with the permissions "
              "'Job: Read' and 'Job Artifact: Delete' as masked CI/CD variable.", file=sys.stderr)
        return 2
    job_name = env.get("ARTIFACT_CLEANUP_JOB", "pylint")
    keep = int(env.get("ARTIFACT_CLEANUP_KEEP", "5"))
    max_age_days = int(env.get("ARTIFACT_CLEANUP_MAX_AGE_DAYS", "30"))
    dry_run = env.get("ARTIFACT_CLEANUP_DRY_RUN", "false").lower() == "true"
    default_branch = env.get("CI_DEFAULT_BRANCH", "main")

    gitlab = GitLab(env["CI_API_V4_URL"], env["CI_PROJECT_ID"], token)
    keep_list, delete = select_for_deletion(
        gitlab.jobs(), job_name, default_branch, keep, max_age_days, now or datetime.now(timezone.utc)
    )
    print(f"{job_name}: {len(keep_list)} job(s) with artifacts kept, {len(delete)} older than {max_age_days} days "
          f"to delete (the newest {keep} on {default_branch} are always kept){' [dry run]' if dry_run else ''}")
    failed = 0
    for job in delete:
        line = f"  job {job['id']} ({job.get('ref')}, {job['created_at']})"
        if dry_run:
            print(line + ": would delete")
            continue
        try:
            gitlab.delete_artifacts(job["id"])
            print(line + ": deleted")
        except urllib.error.HTTPError as e:
            failed += 1
            print(line + f": deletion failed ({e.code} {e.reason})", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
