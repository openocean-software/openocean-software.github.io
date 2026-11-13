---
title: DCCL
template: project.html
project: dccl
hide:
  - navigation
  - toc
---

## Overview

The Dynamic Compact Control Language (DCCL) is a language for marshalling (or roughly analogously: source encoding or compressing) object-based messages for extremely low throughput network links. Originally designed for commanding and retrieving data from autonomous underwater vehicles over acoustic modem links, DCCL has found additional uses in the robotics community, such as for sending messages over satellite or degraded land-based links.

It is suitable when a very small encoded message size matters much more than the speed of encoding and decoding. [Goby3](goby3.md) uses DCCL for its intervehicle layer.

## Install { #install }

Signed binary packages for Debian and Ubuntu, built by the Open Ocean pipeline from signed DCCL release tags. Packaging lives in [openocean-build](https://github.com/openocean-software/openocean-build/tree/main/projects/dccl/debian).

1. Add the Open Ocean apt repository and signing key: follow the [apt setup steps](../toolkit.md#apt-packages) on the Toolkit page.
2. Install the command line tools, the development files and the Python bindings:

    ```bash
    sudo apt install dccl5-apps libdccl5-dev python3-dccl5
    ```

## Packages

| Package | Contents |
|---|---|
| `libdccl5`, `libdccl5-dev` | Library and development files |
| `dccl5-compiler` | `protoc` plugin |
| `dccl5-apps` | Command line tools, including `dccl` |
| `python3-dccl5` | Python bindings |
| `dccl5-doc` | Documentation |

Prereleases go to the beta channel, and builds of the latest commit to the continuous channel; see [channels](../toolkit.md#channels).
