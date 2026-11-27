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
| `usr/share/polkit-1/actions/` | A autorização do assistente do Actualizar, que corre como administrador |
| `usr/lib/systemd/user/` | A unidade de cada utilizador que põe o certificado do WaveLogGate no Firefox logo que o WaveLogGate o cria |
| `etc/` | O aviso de actualizações ao entrar na sessão e a regra que afasta os receptores RTL-SDR do controlador de TV do Linux; antes da sessão gráfica, a verificação que impede um ficheiro de marcadores estragado (por exemplo, depois de um corte de corrente) de deixar o Cinnamon sem painel; o acerto da porta do WaveLogGate ao entrar na sessão; a fixação do muffin no repositório do LogBeamOS (`etc/apt/preferences.d/`) |
| `docs/manual/` | O manual em Markdown, para ler no GitHub; não é instalado. É feito a partir do de `usr/share/logbeamos/manual/` a cada versão das ferramentas |
| `fontes/muffin/` | A correcção de uma linha do muffin e a explicação; o pacote-fonte está no repositório apt |
| `.github/ISSUE_TEMPLATE/` | O formulário do relato de problema |

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
| `usr/lib/systemd/user/` | The per-user unit that puts the WaveLogGate certificate into Firefox as soon as WaveLogGate creates it |
| `etc/` | The update notice at login and the rule that keeps RTL-SDR receivers away from the Linux TV driver; before the graphical session, the check that stops a damaged bookmarks file (for example, after a power cut) from leaving Cinnamon without its panel; the WaveLogGate port setting at login; the pin of muffin to the LogBeamOS repository (`etc/apt/preferences.d/`) |
| `docs/manual/` | The manual in Markdown, to read on GitHub; it is not installed. It is made from the one in `usr/share/logbeamos/manual/` with each version of the tools |
| `fontes/muffin/` | The one-line correction of muffin and its explanation; the source package is in the apt repository |
| `.github/ISSUE_TEMPLATE/` | The problem report form |

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
| `usr/lib/systemd/user/` | La unidad de cada usuario que pone el certificado de WaveLogGate en Firefox en cuanto WaveLogGate lo crea |
| `etc/` | El aviso de actualizaciones al iniciar la sesión y la regla que aparta los receptores RTL-SDR del controlador de TV de Linux; antes de la sesión gráfica, la comprobación que impide que un archivo de marcadores dañado (por ejemplo, tras un corte de corriente) deje Cinnamon sin panel; el ajuste del puerto de WaveLogGate al iniciar la sesión; la fijación de muffin al repositorio de LogBeamOS (`etc/apt/preferences.d/`) |
| `docs/manual/` | El manual en Markdown, para leer en GitHub; no se instala. Se hace a partir del de `usr/share/logbeamos/manual/` en cada versión de las herramientas |
| `fontes/muffin/` | La corrección de una línea de muffin y su explicación; el paquete fuente está en el repositorio apt |
| `.github/ISSUE_TEMPLATE/` | El formulario del informe de problema |

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
| `usr/lib/systemd/user/` | L'unité de chaque utilisateur qui installe le certificat de WaveLogGate dans Firefox dès que WaveLogGate le crée |
| `etc/` | L'avis de mises à jour à l'ouverture de la session et la règle qui écarte les récepteurs RTL-SDR du pilote TV de Linux ; avant la session graphique, la vérification qui empêche un fichier de signets endommagé (par exemple, après une coupure de courant) de laisser Cinnamon sans panneau ; le réglage du port de WaveLogGate à l'ouverture de la session ; l'épinglage de muffin au dépôt de LogBeamOS (`etc/apt/preferences.d/`) |
| `docs/manual/` | Le manuel en Markdown, à lire sur GitHub ; il n'est pas installé. Il est fait à partir de celui de `usr/share/logbeamos/manual/` à chaque version des outils |
| `fontes/muffin/` | La correction d'une ligne de muffin et son explication ; le paquet source est dans le dépôt apt |
| `.github/ISSUE_TEMPLATE/` | Le formulaire de signalement de problème |

### Technologie

Les outils sont écrits en Python 3 avec GTK 3 ; la fenêtre du manuel utilise WebKitGTK. Ils sont distribués dans le paquet `logbeamos-ferramentas`, par le dépôt apt `https://logbeam.org/apt`.
