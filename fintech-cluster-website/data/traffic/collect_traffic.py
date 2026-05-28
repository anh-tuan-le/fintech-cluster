#!/usr/bin/env python3
"""
collect_traffic.py
==================
Pulls GitHub repository traffic from the API and merges it into local JSON
files so you keep history beyond GitHub's 14-day window.

Run automatically by .github/workflows/traffic.yml every day.
You can also run it locally:

    GH_TOKEN=<a token with repo scope> REPO=owner/name python collect_traffic.py

Outputs (in this folder):
    views.json        daily {date, count, uniques}      (page views)
    clones.json       daily {date, count, uniques}      (git clones)
    referrers.json    latest top referring sites (snapshot, 14-day)
    paths.json        latest top pages on the repo (snapshot, 14-day)
    summary.json      totals + last-updated timestamp

NOTE: GitHub's traffic API covers your REPOSITORY (the GitHub pages of your
repo: views/clones/referrers). It does NOT report visitor countries — that
comes from GoatCounter on the live site. The two are complementary.
"""

import json, os, sys, urllib.request, urllib.error
from datetime import datetime, timezone

REPO  = os.environ.get("REPO")          # "owner/name"
TOKEN = os.environ.get("GH_TOKEN")
HERE  = os.path.dirname(os.path.abspath(__file__))

if not REPO or not TOKEN:
    sys.exit("Set REPO=owner/name and GH_TOKEN=<token>. "
             "(In Actions these are provided automatically.)")

API = f"https://api.github.com/repos/{REPO}/traffic"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "traffic-collector",
}

def get(path):
    req = urllib.request.Request(API + path, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"GitHub API error {e.code} on {path}: {e.read().decode()[:300]}")

def load(name):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        try:
            return json.load(open(p))
        except Exception:
            return None
    return None

def save(name, obj):
    json.dump(obj, open(os.path.join(HERE, name), "w"), indent=2)
    print("wrote", name)

def merge_daily(existing, fresh, key="timestamp"):
    """Merge daily series keyed by date; new values overwrite the same date,
    older dates are preserved (this is how we beat the 14-day limit)."""
    by_date = {}
    for row in (existing or []):
        by_date[row[key][:10]] = row
    for row in fresh:
        by_date[row[key][:10]] = {
            "timestamp": row["timestamp"],
            "count": row.get("count", 0),
            "uniques": row.get("uniques", 0),
        }
    return [by_date[d] for d in sorted(by_date)]

# ---- views & clones (daily series we accumulate) ----
views_api  = get("/views")
clones_api = get("/clones")
views  = merge_daily(load("views.json"),  views_api.get("views",  []))
clones = merge_daily(load("clones.json"), clones_api.get("clones", []))
save("views.json", views)
save("clones.json", clones)

# ---- referrers & top paths (snapshots; latest wins) ----
referrers = get("/popular/referrers")    # [{referrer, count, uniques}]
paths     = get("/popular/paths")        # [{path, title, count, uniques}]
save("referrers.json", referrers)
save("paths.json", paths)

# ---- summary ----
summary = {
    "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "repo": REPO,
    "views_total_14d":  views_api.get("count", 0),
    "views_unique_14d": views_api.get("uniques", 0),
    "clones_total_14d": clones_api.get("count", 0),
    "clones_unique_14d": clones_api.get("uniques", 0),
    "views_all_time_recorded":  sum(r["count"] for r in views),
    "clones_all_time_recorded": sum(r["count"] for r in clones),
    "days_recorded": len(views),
}
save("summary.json", summary)
print("done:", json.dumps(summary, indent=2))
