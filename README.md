# openocean-software.github.io

Source for [oceansoft.org](https://oceansoft.org), the Open Ocean Software community hub: member project directory, toolkit, events, and how to join.

## Overview

The site is [MkDocs](https://www.mkdocs.org/) with the [Material](https://squidfunk.github.io/mkdocs-material/) theme. Most pages are plain Markdown under `docs/`. The home page, project directory, project pages, and team page render from YAML in `data/`, loaded by the MkDocs hook in `hooks/oceansoft.py` and drawn by the templates in `overrides/`.

## Editing content

| To change | Edit |
|---|---|
| A member project's card, facts, stage, badge, or standards evidence | `data/projects.yml` (field list at the top of the file) |
| A project page's install steps or overview | `docs/projects/<slug>.md` |
| Add a member project | a `data/projects.yml` entry, a `docs/projects/<slug>.md` with `template: project.html` and `project: <slug>`, and a line under `Projects` in `mkdocs.yml` |
| Events on the home page | `data/events.yml` (past/upcoming is worked out from the build date) |
| Team page and home page crew list | `data/team.yml` |
| Colors, type, layout | `docs/stylesheets/extra.css` |

Fields not yet agreed (stage, badge, license, latest release, standards evidence) can be left out; the templates hide them.

The home page lists the latest forum topics, fetched from Discourse at build time. The deploy workflow rebuilds nightly to keep that list and the events current.

## Building

```bash
pip install -r requirements.txt
mkdocs serve                                   # http://127.0.0.1:8000, live reload
OCEANSOFT_SKIP_FORUM=1 mkdocs build --strict   # offline, same check as CI
```

## Testing

```bash
pip install pytest
pytest -q tests
```

The tests cover the hook's data validation, event splitting, and Discourse parsing, plus a check that the repo's `data/*.yml` files load. Pull requests run these and `mkdocs build --strict` in `.github/workflows/check.yml`.

## Deploying

Pushes to `main` (and the nightly schedule) run `.github/workflows/deploy.yml`, which builds and publishes to GitHub Pages with `mkdocs gh-deploy`.
