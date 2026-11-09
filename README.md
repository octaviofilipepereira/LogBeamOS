<p align="center"><img src="usr/share/logbeamos/manual/logbeam.png" width="96" alt="LogBeamOS"></p>

<h1 align="center">LogBeamOS</h1>

<p align="center">
  <a href="https://logbeam.org"><img alt="logbeam.org" src="https://img.shields.io/badge/site-logbeam.org-2f81f7"></a>
  <img alt="Ubuntu 24.04 LTS" src="https://img.shields.io/badge/based%20on-Ubuntu%2024.04%20LTS-e95420">
  <a href="https://www.gnu.org/licenses/gpl-3.0.html"><img alt="GPL v3 licence" src="https://img.shields.io/badge/licence-GPL%20v3-blue"></a>
</p>

<p align="center"><a href="#english">English</a> · <a href="#português">Português</a> · <a href="#español">Español</a> · <a href="#français">Français</a></p>

---

## English

**LogBeamOS, the Linux distribution for radio amateurs.**

LogBeamOS is a distribution for radio amateurs, based on Ubuntu 24.04 LTS. It starts from a USB drive, keeping your data, or installs alongside Windows, with the amateur radio programs already installed: native Linux programs and, through Wine, N1MM Logger+ and Log4OM.

Those programs belong to their authors and come from the usual places: the Ubuntu repositories, the authors' own releases and Flathub. **This repository contains only what was written for LogBeamOS**: the tools below. LogBeam Uplink, which sends QSOs to [LogBeam](https://logbeam.org), has its own repository: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

### Download

