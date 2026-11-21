# muffin · LogBeamOS

[English](#english) · [Português](#português) · [Español](#español) · [Français](#français)

---

## English

LogBeamOS takes **muffin**, the window manager of the Cinnamon desktop, from its own apt repository (`https://logbeam.org/apt`), with a one-line correction. Without it, Cinnamon could crash ("fallback mode") when N1MM+ or Log4OM, which run through Wine, was closed and opened again: muffin aborted on an assertion in `meta_workspace_add_window`. The crash was found and reported by Bráulio Sousa, CT7APZ.

The same assertion was turned into a warning in mutter, the GNOME window manager muffin derives from, in January 2021 ([GNOME/mutter#992](https://gitlab.gnome.org/GNOME/mutter/-/issues/992), merge request !1692). [workspace.patch](workspace.patch) does the same in muffin.

- Version: `6.6.3+zena+logbeamos1`, made from the Linux Mint source of muffin `6.6.3+zena` with this patch only.
- Source package: `muffin_6.6.3+zena+logbeamos1.dsc` and `.tar.xz`, in the apt repository (`deb-src [signed-by=/usr/share/keyrings/logbeamos.gpg] https://logbeam.org/apt/ ./`).
- The LogBeamOS tools pin muffin to that repository (`etc/apt/preferences.d/logbeamos-muffin`), so that a Linux Mint update does not bring the crash back. A newer muffin from Linux Mint waits until it is published here with the same correction.

## Português

O LogBeamOS vai buscar o **muffin**, o gestor de janelas do ambiente de trabalho Cinnamon, ao seu repositório apt (`https://logbeam.org/apt`), com uma correcção de uma linha. Sem ela, o Cinnamon podia ir abaixo («modo de recurso») ao fechar e voltar a abrir o N1MM+ ou o Log4OM, que correm através do Wine: o muffin abortava numa verificação em `meta_workspace_add_window`. A queda foi descoberta e relatada por Bráulio Sousa, CT7APZ.

A mesma verificação passou a aviso no mutter, o gestor de janelas do GNOME de que o muffin deriva, em Janeiro de 2021 ([GNOME/mutter#992](https://gitlab.gnome.org/GNOME/mutter/-/issues/992), merge request !1692). O [workspace.patch](workspace.patch) faz o mesmo no muffin.

- Versão: `6.6.3+zena+logbeamos1`, feita a partir do código-fonte do muffin `6.6.3+zena` do Linux Mint, só com esta alteração.
- Pacote-fonte: `muffin_6.6.3+zena+logbeamos1.dsc` e `.tar.xz`, no repositório apt (`deb-src [signed-by=/usr/share/keyrings/logbeamos.gpg] https://logbeam.org/apt/ ./`).
- As ferramentas do LogBeamOS fixam o muffin nesse repositório (`etc/apt/preferences.d/logbeamos-muffin`), para que uma actualização do Linux Mint não traga a queda de volta. Um muffin mais recente do Linux Mint fica à espera até ser publicado aqui com a mesma correcção.

## Español

LogBeamOS toma **muffin**, el gestor de ventanas del escritorio Cinnamon, de su propio repositorio apt (`https://logbeam.org/apt`), con una corrección de una línea. Sin ella, Cinnamon podía caerse («modo de emergencia») al cerrar y volver a abrir N1MM+ o Log4OM, que funcionan a través de Wine: muffin abortaba en una comprobación de `meta_workspace_add_window`. La caída la descubrió y comunicó Bráulio Sousa, CT7APZ.

La misma comprobación pasó a ser un aviso en mutter, el gestor de ventanas de GNOME del que deriva muffin, en enero de 2021 ([GNOME/mutter#992](https://gitlab.gnome.org/GNOME/mutter/-/issues/992), merge request !1692). [workspace.patch](workspace.patch) hace lo mismo en muffin.

- Versión: `6.6.3+zena+logbeamos1`, hecha a partir del código fuente de muffin `6.6.3+zena` de Linux Mint, solo con este cambio.
- Paquete fuente: `muffin_6.6.3+zena+logbeamos1.dsc` y `.tar.xz`, en el repositorio apt (`deb-src [signed-by=/usr/share/keyrings/logbeamos.gpg] https://logbeam.org/apt/ ./`).
- Las herramientas de LogBeamOS fijan muffin a ese repositorio (`etc/apt/preferences.d/logbeamos-muffin`), para que una actualización de Linux Mint no vuelva a traer la caída. Un muffin más reciente de Linux Mint espera hasta publicarse aquí con la misma corrección.

## Français

LogBeamOS prend **muffin**, le gestionnaire de fenêtres du bureau Cinnamon, dans son propre dépôt apt (`https://logbeam.org/apt`), avec une correction d'une ligne. Sans elle, Cinnamon pouvait planter (« mode de secours ») à la fermeture puis à la réouverture de N1MM+ ou de Log4OM, qui fonctionnent via Wine : muffin s'arrêtait sur une vérification dans `meta_workspace_add_window`. Le plantage a été découvert et signalé par Bráulio Sousa, CT7APZ.

La même vérification est devenue un avertissement dans mutter, le gestionnaire de fenêtres de GNOME dont muffin dérive, en janvier 2021 ([GNOME/mutter#992](https://gitlab.gnome.org/GNOME/mutter/-/issues/992), merge request !1692). [workspace.patch](workspace.patch) fait de même dans muffin.

- Version : `6.6.3+zena+logbeamos1`, faite à partir du code source de muffin `6.6.3+zena` de Linux Mint, avec ce seul changement.
- Paquet source : `muffin_6.6.3+zena+logbeamos1.dsc` et `.tar.xz`, dans le dépôt apt (`deb-src [signed-by=/usr/share/keyrings/logbeamos.gpg] https://logbeam.org/apt/ ./`).
- Les outils de LogBeamOS épinglent muffin à ce dépôt (`etc/apt/preferences.d/logbeamos-muffin`), pour qu'une mise à jour de Linux Mint ne ramène pas le plantage. Un muffin plus récent de Linux Mint attend d'être publié ici avec la même correction.
