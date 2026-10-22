"""Tests for the pure parts of hooks/oceansoft.py: data validation, event
splitting and Discourse parsing. Nothing here touches the network."""

from __future__ import annotations

import datetime as dt
import http.client
import importlib.util
from pathlib import Path

import pytest

_HOOK = Path(__file__).resolve().parent.parent / "hooks" / "oceansoft.py"
_spec = importlib.util.spec_from_file_location("oceansoft_hooks", _HOOK)
hooks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hooks)

# Trimmed from the shape Discourse returns for /latest.json and
# /categories.json?include_subcategories=true.
LATEST = {
    "topic_list": {
        "topics": [
            {"id": 1, "slug": "welcome", "title": "Welcome", "pinned": True, "visible": True,
             "category_id": 1, "posts_count": 1, "reply_count": 0},
            {"id": 42, "slug": "goby-ros-gateway", "title": "goby_ros_gateway on Jazzy", "pinned": False,
             "visible": True, "category_id": 31, "posts_count": 4, "reply_count": 3},
            {"id": 43, "slug": "hidden", "title": "Hidden", "pinned": False, "visible": False,
             "category_id": 24, "posts_count": 1, "reply_count": 0},
            {"id": 44, "slug": "auv26-recap", "title": "AUV26 recap", "pinned": False, "visible": True,
             "category_id": 24, "posts_count": 1},
        ]
    }
}
CATEGORIES = {
    "category_list": {
        "categories": [
            {"id": 1, "name": "General", "slug": "general",
             "subcategory_list": [{"id": 31, "name": "Middleware", "slug": "middleware"}]},
            {"id": 24, "name": "News", "slug": "news"},
        ]
    }
}


def test_forum_topics_skip_pinned_and_hidden():
    # the pinned welcome post would otherwise sit at the top of the home page forever
    rows = hooks.parse_forum_topics(LATEST, CATEGORIES, base_url="https://forum.example.org/", limit=5)
    assert [r["title"] for r in rows] == ["goby_ros_gateway on Jazzy", "AUV26 recap"]


def test_forum_topics_resolve_subcategory_names_and_urls():
    rows = hooks.parse_forum_topics(LATEST, CATEGORIES, base_url="https://forum.example.org/", limit=5)
    assert rows[0]["category"] == "Middleware"
    assert rows[0]["url"] == "https://forum.example.org/t/goby-ros-gateway/42"


def test_forum_replies_match_posts_count_not_reply_count():
    # reply_count only counts posts made as a reply to another post; the forum's
    # Replies column is posts_count - 1, so a busy thread could have shown "0 replies"
    latest = {"topic_list": {"topics": [
        {"id": 7, "slug": "busy", "title": "Busy", "visible": True, "posts_count": 6, "reply_count": 0},
    ]}}
    rows = hooks.parse_forum_topics(latest, CATEGORIES, base_url="https://forum.example.org", limit=5)
    assert rows[0]["replies"] == 5


def test_forum_titles_stay_raw_for_the_template_to_escape():
    latest = {"topic_list": {"topics": [
        {"id": 8, "slug": "x", "title": "<img src=x onerror=alert(1)>", "visible": True, "posts_count": 1},
    ]}}
    rows = hooks.parse_forum_topics(latest, CATEGORIES, base_url="https://forum.example.org", limit=5)
    assert rows[0]["title"] == "<img src=x onerror=alert(1)>"


@pytest.mark.parametrize(
    "failure",
    [
        ConnectionResetError("reset by peer"),         # OSError, not URLError
        http.client.IncompleteRead(b""),       # HTTPException
        ValueError("bad json"),
    ],
)
def test_forum_fetch_failure_hides_list_instead_of_failing_build(monkeypatch, failure):
    def boom(url, *, timeout_s):
        raise failure
    monkeypatch.setattr(hooks, "_get_json", boom)
    assert hooks.fetch_forum_topics("https://forum.example.org", limit=5, timeout_s=1.0) == []


def test_forum_unexpected_shape_hides_list_instead_of_failing_build(monkeypatch):
    # a topic without title/slug would KeyError in the parser
    monkeypatch.setattr(hooks, "_get_json", lambda url, *, timeout_s: {"topic_list": {"topics": [{"id": 1}]}})
    assert hooks.fetch_forum_topics("https://forum.example.org", limit=5, timeout_s=1.0) == []


def test_forum_topics_respect_limit():
    rows = hooks.parse_forum_topics(LATEST, CATEGORIES, base_url="https://forum.example.org", limit=1)
    assert len(rows) == 1


def test_events_split_on_today_with_today_upcoming():
    events = [
        {"name": "a", "date": dt.date(2026, 9, 4), "venue": "x"},
        {"name": "b", "date": dt.date(2026, 10, 22), "venue": "x"},
        {"name": "c", "date": dt.date(2026, 9, 23), "venue": "x"},
        {"name": "d", "date": dt.date(2027, 1, 5), "venue": "x"},
    ]
    upcoming, recent = hooks.split_events(events, today=dt.date(2026, 10, 22))
    assert [e["name"] for e in upcoming] == ["b", "d"]
    assert [e["name"] for e in recent] == ["c", "a"]


