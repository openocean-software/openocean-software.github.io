---
title: MOOS-IvP
template: project.html
project: moos-ivp
hide:
  - navigation
  - toc
---

## Install { #install }

Signed binary packages for Debian stable/oldstable and Ubuntu active LTS releases, built by the Open Ocean pipeline from tagged MOOS-IvP releases. Packaging lives in [openocean-build](https://github.com/openocean-software/openocean-build/tree/main/moos-ivp/debian).

```bash
# 1. Get the signing key (see DevSecOps for out-of-band verification)
OOS_KEY=D7D7224D53A4F29E303FE01DEB505B68A5D063B0
OOS_KEYRING=/etc/apt/keyrings/oceansoft.gpg
gpg --keyserver keyserver.ubuntu.com --recv-keys $OOS_KEY && gpg --export $OOS_KEY > $OOS_KEYRING

# 2. Add the apt source
DISTRO=$(. /etc/os-release; echo "$ID")             # "ubuntu" or "debian"
DIST=$(. /etc/os-release; echo "$VERSION_CODENAME") # e.g., "resolute"
REPO=http://apt.oceansoft.org/$DISTRO-$DIST/
echo "deb [signed-by=$OOS_KEYRING] $REPO $DIST main" | sudo tee /etc/apt/sources.list.d/oceansoft.list
sudo apt update

# 3. Install the helm, apps, and GUI tools
sudo apt install moos-ivp-apps moos-ivp-gui moos-ivp-tools
```

If your security requirements call for it, verify [our signing key](../devsecops.md#gpg-signing-public-key) out of band before trusting the repository.

## Packages

Descriptions from `moos-ivp/debian/control` in openocean-build.

| Package | Contents |
|---|---|
| `moos-ivp-apps` | pHelmIvP and related tools, except GUI applications |
| `moos-ivp-gui` | Graphical tools for the decision engine |
| `moos-ivp-tools` | Command line utilities |
| `moos-ivp-alog` | ALOG log processing utilities |
| `moos-ivp-missions` | Example missions |
| `libmoos-ivp`, `libmoos-ivp-dev` | Libraries and developer headers |
| `libmoos10-mit`, `moos10-mit-*` | Core MOOS: libraries, core tools, database, essentials, UI |

## Connects with

| Stack | Bridge | Notes |
|---|---|---|
| [Goby3](goby3.md) | <span class="oo-status oo-status--mature">Mature</span> | Goby ↔ MOOS is built into Goby3. |
| ROS 2 | <span class="oo-status oo-status--adhoc">Ad hoc</span> | No maintained bridge yet. [Help wanted](https://forum.oceansoft.org). |
| LCM | <span class="oo-status oo-status--research">Research-grade</span> | Published bridge, not actively maintained. |
