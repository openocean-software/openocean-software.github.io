---
title: Join
hide:
  - navigation
---

# Bring your project aboard

You keep your code, your roadmap, and your home page. We add packaging, security, interoperability, and an audience that runs vehicles at sea.

[Start on the forum](https://forum.oceansoft.org){ .md-button .md-button--primary } [Read the standards (PDF)](https://github.com/openocean-software/openocean-plan/blob/main/member-projects/guidelines/member_project_standards.pdf){ .md-button }

<div class="oo-split-panels" markdown>
<div class="oo-panel" markdown>
<span class="oo-eyebrow">You provide</span>
Source in git, a working build and install (CMake for C/C++, `pyproject.toml` for Python, etc.), and a tagged release schedule.
</div>
<div class="oo-panel oo-panel--band" markdown>
<span class="oo-eyebrow oo-eyebrow--accent">We provide</span>
The secure build pipeline, signed packages, a project page in the [directory](projects/index.md), and a place on the forum.
</div>
</div>

## From pond to ocean

Projects enter where they are. Incubating projects get mentoring; research projects are members as-is; maturing projects move downstream as their practices grow.

<div class="oo-stages" markdown>
<div class="oo-stage oo-stage--pond" markdown>**Pond**<br><span>Incubating</span></div>
<div class="oo-stages__arrow" aria-hidden="true">→</div>
<div class="oo-stages__members" markdown>
<span class="oo-eyebrow">Member projects</span>
<div class="oo-stages__row" markdown>
<div class="oo-stage oo-stage--explorer" markdown>**Explorer**<br><span>Research focus</span></div>
<div class="oo-stage oo-stage--estuary" markdown>**Estuary**<br><span>Maturity level 1</span></div>
<div class="oo-stages__arrow" aria-hidden="true">→</div>
<div class="oo-stage oo-stage--bay" markdown>**Bay**<br><span>Maturity level 2</span></div>
<div class="oo-stages__arrow" aria-hidden="true">→</div>
<div class="oo-stage oo-stage--ocean" markdown>**Ocean**<br><span>Maturity level 3</span></div>
</div>
</div>
</div>

## Eight minimums, any format

We ask what your documentation and process must answer, not which tool writes it. A README, docstrings, tests, or a paper appendix all count.

<div class="oo-split-panels" markdown>
<div markdown>
### Documentation

1. **Purpose.** What the component does and its intended scope.
2. **Usage.** At least one minimal, realistic example.
3. **Interface.** Inputs, outputs, expected behavior, and failure modes.
4. **Assumptions and constraints.** Preconditions, units, coordinate frames, timing.
</div>
<div markdown>
### Maintainability

1. **Build reproducibility.** A contributor can build from a clean state with documented steps.
2. **Interface contracts.** Message formats, types, units, and frames are stated.
3. **Verified behavior.** Tests, a runnable example, or a manual validation procedure.
4. **Issue visibility.** A public way to report defects and see known issues.
</div>
</div>

Plus a published [OSI-approved license](https://github.com/openocean-software/openocean-plan/blob/main/member-projects/guidelines/software-licensing-guidance.md).

## Maintainability badges

A badge tells users what to expect. Each level lists the minimum standard, the DevOps help we offer to reach it, and well-known open-source projects at that level.

=== "Research-Grade"

    **Standard:** builds from documented steps on at least one known platform. Some evidence of tested behavior. Issues reportable via any channel.

    **DevOps:** builds locally. No CI or packaging required.

    **Examples:** many code releases that accompany academic papers.

=== "Community-Grade"

    **Standard:** clean build from documented steps. At least one automated test or runnable example. Public issue tracker. Interface inputs and outputs documented.

    **DevOps:** CI on the primary platform. Dockerfile available.

    **Examples:** MOOS-IvP, MAVLink.

=== "Project-Grade"

    **Standard:** CI runs on changes. Interfaces formally defined and tested. Installable on at least one target platform. Contributing and issue guidelines published.

    **DevOps:** multi-platform CI. Packages in the shared repository. Multi-arch Docker images.

    **Examples:** ROS 2 core packages, ArduSub.

=== "Product-Grade"

    **Standard:** multi-platform packaging. Full regression suite. Schema-validated configuration. Changelog and deprecation policy.

    **DevOps:** integration tests with other member projects. Release automation.

    **Examples:** ArduPilot, PX4.

=== "Ecosystem-Grade"

    **Standard:** formal compatibility guarantees across platforms and versions. Governed CI infrastructure. Long-term support commitments.

    **DevOps:** cross-project CI. Shared build infrastructure. Reproducible deployment stacks.

    **Examples:** ROS 2 full ecosystem, Linux kernel.

## Research code is welcome

The standards explicitly support research and experimental software. For Research-Grade projects these are acceptable:

- Manual validation in place of automated tests
- Source-only distribution with documented build workarounds
- One known-good platform instead of broad portability
- Interface contracts documented in a paper or README section

## How to apply

1. **Introduce the project.** Post on the [forum](https://forum.oceansoft.org). Maintainers can apply; users can nominate a project they depend on.
2. **Self-assess.** Link evidence for the eight minimums and your license.
3. **Peer review.** Member maintainers review and agree on a stage and badge.
4. **Onboard.** Your project page goes live in the directory, and we start on packaging.

[Start on the forum](https://forum.oceansoft.org){ .md-button .md-button--primary }
