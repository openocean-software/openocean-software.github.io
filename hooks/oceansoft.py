"""MkDocs hook that loads the site data files into ``config.extra``.

The home page, project directory, project pages and team page all render
from ``data/*.yml``, so adding a member project is one YAML entry instead of
edits to four pages. The hook also pulls the latest forum topics from
Discourse at build time; the nightly deploy keeps that list current without
needing CORS enabled on the hosted forum.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

# Deliberately outside the "mkdocs" logger namespace: a forum outage should
# warn on stderr, not fail `mkdocs build --strict` on an unrelated PR.
logger = logging.getLogger("oceansoft.hooks")

FORUM_URL = os.environ.get("OCEANSOFT_FORUM_URL", "https://forum.oceansoft.org")
FORUM_TIMEOUT_S = 10.0
FORUM_TOPIC_LIMIT = 5

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_PROJECT_REQUIRED = ("slug", "name", "kind", "category", "filter", "summary")
_PROJECT_KINDS = ("member", "initiative")
# Stages and badges from openocean-plan/member-projects/guidelines.
_STAGES = ("pond", "explorer", "estuary", "bay", "ocean")
_BADGES = ("research", "community", "project", "product", "ecosystem")
_EVENT_REQUIRED = ("name", "date", "venue")
_TEAM_REQUIRED = ("name", "role")

# Cached per process so `mkdocs serve` doesn't hit the forum on every
# live-reload rebuild.
_forum_cache: list[dict[str, Any]] | None = None


def on_config(config: Any, **kwargs: Any) -> Any:
    """Load data files and forum topics into ``config.extra`` for the templates."""
    projects = load_projects(_DATA_DIR / "projects.yml")
    events = load_records(_DATA_DIR / "events.yml", required=_EVENT_REQUIRED)
    team = load_records(_DATA_DIR / "team.yml", required=_TEAM_REQUIRED)

    today = dt.datetime.now(dt.timezone.utc).date()
    upcoming, recent = split_events(events, today=today)

    config.extra["projects"] = projects
    config.extra["events_upcoming"] = upcoming
    config.extra["events_recent"] = recent
    config.extra["team"] = team
    config.extra["forum_url"] = FORUM_URL
    config.extra["forum_topics"] = _get_forum_topics()
    config.extra["stats"] = {
        "members": sum(1 for p in projects if p["kind"] == "member"),
        "events_this_year": sum(1 for e in events if e["date"].year == today.year),
        "year": today.year,
    }
    return config


def on_page_context(context: Any, page: Any, config: Any, **kwargs: Any) -> Any:
    """Fail the build when a project page names a slug that isn't in projects.yml.

    Without this, overrides/project.html renders an empty header for a typo'd
    ``project:`` front matter key instead of erroring.
    """
    slug = page.meta.get("project")
    if slug is not None:
        check_project_slug(slug, config.extra["projects"], page_path=page.file.src_path)
    return context


def check_project_slug(slug: str, projects: list[dict[str, Any]], *, page_path: str) -> None:
    """Raise if ``slug`` doesn't name an entry in ``projects``."""
    known = [p["slug"] for p in projects]
    if slug not in known:
        raise ValueError(f"{page_path}: project '{slug}' is not in data/projects.yml — known slugs: {', '.join(known)}")


def load_projects(path: Path) -> list[dict[str, Any]]:
    """Read and validate ``projects.yml``.

    Raises on anything the templates would otherwise render wrong or
    silently drop, naming the file, the entry and the field to fix.
    """
    projects = load_records(path, required=_PROJECT_REQUIRED)

    seen: set[str] = set()
    for p in projects:
        slug = p["slug"]
        if slug in seen:
            raise ValueError(f"{path}: duplicate slug '{slug}' — slugs name the project page")
        seen.add(slug)
        _check_choice(path, slug, "kind", p.get("kind"), _PROJECT_KINDS)
        _check_choice(path, slug, "stage", p.get("stage"), _STAGES)
        _check_choice(path, slug, "badge", p.get("badge"), _BADGES)
        p.setdefault("page", f"projects/{slug}/")
    return projects


