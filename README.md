<p align="center"><img src="usr/share/logbeamos/manual/logbeam.png" width="96" alt="LogBeamOS"></p>

<h1 align="center">LogBeamOS</h1>

<p align="center"><b>The tools of LogBeamOS, the Linux distribution for radio amateurs.</b></p>

<p align="center">
  <a href="https://logbeam.org"><img alt="logbeam.org" src="https://img.shields.io/badge/site-logbeam.org-2f81f7"></a>
  <img alt="Linux Mint 22" src="https://img.shields.io/badge/based%20on-Linux%20Mint%2022-87cf3e">
  <a href="https://www.gnu.org/licenses/gpl-3.0.html"><img alt="GPL v3 licence" src="https://img.shields.io/badge/licence-GPL%20v3-blue"></a>
</p>

<p align="center"><a href="README.pt.md">Português</a> · <b>English</b> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a></p>

---

LogBeamOS is a Linux Mint based distribution for radio amateurs. It starts from a USB drive, keeping your data, or installs alongside Windows, with the amateur radio programs already installed: native Linux programs and, through Wine, N1MM Logger+ and Log4OM.

Those programs belong to their authors and come from the usual places: the Linux Mint and Ubuntu repositories, the authors' own releases and Flathub. **This repository contains only what was written for LogBeamOS**: the tools below. LogBeam Uplink, which sends QSOs to [LogBeam](https://logbeam.org), has its own repository: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

## The tools

| Tool | What it does |
|---|---|
| **Update LogBeamOS** | One window to update the amateur radio programs and the operating system. It shows the installed version, the available one and the download size, and updates only what is ticked, with the progress in MB, speed and time left. It covers the system packages, the programs published on GitHub (WSJT-X, JS8Call, wfview, SatDump, SDR++, Decodium, qdmr and others), Not1MM, and the LogBeamOS tools themselves. Ten minutes after login, a notice appears if there are updates. |
| **Radio and Equipment** | Detects radios, CAT cables, sound cards and SDR receivers. It shares the radio among the programs through Hamlib's `rigctld`, with automatic speed detection, and configures WSJT-X, JTDX, Decodium, Fldigi, Not1MM and Direwolf to use it. |
| **LogBeamOS manual** | First steps, connecting the radio, which program for what, updating, installing alongside Windows and removing LogBeamOS. Its own window, in the language of the session. |
| **Launchers** | N1MM Logger+ through Wine, receiving the shared radio while it is open; Direwolf with a configuration created if missing; Xastir connected to Direwolf. |

Every window is in Portuguese, English, Spanish and French.

## Installing and updating

The tools come with LogBeamOS. They are distributed by the LogBeamOS apt repository, at `https://logbeam.org/apt`, which also carries LogBeam Uplink. On LogBeamOS, they are updated by **Update LogBeamOS**, like any other program.

The repository index is signed. Key fingerprint:

```
A6D0 1419 9FF3 D8B0 4D6D  000A 9621 41CF 2D04 1E07
```

To add the repository by hand on Linux Mint 22 or Ubuntu 24.04:

```sh
sudo curl -fsSL -o /usr/share/keyrings/logbeamos.gpg https://logbeam.org/apt/logbeamos.gpg
printf 'Types: deb\nURIs: https://logbeam.org/apt/\nSuites: ./\nSigned-By: /usr/share/keyrings/logbeamos.gpg\n' \
  | sudo tee /etc/apt/sources.list.d/logbeamos.sources
sudo apt update
sudo apt install logbeamos-ferramentas
```

The tools were made for LogBeamOS. On another system, the parts that depend on the programs LogBeamOS installs (WSJT-X in `/opt/ham`, N1MM+ in Wine, and so on) will not work.

## Repository layout

Each file is in the folder where it is installed:

| Folder | Contents |
|---|---|
| `usr/local/bin/` | The programs: `logbeamos-actualizar`, `logbeamos-equipamento`, `logbeamos-manual` and the launchers |
| `usr/local/lib/logbeamos/` | What the updater (`actualizar/`) and Radio and Equipment (`equipamento/`) use |
| `usr/share/logbeamos/` | Icons and the manual in the four languages |
| `usr/local/share/applications/` | Menu entries |
| `usr/share/polkit-1/actions/` | Authorisation for the updater's helper, which runs as administrator |
| `etc/` | The update notice at login and the rule that keeps RTL-SDR receivers away from the Linux TV driver |

The tools are written in Python 3 with GTK 3; the manual window uses WebKitGTK.

## Contributing and security

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Security flaws are reported privately: see [SECURITY.md](SECURITY.md).

## Licence

The LogBeamOS tools are free software, distributed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). The full text is in the [LICENSE](LICENSE) file.

## Disclaimer

- The LogBeamOS tools are distributed without any warranty, under the GPL v3 (sections 15 and 16). The author is not liable for any damage or loss arising from their use, whether in the official release or in a modified version.
- Whoever modifies and distributes a version is solely responsible for it.
- Official releases are only those distributed by the repository at `https://logbeam.org/apt`, signed with the key above.

## Author

Octávio Filipe Pereira Gonçalves, CT7BFV · [logbeam.org](https://logbeam.org)
