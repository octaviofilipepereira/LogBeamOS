<!--
  Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
  © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
  Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
-->

# Manuel de LogBeamOS

*Distribution Linux pour radioamateurs*

C'est le manuel fourni avec LogBeamOS (outils 0.3.15).

[Português](manual-pt.md) · [English](manual-en.md) · [Español](manual-es.md) · **Français**

- [1. Premiers pas](#1-premiers-pas)
- [2. Brancher la radio](#2-brancher-la-radio)
- [3. Quel logiciel pour quoi](#3-quel-logiciel-pour-quoi)
- [4. Mettre à jour](#4-mettre-à-jour)
- [5. À côté de Windows](#5-installer-à-côté-de-windows)
- [6. Problèmes courants](#6-problèmes-courants)

## 1. Premiers pas

- LogBeamOS démarre sur la clé USB sans rien installer sur l'ordinateur. Au premier démarrage, il est demandé si vous voulez votre propre utilisateur et mot de passe ; sans eux, la session s'ouvre toute seule.
- Ce que vous faites sur la clé (réglages, journaux, fichiers) y reste enregistré et s'y retrouve au démarrage suivant.
- Sur le bureau : le dossier **Logiciels Radioamateur** (tous les logiciels), **Radio et Matériel**, **Mettre à jour LogBeamOS**, **LogBeam Uplink** et ce manuel. Les logiciels sont aussi dans le menu, dans le groupe *Radio amateur*.
- Pour éteindre : menu → bouton rouge. Ne retirez pas la clé pendant que LogBeamOS fonctionne.

## 2. Brancher la radio

1. **Branchez la radio en USB.** Pour la plupart des radios, aucun pilote n'est à installer : Linux l'a déjà.
2. **Ouvrez Radio et Matériel.** Il affiche la radio, le port CAT, la carte son de la radio et le port COM correspondant pour N1MM+ et Log4OM.
3. **Tester le CAT :** choisissez le modèle ; avec la vitesse *Automatique*, la vitesse à laquelle la radio répond est recherchée. Le test lit seulement la fréquence : il n'émet jamais.
4. **Configurer les logiciels… :** choisissez la radio dans la liste et cliquez sur *Configurer*. WSJT-X, JTDX, Fldigi, Not1MM et Direwolf utilisent alors la radio en même temps, avec le son de la radio et le PTT par le CAT. Une copie des réglages de chaque logiciel est gardée avant de les changer.
5. **N1MM+ et Log4OM :** dans les réglages CAT de chacun, choisissez le port COM indiqué dans Radio et Matériel. Tant que N1MM+ est ouvert, les autres logiciels n'ont pas de CAT ; à sa fermeture, ils le retrouvent.

> La vitesse CAT doit être la même dans le menu de la radio (par exemple, *CAT RATE* sur les Yaesu).

## 3. Quel logiciel pour quoi

| Pour… | Logiciel |
|---|---|
| FT8, FT4, WSPR | WSJT-X ou JTDX · avec FT2 : Decodium · carte des stations entendues : GridTracker2 |
| Messages au clavier à signal faible | JS8Call |
| RTTY, PSK, Olivia et autres modes numériques | Fldigi (avec Flrig, Flmsg et Flamp) |
| Concours | N1MM+ (celui de Windows, via Wine) ou Not1MM |
| Carnet de trafic (logbook) | Log4OM (via Wine), CQRLOG ou KLog · envoi vers logbeam.org : LogBeam Uplink · envoi vers Wavelog : WaveLogGate |
| APRS | Direwolf (le modem par la carte son) et Xastir (la carte) ; Xastir lance Direwolf tout seul et s'y connecte |
| Winlink (courrier par radio) | Pat |
| Satellites | Gpredict (prévisions et poursuite) · images des satellites météo : SatDump |
| Récepteurs SDR | Gqrx ou SDR++ · expériences : GNU Radio |
| Voix numérique et images | FreeDV · SSTV : QSSTV |
| Radios Icom et Kenwood à distance | wfview |
| Programmation des radios DMR | qdmr |
| DMR sans radio (BrandMeister) | VoxDMR (facultatif : s'installe par *Mettre à jour LogBeamOS* ; demande votre ID DMR et le mot de passe hotspot BrandMeister) |
| EchoLink | Qtel (le routeur doit laisser passer les ports UDP 5198–5199 et TCP 5200, ou utilisez un proxy EchoLink) |
| Simulation d'antennes | xnec2c |
| Analyse des bandes | 4ham Spectrum Analysis |

> Dans Xastir, avant d'émettre : indiquez votre indicatif (Xastir le demande la première fois), changez *MYCALL* dans le fichier `direwolf.conf` de votre dossier personnel et activez l'émission dans *Interfaces*. Par défaut, Xastir ne fait que recevoir.

## 4. Mettre à jour

- **Mettre à jour LogBeamOS** affiche les logiciels radio et le système d'exploitation, avec la version installée, la version disponible et la taille à télécharger.
- Les outils de LogBeamOS (cet outil de mise à jour, **Radio et Matériel** et ce manuel) et **LogBeam Uplink** se mettent aussi à jour ici. Ils viennent du dépôt de LogBeamOS sur logbeam.org, qui est signé.
- Cochez ce que vous voulez mettre à jour. Chaque logiciel a sa case ; le *Système d'exploitation* s'ouvre avec la flèche et chaque paquet peut aussi être choisi. Raccourcis : *Radio*, *Système*, *Tout*, *Rien*.
- Cliquez sur *Mettre à jour la sélection*. Pendant la mise à jour s'affichent ce qui est téléchargé, les Mo, la vitesse et le temps restant.
- N1MM+, Log4OM et GridTracker2 se mettent à jour tout seuls.
- Sur la clé USB, aucun mot de passe n'est demandé ; sur LogBeamOS installé, celui de l'utilisateur est demandé.
- Dix minutes après l'ouverture de la session, un avis apparaît s'il y a des mises à jour.

## 5. Installer à côté de Windows

### D'abord, dans Windows

1. **Sauvegardez vos données.**
2. **Lancez « Preparar o Windows.cmd »** par clic droit → *Exécuter en tant qu'administrateur*. Il se trouve à la racine de l'ISO : dans Windows, double-cliquez sur le fichier ISO pour l'ouvrir. Il désactive le démarrage rapide et, si le lecteur C: est chiffré, commence à le déchiffrer ; avant d'installer, attendez que le pourcentage chiffré atteigne 0 %. Cela peut aussi se faire à la main : *Avant d'installer*.

### Installer

3. Démarrez sur la clé USB et ouvrez *Installer LogBeamOS*. Pour le type d'installation, choisissez d'installer à côté de Windows et faites glisser le séparateur : 40 Go suffisent pour LogBeamOS.
4. Ensuite, au démarrage de l'ordinateur, un menu avec LogBeamOS et Windows s'affiche pendant 10 secondes. Le dernier choix est mémorisé.

### Retirer LogBeamOS

5. Dans Windows, dans une console administrateur : `bcdedit /set {fwbootmgr} displayorder {bootmgr} /addfirst`. L'ordinateur démarre alors directement sur Windows.
6. Gestion des disques : supprimez les partitions de LogBeamOS (celles qui suivent C: et n'ont pas de lettre ; jamais la partition EFI ni celle de récupération). Puis clic droit sur C: → *Étendre le volume*.
7. Facultatif, pour supprimer aussi le démarrage de LogBeamOS, dans la même console :
   - `bcdedit /enum firmware` affiche les entrées de démarrage ; supprimez celles qui ont `\EFI\ubuntu` dans le chemin avec `bcdedit /delete {identifiant}` ;
   - `mountvol S: /S` et `rmdir /S /Q S:\EFI\ubuntu` ;
   - si `S:\EFI\Boot\fbx64.efi` existe, l'installateur a remplacé le démarrage de secours du disque : `copy /Y S:\EFI\Microsoft\Boot\bootmgfw.efi S:\EFI\Boot\bootx64.efi` et `del S:\EFI\Boot\fbx64.efi S:\EFI\Boot\mmx64.efi` ;
   - pour finir, `mountvol S: /D`.

## 6. Problèmes courants

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

**Pas de son de la radio dans WSJT-X ou Direwolf**  
Dans Radio et Matériel → *Configurer les logiciels…*, choisissez le son de la radio.

**Direwolf se ferme tout de suite**  
La fenêtre reste ouverte avec l'explication. Les réglages sont dans le fichier `direwolf.conf` de votre dossier personnel.
