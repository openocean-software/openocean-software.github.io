---
title: Member projects
template: projects.html
hide:
  - navigation
  - toc
---

# Member projects and initiatives

Every project here has a named maintainer, a public issue tracker, and a home of its own. Filter by what you need on your vehicle. Entries come from `data/projects.yml`; projects move through the [member stages](../join.md#from-pond-to-ocean) as their practices grow.

[[directory]]

## How member stacks connect today

Bridges exist; maintained bridges are rare. This table tracks each one so you know what to trust before you integrate. Source: [middleware interoperability goal](https://github.com/openocean-software/openocean-plan/blob/main/technical/middleware-interoperability.md) in openocean-plan.

| Bridge | Status | Maintainer | Notes |
|---|---|---|---|
| Goby ↔ MOOS | <span class="oo-status oo-status--mature">Mature</span> | GobySoft | Built into Goby3. The one production-grade bridge. |
| Goby ↔ ROS 2 | <span class="oo-status oo-status--demo">Demo</span> | GobySoft | `goby_ros_gateway`. Not yet used outside demo code. |
| ROS 2 ↔ MOOS | <span class="oo-status oo-status--adhoc">Ad hoc</span> | Various | No single maintained bridge. Labs keep custom solutions. |
| LCM ↔ ROS 2 | <span class="oo-status oo-status--adhoc">Ad hoc</span> | Various | `lcm_to_ros` packages pinned to specific versions. |
| LCM ↔ MOOS | <span class="oo-status oo-status--research">Research-grade</span> | Various | Published bridge (IEEE, 2019), not actively maintained. |

[See how openocean-messages closes the gap →](../toolkit.md#openocean-messages){ .oo-more }
