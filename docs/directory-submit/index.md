# Submit a Project

We welcome submissions from anyone in the marine robotics community.
To add your project to the directory:

## Option 1: GitHub Issue (Easiest)

Fill out our submission template:

[:material-plus-circle: Submit via GitHub Issue](https://github.com/openocean-software/openocean-software.github.io/issues/new?template=project-submission.yml){ .md-button .md-button--primary }

We'll review your submission and add it to the directory.

## Option 2: Pull Request (For Git Users)

1. Fork the repository
2. Edit `data/projects.yml` — add your project entry following the schema
3. Open a pull request

Your entry should include at minimum:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Project name |
| `description` | Yes | 1–3 sentence description |
| `repo_url` | Yes | Link to source code |
| `category` | Yes | One of: autonomy, middleware, communications, vehicle-software, simulation, navigation, sensors, data-management, visualization, devops, other |
| `license` | Yes | SPDX license identifier |
| `status` | Yes | One of: active, maintained, archived, experimental |
| `middleware` | No | Framework(s) used: ROS, ROS 2, MOOS, Goby, LCM, None |
| `languages` | No | Programming languages |
| `docs_url` | No | Link to documentation |
| `website_url` | No | Project homepage |
| `maintainer_org` | No | Maintaining organization |
| `tags` | No | Free-form keyword tags |

## What Qualifies?

- Open-source software (OSI-approved license)
- Related to marine robotics, ocean science instrumentation, or underwater systems
- Publicly accessible repository

Projects do not need to be affiliated with OpenOcean.Software founding members.
We specifically want to catalog the long tail of useful projects that are hard to discover.
