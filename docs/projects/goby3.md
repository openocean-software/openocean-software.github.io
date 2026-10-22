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

## Connects with

| Stack | Bridge | Notes |
|---|---|---|
| [MOOS-IvP](moos-ivp.md) | <span class="oo-status oo-status--mature">Mature</span> | Built into Goby3. Translates between Goby pub/sub and MOOSDB variables. |
| ROS 2 | <span class="oo-status oo-status--demo">Demo</span> | `goby_ros_gateway` bridges the Goby3 interprocess layer to ROS 2 topics. Not yet used outside the original demo code. |
