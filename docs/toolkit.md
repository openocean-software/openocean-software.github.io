---
title: Toolkit
hide:
  - navigation
---

# Toolkit

The build pipeline, the signed apt repositories and the public plan. All of it is open source under the [openocean-software](https://github.com/openocean-software) GitHub organization.

## Packages

Member projects keep a working build (CMake, `pyproject.toml`, etc.) and a tagged release schedule. The [openocean-build](https://github.com/openocean-software/openocean-build) pipeline builds, signs, and publishes the packages to `apt.oceansoft.org`. Its documentation is at [build.oceansoft.org](https://build.oceansoft.org), including a [getting started guide for member projects](https://build.oceansoft.org/getting-started/).

<div class="oo-pipeline" markdown>
<div class="oo-pipeline__step" markdown>
**Member project**

<span class="oo-meta">git, a working build, signed release tags</span>
</div>
<div class="oo-pipeline__arrow" aria-hidden="true">→</div>
<div class="oo-pipeline__step oo-pipeline__step--source" markdown>
**Open Ocean pipeline**

<span class="oo-meta">sbuild in Docker, install test, GPG signing</span>
</div>
<div class="oo-pipeline__arrow" aria-hidden="true">→</div>
<div class="oo-pipeline__step oo-pipeline__step--ink" markdown>
**apt.oceansoft.org**

<span class="oo-meta">Debian stable, oldstable, Ubuntu LTS · amd64, arm64</span>
</div>
</div>

| Tier | Targets | Status |
|---|---|---|
| Tier 1 | Debian and Ubuntu (`.deb`) | <span class="oo-status oo-status--demo">In progress</span> MOOS-IvP, Goby3, DCCL and NETSIM ready to install |
| Tier 2 | OpenEmbedded (Yocto), Homebrew | <span class="oo-status oo-status--adhoc">Planned</span> |

### Channels { #channels }

Packages are published to three [channels](https://build.oceansoft.org/channels/), each its own set of apt repositories:

| Channel | Contents | Signed with | Projects |
|---|---|---|---|
| Release | Tagged releases, published after a reviewer approves | [Release key](#gpg-signing-public-key) | [MOOS-IvP](projects/moos-ivp.md), [Goby3](projects/goby3.md), [DCCL](projects/dccl.md), [NETSIM](projects/netsim.md) |
| Beta | Tagged prereleases | [Release key](#gpg-signing-public-key) | openocean-messages |
| Continuous | The latest trusted commit on each project's main branch | [Continuous key](#continuous-key) | Goby3, DCCL, NETSIM, [IvPico](projects/ivpico.md), the IvP Helm libraries without MOOS, openocean-messages |

The release channel also carries the dependencies these projects need that Debian and Ubuntu don't package (MAVLink, libais, Wt).

### Install from apt.oceansoft.org { #apt-packages }

!!! warning "Trust"

    These instructions assume oceansoft.org and the openocean-build repository haven't been compromised (and thus list the correct GPG fingerprints). This is normally a safe assumption, but if your security requirements call for it, consider independently verifying [our signing key](#gpg-signing-public-key), e.g. using Keybase or other out-of-band techniques.

For Debian bookworm and trixie, and Ubuntu jammy, noble and resolute, on amd64 and arm64. A few projects skip a release whose dependencies are too old.

=== "Setup script"

    [`apt-setup`](https://github.com/openocean-software/openocean-build/blob/main/scripts/apt-setup) adds the release channel, checking the key's fingerprint before apt is told to trust it:

    ```bash
    curl -fsSLO https://raw.githubusercontent.com/openocean-software/openocean-build/main/scripts/apt-setup
    ```

    ```bash
    sudo bash apt-setup
    ```

    Options add more: `--beta` and `--continuous` for those channels, and `--zenoh` for Eclipse Zenoh's repository, which `goby3-zenoh` needs.

=== "By hand"

    - Get the release key and check its fingerprint ([details](#gpg-signing-public-key)):
      ```bash
      OOS_KEY=D7D7224D53A4F29E303FE01DEB505B68A5D063B0
      OOS_KEYRING=/usr/share/keyrings/openocean-release.asc
      curl -fsSLO https://raw.githubusercontent.com/openocean-software/openocean-build/main/keys/release.asc
      gpg --show-keys --with-colons release.asc | grep -x "fpr:::::::::$OOS_KEY:" && sudo install -m 0644 release.asc $OOS_KEYRING
      ```
    - Add `apt` sources:
      ```bash
      DISTRO=$(. /etc/os-release; echo "$ID")             # "ubuntu" or "debian"
      DIST=$(. /etc/os-release; echo "$VERSION_CODENAME") # e.g., "resolute"
      printf 'Types: deb\nURIs: https://apt.oceansoft.org/release/%s-%s\nSuites: %s\nComponents: main\nSigned-By: %s\n' \
        $DISTRO $DIST $DIST $OOS_KEYRING | sudo tee /etc/apt/sources.list.d/openocean-release.sources
      sudo apt update
      ```

    The beta channel is the same with `beta` in place of `release` in the URL. The continuous channel also needs its [own key](#continuous-key). See [Installing packages](https://build.oceansoft.org/installing/).

Then:

- Install packages:
  ```bash
  sudo apt install ...
  ```

- Full list of packages available:
  ```bash
  sudo apt install lz4
  lz4cat /var/lib/apt/lists/apt.oceansoft.org*_Packages.lz4 | grep '^Package:'
  ```

!!! note "Set up before November 2026?"

    The repositories moved from `apt.oceansoft.org/<distro>-<dist>/` to `apt.oceansoft.org/release/<distro>-<dist>`. Remove `/etc/apt/sources.list.d/oceansoft.list` and `/etc/apt/keyrings/oceansoft.gpg`, then follow the steps above.

### Signing keys { #gpg-signing-public-key }

<a href="https://xkcd.com/1553/"><img title="I guess I should be signing stuff, but I've never been sure what to sign. Maybe if I post my private key, I can crowdsource my decisions about what to sign." src="https://imgs.xkcd.com/comics/public_key.png"/></a>

The release key signs the release and beta channels at https://apt.oceansoft.org. The repositories are signed by a subkey; the primary key stays offline, so the subkey can be replaced without changing the key you trust. More on each key is in [Keys](https://build.oceansoft.org/keys/).

- User: Toby Schneider ([tsaubergine](https://keybase.io/tsaubergine) on Keybase)
- Primary key fingerprint: `EAD278F6A25644C2C559DBB6D28A2EAB14D2A9E5`
- Signing subkey fingerprint: `D7D7224D53A4F29E303FE01DEB505B68A5D063B0`
- In openocean-build: [`keys/release.asc`](https://github.com/openocean-software/openocean-build/blob/main/keys/release.asc)
- Keybase: /keybase/public/tsaubergine/openocean-software-signing-pub-key.asc

#### Continuous key { #continuous-key }

Continuous builds are published without a reviewer, so they are signed with a separate key: nothing built from an unreviewed commit can be signed as a release.

- Fingerprint: `DAF08DD7788E6C84C6F8E8D3E59E1A81FECDB228`
- In openocean-build: [`keys/continuous.asc`](https://github.com/openocean-software/openocean-build/blob/main/keys/continuous.asc)

??? note "Full PGP public key (release)"

     ```
     -----BEGIN PGP PUBLIC KEY BLOCK-----
     
     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
     KMdONYUBMCU2j4li8KdgnQ0=
     =E/xS
     -----END PGP PUBLIC KEY BLOCK-----
     ```

## Roadmap

The plan is public in [openocean-plan](https://github.com/openocean-software/openocean-plan). The technical goals come from 114 interviews with people in academia, industry and government, described in the [AUV26 paper](https://github.com/openocean-software/openocean-plan/blob/main/papers/OpenOcean_IEEE_AUV_2026_Paper-FINAL.pdf). Comment on any of them on the [forum](https://forum.oceansoft.org).

| Goal | Status | What it gives member projects |
|---|---|---|
| [Middleware interoperability](https://github.com/openocean-software/openocean-plan/blob/main/technical/middleware-interoperability.md) | <span class="oo-status oo-status--demo">In progress</span> | Common message set and maintained bridges |
| [Linux packages](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--demo">In progress</span> | Shared, signed apt repositories: release, beta and continuous |
| [Continuous integration](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Shared CI templates and maturity badges |
| [Embedded builds](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Raspberry Pi and ARM builds in CI |
| [Docker images](https://github.com/openocean-software/openocean-plan/blob/main/technical/devops-technical-support.md) | <span class="oo-status oo-status--adhoc">Planned</span> | Dockerfile templates and multi-arch images |
| [Data QA/QC and FAIR data](https://github.com/openocean-software/openocean-plan/blob/main/technical/fair-data-qa-qc.md) | <span class="oo-status oo-status--adhoc">Planned</span> | QC checklists, metadata templates, provenance |
