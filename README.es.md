<p align="center"><img src="usr/share/logbeamos/manual/logbeam.png" width="96" alt="LogBeamOS"></p>

<h1 align="center">LogBeamOS</h1>

<p align="center"><b>Las herramientas de LogBeamOS, la distribución Linux para radioaficionados.</b></p>

<p align="center">
  <a href="https://logbeam.org"><img alt="logbeam.org" src="https://img.shields.io/badge/sitio-logbeam.org-2f81f7"></a>
  <img alt="Linux Mint 22" src="https://img.shields.io/badge/basada%20en-Linux%20Mint%2022-87cf3e">
  <a href="https://www.gnu.org/licenses/gpl-3.0.html"><img alt="Licencia GPL v3" src="https://img.shields.io/badge/licencia-GPL%20v3-blue"></a>
</p>

<p align="center"><a href="README.pt.md">Português</a> · <a href="README.md">English</a> · <b>Español</b> · <a href="README.fr.md">Français</a></p>

---

LogBeamOS es una distribución para radioaficionados basada en Linux Mint. Arranca desde una memoria USB, guardando los datos, o se instala junto a Windows, con los programas de radioaficionado ya instalados: programas nativos de Linux y, a través de Wine, N1MM Logger+ y Log4OM.

Esos programas son de sus autores y vienen de los sitios habituales: los repositorios de Linux Mint y de Ubuntu, las publicaciones de los propios autores y Flathub. **Este repositorio contiene solo lo que se escribió para LogBeamOS**: las herramientas de abajo. LogBeam Uplink, que envía los QSO a [LogBeam](https://logbeam.org), tiene su propio repositorio: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

## Las herramientas

| Herramienta | Qué hace |
|---|---|
| **Actualizar LogBeamOS** | Una ventana para actualizar los programas de radioaficionado y el sistema operativo. Muestra la versión instalada, la disponible y el tamaño a descargar, y actualiza solo lo que esté marcado, con el progreso en MB, la velocidad y el tiempo restante. Abarca los paquetes del sistema, los programas publicados en GitHub (WSJT-X, JS8Call, wfview, SatDump, SDR++, Decodium, qdmr y otros), Not1MM y las propias herramientas de LogBeamOS. Diez minutos después de iniciar la sesión, aparece un aviso si hay actualizaciones. |
| **Radio y Equipo** | Detecta radios, cables CAT, tarjetas de sonido y receptores SDR. Comparte la radio entre los programas a través de `rigctld` de Hamlib, con detección automática de la velocidad, y configura WSJT-X, JTDX, Decodium, Fldigi, Not1MM y Direwolf para que la usen. |
| **Manual de LogBeamOS** | Primeros pasos, conectar la radio, qué programa para qué, actualizar, instalar junto a Windows y quitar LogBeamOS. En su propia ventana, en el idioma de la sesión. |
| **Lanzadores** | N1MM Logger+ a través de Wine, recibiendo la radio compartida mientras está abierto; Direwolf, con una configuración creada si falta; Xastir, conectado a Direwolf. |

Todas las ventanas están en portugués, inglés, español y francés.

## Instalar y actualizar

Las herramientas vienen con LogBeamOS. Se distribuyen desde el repositorio apt de LogBeamOS, en `https://logbeam.org/apt`, que también trae LogBeam Uplink. En LogBeamOS se actualizan con **Actualizar LogBeamOS**, como cualquier otro programa.

El índice del repositorio está firmado. Huella de la clave:

```
A6D0 1419 9FF3 D8B0 4D6D  000A 9621 41CF 2D04 1E07
```

Para añadir el repositorio a mano en Linux Mint 22 o Ubuntu 24.04:

```sh
sudo curl -fsSL -o /usr/share/keyrings/logbeamos.gpg https://logbeam.org/apt/logbeamos.gpg
printf 'Types: deb\nURIs: https://logbeam.org/apt/\nSuites: ./\nSigned-By: /usr/share/keyrings/logbeamos.gpg\n' \
  | sudo tee /etc/apt/sources.list.d/logbeamos.sources
sudo apt update
sudo apt install logbeamos-ferramentas
```

Las herramientas se hicieron para LogBeamOS. En otro sistema, las partes que dependen de los programas que instala LogBeamOS (WSJT-X en `/opt/ham`, N1MM+ en Wine, etc.) no funcionan.

## Organización del repositorio

Cada archivo está en la carpeta donde se instala:

| Carpeta | Contenido |
|---|---|
| `usr/local/bin/` | Los programas: `logbeamos-actualizar`, `logbeamos-equipamento`, `logbeamos-manual` y los lanzadores |
| `usr/local/lib/logbeamos/` | Lo que usan Actualizar (`actualizar/`) y Radio y Equipo (`equipamento/`) |
| `usr/share/logbeamos/` | Los iconos y el manual en los cuatro idiomas |
| `usr/local/share/applications/` | Las entradas del menú |
| `usr/share/polkit-1/actions/` | La autorización del asistente de Actualizar, que se ejecuta como administrador |
| `etc/` | El aviso de actualizaciones al iniciar la sesión y la regla que aparta los receptores RTL-SDR del controlador de TV de Linux |

Las herramientas están escritas en Python 3 con GTK 3; la ventana del manual usa WebKitGTK.

## Contribuir y seguridad

Las contribuciones son bienvenidas: ver [CONTRIBUTING.md](CONTRIBUTING.md). Los fallos de seguridad se comunican en privado: ver [SECURITY.md](SECURITY.md).

## Licencia

Las herramientas de LogBeamOS son software libre, distribuido con la [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). El texto completo está en el archivo [LICENSE](LICENSE).

## Exención de responsabilidad

- Las herramientas de LogBeamOS se distribuyen sin ninguna garantía, según la GPL v3 (secciones 15 y 16). El autor no es responsable de daños o pérdidas derivados de su uso, ya sea en la versión oficial o en una versión modificada.
- Quien modifique y distribuya una versión es el único responsable de ella.
- Las versiones oficiales son solo las distribuidas por el repositorio en `https://logbeam.org/apt`, firmadas con la clave de arriba.

## Autor

Octávio Filipe Pereira Gonçalves, CT7BFV · [logbeam.org](https://logbeam.org)
