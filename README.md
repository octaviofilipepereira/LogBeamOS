<p align="center"><img src="usr/share/logbeamos/manual/logbeam.png" width="96" alt="LogBeamOS"></p>

<h1 align="center">LogBeamOS</h1>

<p align="center">
  <a href="https://logbeam.org"><img alt="logbeam.org" src="https://img.shields.io/badge/site-logbeam.org-2f81f7"></a>
  <img alt="Ubuntu 24.04 LTS" src="https://img.shields.io/badge/based%20on-Ubuntu%2024.04%20LTS-e95420">
  <a href="https://www.gnu.org/licenses/gpl-3.0.html"><img alt="GPL v3 licence" src="https://img.shields.io/badge/licence-GPL%20v3-blue"></a>
</p>

<p align="center"><a href="#português">Português</a> · <a href="#english">English</a> · <a href="#español">Español</a> · <a href="#français">Français</a></p>

---

## Português

**LogBeamOS, a distribuição Linux para radioamadores.**

O LogBeamOS é uma distribuição para radioamadores, baseada no Ubuntu 24.04 LTS. Arranca de uma pen, guardando os dados, ou instala-se ao lado do Windows, já com os programas de radioamador instalados: programas nativos de Linux e, através do Wine, o N1MM Logger+ e o Log4OM.

Esses programas são dos respectivos autores e vêm dos sítios habituais: os repositórios do Ubuntu, as publicações dos próprios autores e o Flathub. **Este repositório tem só o que foi escrito para o LogBeamOS**: as ferramentas abaixo. O LogBeam Uplink, que envia os QSOs para o [LogBeam](https://logbeam.org), tem repositório próprio: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

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

## English

**LogBeamOS, the Linux distribution for radio amateurs.**

LogBeamOS is a distribution for radio amateurs, based on Ubuntu 24.04 LTS. It starts from a USB drive, keeping your data, or installs alongside Windows, with the amateur radio programs already installed: native Linux programs and, through Wine, N1MM Logger+ and Log4OM.

Those programs belong to their authors and come from the usual places: the Ubuntu repositories, the authors' own releases and Flathub. **This repository contains only what was written for LogBeamOS**: the tools below. LogBeam Uplink, which sends QSOs to [LogBeam](https://logbeam.org), has its own repository: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

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

## Español

**LogBeamOS, la distribución Linux para radioaficionados.**

LogBeamOS es una distribución para radioaficionados basada en Ubuntu 24.04 LTS. Arranca desde una memoria USB, guardando los datos, o se instala junto a Windows, con los programas de radioaficionado ya instalados: programas nativos de Linux y, a través de Wine, N1MM Logger+ y Log4OM.

Esos programas son de sus autores y vienen de los sitios habituales: los repositorios de Ubuntu, las publicaciones de los propios autores y Flathub. **Este repositorio contiene solo lo que se escribió para LogBeamOS**: las herramientas de abajo. LogBeam Uplink, que envía los QSO a [LogBeam](https://logbeam.org), tiene su propio repositorio: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

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