def test_events_reject_quoted_dates():
    # a quoted date in YAML loads as str and would compare wrong against today
    with pytest.raises(ValueError, match="expected YYYY-MM-DD"):
        hooks.split_events([{"name": "a", "date": "2026-09-04", "venue": "x"}], today=dt.date(2026, 1, 1))


def test_events_reject_datetime():
    # "2026-11-05 09:00" loads as a datetime, which passes isinstance(date) but
    # raises TypeError when compared with today's date
    with pytest.raises(ValueError, match="expected YYYY-MM-DD"):
        hooks.split_events([{"name": "a", "date": dt.datetime(2026, 11, 5, 9, 0), "venue": "x"}],
                           today=dt.date(2026, 1, 1))


def _write(tmp_path: Path, text: str) -> Path:
    p = tmp_path / "projects.yml"
    p.write_text(text, encoding="utf-8")
    return p


def test_projects_default_page_to_projects_slug(tmp_path):
    p = _write(tmp_path, "- {slug: dccl, name: DCCL, kind: member, category: Encoding, filter: encoding, summary: s}\n")
    assert hooks.load_projects(p)[0]["page"] == "projects/dccl/"


def test_projects_missing_field_names_entry_and_field(tmp_path):
    p = _write(tmp_path, "- {slug: dccl, name: DCCL, kind: member, category: Encoding, filter: encoding}\n")
    with pytest.raises(ValueError, match="'dccl' is missing summary"):
        hooks.load_projects(p)


def test_projects_reject_unknown_stage(tmp_path):
    p = _write(tmp_path, "- {slug: dccl, name: DCCL, kind: member, category: Encoding, filter: encoding, "
                         "summary: s, stage: lagoon}\n")
    with pytest.raises(ValueError, match="stage 'lagoon'"):
        hooks.load_projects(p)


def test_projects_reject_unknown_filter(tmp_path):
    # an unknown filter shows the card under "All" only and under no chip
    p = _write(tmp_path, "- {slug: dccl, name: DCCL, kind: member, category: Encoding, filter: comms, summary: s}\n")
    with pytest.raises(ValueError, match="filter 'comms'"):
        hooks.load_projects(p)


def test_projects_reject_duplicate_slug(tmp_path):
    entry = "- {slug: dccl, name: DCCL, kind: member, category: Encoding, filter: encoding, summary: s}\n"
    with pytest.raises(ValueError, match="duplicate slug"):
        hooks.load_projects(_write(tmp_path, entry * 2))


_PROJECTS = [{"slug": "dccl"}, {"slug": "goby3"}]


def test_project_page_with_unknown_slug_fails():
    # a typo'd `project:` front matter key would otherwise render an empty project page
    hooks.check_project_page({"template": "project.html", "project": "goby3"}, _PROJECTS, page_path="projects/goby3.md")
    with pytest.raises(ValueError, match="'goby' is not in data/projects.yml"):
        hooks.check_project_page({"template": "project.html", "project": "goby"}, _PROJECTS, page_path="projects/goby.md")


def test_project_template_without_slug_fails():
    with pytest.raises(ValueError, match="has no `project: <slug>`"):
        hooks.check_project_page({"template": "project.html"}, _PROJECTS, page_path="projects/new.md")


def test_ordinary_page_needs_no_slug():
    hooks.check_project_page({"title": "Toolkit"}, _PROJECTS, page_path="toolkit.md")


def test_directory_marker_missing_fails():
    # an edited marker would drop the card grid while --strict still passes
    hooks.check_directory_marker("<h1>x</h1>\n<p>[[directory]]</p>\n", page_path="projects/index.md")
    with pytest.raises(ValueError, match="no '\\[\\[directory\\]\\]' paragraph"):
        hooks.check_directory_marker("<p>Cards: [[directory]]</p>", page_path="projects/index.md")


def test_fingerprint_must_match_devsecops_page():
    fp = "D7D7224D53A4F29E303FE01DEB505B68A5D063B0"
    hooks.check_fingerprint_in_page(f"OOS_KEY={fp}", fp, page_path="devsecops.md")
    with pytest.raises(ValueError, match="update both together"):
        hooks.check_fingerprint_in_page("OOS_KEY=0000", fp, page_path="devsecops.md")


def test_repo_data_files_load():
    # catches a bad edit to data/*.yml before it reaches the deploy
    data = _HOOK.parent.parent / "data"
    assert hooks.load_projects(data / "projects.yml")
    assert hooks.load_records(data / "events.yml", required=hooks._EVENT_REQUIRED)
    assert hooks.load_records(data / "team.yml", required=hooks._TEAM_REQUIRED)
