---
title: Goby3
template: project.html
project: goby3
hide:
  - navigation
  - toc
---

## Overview

The Goby Underwater Autonomy Project aims to create a unified framework for autonomous marine vehicle collaboration, seamlessly incorporating efficient intervehicle (acoustic, satellite, etc.), flexible interprocess (ethernet, local sockets, etc.), and intuitive interthread (shared pointer) communications. Goby also provides tools for interacting with other marine-related middleware, as well as marine engineering and oceanographic data.

Goby3 uses [DCCL](dccl.md) to encode messages for low-throughput links.

## Install { #install }

Signed binary packages for Debian and Ubuntu, built by the Open Ocean pipeline from signed Goby3 release tags. Packaging lives in [openocean-build](https://github.com/openocean-software/openocean-build/tree/main/projects/goby3/debian).

1. Add the Open Ocean apt repository and signing key: follow the [apt setup steps](../toolkit.md#apt-packages) on the Toolkit page. For the Zenoh transport, run the setup script with `--zenoh`.
2. Install the applications and the development files:

    ```bash
    sudo apt install goby3-apps libgoby3-dev
    ```

## Packages

| Package | Contents |
|---|---|
| `goby3-apps`, `goby3-gui` | Applications, and the GUI applications |
| `libgoby3`, `libgoby3-dev`, `libgoby3-gui-dev` | Libraries and development files |
| `goby3-moos`, `libgoby3-moos`, `libgoby3-moos-dev` | MOOS middleware connections |
| `goby3-zenoh`, `libgoby3-zenoh`, `libgoby3-zenoh-dev` | Zenoh transport |
| `python3-goby3`, `goby3-julia` | Python and Julia support |
| `goby3-clang-tool`, `goby3-interfaces` | `goby_clang_tool` and the interface definition files |
| `goby3-doc`, `goby3-test` | Documentation and unit tests |

The [continuous channel](../toolkit.md#channels) carries builds of the latest commit.

## Connects with

| Stack | Bridge | Notes |
|---|---|---|
| [MOOS-IvP](moos-ivp.md) | <span class="oo-status oo-status--mature">Mature</span> | Built into Goby3. Translates between Goby pub/sub and MOOSDB variables. |
| [IvPico](ivpico.md) | <span class="oo-status oo-status--demo">Demo</span> | Runs the IvP Helm as a Goby3 application, without MOOS. |
| ROS 2 | <span class="oo-status oo-status--demo">Demo</span> | `goby_ros_gateway` bridges the Goby3 interprocess layer to ROS 2 topics. Not yet used outside the original demo code. |
