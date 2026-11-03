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
"""Delete old job artifacts while keeping the newest ones on the default branch, optionally erase old job logs.

GitLab can only expire artifacts by age (artifacts:expire_in). This script implements "expire after N days, but
always keep the newest K artifacts on the default branch": the job's artifacts never expire (expire_in: never) and
this script, run from a scheduled pipeline, deletes the artifacts of all other jobs that are older than N days.

Deleting artifacts keeps the job log (trace). With ARTIFACT_CLEANUP_ERASE_LOGS=true the script also erases jobs of
the same name that have nothing but their log left and are older than ARTIFACT_CLEANUP_LOG_MAX_AGE_DAYS: GitLab removes
the log (and any artifacts) of an erased job; the job itself stays in the pipeline. Erasing cannot be undone. Jobs
whose artifacts are deleted in a run have only their log left and are erased in a later run once they are old enough.

Configuration (environment variables):
    ARTIFACT_CLEANUP_TOKEN          access token, required: a fine-grained personal access token for the project
                                    with the permissions "Job: Read" (list jobs) and "Job Artifact: Delete", plus
                                    "Job: Delete" (erase jobs) when logs are erased; its owner needs the Maintainer
                                    role. A legacy token with scope api works as well.
    ARTIFACT_CLEANUP_JOB            name of the job whose artifacts are cleaned up (default: pylint)
    ARTIFACT_CLEANUP_KEEP           number of newest artifacts on the default branch to keep (default: 5)
    ARTIFACT_CLEANUP_MAX_AGE_DAYS   other artifacts are deleted once they are older than this (default: 30)
    ARTIFACT_CLEANUP_ERASE_LOGS     "true": also erase jobs that only have their log left (default: false)
    ARTIFACT_CLEANUP_LOG_MAX_AGE_DAYS  such jobs are erased once they are older than this (default: 183, six months)
    ARTIFACT_CLEANUP_DRY_RUN        "true": only report what would be deleted and erased
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

# Jobs in these states are not finished yet and are never erased
UNFINISHED = {"created", "waiting_for_resource", "preparing", "pending", "running", "scheduled", "manual"}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def has_artifacts(job: Dict) -> bool:
    """True if the job still has artifacts besides its log (trace), which is not deleted."""
    return any(a.get("file_type") != "trace" for a in job.get("artifacts") or [])


def has_only_log(job: Dict) -> bool:
    """True if the job's log (trace) is all that is left of it."""
    artifacts = job.get("artifacts") or []
    return bool(artifacts) and all(a.get("file_type") == "trace" for a in artifacts)


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


def select_logs_for_erasure(jobs: Iterable[Dict], job_name: str, max_age_days: int, now: datetime) -> List[Dict]:
    """Return the finished jobs named ``job_name`` that only have their log left and are older than
    ``max_age_days`` (oldest first)."""
    limit = now - timedelta(days=max_age_days)
    return sorted(
        (j for j in jobs
         if j.get("name") == job_name and has_only_log(j) and j.get("status") not in UNFINISHED
         and parse_time(j["created_at"]) < limit),
        key=lambda j: parse_time(j["created_at"]),
    )


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

    def erase(self, job_id: int) -> None:
        """Erase a job: removes its log and artifacts (cannot be undone)."""
        self.request("POST", f"/jobs/{job_id}/erase")


def apply(jobs: List[Dict], action, done: str, would: str, failure: str, hint: str = "") -> int:
    """Run ``action`` on every job and report ``done``; in a dry run (``would`` is set) only report ``would``.

    Return the number of failures.
    """
    failed = 0
    for job in jobs:
        line = f"  job {job['id']} ({job.get('ref')}, {job['created_at']})"
        if would:
            print(f"{line}: {would}")
            continue
        try:
            action(job["id"])
            print(f"{line}: {done}")
        except urllib.error.HTTPError as e:
            failed += 1
            print(f"{line}: {failure} failed ({e.code} {e.reason}){hint if e.code == 403 else ''}", file=sys.stderr)
    return failed


def main(environ: Optional[Dict[str, str]] = None, now: Optional[datetime] = None) -> int:
    env = os.environ if environ is None else environ
    token = env.get("ARTIFACT_CLEANUP_TOKEN")
    erase_logs = env.get("ARTIFACT_CLEANUP_ERASE_LOGS", "false").lower() == "true"
    if not token:
        print("ARTIFACT_CLEANUP_TOKEN is not set: add a fine-grained personal access token with the permissions "
              "'Job: Read' and 'Job Artifact: Delete'" + (" and 'Job: Delete'" if erase_logs else "")
              + " as masked CI/CD variable.", file=sys.stderr)
        return 2
    job_name = env.get("ARTIFACT_CLEANUP_JOB", "pylint")
    keep = int(env.get("ARTIFACT_CLEANUP_KEEP", "5"))
    max_age_days = int(env.get("ARTIFACT_CLEANUP_MAX_AGE_DAYS", "30"))
    log_max_age_days = int(env.get("ARTIFACT_CLEANUP_LOG_MAX_AGE_DAYS", "183"))
    dry_run = env.get("ARTIFACT_CLEANUP_DRY_RUN", "false").lower() == "true"
    default_branch = env.get("CI_DEFAULT_BRANCH", "main")
    now = now or datetime.now(timezone.utc)
    dry = " [dry run]" if dry_run else ""

    gitlab = GitLab(env["CI_API_V4_URL"], env["CI_PROJECT_ID"], token)
    jobs = gitlab.jobs()

    keep_list, delete = select_for_deletion(jobs, job_name, default_branch, keep, max_age_days, now)
    print(f"{job_name}: {len(keep_list)} job(s) with artifacts kept, {len(delete)} older than {max_age_days} days "
          f"to delete (the newest {keep} on {default_branch} are always kept){dry}")
    failed = apply(delete, gitlab.delete_artifacts, "deleted", "would delete" if dry_run else "", "deletion")

    logs = select_logs_for_erasure(jobs, job_name, log_max_age_days, now)
    if not erase_logs:
        print(f"{job_name}: {len(logs)} job(s) with only a log left older than {log_max_age_days} days "
              f"(set ARTIFACT_CLEANUP_ERASE_LOGS=true to erase them)")
        return 1 if failed else 0
    print(f"{job_name}: {len(logs)} job(s) with only a log left older than {log_max_age_days} days to erase{dry}")
    failed += apply(logs, gitlab.erase, "erased", "would erase" if dry_run else "", "erasing",
                    " - does the token have the permission 'Job: Delete'?")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
