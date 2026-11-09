<p align="center"><img src="usr/share/logbeamos/manual/logbeam.png" width="96" alt="LogBeamOS"></p>

<h1 align="center">LogBeamOS</h1>

<p align="center"><b>LogBeamOS, la distribution Linux pour radioamateurs.</b></p>

<p align="center">
  <a href="https://logbeam.org"><img alt="logbeam.org" src="https://img.shields.io/badge/site-logbeam.org-2f81f7"></a>
  <img alt="Ubuntu 24.04 LTS" src="https://img.shields.io/badge/bas%C3%A9e%20sur-Ubuntu%2024.04%20LTS-e95420">
  <a href="https://www.gnu.org/licenses/gpl-3.0.html"><img alt="Licence GPL v3" src="https://img.shields.io/badge/licence-GPL%20v3-blue"></a>
</p>

<p align="center"><a href="README.pt.md">Português</a> · <a href="README.md">English</a> · <a href="README.es.md">Español</a> · <b>Français</b></p>

---

LogBeamOS est une distribution pour radioamateurs basée sur Ubuntu 24.04 LTS. Elle démarre depuis une clé USB, en gardant les données, ou s'installe à côté de Windows, avec les logiciels de radioamateur déjà installés : des logiciels natifs Linux et, via Wine, N1MM Logger+ et Log4OM.

Ces logiciels appartiennent à leurs auteurs et viennent des sources habituelles : les dépôts d'Ubuntu, les publications des auteurs eux-mêmes et Flathub. **Ce dépôt ne contient que ce qui a été écrit pour LogBeamOS** : les outils ci-dessous. LogBeam Uplink, qui envoie les QSO à [LogBeam](https://logbeam.org), a son propre dépôt : [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

## Les outils

| Outil | Ce qu'il fait |
|---|---|
| **Mettre à jour LogBeamOS** | Une fenêtre pour mettre à jour les logiciels de radioamateur et le système d'exploitation. Elle affiche la version installée, la version disponible et la taille à télécharger, et ne met à jour que ce qui est coché, avec la progression en Mo, la vitesse et le temps restant. Elle couvre les paquets du système, les logiciels publiés sur GitHub (WSJT-X, JS8Call, wfview, SatDump, SDR++, Decodium, qdmr et d'autres), Not1MM et les outils de LogBeamOS eux-mêmes. Dix minutes après l'ouverture de la session, un avis apparaît s'il y a des mises à jour. |
| **Radio et Matériel** | Détecte les radios, les câbles CAT, les cartes son et les récepteurs SDR. Partage la radio entre les logiciels via `rigctld` de Hamlib, avec détection automatique de la vitesse, et configure WSJT-X, JTDX, Decodium, Fldigi, Not1MM et Direwolf pour l'utiliser. |
| **Manuel de LogBeamOS** | Premiers pas, brancher la radio, quel logiciel pour quoi, mettre à jour, installer à côté de Windows et retirer LogBeamOS. Dans sa propre fenêtre, dans la langue de la session. |
| **Lanceurs** | N1MM Logger+ via Wine, recevant la radio partagée tant qu'il est ouvert ; Direwolf, avec une configuration créée si elle manque ; Xastir, relié à Direwolf. |

Toutes les fenêtres sont en portugais, anglais, espagnol et français.

## Installer et mettre à jour

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

## Organisation du dépôt

Chaque fichier est dans le dossier où il est installé :

| Dossier | Contenu |
|---|---|
| `usr/local/bin/` | Les programmes : `logbeamos-actualizar`, `logbeamos-equipamento`, `logbeamos-manual` et les lanceurs |
| `usr/local/lib/logbeamos/` | Ce qu'utilisent Mettre à jour (`actualizar/`) et Radio et Matériel (`equipamento/`) |
| `usr/share/logbeamos/` | Les icônes et le manuel dans les quatre langues |
| `usr/local/share/applications/` | Les entrées du menu |
| `usr/share/polkit-1/actions/` | L'autorisation de l'assistant de mise à jour, qui s'exécute en administrateur |
| `etc/` | L'avis de mises à jour à l'ouverture de la session et la règle qui écarte les récepteurs RTL-SDR du pilote TV de Linux |

Les outils sont écrits en Python 3 avec GTK 3 ; la fenêtre du manuel utilise WebKitGTK.

## Contribuer et sécurité

Les contributions sont les bienvenues : voir [CONTRIBUTING.md](CONTRIBUTING.md). Les failles de sécurité se signalent en privé : voir [SECURITY.md](SECURITY.md).

## Licence

Les outils de LogBeamOS sont des logiciels libres, distribués sous la [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). Le texte complet se trouve dans le fichier [LICENSE](LICENSE).

## Exclusion de responsabilité

- Les outils de LogBeamOS sont distribués sans aucune garantie, selon la GPL v3 (articles 15 et 16). L'auteur n'est pas responsable des dommages ou pertes résultant de leur utilisation, que ce soit dans la version officielle ou dans une version modifiée.
- Quiconque modifie et distribue une version en est seul responsable.
- Les versions officielles sont uniquement celles distribuées par le dépôt à `https://logbeam.org/apt`, signées avec la clé ci-dessus.

## Auteur

Octávio Filipe Pereira Gonçalves, CT7BFV · [logbeam.org](https://logbeam.org)
