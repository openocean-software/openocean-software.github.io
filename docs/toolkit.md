---
title: Toolkit
hide:
  - navigation
---

# Toolkit

Shared tools that make member projects work together: common messages, signed packages, and a public plan. Everything here is open source in the [openocean-software](https://github.com/openocean-software) GitHub organization.

## openocean-messages

Define a message once in Protobuf and use it natively everywhere. ROS 2 and LCM outputs are first-class native types, so Protobuf is not needed at runtime for them. Apache-2.0.

[openocean-messages](https://github.com/openocean-software/openocean-messages){ .md-button .md-button--primary } [Examples](https://github.com/openocean-software/openocean-messages-examples){ .md-button }

<div class="oo-pipeline" markdown>
<div class="oo-pipeline__step oo-pipeline__step--source" markdown>
<span class="oo-eyebrow">Source</span>

`openocean/messages/*.proto`

<span class="oo-meta">Units and frames annotated per field</span>
</div>
<div class="oo-pipeline__arrow" aria-hidden="true">→ protoc →</div>
<div class="oo-pipeline__step oo-pipeline__step--band" markdown>
<span class="oo-eyebrow">Protobuf</span>

**C++** built-in · **Python** built-in · **Rust** prost · **C** nanopb
</div>
<div class="oo-pipeline__step oo-pipeline__step--ink" markdown>
<span class="oo-eyebrow">Native types</span>

**ROS 2** `openocean_msgs`, with `to_ros()` / `from_ros()`

**LCM** `.lcm` types, with `to_lcm()` / `from_lcm()`
</div>
</div>

### Example: publish a `Navigation`

From [openocean-messages-examples](https://github.com/openocean-software/openocean-messages-examples); each directory there is an independent CMake project that uses `find_package(openocean_messages)`.

=== "Python"

    ```python
    from openocean.messages import common_pb2, navigation_pb2

    nav = navigation_pb2.Navigation()
    nav.vehicle.name = "auv1"
    nav.geodetic.latitude = 41.52
    nav.geodetic.longitude = -70.67
    nav.geodetic.depth = 10
    nav.attitude.heading = 1.57  # radians
    nav.speed.add(value=1.5, mode=common_pb2.SPEED_MODE_OVER_GROUND)

    received = navigation_pb2.Navigation.FromString(nav.SerializeToString())
    ```

=== "C++"

    ```cpp
    openocean::Navigation nav;
    nav.mutable_vehicle()->set_name("auv1");
    nav.mutable_geodetic()->set_latitude(41.52);
    nav.mutable_geodetic()->set_longitude(-70.67);
    nav.mutable_geodetic()->set_depth(10);
    nav.mutable_attitude()->set_heading(1.57); // radians
    auto* speed = nav.add_speed();
    speed->set_value(1.5);
    speed->set_mode(openocean::SPEED_MODE_OVER_GROUND);

    std::string bytes = nav.SerializeAsString();
    ```

=== "ROS 2"

    ```cpp
    auto publisher = node->create_publisher<openocean_msgs::msg::Navigation>("navigation", 10);

    openocean::Navigation nav;
    nav.mutable_vehicle()->set_name("auv1");
    nav.mutable_geodetic()->set_latitude(41.52);
    nav.mutable_geodetic()->set_depth(10);

    openocean_msgs::msg::Navigation msg;
    openocean::to_ros(nav, &msg);
    publisher->publish(msg);
    ```

### Messages

| Message | Contents |
|---|---|
| `Navigation` | Time, vehicle, geodetic and ENU position, attitude, velocity, speed |
| `ControlSetpoint` | Commanded attitude, speed, depth, altitude, plus custom values |
| `Speed`, `Euler`, `CustomValue` | Shared building blocks; `CustomValue` carries UDUNITS-2 units |

Frames: geodetic is WGS-84 with depth positive down; ENU is relative to a datum; body frame is x forward, y starboard, z down (Fossen / SNAME). See the [message reference](https://github.com/openocean-software/openocean-messages/blob/main/src/doc/messages.md).

## Packages

Member projects keep a working build (CMake, `pyproject.toml`, etc.) and a tagged release schedule. The [openocean-build](https://github.com/openocean-software/openocean-build) pipeline builds, signs, and publishes the packages to `apt.oceansoft.org`.

<div class="oo-pipeline" markdown>
<div class="oo-pipeline__step" markdown>
**Member project**

<span class="oo-meta">git, a working build, tagged releases</span>
</div>
<div class="oo-pipeline__arrow" aria-hidden="true">→</div>
<div class="oo-pipeline__step oo-pipeline__step--source" markdown>
**Open Ocean pipeline**

<span class="oo-meta">sbuild in Docker, Debian packaging, GPG signing</span>
</div>
<div class="oo-pipeline__arrow" aria-hidden="true">→</div>
<div class="oo-pipeline__step oo-pipeline__step--ink" markdown>
**apt.oceansoft.org**

<span class="oo-meta">Debian stable, oldstable, Ubuntu LTS</span>
</div>
</div>

| Tier | Targets | Status |
|---|---|---|
| Tier 1 | Debian and Ubuntu (`.deb`) | <span class="oo-status oo-status--demo">In progress</span> MOOS-IvP available now |
| Tier 2 | OpenEmbedded (Yocto), Homebrew | <span class="oo-status oo-status--adhoc">Planned</span> |

Install steps and the full signing key are on the [DevSecOps](devsecops.md) page.

## Roadmap

The plan is public in [openocean-plan](https://github.com/openocean-software/openocean-plan). Technical goals come from interviews with the community; comment on any of them in the [forum](https://forum.oceansoft.org).

| Goal | Status | What it gives member projects |
|---|---|---|
| [Middleware interoperability](https://github.com/openocean-software/openocean-plan/blob/main/technical/middleware-interoperability.md) | <span class="oo-status oo-status--mature">Available</span> | Common message set today; maintained bridges next |
| [Linux packages](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--demo">In progress</span> | Shared, signed apt repository |
| [Continuous integration](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Shared CI templates and maturity badges |
| [Embedded builds](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Raspberry Pi and ARM builds in CI |
| [Docker images](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Dockerfile templates and multi-arch images |
| [Data QA/QC and FAIR data](https://github.com/openocean-software/openocean-plan/blob/main/technical/fair-data-qa-qc.md) | <span class="oo-status oo-status--adhoc">Planned</span> | QC checklists, metadata templates, provenance |