The ISO image, its SHA-256 fingerprint and the instructions for writing the USB drive and installing alongside Windows are on the LogBeamOS page: **[logbeam.org/logbeamos](https://logbeam.org/logbeamos/?hl=en)**.

### The tools

| Tool | What it does |
|---|---|
| **Update LogBeamOS** | One window to update the amateur radio programs and the operating system. It shows the installed version, the available one and the download size, and updates only what is ticked, with the progress in MB, speed and time left. It covers the system packages, the programs published on GitHub (WSJT-X, JS8Call, wfview, SatDump, SDR++, Decodium, qdmr and others), Not1MM, and the LogBeamOS tools themselves. Ten minutes after login, a notice appears if there are updates. |
| **Radio and Equipment** | Detects radios, CAT cables, sound cards and SDR receivers. It shares the radio among the programs through Hamlib's `rigctld`, with automatic speed detection, and configures WSJT-X, JTDX, Decodium, Fldigi, Not1MM and Direwolf to use it. |
| **LogBeamOS manual** | First steps, connecting the radio, which program for what, updating, installing alongside Windows and removing LogBeamOS. Its own window, in the language of the session. |
| **Launchers** | N1MM Logger+ through Wine, receiving the shared radio while it is open; Direwolf with a configuration created if missing; Xastir connected to Direwolf. |

Every window is in Portuguese, English, Spanish and French.

### Installing and updating

The tools come with LogBeamOS. They are distributed by the LogBeamOS apt repository, at `https://logbeam.org/apt`, which also carries LogBeam Uplink. On LogBeamOS, they are updated by **Update LogBeamOS**, like any other program.

The repository index is signed. Key fingerprint:

```
A6D0 1419 9FF3 D8B0 4D6D  000A 9621 41CF 2D04 1E07
```

To add the repository by hand on Ubuntu 24.04 or a distribution based on it:

```sh
sudo curl -fsSL -o /usr/share/keyrings/logbeamos.gpg https://logbeam.org/apt/logbeamos.gpg
printf 'Types: deb\nURIs: https://logbeam.org/apt/\nSuites: ./\nSigned-By: /usr/share/keyrings/logbeamos.gpg\n' \
  | sudo tee /etc/apt/sources.list.d/logbeamos.sources
sudo apt update
sudo apt install logbeamos-ferramentas
```

The tools were made for LogBeamOS. On another system, the parts that depend on the programs LogBeamOS installs (WSJT-X in `/opt/ham`, N1MM+ in Wine, and so on) will not work.


### Amateur radio programs in LogBeamOS

Each program belongs to its authors and keeps its own licence. LogBeamOS installs them unchanged.

| Program | What for | Licence | Official page |
|---|---|---|---|
| WSJT-X | FT8, FT4, WSPR and other weak-signal modes | GPL-3.0 | [wsjt.sourceforge.io](https://wsjt.sourceforge.io) |
| JTDX | FT8 and FT4 | GPL-3.0 | [www.jtdx.tech](https://www.jtdx.tech) |
| JS8Call | Keyboard messaging with weak signals | GPL-3.0 | [github.com/JS8Call-improved/JS8Call-improved](https://github.com/JS8Call-improved/JS8Call-improved) |
| Decodium | FT8, FT4 and FT2 | GPL-3.0 | [www.ft2.it](https://www.ft2.it) |
| Fldigi, Flmsg, Flamp, Flarq | Digital modes and messages | GPL-3.0 | [www.w1hkj.org](https://www.w1hkj.org) |
| FreeDV | Digital voice | LGPL-2.1 | [freedv.org](https://freedv.org) |
| QSSTV | SSTV | GPL-3.0 | [www.qsl.net/on4qz](https://www.qsl.net/on4qz/) |
| N1MM Logger+ | Contest logging (through Wine) | Free of charge, not open source | [n1mmwp.hamdocs.com](https://n1mmwp.hamdocs.com) |
| Log4OM 2 | Logbook (through Wine) | Free of charge, not open source | [www.log4om.com](https://www.log4om.com) |
| Not1MM | Contest logging | GPL-3.0 | [github.com/mbridak/not1mm](https://github.com/mbridak/not1mm) |
| Tlf | Contest logging in the terminal | GPL-2.0 | [tlf.github.io](https://tlf.github.io) |
| CQRLOG | Logbook | GPL-2.0 | [www.cqrlog.com](https://www.cqrlog.com) |
| KLog | Logbook | GPL-3.0 | [github.com/ea4k/klog](https://github.com/ea4k/klog) |
| GridTracker2 | Map of the stations heard | BSD-3-Clause | [gridtracker.org](https://gridtracker.org) |
| WaveLogGate | Sends the QSOs and the radio frequency to Wavelog | MIT | [github.com/wavelog/WaveLogGate](https://github.com/wavelog/WaveLogGate) |
| LogBeam Uplink | Sends the QSOs to LogBeam | GPL-3.0 | [logbeam.org/uplink](https://logbeam.org/uplink/) |
| Hamlib | Radio control (CAT) | LGPL-2.1 / GPL-2.0 | [hamlib.github.io](https://hamlib.github.io) |
| flrig | Radio control | GPL-2.0 | [www.w1hkj.org](https://www.w1hkj.org) |
| wfview | Control of Icom and Kenwood radios | GPL-3.0 | [wfview.org](https://wfview.org) |
| Gqrx | SDR receiver | GPL-3.0 | [www.gqrx.dk](https://www.gqrx.dk) |
| SDR++ | SDR receiver | GPL-3.0 | [www.sdrpp.org](https://www.sdrpp.org) |
| SatDump | Satellite reception | GPL-3.0 | [github.com/SatDump/SatDump](https://github.com/SatDump/SatDump) |
| GNU Radio | Signal processing | GPL-3.0 | [www.gnuradio.org](https://www.gnuradio.org) |
| 4ham Spectrum Analysis | Spectrum analysis | AGPL-3.0 | [github.com/octaviofilipepereira/4ham-spectrum-analysis](https://github.com/octaviofilipepereira/4ham-spectrum-analysis) |
| Direwolf | APRS and packet modem | GPL-2.0 | [github.com/wb2osz/direwolf](https://github.com/wb2osz/direwolf) |
| Xastir | APRS map | GPL-2.0 | [github.com/Xastir/Xastir](https://github.com/Xastir/Xastir) |
| Pat | Winlink e-mail over radio | MIT | [getpat.io](https://getpat.io) |
| Gpredict | Satellite tracking | GPL-2.0 | [oz9aec.dk/gpredict](https://oz9aec.dk/gpredict/) |
| qdmr | Programming DMR radios | GPL-3.0 | [dm3mat.de/software/qdmr](https://dm3mat.de/software/qdmr/) |
| Qtel | EchoLink | GPL-2.0 | [www.svxlink.org](https://www.svxlink.org) |
| xnec2c | Antenna modelling | GPL-3.0 | [www.xnec2c.org](https://www.xnec2c.org) |

### Programs that are not open source

LogBeamOS includes two programs that are free of charge but are not open source. They belong to their authors and are included unchanged:

- **N1MM Logger+**: [n1mmwp.hamdocs.com](https://n1mmwp.hamdocs.com)
- **Log4OM 2**: [www.log4om.com](https://www.log4om.com)

**VoxDMR** (DMR on BrandMeister without a radio) is not in the image: Update LogBeamOS installs it only if you ask for it. It is free of charge and does not publish a licence: [voxdmr.com](https://www.voxdmr.com).

### Contributing and security

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Security flaws are reported privately: see [SECURITY.md](SECURITY.md).

### Licence

The LogBeamOS tools are free software, distributed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). The full text is in the [LICENSE](LICENSE) file.

### Disclaimer

- The LogBeamOS tools are distributed without any warranty, under the GPL v3 (sections 15 and 16). The author is not liable for any damage or loss arising from their use, whether in the official release or in a modified version.
- Whoever modifies and distributes a version is solely responsible for it.
- Official releases are only those distributed by the repository at `https://logbeam.org/apt`, signed with the key above.

### Author

Octávio Filipe Pereira Gonçalves, CT7BFV · [logbeam.org](https://logbeam.org)

---

## Português

**LogBeamOS, a distribuição Linux para radioamadores.**

O LogBeamOS é uma distribuição para radioamadores, baseada no Ubuntu 24.04 LTS. Arranca de uma pen, guardando os dados, ou instala-se ao lado do Windows, já com os programas de radioamador instalados: programas nativos de Linux e, através do Wine, o N1MM Logger+ e o Log4OM.

Esses programas são dos respectivos autores e vêm dos sítios habituais: os repositórios do Ubuntu, as publicações dos próprios autores e o Flathub. **Este repositório tem só o que foi escrito para o LogBeamOS**: as ferramentas abaixo. O LogBeam Uplink, que envia os QSOs para o [LogBeam](https://logbeam.org), tem repositório próprio: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

### Descarregar

A imagem ISO, a impressão digital SHA-256 e as instruções para gravar a pen e instalar ao lado do Windows estão na página do LogBeamOS: **[logbeam.org/logbeamos](https://logbeam.org/logbeamos/)**.

### As ferramentas

| Ferramenta | O que faz |
|---|---|
| **Actualizar LogBeamOS** | Uma janela para actualizar os programas de radioamador e o sistema operativo. Mostra a versão instalada, a disponível e o tamanho a descarregar, e actualiza só o que estiver marcado, com o progresso em MB, a velocidade e o tempo que falta. Abrange os pacotes do sistema, os programas publicados no GitHub (WSJT-X, JS8Call, wfview, SatDump, SDR++, Decodium, qdmr e outros), o Not1MM e as próprias ferramentas do LogBeamOS. Dez minutos depois de entrar na sessão, aparece um aviso se houver actualizações. |
| **Rádio e Equipamento** | Detecta rádios, cabos de CAT, placas de som e receptores SDR. Partilha o rádio entre os programas através do `rigctld` do Hamlib, com detecção automática da velocidade, e configura o WSJT-X, o JTDX, o Decodium, o Fldigi, o Not1MM e o Direwolf para o usarem. |
| **Manual do LogBeamOS** | Primeiros passos, ligar o rádio, que programa para quê, actualizar, instalar ao lado do Windows e retirar o LogBeamOS. Em janela própria, na língua da sessão. |
| **Lançadores** | O N1MM Logger+ através do Wine, a receber o rádio partilhado enquanto está aberto; o Direwolf, com uma configuração criada se faltar; o Xastir, ligado ao Direwolf. |

Todas as janelas estão em português, inglês, espanhol e francês.

### Instalar e actualizar

As ferramentas vêm com o LogBeamOS. São distribuídas pelo repositório apt do LogBeamOS, em `https://logbeam.org/apt`, que traz também o LogBeam Uplink. No LogBeamOS, actualizam-se pelo **Actualizar LogBeamOS**, como qualquer outro programa.

O índice do repositório é assinado. Impressão digital da chave:

```
A6D0 1419 9FF3 D8B0 4D6D  000A 9621 41CF 2D04 1E07
```

Para juntar o repositório à mão no Ubuntu 24.04 ou numa distribuição baseada nele:

```sh
sudo curl -fsSL -o /usr/share/keyrings/logbeamos.gpg https://logbeam.org/apt/logbeamos.gpg
printf 'Types: deb\nURIs: https://logbeam.org/apt/\nSuites: ./\nSigned-By: /usr/share/keyrings/logbeamos.gpg\n' \
  | sudo tee /etc/apt/sources.list.d/logbeamos.sources
sudo apt update
sudo apt install logbeamos-ferramentas
```

As ferramentas foram feitas para o LogBeamOS. Noutro sistema, as partes que dependem dos programas que o LogBeamOS instala (o WSJT-X em `/opt/ham`, o N1MM+ no Wine, etc.) não funcionam.


### Programas de radioamador do LogBeamOS

Cada programa é dos respectivos autores e mantém a sua própria licença. O LogBeamOS instala-os sem alterações.

| Programa | Para quê | Licença | Página oficial |
|---|---|---|---|
| WSJT-X | FT8, FT4, WSPR e outros modos de sinal fraco | GPL-3.0 | [wsjt.sourceforge.io](https://wsjt.sourceforge.io) |
| JTDX | FT8 e FT4 | GPL-3.0 | [www.jtdx.tech](https://www.jtdx.tech) |
| JS8Call | Mensagens por teclado em sinal fraco | GPL-3.0 | [github.com/JS8Call-improved/JS8Call-improved](https://github.com/JS8Call-improved/JS8Call-improved) |
| Decodium | FT8, FT4 e FT2 | GPL-3.0 | [www.ft2.it](https://www.ft2.it) |
| Fldigi, Flmsg, Flamp, Flarq | Modos digitais e mensagens | GPL-3.0 | [www.w1hkj.org](https://www.w1hkj.org) |
| FreeDV | Voz digital | LGPL-2.1 | [freedv.org](https://freedv.org) |
| QSSTV | SSTV | GPL-3.0 | [www.qsl.net/on4qz](https://www.qsl.net/on4qz/) |
| N1MM Logger+ | Registo de concursos (através do Wine) | Gratuito, de código fechado | [n1mmwp.hamdocs.com](https://n1mmwp.hamdocs.com) |
| Log4OM 2 | Registo de contactos (através do Wine) | Gratuito, de código fechado | [www.log4om.com](https://www.log4om.com) |
| Not1MM | Registo de concursos | GPL-3.0 | [github.com/mbridak/not1mm](https://github.com/mbridak/not1mm) |
| Tlf | Registo de concursos no terminal | GPL-2.0 | [tlf.github.io](https://tlf.github.io) |
| CQRLOG | Registo de contactos | GPL-2.0 | [www.cqrlog.com](https://www.cqrlog.com) |
| KLog | Registo de contactos | GPL-3.0 | [github.com/ea4k/klog](https://github.com/ea4k/klog) |
| GridTracker2 | Mapa das estações ouvidas | BSD-3-Clause | [gridtracker.org](https://gridtracker.org) |
| WaveLogGate | Envia os QSOs e a frequência do rádio para o Wavelog | MIT | [github.com/wavelog/WaveLogGate](https://github.com/wavelog/WaveLogGate) |
| LogBeam Uplink | Envia os QSOs para o LogBeam | GPL-3.0 | [logbeam.org/uplink](https://logbeam.org/uplink/) |
| Hamlib | Controlo do rádio (CAT) | LGPL-2.1 / GPL-2.0 | [hamlib.github.io](https://hamlib.github.io) |
| flrig | Controlo do rádio | GPL-2.0 | [www.w1hkj.org](https://www.w1hkj.org) |
| wfview | Controlo de rádios Icom e Kenwood | GPL-3.0 | [wfview.org](https://wfview.org) |
| Gqrx | Receptor SDR | GPL-3.0 | [www.gqrx.dk](https://www.gqrx.dk) |
| SDR++ | Receptor SDR | GPL-3.0 | [www.sdrpp.org](https://www.sdrpp.org) |
| SatDump | Recepção de satélites | GPL-3.0 | [github.com/SatDump/SatDump](https://github.com/SatDump/SatDump) |
| GNU Radio | Processamento de sinal | GPL-3.0 | [www.gnuradio.org](https://www.gnuradio.org) |
| 4ham Spectrum Analysis | Análise de espectro | AGPL-3.0 | [github.com/octaviofilipepereira/4ham-spectrum-analysis](https://github.com/octaviofilipepereira/4ham-spectrum-analysis) |
| Direwolf | Modem de APRS e packet | GPL-2.0 | [github.com/wb2osz/direwolf](https://github.com/wb2osz/direwolf) |
| Xastir | Mapa de APRS | GPL-2.0 | [github.com/Xastir/Xastir](https://github.com/Xastir/Xastir) |
| Pat | Correio Winlink por rádio | MIT | [getpat.io](https://getpat.io) |
| Gpredict | Seguimento de satélites | GPL-2.0 | [oz9aec.dk/gpredict](https://oz9aec.dk/gpredict/) |
| qdmr | Programação de rádios DMR | GPL-3.0 | [dm3mat.de/software/qdmr](https://dm3mat.de/software/qdmr/) |
| Qtel | EchoLink | GPL-2.0 | [www.svxlink.org](https://www.svxlink.org) |
| xnec2c | Modelação de antenas | GPL-3.0 | [www.xnec2c.org](https://www.xnec2c.org) |

### Programas que não são de código aberto

O LogBeamOS inclui dois programas que são gratuitos, mas não são de código aberto. São dos respectivos autores e vêm sem alterações:

- **N1MM Logger+**: [n1mmwp.hamdocs.com](https://n1mmwp.hamdocs.com)
- **Log4OM 2**: [www.log4om.com](https://www.log4om.com)

O **VoxDMR** (DMR do BrandMeister sem rádio) não vem na imagem: o Actualizar LogBeamOS só o instala se o utilizador o pedir. É gratuito e não publica licença: [voxdmr.com](https://www.voxdmr.com).

### Contribuir e segurança

As contribuições são bem-vindas: ver o [CONTRIBUTING.md](CONTRIBUTING.md). As falhas de segurança comunicam-se em privado: ver o [SECURITY.md](SECURITY.md).

### Licença

As ferramentas do LogBeamOS são software livre, distribuído com a [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). O texto completo está no ficheiro [LICENSE](LICENSE).

### Exclusão de responsabilidade

- As ferramentas do LogBeamOS são distribuídas sem qualquer garantia, nos termos da GPL v3 (secções 15 e 16). O autor não é responsável por danos ou perdas resultantes do seu uso, seja na versão oficial, seja numa versão modificada.
- Quem modificar e distribuir uma versão é o único responsável por ela.
- As versões oficiais são só as distribuídas pelo repositório em `https://logbeam.org/apt`, assinadas com a chave acima.

### Autor

Octávio Filipe Pereira Gonçalves, CT7BFV · [logbeam.org](https://logbeam.org)

---

## Español

**LogBeamOS, la distribución Linux para radioaficionados.**

LogBeamOS es una distribución para radioaficionados basada en Ubuntu 24.04 LTS. Arranca desde una memoria USB, guardando los datos, o se instala junto a Windows, con los programas de radioaficionado ya instalados: programas nativos de Linux y, a través de Wine, N1MM Logger+ y Log4OM.

Esos programas son de sus autores y vienen de los sitios habituales: los repositorios de Ubuntu, las publicaciones de los propios autores y Flathub. **Este repositorio contiene solo lo que se escribió para LogBeamOS**: las herramientas de abajo. LogBeam Uplink, que envía los QSO a [LogBeam](https://logbeam.org), tiene su propio repositorio: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

### Descargar

La imagen ISO, su huella digital SHA-256 y las instrucciones para grabar la memoria USB e instalar junto a Windows están en la página de LogBeamOS: **[logbeam.org/logbeamos](https://logbeam.org/logbeamos/?hl=es)**.

### Las herramientas

| Herramienta | Qué hace |
|---|---|
| **Actualizar LogBeamOS** | Una ventana para actualizar los programas de radioaficionado y el sistema operativo. Muestra la versión instalada, la disponible y el tamaño a descargar, y actualiza solo lo que esté marcado, con el progreso en MB, la velocidad y el tiempo restante. Abarca los paquetes del sistema, los programas publicados en GitHub (WSJT-X, JS8Call, wfview, SatDump, SDR++, Decodium, qdmr y otros), Not1MM y las propias herramientas de LogBeamOS. Diez minutos después de iniciar la sesión, aparece un aviso si hay actualizaciones. |
| **Radio y Equipo** | Detecta radios, cables CAT, tarjetas de sonido y receptores SDR. Comparte la radio entre los programas a través de `rigctld` de Hamlib, con detección automática de la velocidad, y configura WSJT-X, JTDX, Decodium, Fldigi, Not1MM y Direwolf para que la usen. |
| **Manual de LogBeamOS** | Primeros pasos, conectar la radio, qué programa para qué, actualizar, instalar junto a Windows y quitar LogBeamOS. En su propia ventana, en el idioma de la sesión. |
| **Lanzadores** | N1MM Logger+ a través de Wine, recibiendo la radio compartida mientras está abierto; Direwolf, con una configuración creada si falta; Xastir, conectado a Direwolf. |

Todas las ventanas están en portugués, inglés, español y francés.

### Instalar y actualizar

Las herramientas vienen con LogBeamOS. Se distribuyen desde el repositorio apt de LogBeamOS, en `https://logbeam.org/apt`, que también trae LogBeam Uplink. En LogBeamOS se actualizan con **Actualizar LogBeamOS**, como cualquier otro programa.

El índice del repositorio está firmado. Huella de la clave:

```
A6D0 1419 9FF3 D8B0 4D6D  000A 9621 41CF 2D04 1E07
```

Para añadir el repositorio a mano en Ubuntu 24.04 o en una distribución basada en él:

```sh
sudo curl -fsSL -o /usr/share/keyrings/logbeamos.gpg https://logbeam.org/apt/logbeamos.gpg
printf 'Types: deb\nURIs: https://logbeam.org/apt/\nSuites: ./\nSigned-By: /usr/share/keyrings/logbeamos.gpg\n' \
  | sudo tee /etc/apt/sources.list.d/logbeamos.sources
sudo apt update
sudo apt install logbeamos-ferramentas
```

Las herramientas se hicieron para LogBeamOS. En otro sistema, las partes que dependen de los programas que instala LogBeamOS (WSJT-X en `/opt/ham`, N1MM+ en Wine, etc.) no funcionan.


### Programas de radioaficionado de LogBeamOS

Cada programa es de sus autores y mantiene su propia licencia. LogBeamOS los instala sin cambios.

| Programa | Para qué | Licencia | Página oficial |
|---|---|---|---|
| WSJT-X | FT8, FT4, WSPR y otros modos de señal débil | GPL-3.0 | [wsjt.sourceforge.io](https://wsjt.sourceforge.io) |
| JTDX | FT8 y FT4 | GPL-3.0 | [www.jtdx.tech](https://www.jtdx.tech) |
| JS8Call | Mensajes por teclado con señal débil | GPL-3.0 | [github.com/JS8Call-improved/JS8Call-improved](https://github.com/JS8Call-improved/JS8Call-improved) |
| Decodium | FT8, FT4 y FT2 | GPL-3.0 | [www.ft2.it](https://www.ft2.it) |
| Fldigi, Flmsg, Flamp, Flarq | Modos digitales y mensajes | GPL-3.0 | [www.w1hkj.org](https://www.w1hkj.org) |
| FreeDV | Voz digital | LGPL-2.1 | [freedv.org](https://freedv.org) |
| QSSTV | SSTV | GPL-3.0 | [www.qsl.net/on4qz](https://www.qsl.net/on4qz/) |
| N1MM Logger+ | Registro de concursos (a través de Wine) | Gratuito, de código cerrado | [n1mmwp.hamdocs.com](https://n1mmwp.hamdocs.com) |
| Log4OM 2 | Registro de contactos (a través de Wine) | Gratuito, de código cerrado | [www.log4om.com](https://www.log4om.com) |
| Not1MM | Registro de concursos | GPL-3.0 | [github.com/mbridak/not1mm](https://github.com/mbridak/not1mm) |
| Tlf | Registro de concursos en el terminal | GPL-2.0 | [tlf.github.io](https://tlf.github.io) |
| CQRLOG | Registro de contactos | GPL-2.0 | [www.cqrlog.com](https://www.cqrlog.com) |
| KLog | Registro de contactos | GPL-3.0 | [github.com/ea4k/klog](https://github.com/ea4k/klog) |
| GridTracker2 | Mapa de las estaciones oídas | BSD-3-Clause | [gridtracker.org](https://gridtracker.org) |
| WaveLogGate | Envía los QSO y la frecuencia de la radio a Wavelog | MIT | [github.com/wavelog/WaveLogGate](https://github.com/wavelog/WaveLogGate) |
| LogBeam Uplink | Envía los QSO a LogBeam | GPL-3.0 | [logbeam.org/uplink](https://logbeam.org/uplink/) |
| Hamlib | Control de la radio (CAT) | LGPL-2.1 / GPL-2.0 | [hamlib.github.io](https://hamlib.github.io) |
| flrig | Control de la radio | GPL-2.0 | [www.w1hkj.org](https://www.w1hkj.org) |
| wfview | Control de radios Icom y Kenwood | GPL-3.0 | [wfview.org](https://wfview.org) |
| Gqrx | Receptor SDR | GPL-3.0 | [www.gqrx.dk](https://www.gqrx.dk) |
| SDR++ | Receptor SDR | GPL-3.0 | [www.sdrpp.org](https://www.sdrpp.org) |
| SatDump | Recepción de satélites | GPL-3.0 | [github.com/SatDump/SatDump](https://github.com/SatDump/SatDump) |
| GNU Radio | Procesamiento de señal | GPL-3.0 | [www.gnuradio.org](https://www.gnuradio.org) |
| 4ham Spectrum Analysis | Análisis de espectro | AGPL-3.0 | [github.com/octaviofilipepereira/4ham-spectrum-analysis](https://github.com/octaviofilipepereira/4ham-spectrum-analysis) |
| Direwolf | Módem de APRS y packet | GPL-2.0 | [github.com/wb2osz/direwolf](https://github.com/wb2osz/direwolf) |
| Xastir | Mapa de APRS | GPL-2.0 | [github.com/Xastir/Xastir](https://github.com/Xastir/Xastir) |
| Pat | Correo Winlink por radio | MIT | [getpat.io](https://getpat.io) |
| Gpredict | Seguimiento de satélites | GPL-2.0 | [oz9aec.dk/gpredict](https://oz9aec.dk/gpredict/) |
| qdmr | Programación de radios DMR | GPL-3.0 | [dm3mat.de/software/qdmr](https://dm3mat.de/software/qdmr/) |
| Qtel | EchoLink | GPL-2.0 | [www.svxlink.org](https://www.svxlink.org) |
| xnec2c | Modelado de antenas | GPL-3.0 | [www.xnec2c.org](https://www.xnec2c.org) |

### Programas que no son de código abierto

LogBeamOS incluye dos programas que son gratuitos, pero no son de código abierto. Son de sus autores y se incluyen sin cambios:

- **N1MM Logger+**: [n1mmwp.hamdocs.com](https://n1mmwp.hamdocs.com)
- **Log4OM 2**: [www.log4om.com](https://www.log4om.com)

**VoxDMR** (DMR de BrandMeister sin radio) no está en la imagen: Actualizar LogBeamOS solo lo instala si el usuario lo pide. Es gratuito y no publica licencia: [voxdmr.com](https://www.voxdmr.com).

### Contribuir y seguridad

Las contribuciones son bienvenidas: ver [CONTRIBUTING.md](CONTRIBUTING.md). Los fallos de seguridad se comunican en privado: ver [SECURITY.md](SECURITY.md).

### Licencia

Las herramientas de LogBeamOS son software libre, distribuido con la [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). El texto completo está en el archivo [LICENSE](LICENSE).

### Exención de responsabilidad

- Las herramientas de LogBeamOS se distribuyen sin ninguna garantía, según la GPL v3 (secciones 15 y 16). El autor no es responsable de daños o pérdidas derivados de su uso, ya sea en la versión oficial o en una versión modificada.
- Quien modifique y distribuya una versión es el único responsable de ella.
- Las versiones oficiales son solo las distribuidas por el repositorio en `https://logbeam.org/apt`, firmadas con la clave de arriba.

### Autor

Octávio Filipe Pereira Gonçalves, CT7BFV · [logbeam.org](https://logbeam.org)

---

## Français

**LogBeamOS, la distribution Linux pour radioamateurs.**

LogBeamOS est une distribution pour radioamateurs basée sur Ubuntu 24.04 LTS. Elle démarre depuis une clé USB, en gardant les données, ou s'installe à côté de Windows, avec les logiciels de radioamateur déjà installés : des logiciels natifs Linux et, via Wine, N1MM Logger+ et Log4OM.

Ces logiciels appartiennent à leurs auteurs et viennent des sources habituelles : les dépôts d'Ubuntu, les publications des auteurs eux-mêmes et Flathub. **Ce dépôt ne contient que ce qui a été écrit pour LogBeamOS** : les outils ci-dessous. LogBeam Uplink, qui envoie les QSO à [LogBeam](https://logbeam.org), a son propre dépôt : [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

### Télécharger

L'image ISO, son empreinte SHA-256 et les instructions pour préparer la clé USB et installer à côté de Windows sont sur la page de LogBeamOS : **[logbeam.org/logbeamos](https://logbeam.org/logbeamos/?hl=fr)**.

### Les outils

| Outil | Ce qu'il fait |
|---|---|
| **Mettre à jour LogBeamOS** | Une fenêtre pour mettre à jour les logiciels de radioamateur et le système d'exploitation. Elle affiche la version installée, la version disponible et la taille à télécharger, et ne met à jour que ce qui est coché, avec la progression en Mo, la vitesse et le temps restant. Elle couvre les paquets du système, les logiciels publiés sur GitHub (WSJT-X, JS8Call, wfview, SatDump, SDR++, Decodium, qdmr et d'autres), Not1MM et les outils de LogBeamOS eux-mêmes. Dix minutes après l'ouverture de la session, un avis apparaît s'il y a des mises à jour. |
| **Radio et Matériel** | Détecte les radios, les câbles CAT, les cartes son et les récepteurs SDR. Partage la radio entre les logiciels via `rigctld` de Hamlib, avec détection automatique de la vitesse, et configure WSJT-X, JTDX, Decodium, Fldigi, Not1MM et Direwolf pour l'utiliser. |
| **Manuel de LogBeamOS** | Premiers pas, brancher la radio, quel logiciel pour quoi, mettre à jour, installer à côté de Windows et retirer LogBeamOS. Dans sa propre fenêtre, dans la langue de la session. |
| **Lanceurs** | N1MM Logger+ via Wine, recevant la radio partagée tant qu'il est ouvert ; Direwolf, avec une configuration créée si elle manque ; Xastir, relié à Direwolf. |

Toutes les fenêtres sont en portugais, anglais, espagnol et français.

### Installer et mettre à jour

Les outils sont fournis avec LogBeamOS. Ils sont distribués par le dépôt apt de LogBeamOS, à `https://logbeam.org/apt`, qui contient aussi LogBeam Uplink. Sur LogBeamOS, ils se mettent à jour avec **Mettre à jour LogBeamOS**, comme n'importe quel autre logiciel.

L'index du dépôt est signé. Empreinte de la clé :

```
A6D0 1419 9FF3 D8B0 4D6D  000A 9621 41CF 2D04 1E07
```

Pour ajouter le dépôt à la main sur Ubuntu 24.04 ou une distribution basée sur elle :

```sh
sudo curl -fsSL -o /usr/share/keyrings/logbeamos.gpg https://logbeam.org/apt/logbeamos.gpg
printf 'Types: deb\nURIs: https://logbeam.org/apt/\nSuites: ./\nSigned-By: /usr/share/keyrings/logbeamos.gpg\n' \
  | sudo tee /etc/apt/sources.list.d/logbeamos.sources
sudo apt update
sudo apt install logbeamos-ferramentas
```

Les outils ont été faits pour LogBeamOS. Sur un autre système, les parties qui dépendent des logiciels que LogBeamOS installe (WSJT-X dans `/opt/ham`, N1MM+ dans Wine, etc.) ne fonctionnent pas.


### Logiciels de radioamateur de LogBeamOS

Chaque logiciel appartient à ses auteurs et garde sa propre licence. LogBeamOS les installe sans modification.

| Logiciel | Pour quoi | Licence | Page officielle |
|---|---|---|---|
| WSJT-X | FT8, FT4, WSPR et autres modes à signal faible | GPL-3.0 | [wsjt.sourceforge.io](https://wsjt.sourceforge.io) |
| JTDX | FT8 et FT4 | GPL-3.0 | [www.jtdx.tech](https://www.jtdx.tech) |
| JS8Call | Messages au clavier à signal faible | GPL-3.0 | [github.com/JS8Call-improved/JS8Call-improved](https://github.com/JS8Call-improved/JS8Call-improved) |
| Decodium | FT8, FT4 et FT2 | GPL-3.0 | [www.ft2.it](https://www.ft2.it) |
| Fldigi, Flmsg, Flamp, Flarq | Modes numériques et messages | GPL-3.0 | [www.w1hkj.org](https://www.w1hkj.org) |
| FreeDV | Voix numérique | LGPL-2.1 | [freedv.org](https://freedv.org) |
| QSSTV | SSTV | GPL-3.0 | [www.qsl.net/on4qz](https://www.qsl.net/on4qz/) |
| N1MM Logger+ | Carnet de concours (via Wine) | Gratuit, code source fermé | [n1mmwp.hamdocs.com](https://n1mmwp.hamdocs.com) |
| Log4OM 2 | Carnet de trafic (via Wine) | Gratuit, code source fermé | [www.log4om.com](https://www.log4om.com) |
| Not1MM | Carnet de concours | GPL-3.0 | [github.com/mbridak/not1mm](https://github.com/mbridak/not1mm) |
| Tlf | Carnet de concours dans le terminal | GPL-2.0 | [tlf.github.io](https://tlf.github.io) |
| CQRLOG | Carnet de trafic | GPL-2.0 | [www.cqrlog.com](https://www.cqrlog.com) |
| KLog | Carnet de trafic | GPL-3.0 | [github.com/ea4k/klog](https://github.com/ea4k/klog) |
| GridTracker2 | Carte des stations entendues | BSD-3-Clause | [gridtracker.org](https://gridtracker.org) |
| WaveLogGate | Envoie les QSO et la fréquence de la radio à Wavelog | MIT | [github.com/wavelog/WaveLogGate](https://github.com/wavelog/WaveLogGate) |
| LogBeam Uplink | Envoie les QSO à LogBeam | GPL-3.0 | [logbeam.org/uplink](https://logbeam.org/uplink/) |
| Hamlib | Contrôle de la radio (CAT) | LGPL-2.1 / GPL-2.0 | [hamlib.github.io](https://hamlib.github.io) |
| flrig | Contrôle de la radio | GPL-2.0 | [www.w1hkj.org](https://www.w1hkj.org) |
| wfview | Contrôle des radios Icom et Kenwood | GPL-3.0 | [wfview.org](https://wfview.org) |
| Gqrx | Récepteur SDR | GPL-3.0 | [www.gqrx.dk](https://www.gqrx.dk) |
| SDR++ | Récepteur SDR | GPL-3.0 | [www.sdrpp.org](https://www.sdrpp.org) |
| SatDump | Réception de satellites | GPL-3.0 | [github.com/SatDump/SatDump](https://github.com/SatDump/SatDump) |
| GNU Radio | Traitement du signal | GPL-3.0 | [www.gnuradio.org](https://www.gnuradio.org) |
| 4ham Spectrum Analysis | Analyse de spectre | AGPL-3.0 | [github.com/octaviofilipepereira/4ham-spectrum-analysis](https://github.com/octaviofilipepereira/4ham-spectrum-analysis) |
| Direwolf | Modem APRS et packet | GPL-2.0 | [github.com/wb2osz/direwolf](https://github.com/wb2osz/direwolf) |
| Xastir | Carte APRS | GPL-2.0 | [github.com/Xastir/Xastir](https://github.com/Xastir/Xastir) |
| Pat | Courrier Winlink par radio | MIT | [getpat.io](https://getpat.io) |
| Gpredict | Suivi de satellites | GPL-2.0 | [oz9aec.dk/gpredict](https://oz9aec.dk/gpredict/) |
| qdmr | Programmation des radios DMR | GPL-3.0 | [dm3mat.de/software/qdmr](https://dm3mat.de/software/qdmr/) |
| Qtel | EchoLink | GPL-2.0 | [www.svxlink.org](https://www.svxlink.org) |
| xnec2c | Modélisation d'antennes | GPL-3.0 | [www.xnec2c.org](https://www.xnec2c.org) |

### Logiciels qui ne sont pas à code source ouvert

LogBeamOS contient deux logiciels gratuits, mais qui ne sont pas à code source ouvert. Ils appartiennent à leurs auteurs et sont inclus sans modification :

- **N1MM Logger+**: [n1mmwp.hamdocs.com](https://n1mmwp.hamdocs.com)
- **Log4OM 2**: [www.log4om.com](https://www.log4om.com)

**VoxDMR** (DMR de BrandMeister sans radio) n'est pas dans l'image : Mettre à jour LogBeamOS ne l'installe que si l'utilisateur le demande. Il est gratuit et ne publie pas de licence : [voxdmr.com](https://www.voxdmr.com).

### Contribuer et sécurité

Les contributions sont les bienvenues : voir [CONTRIBUTING.md](CONTRIBUTING.md). Les failles de sécurité se signalent en privé : voir [SECURITY.md](SECURITY.md).

### Licence

Les outils de LogBeamOS sont des logiciels libres, distribués sous la [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). Le texte complet se trouve dans le fichier [LICENSE](LICENSE).

### Exclusion de responsabilité

- Les outils de LogBeamOS sont distribués sans aucune garantie, selon la GPL v3 (articles 15 et 16). L'auteur n'est pas responsable des dommages ou pertes résultant de leur utilisation, que ce soit dans la version officielle ou dans une version modifiée.
- Quiconque modifie et distribue une version en est seul responsable.
- Les versions officielles sont uniquement celles distribuées par le dépôt à `https://logbeam.org/apt`, signées avec la clé ci-dessus.

### Auteur

Octávio Filipe Pereira Gonçalves, CT7BFV · [logbeam.org](https://logbeam.org)
