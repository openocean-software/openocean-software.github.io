---
title: IvPico
template: project.html
project: ivpico
hide:
  - navigation
  - toc
---

## Overview

IvPico creates lightweight applications for the IvP solver from [MOOS-IvP](moos-ivp.md). Rather than using bridges or gateways to connect middlewares, it runs the IvP Helm and the maritime behaviors as first-class applications in the middleware of choice: the equivalent of the MOOS-based pHelmIvP for your publish/subscribe middleware.

The [Goby3](goby3.md) application, `goby_helm_ivp`, is packaged today. A ROS node is in the source tree.

## Install { #install }

IvPico has no tagged releases yet, so its packages are snapshots of the latest commit, in the [continuous channel](../toolkit.md#channels) only. They are signed with the [continuous key](../toolkit.md#continuous-key), for Debian bookworm and trixie, and Ubuntu noble and resolute. Packaging lives in [openocean-build](https://github.com/openocean-software/openocean-build/tree/main/projects/ivpico/debian).

1. Add the release and continuous channels with the [setup script](../toolkit.md#apt-packages):

    ```bash
    sudo bash apt-setup --continuous
    ```

2. Install:

    ```bash
    sudo apt install ivpico
    ```

## Packages

| Package | Contents |
|---|---|
| `ivpico` | `goby_helm_ivp`, the `ivpico_helm` and `ivpico_interface` libraries, and a plugin for `goby_moos_gateway` |

IvPico builds on the IvP Helm libraries built without MOOS (`libivp-helm0`), openocean-messages and Goby3, all from the same repositories.
