# Documento técnico · Technical document · Documento técnico · Document technique

[Português](#português) · [English](#english) · [Español](#español) · [Français](#français)

---

## Português

### Organização do repositório

Cada ficheiro está na pasta onde é instalado:

| Pasta | Conteúdo |
|---|---|
| `usr/local/bin/` | Os programas: `logbeamos-actualizar`, `logbeamos-equipamento`, `logbeamos-manual` e os lançadores |
| `usr/local/lib/logbeamos/` | O que o Actualizar (`actualizar/`) e o Rádio e Equipamento (`equipamento/`) usam |
| `usr/share/logbeamos/` | Os ícones e o manual nas quatro línguas |
| `usr/local/share/applications/` | As entradas do menu |
| `usr/share/polkit-1/actions/` | A autorização do ajudante do Actualizar, que corre como administrador |
| `etc/` | O aviso de actualizações ao entrar na sessão e a regra que afasta os receptores RTL-SDR do controlador de TV do Linux |

### Tecnologia

As ferramentas estão escritas em Python 3 com GTK 3; a janela do manual usa o WebKitGTK. São distribuídas no pacote `logbeamos-ferramentas`, pelo repositório apt `https://logbeam.org/apt`.

---

## English

### Repository layout

Each file is in the folder where it is installed:

| Folder | Contents |
|---|---|
| `usr/local/bin/` | The programs: `logbeamos-actualizar`, `logbeamos-equipamento`, `logbeamos-manual` and the launchers |
| `usr/local/lib/logbeamos/` | What the updater (`actualizar/`) and Radio and Equipment (`equipamento/`) use |
| `usr/share/logbeamos/` | Icons and the manual in the four languages |
| `usr/local/share/applications/` | Menu entries |
| `usr/share/polkit-1/actions/` | Authorisation for the updater's helper, which runs as administrator |
| `etc/` | The update notice at login and the rule that keeps RTL-SDR receivers away from the Linux TV driver |

### Technology

The tools are written in Python 3 with GTK 3; the manual window uses WebKitGTK. They are distributed in the `logbeamos-ferramentas` package, by the apt repository at `https://logbeam.org/apt`.

---

## Español

### Organización del repositorio

Cada archivo está en la carpeta donde se instala:

| Carpeta | Contenido |
|---|---|
| `usr/local/bin/` | Los programas: `logbeamos-actualizar`, `logbeamos-equipamento`, `logbeamos-manual` y los lanzadores |
| `usr/local/lib/logbeamos/` | Lo que usan Actualizar (`actualizar/`) y Radio y Equipo (`equipamento/`) |
| `usr/share/logbeamos/` | Los iconos y el manual en los cuatro idiomas |
| `usr/local/share/applications/` | Las entradas del menú |
| `usr/share/polkit-1/actions/` | La autorización del asistente de Actualizar, que se ejecuta como administrador |
| `etc/` | El aviso de actualizaciones al iniciar la sesión y la regla que aparta los receptores RTL-SDR del controlador de TV de Linux |

### Tecnología

Las herramientas están escritas en Python 3 con GTK 3; la ventana del manual usa WebKitGTK. Se distribuyen en el paquete `logbeamos-ferramentas`, desde el repositorio apt `https://logbeam.org/apt`.

---

## Français

### Organisation du dépôt

Chaque fichier est dans le dossier où il est installé :

| Dossier | Contenu |
|---|---|
| `usr/local/bin/` | Les programmes : `logbeamos-actualizar`, `logbeamos-equipamento`, `logbeamos-manual` et les lanceurs |
| `usr/local/lib/logbeamos/` | Ce qu'utilisent Mettre à jour (`actualizar/`) et Radio et Matériel (`equipamento/`) |
| `usr/share/logbeamos/` | Les icônes et le manuel dans les quatre langues |
| `usr/local/share/applications/` | Les entrées du menu |
| `usr/share/polkit-1/actions/` | L'autorisation de l'assistant de mise à jour, qui s'exécute en administrateur |
| `etc/` | L'avis de mises à jour à l'ouverture de la session et la règle qui écarte les récepteurs RTL-SDR du pilote TV de Linux |

### Technologie

Les outils sont écrits en Python 3 avec GTK 3 ; la fenêtre du manuel utilise WebKitGTK. Ils sont distribués dans le paquet `logbeamos-ferramentas`, par le dépôt apt `https://logbeam.org/apt`.
