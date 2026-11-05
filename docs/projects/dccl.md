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
