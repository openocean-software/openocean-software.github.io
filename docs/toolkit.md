---
title: Toolkit
hide:
  - navigation
---

# Toolkit

The build pipeline, the signed apt repository and the public plan. All of it is open source under the [openocean-software](https://github.com/openocean-software) GitHub organization.

## Packages

Member projects keep a working build (CMake, `pyproject.toml`, etc.) and a tagged release schedule. The [openocean-build](https://github.com/openocean-software/openocean-build) pipeline builds, signs, and publishes the packages to `apt.oceansoft.org`.

<div class="oo-pipeline" markdown>
<div class="oo-pipeline__step" markdown>
**Member project**

<span class="oo-meta">git, a working build, tagged releases</span>
</div>
<div class="oo-pipeline__arrow" aria-hidden="true">→</div>
<div class="oo-pipeline__step oo-pipeline__step--source" markdown>
**Open Ocean pipeline**

<span class="oo-meta">sbuild in Docker, Debian packaging, GPG signing</span>
</div>
<div class="oo-pipeline__arrow" aria-hidden="true">→</div>
<div class="oo-pipeline__step oo-pipeline__step--ink" markdown>
**apt.oceansoft.org**

<span class="oo-meta">Debian stable, oldstable, Ubuntu LTS</span>
</div>
</div>

| Tier | Targets | Status |
|---|---|---|
| Tier 1 | Debian and Ubuntu (`.deb`) | <span class="oo-status oo-status--demo">In progress</span> MOOS-IvP available now |
| Tier 2 | OpenEmbedded (Yocto), Homebrew | <span class="oo-status oo-status--adhoc">Planned</span> |

Install steps and the full signing key are on the [DevSecOps](devsecops.md) page.

## Roadmap

The plan is public in [openocean-plan](https://github.com/openocean-software/openocean-plan). The technical goals come from 114 interviews with people in academia, industry and government, described in the [AUV26 paper](https://github.com/openocean-software/openocean-plan/blob/main/papers/OpenOcean_IEEE_AUV_2026_Paper-FINAL.pdf). Comment on any of them on the [forum](https://forum.oceansoft.org).

| Goal | Status | What it gives member projects |
|---|---|---|
| [Middleware interoperability](https://github.com/openocean-software/openocean-plan/blob/main/technical/middleware-interoperability.md) | <span class="oo-status oo-status--demo">In progress</span> | Common message set and maintained bridges |
| [Linux packages](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--demo">In progress</span> | Shared, signed apt repository |
| [Continuous integration](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Shared CI templates and maturity badges |
| [Embedded builds](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Raspberry Pi and ARM builds in CI |
| [Docker images](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Dockerfile templates and multi-arch images |
| [Data QA/QC and FAIR data](https://github.com/openocean-software/openocean-plan/blob/main/technical/fair-data-qa-qc.md) | <span class="oo-status oo-status--adhoc">Planned</span> | QC checklists, metadata templates, provenance |
