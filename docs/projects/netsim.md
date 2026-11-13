---
title: NETSIM
template: project.html
project: netsim
hide:
  - navigation
  - toc
---

## Overview

NETSIM simulates underwater acoustic networks. It carries the audio of simulated acoustic modems through an acoustic propagation model, such as Bellhop from the Acoustics Toolbox, so the modems' software can be tested together without water.

NETSIM is built on [Goby3](goby3.md).

## Install { #install }

Signed binary packages for Debian and Ubuntu, built by the Open Ocean pipeline from signed NETSIM release tags. Packaging lives in [openocean-build](https://github.com/openocean-software/openocean-build/tree/main/projects/netsim/debian).

1. Add the Open Ocean apt repository and signing key: follow the [apt setup steps](../toolkit.md#apt-packages) on the Toolkit page.
2. Install the applications and the development files:

    ```bash
    sudo apt install netsim-apps libnetsim-dev
    ```

## Packages

| Package | Contents |
|---|---|
| `netsim-apps` | Applications, including `netsim_manager` and `netsim_tool` |
| `libnetsim`, `libnetsim-dev` | Libraries, headers and the CMake package (`find_package(netsim)`) |
| `netsim-interfaces` | Interface files |
| `netsim-doc` | Documentation |

The [continuous channel](../toolkit.md#channels) carries builds of the latest commit.
