<!--
  Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
  © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
  Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
-->

# Manuel de LogBeamOS

*Distribution Linux pour radioamateurs*

C'est le manuel fourni avec LogBeamOS (LogBeamOS Update 1.0.0-1).

[Português](manual-pt.md) · [English](manual-en.md) · [Español](manual-es.md) · **Français**

- [1. Premiers pas](#1-premiers-pas)
- [2. Brancher la radio](#2-brancher-la-radio)
- [3. Quel logiciel pour quoi](#3-quel-logiciel-pour-quoi)
- [4. Installer et supprimer des logiciels](#4-installer-et-supprimer-des-logiciels)
- [5. Mettre à jour](#5-mettre-à-jour)
- [6. À côté de Windows](#6-installer-à-côté-de-windows)
- [7. Problèmes courants](#7-problèmes-courants)
- [8. Signaler un problème](#8-signaler-un-problème)

## 1. Premiers pas

- LogBeamOS démarre sur la clé USB sans rien installer sur l'ordinateur. Au premier démarrage, il est demandé si vous voulez votre propre utilisateur et mot de passe ; sans eux, la session s'ouvre toute seule.
- Ce que vous faites sur la clé (réglages, journaux, fichiers) y reste enregistré et s'y retrouve au démarrage suivant.
- Sur le bureau : le dossier **Logiciels Radioamateur** (tous les logiciels), **Radio et Matériel**, **Mettre à jour LogBeamOS**, **Gestionnaire de logiciels LogBeamOS**, **LogBeam Uplink** et ce manuel. Les logiciels sont aussi dans le menu, dans le groupe *Radio amateur*.
- Pour éteindre : menu → bouton rouge. Ne retirez pas la clé pendant que LogBeamOS fonctionne.

## 2. Brancher la radio

1. **Branchez la radio en USB.** Pour la plupart des radios, aucun pilote n'est à installer : Linux l'a déjà.
2. **Ouvrez Radio et Matériel.** Il affiche la radio, le port CAT, la carte son de la radio et le port COM correspondant pour N1MM+ et Log4OM.
3. **Tester le CAT :** choisissez le modèle ; avec la vitesse *Automatique*, la vitesse à laquelle la radio répond est recherchée. Le test lit seulement la fréquence : il n'émet jamais.
4. **Configurer les logiciels… :** choisissez la radio dans la liste et cliquez sur *Configurer*. WSJT-X, JTDX, Fldigi, Not1MM et Direwolf utilisent alors la radio en même temps, avec le son de la radio et le PTT par le CAT. Une copie des réglages de chaque logiciel est gardée avant de les changer.
5. **N1MM+ et Log4OM :** sur le même écran, choisissez comment chacun utilise la radio. *Seul N1MM+ (ou Log4OM) utilise la radio* : le logiciel communique directement avec la radio ; tant qu'il est ouvert, les autres logiciels n'ont pas de CAT et, à sa fermeture, ils le retrouvent. *Utilise la radio avec les autres logiciels* : tous utilisent la radio en même temps ; N1MM+ voit un « Kenwood TS-2000 » et les fonctions propres à votre radio peuvent ne pas fonctionner. Vous pouvez changer ce choix quand vous voulez, dans *Configurer les logiciels…*. Log4OM doit être ouvert une fois avant de pouvoir être configuré.

> La vitesse CAT doit être la même dans le menu de la radio (par exemple, *CAT RATE* sur les Yaesu).

## 3. Quel logiciel pour quoi

| Pour… | Logiciel |
|---|---|
| FT8, FT4, WSPR | WSJT-X ou JTDX · avec FT2 : Decodium · carte des stations entendues : GridTracker2 |
| Messages au clavier à signal faible | JS8Call |
| RTTY, PSK, Olivia et autres modes numériques | Fldigi (avec Flrig, Flmsg et Flamp) |
| Concours | N1MM+ (celui de Windows, via Wine) ou Not1MM |
| Carnet de trafic (logbook) | Log4OM (via Wine), CQRLOG ou KLog · envoi vers logbeam.org : LogBeam Uplink · envoi vers Wavelog : WaveLogGate |
| Confirmations Logbook of The World (LoTW) | TQSL, de l'ARRL : signe vos QSO et les envoie à LoTW |
| APRS | Direwolf (le modem par la carte son) et Xastir (la carte) ; Xastir lance Direwolf tout seul et s'y connecte |
| Winlink (courrier par radio) | Pat |
| Satellites | Gpredict (prévisions et poursuite) · images des satellites météo : SatDump |
| Récepteurs SDR | Gqrx ou SDR++ · expériences : GNU Radio |
| Voix numérique et images | FreeDV · SSTV : QSSTV |
| Radios Icom et Kenwood à distance | wfview |
| Programmation des radios DMR | qdmr |
| DMR sans radio (BrandMeister) | VoxDMR (facultatif : s'installe par le *Gestionnaire de logiciels LogBeamOS* ; demande votre ID DMR et le mot de passe hotspot BrandMeister) |
| EchoLink | Qtel (le routeur doit laisser passer les ports UDP 5198–5199 et TCP 5200, ou utilisez un proxy EchoLink) |
| WIRES-X (Yaesu) | WIRES-X, via Wine. Il n'est pas fourni avec LogBeamOS : téléchargez-le sur le site WIRES-X de Yaesu (une connexion avec votre ID est nécessaire), ouvrez *WIRES-X* et indiquez le fichier .zip téléchargé. Le port COM de la HRI-200 ou de la radio (mode PDN) est ensuite indiqué, à choisir dans l'écran *COM port setting* de WIRES-X. |
| Simulation d'antennes | xnec2c |
| Analyse de spectre et analyses académiques du spectre radioélectrique | 4ham Spectrum Analysis |

> qdmr, SatDump, Not1MM, Gqrx, GNU Radio, GridTracker2, Decodium et wfview s'installent quand on les demande : l'icône est là et, la première fois, il est demandé si vous voulez installer le logiciel (une connexion à Internet est nécessaire). Voir [4. Installer et supprimer des logiciels](#4-installer-et-supprimer-des-logiciels).

> Dans Xastir, avant d'émettre : indiquez votre indicatif (Xastir le demande la première fois), changez *MYCALL* dans le fichier `direwolf.conf` de votre dossier personnel et activez l'émission dans *Interfaces*. Par défaut, Xastir ne fait que recevoir.

## 4. Installer et supprimer des logiciels

- Le **Gestionnaire de logiciels LogBeamOS** recherche, installe et supprime des logiciels : les logiciels radio et tous les autres.
- La page d'accueil présente les **Logiciels Radioamateur**, par groupes (modes numériques, carnets de trafic et concours, SDR, satellites, APRS et Winlink, voix numérique, radio et utilitaires), chacun avec son état. *Autres logiciels radio* regroupe les autres logiciels radio d'Ubuntu.
- Plus bas se trouvent les autres catégories : Internet, son et vidéo, graphisme, bureautique, jeux, Flatpak, logiciels installés et d'autres. La recherche, en haut, trouve n'importe quel logiciel par son nom ou sa description.
- Chaque logiciel a sa page, avec la description, la version, la source, l'espace occupé et les boutons *Installer*, *Supprimer* et *Ouvrir*.
- **Logiciels à la demande :** qdmr, SatDump, Not1MM, Gqrx, GNU Radio, GridTracker2, Decodium et wfview ne sont pas installés, pour que l'image soit plus petite, mais leur icône est dans le menu et dans le dossier **Logiciels Radioamateur**. Un clic dessus demande s'il faut l'installer. Le bouton *Tout installer* les installe tous d'un coup, pour qu'ils soient disponibles même sans connexion à Internet.
- Quand un logiciel radio est supprimé, son lanceur quitte le menu et le dossier (les logiciels à la demande gardent leur icône). Pour 4ham, les données et les réglages sont conservés dans `/var/lib/logbeamos/guardado`.
- N1MM+, Log4OM et WIRES-X (logiciels Windows, via Wine) se suppriment aussi ici. Pour les réinstaller, l'installateur se télécharge sur le site officiel et le gestionnaire l'installe dans Wine.
- Dans le menu, *Désinstaller* sur un logiciel radio ouvre le gestionnaire sur la page de ce logiciel. Les outils de LogBeamOS (Mettre à jour, Radio et Matériel, ce manuel, TQSL) font partie du système et ne peuvent pas être supprimés.
- Sur la clé USB, un logiciel installé occupe la partie de la clé réservée aux données ; le supprimer ensuite ne libère pas l'espace des logiciels qui venaient dans l'image.

## 5. Mettre à jour

- **Mettre à jour LogBeamOS** affiche les logiciels radio et le système d'exploitation, avec la version installée, la version disponible et la taille à télécharger.
- **LogBeamOS Update** (cet outil de mise à jour, **Radio et Matériel** et ce manuel) et **LogBeam Uplink** se mettent aussi à jour ici. Ils viennent du dépôt de LogBeamOS sur logbeam.org, qui est signé. La version de LogBeamOS et celle de LogBeamOS Update sont affichées en haut de la fenêtre.
- Il met aussi à jour les applications Flatpak et les extensions de Cinnamon. Sur un LogBeamOS installé sur le disque, il retire les anciens noyaux : restent celui en cours d'utilisation et le plus récent.
- Chaque nouvelle version de LogBeamOS arrive aussi par ici, sans réinstallation. Seul ce qui fait partie du démarrage de la clé USB demande de la graver à nouveau. Les nouveautés de chaque version sont sur [logbeam.org/logbeamos/novidades](https://logbeam.org/logbeamos/novidades/?hl=fr).
- Cochez ce que vous voulez mettre à jour. Chaque logiciel a sa case ; le *Système d'exploitation* s'ouvre avec la flèche et chaque paquet peut aussi être choisi. Raccourcis : *Radio*, *Système*, *Tout*, *Rien*.
- Cliquez sur *Mettre à jour la sélection*. Pendant la mise à jour s'affichent ce qui est téléchargé, les Mo, la vitesse et le temps restant.
- N1MM+, Log4OM et GridTracker2 se mettent à jour tout seuls.
- Sur la clé USB, aucun mot de passe n'est demandé ; sur LogBeamOS installé, celui de l'utilisateur est demandé.
- Dix minutes après l'ouverture de la session, un avis apparaît s'il y a des mises à jour.

## 6. Installer à côté de Windows

### D'abord, dans Windows

1. **Sauvegardez vos données.**
2. **Lancez « Preparar o Windows.cmd »** par clic droit → *Exécuter en tant qu'administrateur*. Il se trouve à la racine de l'ISO : dans Windows, double-cliquez sur le fichier ISO pour l'ouvrir. Il désactive le démarrage rapide et, si le lecteur C: est chiffré, commence à le déchiffrer ; avant d'installer, attendez que le pourcentage chiffré atteigne 0 %. Cela peut aussi se faire à la main : *Avant d'installer*.

### Installer

3. Démarrez sur la clé USB et ouvrez *Installer LogBeamOS*. Pour le type d'installation, choisissez d'installer à côté de Windows et faites glisser le séparateur pour donner au moins 50 Go à LogBeamOS ; l'installateur n'accepte pas moins.
4. Ensuite, au démarrage de l'ordinateur, un menu avec LogBeamOS et Windows s'affiche pendant 10 secondes. Le dernier choix est mémorisé.

### Retirer LogBeamOS

5. Dans Windows, dans une console administrateur : `bcdedit /set {fwbootmgr} displayorder {bootmgr} /addfirst`. L'ordinateur démarre alors directement sur Windows.
6. Gestion des disques : supprimez les partitions de LogBeamOS (celles qui suivent C: et n'ont pas de lettre ; jamais la partition EFI ni celle de récupération). Puis clic droit sur C: → *Étendre le volume*.
7. Facultatif, pour supprimer aussi le démarrage de LogBeamOS, dans la même console :
   - `bcdedit /enum firmware` affiche les entrées de démarrage ; supprimez celles qui ont `\EFI\ubuntu` dans le chemin avec `bcdedit /delete {identifiant}` ;
   - `mountvol S: /S` et `rmdir /S /Q S:\EFI\ubuntu` ;
   - si `S:\EFI\Boot\fbx64.efi` existe, l'installateur a remplacé le démarrage de secours du disque : `copy /Y S:\EFI\Microsoft\Boot\bootmgfw.efi S:\EFI\Boot\bootx64.efi` et `del S:\EFI\Boot\fbx64.efi S:\EFI\Boot\mmx64.efi` ;
   - pour finir, `mountvol S: /D`.

## 7. Problèmes courants

**La clé USB ne démarre pas : « Unable to find a medium containing a live file system »**  
Retirez la clé, attendez 5 secondes, rebranchez-la et redémarrez.

**Windows demande de formater la clé USB**  
Annulez toujours. C'est la partie de la clé où sont gardées vos données LogBeamOS, que Windows ne sait pas lire.

**Un logiciel est bloqué**  
Ouvrez le Moniteur système (icône dans la barre), onglet *Processus*, clic droit sur le logiciel → *Terminer*.

**Le bureau a planté (« mode de secours »)**  
Appuyez sur Ctrl+Alt+Échap pour le relancer, ou fermez la session et rouvrez-la.

**La radio ne répond pas au CAT**  
Dans Radio et Matériel, vérifiez le modèle et utilisez la vitesse *Automatique* ; vérifiez que le CAT est activé dans le menu de la radio et fermez les logiciels qui utilisent le port.

**N1MM+ : « The given port name is invalid… not a serial port » ou « Radio … is not responding »**  
Le port COM choisi dans N1MM+ n'est pas celui du câble de la radio. Dans Radio et Matériel, cliquez sur *Configurer les logiciels…* et choisissez comment N1MM+ utilise la radio : le bon port est écrit dans N1MM+. Le COM de chaque câble est indiqué dans Radio et Matériel (« dans N1MM+ et Log4OM : COM… »).

**LogBeam Uplink signale « le port 2333 est occupé par un autre logiciel »**  
C'est en général WaveLogGate, qui reçoit aussi des QSO sur ce port. LogBeamOS passe WaveLogGate sur le port 2335 à l'ouverture de la session ; s'il a été remis sur 2333, changez-le dans WaveLogGate : *Configuration* → *Advanced* → *UDP Port* 2335 → *Save*. Fermez ensuite LogBeam Uplink et rouvrez-le. Si un logiciel envoyait des QSO à WaveLogGate, changez aussi son port de destination en 2335.

**WaveLogGate : « HTTPS/WSS require a trusted certificate »**  
LogBeamOS installe lui-même le certificat de WaveLogGate dans Firefox, sans mot de passe, dès que WaveLogGate le crée : il n'est pas nécessaire de cliquer sur *Install Certificate*. Si l'avertissement persiste, fermez WaveLogGate et rouvrez-le.

**Pas de son de la radio dans WSJT-X ou Direwolf**  
Dans Radio et Matériel → *Configurer les logiciels…*, choisissez le son de la radio.

**Direwolf se ferme tout de suite**  
La fenêtre reste ouverte avec l'explication. Les réglages sont dans le fichier `direwolf.conf` de votre dossier personnel.

## 8. Signaler un problème

Quand quelque chose ne fonctionne pas, un signalement fait avec ces trois étapes suffit pour comprendre ce qui s'est passé.

1. **Notez ce qui s'est passé :** ce que vous faisiez, ce que vous attendiez et ce qui est apparu. S'il y a un message d'erreur, copiez son texte ou photographiez l'écran (touche *Impr écran*).
2. **Créez le rapport de diagnostic** juste après la panne, avant de redémarrer : dans le menu, *Rapport de diagnostic* ; ou, dans un terminal, `logbeamos-diagnostic`. Un fichier texte est enregistré sur le bureau. Si l'ordinateur s'est bloqué et a dû être redémarré, utilisez `logbeamos-diagnostic --precedent`, qui rassemble aussi les erreurs du démarrage précédent.
3. **Envoyez le signalement** avec le fichier en pièce jointe : sur [github.com/octaviofilipepereira/LogBeamOS](https://github.com/octaviofilipepereira/LogBeamOS/issues/new/choose), onglet *Issues* (il faut un compte GitHub, gratuit).

> Le rapport ne contient ni mots de passe ni clés, et le nom d'utilisateur, le nom de l'ordinateur et les adresses réseau en sont retirés. Il contient les versions, le modèle de l'ordinateur, les périphériques USB branchés, la configuration de la radio dans chaque logiciel et les avertissements et erreurs du système. Vous pouvez le lire avant de l'envoyer.