def load_records(path: Path, *, required: tuple[str, ...]) -> list[dict[str, Any]]:
    """Read a YAML list of mappings and check each has the ``required`` keys."""
    with path.open(encoding="utf-8") as f:
        records = yaml.safe_load(f) or []
    if not isinstance(records, list):
        raise ValueError(f"{path}: expected a list of entries at the top level")

    for i, rec in enumerate(records):
        label = rec.get("slug") or rec.get("name") or f"entry {i}"
        missing = [k for k in required if not rec.get(k)]
        if missing:
            raise ValueError(
                f"{path}: '{label}' is missing {', '.join(missing)} — see the field list at the top of the file"
            )
    return records


def split_events(
    events: list[dict[str, Any]], *, today: dt.date
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split events into (upcoming soonest-first, recent newest-first).

    An event on ``today`` still counts as upcoming so it stays at the top of
    the home page for the whole day.
    """
    for e in events:
        if not isinstance(e["date"], dt.date):
            raise ValueError(f"event '{e['name']}' has date {e['date']!r}, expected YYYY-MM-DD")
    upcoming = sorted((e for e in events if e["date"] >= today), key=lambda e: e["date"])
    recent = sorted((e for e in events if e["date"] < today), key=lambda e: e["date"], reverse=True)
    return upcoming, recent


def parse_forum_topics(
    latest: dict[str, Any],
    categories: dict[str, Any],
    *,
    base_url: str,
    limit: int,
) -> list[dict[str, Any]]:
    """Turn Discourse ``latest.json`` + ``categories.json`` into template rows.

    Pinned topics are skipped: the forum's pinned welcome post would
    otherwise sit at the top of the home page forever.
    """
    names: dict[int, str] = {}
    for c in categories.get("category_list", {}).get("categories", []):
        names[c["id"]] = c["name"]
        # Only present when requested with include_subcategories=true.
        for sub in c.get("subcategory_list") or []:
            names[sub["id"]] = sub["name"]

    rows = []
    for t in latest.get("topic_list", {}).get("topics", []):
        if t.get("pinned") or not t.get("visible", True):
            continue
        rows.append(
            {
                "title": t["title"],
                "url": f"{base_url.rstrip('/')}/t/{t['slug']}/{t['id']}",
                "category": names.get(t.get("category_id"), ""),
                "replies": t.get("reply_count", max(t.get("posts_count", 1) - 1, 0)),
            }
        )
        if len(rows) == limit:
            break
    return rows


def fetch_forum_topics(base_url: str, *, limit: int, timeout_s: float) -> list[dict[str, Any]]:
    """Fetch the latest topics from Discourse, or ``[]`` if the forum is unreachable.

    The home page hides the forum list when it is empty, so a failed fetch
    costs one stale section, never a failed deploy.
    """
    try:
        latest = _get_json(f"{base_url}/latest.json", timeout_s=timeout_s)
        categories = _get_json(f"{base_url}/categories.json?include_subcategories=true", timeout_s=timeout_s)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        logger.warning("forum fetch from %s failed (timeout: %.0f s), hiding forum list: %s", base_url, timeout_s, e)
        return []
    return parse_forum_topics(latest, categories, base_url=base_url, limit=limit)


def _get_forum_topics() -> list[dict[str, Any]]:
    global _forum_cache
    if os.environ.get("OCEANSOFT_SKIP_FORUM"):
        return []
    if _forum_cache is None:
        _forum_cache = fetch_forum_topics(FORUM_URL, limit=FORUM_TOPIC_LIMIT, timeout_s=FORUM_TIMEOUT_S)
    return _forum_cache


def _get_json(url: str, *, timeout_s: float) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return json.load(resp)


def _check_choice(path: Path, slug: str, key: str, value: Any, choices: tuple[str, ...]) -> None:
    if value is not None and value not in choices:
        raise ValueError(f"{path}: '{slug}' has {key} '{value}', expected one of {', '.join(choices)}")
