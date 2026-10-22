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
# Directory filter chips, in display order. overrides/projects.html draws the
# chips from this, so a project's `filter` can't name a chip that doesn't exist.
_FILTERS = {
    "autonomy": "Autonomy",
    "middleware": "Middleware and comms",
    "ros": "ROS 2",
    "encoding": "Encoding",
    "oos": "Built by Open Ocean",
}
# Stages and badges from openocean-plan/member-projects/guidelines.
_STAGES = ("pond", "explorer", "estuary", "bay", "ocean")
_BADGES = ("research", "community", "project", "product", "ecosystem")
_EVENT_REQUIRED = ("name", "date", "venue")
_TEAM_REQUIRED = ("name", "role")

# projects/index.md marks where the card grid goes; overrides/projects.html
# replaces this exact rendered paragraph.
DIRECTORY_MARKER = "<p>[[directory]]</p>"

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
    config.extra["filters"] = [{"key": k, "label": v} for k, v in _FILTERS.items()]
    config.extra["directory_marker"] = DIRECTORY_MARKER
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


def on_page_markdown(markdown: str, page: Any, config: Any, **kwargs: Any) -> str:
    """Fail the build if devsecops.md and mkdocs.yml disagree on the signing key.

    The fingerprint is written out in prose on the DevSecOps page and read from
    ``extra.signing_key`` by the project page trust panel; a key rotation that
    updates only one of them would show users a stale fingerprint.
    """
    if page.file.src_path == "devsecops.md":
        check_fingerprint_in_page(markdown, config.extra["signing_key"]["fingerprint"], page_path=page.file.src_path)
    return markdown


def on_page_content(html: str, page: Any, config: Any, **kwargs: Any) -> str:
    """Fail the build when a directory page has lost its ``[[directory]]`` marker."""
    if page.meta.get("template") == "projects.html":
        check_directory_marker(html, page_path=page.file.src_path)
    return html


def on_page_context(context: Any, page: Any, config: Any, **kwargs: Any) -> Any:
    """Fail the build when a project page doesn't name a slug from projects.yml.

    Without this, overrides/project.html renders an empty header for a missing
    or typo'd ``project:`` front matter key instead of erroring.
    """
    check_project_page(page.meta, config.extra["projects"], page_path=page.file.src_path)
    return context


def check_project_page(meta: dict[str, Any], projects: list[dict[str, Any]], *, page_path: str) -> None:
    """Raise if a page using project.html, or naming a ``project:``, has no known slug."""
    slug = meta.get("project")
    if slug is None:
        if meta.get("template") == "project.html":
            raise ValueError(f"{page_path}: uses template project.html but has no `project: <slug>` in its front matter")
        return
    known = [p["slug"] for p in projects]
    if slug not in known:
        raise ValueError(f"{page_path}: project '{slug}' is not in data/projects.yml — known slugs: {', '.join(known)}")


def check_directory_marker(html: str, *, page_path: str) -> None:
    """Raise if the rendered directory page doesn't contain :data:`DIRECTORY_MARKER`."""
    if DIRECTORY_MARKER not in html:
        raise ValueError(
            f"{page_path}: no '[[directory]]' paragraph found — put [[directory]] alone on its own line "
            "where the project cards should go"
        )


def check_fingerprint_in_page(markdown: str, fingerprint: str, *, page_path: str) -> None:
    """Raise if ``fingerprint`` (no spaces) doesn't appear in the page source."""
    if fingerprint not in markdown:
        raise ValueError(
            f"{page_path}: signing key fingerprint {fingerprint} from mkdocs.yml extra.signing_key "
            "is not on this page — update both together"
        )


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
        _check_choice(path, slug, "filter", p.get("filter"), tuple(_FILTERS))
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
        # YAML loads "2026-11-05 09:00" as a datetime, which is a date subclass
        # but can't be compared with today's date.
        if isinstance(e["date"], dt.datetime) or not isinstance(e["date"], dt.date):
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
    otherwise sit at the top of the home page forever. Titles are returned
    raw (Discourse's ``title``, not the pre-escaped ``fancy_title``); the
    templates escape them.
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
                "url": f"{base_url.rstrip('/')}/t/{t['slug']}/{int(t['id'])}",
                "category": names.get(t.get("category_id"), ""),
                # posts_count - 1 matches the forum's own Replies column;
                # reply_count only counts posts made as a reply to another post.
                "replies": max(t.get("posts_count", 1) - 1, 0),
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
        return parse_forum_topics(latest, categories, base_url=base_url, limit=limit)
    except Exception as e:  # network, HTTP, JSON or response-shape failure: hide the list, keep building
        logger.warning(
            "forum fetch from %s failed (timeout: %.0f s), hiding forum list: %s: %s",
            base_url, timeout_s, type(e).__name__, e,
        )
        return []


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
