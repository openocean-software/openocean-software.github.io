---
title: MOOS-IvP
template: project.html
project: moos-ivp
hide:
  - navigation
  - toc
---

## Install { #install }

Signed binary packages for Debian stable/oldstable and Ubuntu active LTS releases, built by the Open Ocean pipeline from tagged MOOS-IvP releases. Packaging lives in [openocean-build](https://github.com/openocean-software/openocean-build/tree/main/moos-ivp/debian).

1. Add the Open Ocean apt repository and signing key: follow the [apt setup steps](../devsecops.md#apt-packages) on the DevSecOps page.
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

## Connects with

| Stack | Bridge | Notes |
|---|---|---|
| [Goby3](goby3.md) | <span class="oo-status oo-status--mature">Mature</span> | Goby ↔ MOOS is built into Goby3. |
| ROS 2 | <span class="oo-status oo-status--adhoc">Ad hoc</span> | No maintained bridge yet. [Help wanted](https://forum.oceansoft.org). |
| LCM | <span class="oo-status oo-status--research">Research-grade</span> | Published bridge, not actively maintained. |
