# Segurança · Security · Seguridad · Sécurité

[Português](#português) · [English](#english) · [Español](#español) · [Français](#français)

---

## Português

### Versões suportadas

Só a versão mais recente do pacote `logbeamos-ferramentas`, distribuída pelo repositório `https://logbeam.org/apt`, recebe correcções de segurança.

### Comunicar uma falha

**Não abra uma *issue* pública** para falhas de segurança. Use a comunicação privada do GitHub: separador **Security** deste repositório → **Report a vulnerability**. Só o autor vê o relatório.

Inclua, se possível: a versão do LogBeamOS e das ferramentas, os passos para reproduzir a falha, o efeito e uma proposta de correcção, se a tiver.

A recepção é confirmada em até 7 dias. A correcção é publicada numa versão nova, e a falha só é descrita publicamente depois disso.

### Boas práticas já seguidas

- O índice do repositório apt é assinado; a chave privada nunca sai das máquinas do autor.
- O ajudante do Actualizar, que corre como administrador, nunca recebe endereços da janela: procura-os ele próprio. Os ficheiros descarregados são conferidos pelo SHA-256 publicado pelo autor de cada programa, quando existe, antes de serem instalados.
- A autorização de administrador passa pelo polkit, com a password do utilizador.

---

## English

### Supported versions

Only the latest version of the `logbeamos-ferramentas` package, distributed by the repository at `https://logbeam.org/apt`, receives security fixes.

### Reporting a flaw

**Do not open a public issue** for security flaws. Use GitHub's private reporting: the **Security** tab of this repository → **Report a vulnerability**. Only the author sees the report.

Include, if possible: the version of LogBeamOS and of the tools, the steps to reproduce the flaw, its effect and a proposed fix, if you have one.

Receipt is confirmed within 7 days. The fix is published in a new version, and the flaw is only described publicly after that.

### Practices already followed

- The apt repository index is signed; the private key never leaves the author's machines.
- The updater's helper, which runs as administrator, never takes addresses from the window: it looks them up itself. Downloaded files are checked against the SHA-256 published by each program's author, when there is one, before being installed.
- Administrator authorisation goes through polkit, with the user's password.

---

## Español

### Versiones soportadas

Solo la versión más reciente del paquete `logbeamos-ferramentas`, distribuida por el repositorio `https://logbeam.org/apt`, recibe correcciones de seguridad.

### Comunicar un fallo

**No abra una *issue* pública** para fallos de seguridad. Use la comunicación privada de GitHub: pestaña **Security** de este repositorio → **Report a vulnerability**. Solo el autor ve el informe.

Incluya, si es posible: la versión de LogBeamOS y de las herramientas, los pasos para reproducir el fallo, su efecto y una propuesta de corrección, si la tiene.

La recepción se confirma en un plazo de 7 días. La corrección se publica en una versión nueva, y el fallo solo se describe públicamente después.

### Buenas prácticas ya seguidas

- El índice del repositorio apt está firmado; la clave privada nunca sale de las máquinas del autor.
- El asistente de Actualizar, que se ejecuta como administrador, nunca recibe direcciones de la ventana: las busca él mismo. Los archivos descargados se comprueban con el SHA-256 publicado por el autor de cada programa, cuando existe, antes de instalarse.
- La autorización de administrador pasa por polkit, con la contraseña del usuario.

---

## Français

### Versions prises en charge

Seule la version la plus récente du paquet `logbeamos-ferramentas`, distribuée par le dépôt `https://logbeam.org/apt`, reçoit des correctifs de sécurité.

### Signaler une faille

**N'ouvrez pas d'*issue* publique** pour une faille de sécurité. Utilisez le signalement privé de GitHub : onglet **Security** de ce dépôt → **Report a vulnerability**. Seul l'auteur voit le rapport.

Indiquez si possible : la version de LogBeamOS et des outils, les étapes pour reproduire la faille, son effet et une proposition de correction, si vous en avez une.

La réception est confirmée sous 7 jours. Le correctif est publié dans une nouvelle version, et la faille n'est décrite publiquement qu'ensuite.

### Bonnes pratiques déjà suivies

- L'index du dépôt apt est signé ; la clé privée ne quitte jamais les machines de l'auteur.
- L'assistant de mise à jour, qui s'exécute en administrateur, ne reçoit jamais d'adresses de la fenêtre : il les cherche lui-même. Les fichiers téléchargés sont vérifiés avec le SHA-256 publié par l'auteur de chaque logiciel, quand il existe, avant d'être installés.
- L'autorisation d'administrateur passe par polkit, avec le mot de passe de l'utilisateur.
