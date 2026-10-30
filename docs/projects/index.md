---
title: Member projects
template: projects.html
hide:
  - navigation
  - toc
---

# Member projects

<!-- Cards come from data/projects.yml. -->

Each project lists its maintainer, where the code lives and where to report issues. New projects move through the [member stages](../join.md#member-stages) as their practices grow.

[[directory]]

## How member stacks connect today

What we know about each bridge between member stacks today. Send corrections on the [forum](https://forum.oceansoft.org). Source: [middleware interoperability goal](https://github.com/openocean-software/openocean-plan/blob/main/technical/middleware-interoperability.md) in openocean-plan.

| Bridge | Status | Maintainer | Notes |
|---|---|---|---|
| Goby ↔ MOOS | <span class="oo-status oo-status--mature">Mature</span> | GobySoft | Built into Goby3. The one production-grade bridge. |
| Goby ↔ ROS 2 | <span class="oo-status oo-status--demo">Demo</span> | GobySoft | `goby_ros_gateway`. Not yet used outside demo code. |
| ROS 2 ↔ MOOS | <span class="oo-status oo-status--adhoc">Ad hoc</span> | Various | No single maintained bridge. Labs keep custom solutions. |
| LCM ↔ ROS 2 | <span class="oo-status oo-status--adhoc">Ad hoc</span> | Various | `lcm_to_ros` packages pinned to specific versions. |
| LCM ↔ MOOS | <span class="oo-status oo-status--research">Research-grade</span> | Various | Published bridge (IEEE, 2019), not actively maintained. |
