---
title: MOOS-IvP
template: project.html
project: moos-ivp
hide:
  - navigation
  - toc
---

## Install { #install }

Signed binary packages for Debian and Ubuntu, built by the Open Ocean pipeline from tagged MOOS-IvP releases. Packaging lives in [openocean-build](https://github.com/openocean-software/openocean-build/tree/main/projects/moos-ivp/debian).

1. Add the Open Ocean apt repository and signing key: follow the [apt setup steps](../toolkit.md#apt-packages) on the Toolkit page.
2. Install the helm, apps, and GUI tools:

    ```bash
    sudo apt install moos-ivp-apps moos-ivp-gui moos-ivp-tools
    ```

## Packages

Descriptions from `moos-ivp/debian/control` in openocean-build.

| Package | Contents |
|---|---|
| `moos-ivp-apps` | pHelmIvP and related tools, except GUI applications |
| `moos-ivp-gui` | Graphical tools for the decision engine |
| `moos-ivp-tools` | Command line utilities |
| `moos-ivp-alog` | ALOG log processing utilities |
| `moos-ivp-missions` | Example missions |
| `libmoos-ivp`, `libmoos-ivp-dev` | Libraries and developer headers |
| `libmoos10-mit`, `moos10-mit-*` | Core MOOS: libraries, core tools, database, essentials, UI |

The IvP Helm libraries built without MOOS (`libivp-helm0`, `libivp-helm-dev`) are in the [continuous channel](../toolkit.md#channels), as snapshots until a MOOS-IvP release includes that build option. They install beside `libmoos-ivp`.

## Connects with

| Stack | Bridge | Notes |
|---|---|---|
| [Goby3](goby3.md) | <span class="oo-status oo-status--mature">Mature</span> | Goby ↔ MOOS is built into Goby3. |
| ROS 2 | <span class="oo-status oo-status--adhoc">Ad hoc</span> | No maintained bridge yet. [Help wanted](https://forum.oceansoft.org). |
| LCM | <span class="oo-status oo-status--research">Research-grade</span> | Published bridge, not actively maintained. |
