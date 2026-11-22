# Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
# © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
# Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
# LogBeamOS: the catalogue of the amateur radio programs of the "LogBeamOS Programs" manager (Gestor de Programas
# LogBeamOS, 1.0.0, author's decisions of 22/11/2026): where each program comes from, how it is installed and removed,
# its launchers, its icon and its description in the four languages of LogBeamOS. Used by the manager window (as the
# user), by its helper (as root), by the on-demand launchers and by the menu "Uninstall" (programas-desinstalar).
# The helper never receives addresses from the window: it reads them here and in lb_actualizar.GITHUB.
#
# Kinds of program ("tipo"):
#   apt         packages of the Ubuntu, Mint or LogBeamOS repositories ("pacotes")
#   github      a program of lb_actualizar.GITHUB ("github" = its key): .deb, AppImage, makeself, flatpak or source
#   deb         a .deb from a fixed address with its SHA-256 ("url", "sha256", "pacote"); it updates itself later
#   pipx        Not1MM, in /opt/pipx (as the image has it since 0.3.0)
#   wine        a Windows program in the user's own Wine prefix (see wine-env.sh): installed and removed as the user
#   logbeamos   part of LogBeamOS itself: shown, never removed
import json
import os
import re
import subprocess

ICONES = "/usr/share/logbeamos/programas"   # a copy of every icon, so that it shows while the program is not installed
APLICACOES = "/usr/local/share/applications"

# Sub-categories of the amateur radio category (the main one, on the home page of the manager)
CATEGORIAS = [
    ("digitais", {"pt": "Modos digitais", "en": "Digital modes", "es": "Modos digitales", "fr": "Modes numériques"}),
    ("logs", {"pt": "Logs e concursos", "en": "Logging and contests", "es": "Registro y concursos",
              "fr": "Carnets de trafic et concours"}),
    ("sdr", {"pt": "SDR e espectro", "en": "SDR and spectrum", "es": "SDR y espectro", "fr": "SDR et spectre"}),
    ("satelites", {"pt": "Satélites", "en": "Satellites", "es": "Satélites", "fr": "Satellites"}),
    ("aprs", {"pt": "APRS, pacote e Winlink", "en": "APRS, packet and Winlink", "es": "APRS, paquetes y Winlink",
              "fr": "APRS, paquet et Winlink"}),
    ("voz", {"pt": "Voz digital e ligações", "en": "Digital voice and linking", "es": "Voz digital y enlaces",
             "fr": "Voix numérique et liaisons"}),
    ("radio", {"pt": "Rádio e utilitários", "en": "Radio and utilities", "es": "Radio y utilidades",
               "fr": "Radio et utilitaires"}),
]


def _p(chave, nome, categoria, tipo, resumo, descricao, site, **outros):
    d = {"chave": chave, "nome": nome, "categoria": categoria, "tipo": tipo, "resumo": resumo,
         "descricao": descricao, "site": site, "lancadores": [chave], "a_pedido": False}
    d.update(outros)
    return d


def _t(pt, en, es, fr):
    return {"pt": pt, "en": en, "es": es, "fr": fr}


PROGRAMAS = [
    # --- Digital modes
    _p("wsjtx", "WSJT-X", "digitais", "github",
       _t("FT8, FT4, WSPR e outros modos de sinal fraco", "FT8, FT4, WSPR and other weak-signal modes",
          "FT8, FT4, WSPR y otros modos de señal débil", "FT8, FT4, WSPR et autres modes à signal faible"),
       _t("O programa de referência dos modos digitais de sinal fraco: FT8, FT4, WSPR, JT65, Q65 e MSK144, entre outros. "
          "Permite contactos com sinais muito abaixo do ruído, em HF e acima.",
          "The reference program for weak-signal digital modes: FT8, FT4, WSPR, JT65, Q65 and MSK144, among others. "
          "It makes contacts with signals far below the noise, on HF and above.",
          "El programa de referencia de los modos digitales de señal débil: FT8, FT4, WSPR, JT65, Q65 y MSK144, entre "
          "otros. Permite contactos con señales muy por debajo del ruido, en HF y superiores.",
          "Le logiciel de référence des modes numériques à signal faible : FT8, FT4, WSPR, JT65, Q65 et MSK144, entre "
          "autres. Il permet des contacts avec des signaux très en dessous du bruit, en HF et au-delà."),
       "https://wsjt.sourceforge.io", github="wsjtx", lancadores=["wsjtx", "message_aggregator"], comando="wsjtx"),
    _p("jtdx", "JTDX", "digitais", "apt",
       _t("FT8, FT4 e JT65 com descodificação melhorada", "FT8, FT4 and JT65 with improved decoding",
          "FT8, FT4 y JT65 con decodificación mejorada", "FT8, FT4 et JT65 avec un décodage amélioré"),
       _t("Derivado do WSJT-X, centrado no FT8, no FT4 e no JT65, com descodificação afinada para bandas cheias e "
          "para o DX.",
          "Derived from WSJT-X, focused on FT8, FT4 and JT65, with decoding tuned for crowded bands and for DX.",
          "Derivado de WSJT-X, centrado en FT8, FT4 y JT65, con decodificación afinada para bandas llenas y para el DX.",
          "Dérivé de WSJT-X, centré sur le FT8, le FT4 et le JT65, avec un décodage affiné pour les bandes chargées et "
          "le DX."),
       "https://www.jtdx.tech", pacotes=["jtdx"], comando="jtdx"),
    _p("js8call", "JS8Call", "digitais", "github",
       _t("Mensagens por teclado em sinal fraco", "Keyboard messaging with weak signals",
          "Mensajes por teclado con señal débil", "Messages au clavier à signal faible"),
       _t("Conversas e mensagens por teclado com a robustez do FT8, incluindo mensagens guardadas e retransmitidas "
          "por outras estações. Muito usado em emergência e no campo, sem Internet.",
          "Keyboard conversations and messages with the robustness of FT8, including messages stored and relayed by "
          "other stations. Much used in emergencies and in the field, without the Internet.",
          "Conversaciones y mensajes por teclado con la robustez del FT8, incluidos mensajes guardados y retransmitidos "
          "por otras estaciones. Muy usado en emergencias y en el campo, sin Internet.",
          "Conversations et messages au clavier avec la robustesse du FT8, y compris des messages stockés et relayés "
          "par d'autres stations. Très utilisé en urgence et sur le terrain, sans Internet."),
       "https://js8call-improved.com", github="js8call", comando="js8call"),
    _p("decodium", "Decodium", "digitais", "github",
       _t("FT8, FT4, FT2 e outros modos de sinal fraco", "FT8, FT4, FT2 and other weak-signal modes",
          "FT8, FT4, FT2 y otros modos de señal débil", "FT8, FT4, FT2 et autres modes à signal faible"),
       _t("Derivado do WSJT-X feito por IU8LMC, com o modo FT2 e melhorias na descodificação.",
          "A WSJT-X derivative by IU8LMC, with the FT2 mode and decoding improvements.",
          "Derivado de WSJT-X hecho por IU8LMC, con el modo FT2 y mejoras en la decodificación.",
          "Un dérivé de WSJT-X réalisé par IU8LMC, avec le mode FT2 et des améliorations du décodage."),
       "https://github.com/iu8lmc/Decodium-4.0-Core-Shannon", github="decodium", comando="decodium", a_pedido=True),
    _p("fldigi", "Fldigi", "digitais", "apt",
       _t("PSK, RTTY, CW, Olivia, MFSK e muitos outros modos", "PSK, RTTY, CW, Olivia, MFSK and many other modes",
          "PSK, RTTY, CW, Olivia, MFSK y muchos otros modos", "PSK, RTTY, CW, Olivia, MFSK et bien d'autres modes"),
       _t("O modem digital mais completo: PSK31, RTTY, CW, Olivia, Contestia, MFSK, Thor e dezenas de outros modos, "
          "com o Flarq para transferir ficheiros.",
          "The most complete digital modem: PSK31, RTTY, CW, Olivia, Contestia, MFSK, Thor and dozens of other modes, "
          "with Flarq for file transfers.",
          "El módem digital más completo: PSK31, RTTY, CW, Olivia, Contestia, MFSK, Thor y decenas de otros modos, con "
          "Flarq para transferir archivos.",
          "Le modem numérique le plus complet : PSK31, RTTY, CW, Olivia, Contestia, MFSK, Thor et des dizaines d'autres "
          "modes, avec Flarq pour transférer des fichiers."),
       "http://www.w1hkj.org", pacotes=["fldigi"], lancadores=["fldigi", "flarq"], comando="fldigi"),
    _p("flmsg", "Flmsg", "digitais", "apt",
       _t("Formulários e mensagens para emergência", "Forms and messages for emergency traffic",
          "Formularios y mensajes para emergencias", "Formulaires et messages pour le trafic d'urgence"),
       _t("Prepara e envia, com o Fldigi, mensagens em formulários normalizados (ICS, Radiogram, Red Cross e outros).",
          "Prepares and sends, with Fldigi, messages in standard forms (ICS, Radiogram, Red Cross and others).",
          "Prepara y envía, con Fldigi, mensajes en formularios normalizados (ICS, Radiogram, Red Cross y otros).",
          "Prépare et envoie, avec Fldigi, des messages sur des formulaires normalisés (ICS, Radiogram, Red Cross et "
          "autres)."),
       "http://www.w1hkj.org", pacotes=["flmsg"], comando="flmsg"),
    _p("flamp", "Flamp", "digitais", "apt",
       _t("Envio de ficheiros para várias estações", "Sends files to many stations at once",
          "Envío de archivos a varias estaciones", "Envoi de fichiers à plusieurs stations"),
       _t("Transmite ficheiros a várias estações ao mesmo tempo, com o Fldigi, e cada uma pede só os blocos que lhe "
          "faltam.",
          "Transmits files to many stations at once, with Fldigi; each one asks only for the blocks it is missing.",
          "Transmite archivos a varias estaciones a la vez, con Fldigi, y cada una pide solo los bloques que le faltan.",
          "Transmet des fichiers à plusieurs stations à la fois, avec Fldigi ; chacune ne redemande que les blocs qui "
          "lui manquent."),
       "http://www.w1hkj.org", pacotes=["flamp"], comando="flamp"),
    _p("qsstv", "QSSTV", "digitais", "apt",
       _t("Imagens por rádio (SSTV e DRM)", "Pictures over radio (SSTV and DRM)", "Imágenes por radio (SSTV y DRM)",
          "Images par radio (SSTV et DRM)"),
       _t("Recebe e envia imagens em SSTV analógica e em SSTV digital (DRM).",
          "Receives and sends pictures in analogue SSTV and in digital SSTV (DRM).",
          "Recibe y envía imágenes en SSTV analógica y en SSTV digital (DRM).",
          "Reçoit et envoie des images en SSTV analogique et en SSTV numérique (DRM)."),
       "https://github.com/ON4QZ/QSSTV", pacotes=["qsstv"], comando="qsstv"),
    # --- Logging and contests
    _p("n1mm", "N1MM Logger+", "logs", "wine",
       _t("Logger de concursos (Windows, pelo Wine)", "Contest logger (Windows, through Wine)",
          "Registro de concursos (Windows, mediante Wine)", "Logiciel de concours (Windows, via Wine)"),
       _t("O logger de concursos mais usado no mundo, a correr pelo Wine com o rádio partilhado do LogBeamOS. "
          "Actualiza-se sozinho.",
          "The most widely used contest logger, running through Wine with the LogBeamOS shared radio. It updates "
          "itself.",
          "El registro de concursos más usado del mundo, funcionando mediante Wine con la radio compartida de "
          "LogBeamOS. Se actualiza solo.",
          "Le logiciel de concours le plus utilisé au monde, via Wine avec la radio partagée de LogBeamOS. Il se met à "
          "jour tout seul."),
       "https://n1mmwp.hamdocs.com", comando="n1mm"),
    _p("log4om", "Log4OM 2", "logs", "wine",
       _t("Log da estação (Windows, pelo Wine)", "Station logbook (Windows, through Wine)",
          "Libro de guardia (Windows, mediante Wine)", "Carnet de trafic (Windows, via Wine)"),
       _t("Log completo da estação, com envio para o LoTW, o eQSL, o QRZ.com e o ClubLog, a correr pelo Wine com o "
          "rádio partilhado do LogBeamOS. Actualiza-se sozinho.",
          "A complete station logbook that uploads to LoTW, eQSL, QRZ.com and ClubLog, running through Wine with the "
          "LogBeamOS shared radio. It updates itself.",
          "Libro de guardia completo, con envío a LoTW, eQSL, QRZ.com y ClubLog, funcionando mediante Wine con la "
          "radio compartida de LogBeamOS. Se actualiza solo.",
          "Carnet de trafic complet, avec envoi vers LoTW, eQSL, QRZ.com et ClubLog, via Wine avec la radio partagée "
          "de LogBeamOS. Il se met à jour tout seul."),
       "https://www.log4om.com", comando="log4om"),
    _p("not1mm", "Not1MM", "logs", "pipx",
       _t("Logger de concursos para Linux", "Contest logger for Linux", "Registro de concursos para Linux",
          "Logiciel de concours pour Linux"),
       _t("Logger de concursos nativo para Linux, inspirado no N1MM+, com rádio por CAT, CW e ligação ao WSJT-X.",
          "A native Linux contest logger inspired by N1MM+, with CAT radio control, CW and a link to WSJT-X.",
          "Registro de concursos nativo para Linux, inspirado en N1MM+, con radio por CAT, CW y enlace con WSJT-X.",
          "Logiciel de concours natif pour Linux, inspiré de N1MM+, avec la radio par CAT, la CW et le lien avec "
          "WSJT-X."),
       "https://github.com/mbridak/not1mm", lancadores=["k6gte-not1mm"], comando="not1mm", a_pedido=True),
    _p("cqrlog", "CQRLOG", "logs", "apt",
       _t("Log da estação para Linux", "Station logbook for Linux", "Libro de guardia para Linux",
          "Carnet de trafic pour Linux"),
       _t("Log da estação nativo para Linux, com base de dados, DX cluster, controlo do rádio e envio para o LoTW e "
          "o eQSL.",
          "A native Linux station logbook with a database, DX cluster, radio control and uploads to LoTW and eQSL.",
          "Libro de guardia nativo para Linux, con base de datos, DX cluster, control de la radio y envío a LoTW y "
          "eQSL.",
          "Carnet de trafic natif pour Linux, avec base de données, DX cluster, contrôle de la radio et envoi vers LoTW "
          "et eQSL."),
       "https://www.cqrlog.com", pacotes=["cqrlog"], comando="cqrlog"),
    _p("klog", "KLog", "logs", "apt",
       _t("Log da estação simples", "A simple station logbook", "Libro de guardia sencillo", "Carnet de trafic simple"),
       _t("Log da estação simples e completo, com DXCC, concursos e exportação em ADIF.",
          "A simple and complete station logbook, with DXCC, contests and ADIF export.",
          "Libro de guardia sencillo y completo, con DXCC, concursos y exportación en ADIF.",
          "Carnet de trafic simple et complet, avec DXCC, concours et export ADIF."),
       "https://www.klog.xyz", pacotes=["klog"], comando="klog"),
    _p("tlf", "Tlf", "logs", "apt",
       _t("Logger de concursos no terminal", "Contest logger in the terminal", "Registro de concursos en el terminal",
          "Logiciel de concours dans le terminal"),
       _t("Logger de concursos em modo de texto, rápido e só com o teclado, para CW, SSB e modos digitais.",
          "A text-mode contest logger, fast and keyboard-only, for CW, SSB and digital modes.",
          "Registro de concursos en modo texto, rápido y solo con el teclado, para CW, SSB y modos digitales.",
          "Logiciel de concours en mode texte, rapide et entièrement au clavier, pour la CW, la SSB et les modes "
          "numériques."),
       "https://tlf.github.io", pacotes=["tlf"], lancadores=[], comando="x-terminal-emulator -e tlf"),
    _p("gridtracker2", "GridTracker2", "logs", "deb",
       _t("Mapa e alertas para o WSJT-X e o JTDX", "Map and alerts for WSJT-X and JTDX",
          "Mapa y alertas para WSJT-X y JTDX", "Carte et alertes pour WSJT-X et JTDX"),
       _t("Mostra no mapa as estações ouvidas pelo WSJT-X e pelo JTDX e avisa dos contactos que faltam para os "
          "diplomas. Precisa de Internet (mapas e spots) e actualiza-se sozinho.",
          "Shows on a map the stations heard by WSJT-X and JTDX and points out the contacts still missing for awards. "
          "It needs the Internet (maps and spots) and updates itself.",
          "Muestra en el mapa las estaciones oídas por WSJT-X y JTDX y avisa de los contactos que faltan para los "
          "diplomas. Necesita Internet (mapas y spots) y se actualiza solo.",
          "Affiche sur une carte les stations entendues par WSJT-X et JTDX et signale les contacts qui manquent pour "
          "les diplômes. Il a besoin d'Internet (cartes et spots) et se met à jour tout seul."),
       "https://gridtracker.org", pacote="gridtracker2",
       # The newest .deb listed on the official downloads page (over HTTPS; no checksum is published there, so its
       # SHA-256 goes to the details). A fixed address broke: the server keeps only the current version (22/11/2026:
       # 2.261019.5, the one in the 0.9.0 image, answered 404; 2.261117.7 was listed)
       pagina="https://gridtracker.org/index.php/downloads/gridtracker-downloads",
       padrao=r"https://download2\.gridtracker\.org/GridTracker2-([0-9.]+)-amd64\.deb", comando="gridtracker2",
       a_pedido=True),
    _p("waveloggate", "WaveLogGate", "logs", "github",
       _t("Envia os QSOs e a frequência do rádio para o Wavelog",
          "Sends the QSOs and the radio frequency to Wavelog",
          "Envía los QSO y la frecuencia de la radio a Wavelog",
          "Envoie les QSO et la fréquence de la radio à Wavelog"),
       _t("Ponte entre os programas da estação e o Wavelog: os contactos e a frequência do rádio chegam ao log na "
          "Internet sem os escrever outra vez.",
          "A bridge between the station programs and Wavelog: contacts and the radio frequency reach the online log "
          "without typing them again.",
          "Puente entre los programas de la estación y Wavelog: los contactos y la frecuencia de la radio llegan al "
          "libro en Internet sin volver a escribirlos.",
          "Pont entre les logiciels de la station et Wavelog : les contacts et la fréquence de la radio arrivent au "
          "carnet en ligne sans les saisir à nouveau."),
       "https://github.com/wavelog/WaveLogGate", github="waveloggate", lancadores=["wavelog-gate"],
       comando="wavelog-gate"),
    _p("uplink", "LogBeam Uplink", "logs", "apt",
       _t("Envia os QSOs para o LogBeam em tempo real", "Sends the QSOs to LogBeam in real time",
          "Envía los QSO a LogBeam en tiempo real", "Envoie les QSO à LogBeam en temps réel"),
       _t("Recebe os contactos do WSJT-X, do N1MM+, do Log4OM e de outros programas e envia-os para o seu log no "
          "logbeam.org, onde aparecem no mapa 3D.",
          "Receives the contacts of WSJT-X, N1MM+, Log4OM and other programs and sends them to your log on "
          "logbeam.org, where they show on the 3D map.",
          "Recibe los contactos de WSJT-X, N1MM+, Log4OM y otros programas y los envía a su libro en logbeam.org, "
          "donde aparecen en el mapa 3D.",
          "Reçoit les contacts de WSJT-X, N1MM+, Log4OM et d'autres logiciels et les envoie vers votre carnet sur "
          "logbeam.org, où ils apparaissent sur la carte 3D."),
       "https://logbeam.org/uplink/", pacotes=["logbeam-uplink"], lancadores=["logbeam-uplink"],
       comando="logbeam-uplink"),
    _p("tqsl", "TQSL", "logs", "logbeamos",
       _t("Assina os QSOs e envia-os para o LoTW da ARRL", "Signs the QSOs and uploads them to ARRL LoTW",
          "Firma los QSO y los envía a LoTW de la ARRL", "Signe les QSO et les envoie au LoTW de l'ARRL"),
       _t("O programa oficial da ARRL para assinar os contactos e enviá-los para o Logbook of The World. Faz parte do "
          "LogBeamOS.",
          "The official ARRL program to sign contacts and upload them to Logbook of The World. Part of LogBeamOS.",
          "El programa oficial de la ARRL para firmar los contactos y enviarlos a Logbook of The World. Forma parte de "
          "LogBeamOS.",
          "Le logiciel officiel de l'ARRL pour signer les contacts et les envoyer au Logbook of The World. Il fait "
          "partie de LogBeamOS."),
       "https://lotw.arrl.org", pacotes=["logbeamos-tqsl"], comando="tqsl"),
    # --- SDR and spectrum
    _p("sdrpp", "SDR++", "sdr", "github",
       _t("Receptor SDR para RTL-SDR, Airspy, HackRF e outros", "SDR receiver for RTL-SDR, Airspy, HackRF and more",
          "Receptor SDR para RTL-SDR, Airspy, HackRF y otros", "Récepteur SDR pour RTL-SDR, Airspy, HackRF et autres"),
       _t("Receptor SDR rápido e leve, com cascata, gravação e muitos receptores suportados. É o receptor SDR do "
          "LogBeamOS para todos.",
          "A fast and light SDR receiver with waterfall, recording and many supported devices. It is the LogBeamOS SDR "
          "receiver for everyone.",
          "Receptor SDR rápido y ligero, con cascada, grabación y muchos receptores compatibles. Es el receptor SDR de "
          "LogBeamOS para todos.",
          "Récepteur SDR rapide et léger, avec chute d'eau, enregistrement et de nombreux récepteurs pris en charge. "
          "C'est le récepteur SDR de LogBeamOS pour tous."),
       "https://www.sdrpp.org", github="sdrpp", comando="sdrpp"),
    _p("gqrx", "Gqrx", "sdr", "apt",
       _t("Receptor SDR com o GNU Radio", "SDR receiver built on GNU Radio", "Receptor SDR con GNU Radio",
          "Récepteur SDR basé sur GNU Radio"),
       _t("Receptor SDR clássico, feito sobre o GNU Radio, com cascata, gravação e controlo remoto pela rede.",
          "A classic SDR receiver built on GNU Radio, with waterfall, recording and remote control over the network.",
          "Receptor SDR clásico, construido sobre GNU Radio, con cascada, grabación y control remoto por la red.",
          "Récepteur SDR classique, construit sur GNU Radio, avec chute d'eau, enregistrement et contrôle à distance "
          "par le réseau."),
       "https://gqrx.dk", pacotes=["gqrx-sdr"], lancadores=["dk.gqrx.gqrx"], comando="gqrx", a_pedido=True),
    _p("gnuradio", "GNU Radio", "sdr", "apt",
       _t("Ferramentas para construir rádios por software", "Toolkit to build software radios",
          "Herramientas para construir radios por software", "Outils pour construire des radios logicielles"),
       _t("O GNU Radio Companion desenha, em blocos, receptores, transmissores e análises de sinal. Para quem "
          "desenvolve e experimenta.",
          "GNU Radio Companion designs receivers, transmitters and signal analysis in blocks. For those who develop and "
          "experiment.",
          "GNU Radio Companion diseña, en bloques, receptores, transmisores y análisis de señal. Para quien desarrolla "
          "y experimenta.",
          "GNU Radio Companion conçoit, par blocs, des récepteurs, des émetteurs et des analyses de signal. Pour ceux "
          "qui développent et expérimentent."),
       "https://www.gnuradio.org", pacotes=["gnuradio"], lancadores=["gnuradio-grc"], comando="gnuradio-companion",
       a_pedido=True),
    _p("4ham", "4ham Spectrum Analysis", "sdr", "github",
       _t("Análise de espectro e análises académicas do espectro radioeléctrico",
          "Spectrum analysis and academic studies of the radio spectrum",
          "Análisis de espectro y análisis académicos del espectro radioeléctrico",
          "Analyse de spectre et études académiques du spectre radioélectrique"),
       _t("Analisa o espectro com receptores SDR, guarda as medições e mostra-as num painel no navegador. Os dados e "
          "as definições ficam quando se actualiza.",
          "Analyses the spectrum with SDR receivers, keeps the measurements and shows them on a dashboard in the "
          "browser. Data and settings are kept on updates.",
          "Analiza el espectro con receptores SDR, guarda las mediciones y las muestra en un panel en el navegador. Los "
          "datos y la configuración se conservan al actualizar.",
          "Analyse le spectre avec des récepteurs SDR, garde les mesures et les affiche dans un tableau de bord dans le "
          "navigateur. Les données et les réglages sont conservés lors des mises à jour."),
       "https://github.com/octaviofilipepereira/4ham-spectrum-analysis", github="4ham", comando="4ham"),
    # --- Satellites
    _p("satdump", "SatDump", "satelites", "github",
       _t("Imagens dos satélites meteorológicos", "Weather satellite pictures", "Imágenes de satélites meteorológicos",
          "Images des satellites météorologiques"),
       _t("Recebe e descodifica as transmissões dos satélites meteorológicos (NOAA, Meteor, Metop e outros) e faz as "
          "imagens.",
          "Receives and decodes weather satellite transmissions (NOAA, Meteor, Metop and others) and makes the "
          "pictures.",
          "Recibe y decodifica las transmisiones de los satélites meteorológicos (NOAA, Meteor, Metop y otros) y "
          "genera las imágenes.",
          "Reçoit et décode les transmissions des satellites météorologiques (NOAA, Meteor, Metop et autres) et en "
          "fait des images."),
       "https://www.satdump.org", github="satdump", comando="satdump-ui", a_pedido=True),
    _p("gpredict", "Gpredict", "satelites", "apt",
       _t("Passagens de satélites e controlo do rotor", "Satellite passes and rotator control",
          "Pasos de satélites y control del rotor", "Passages des satellites et contrôle du rotor"),
       _t("Mostra onde estão os satélites, prevê as passagens e corrige o Doppler e o rotor durante a passagem. "
          "Traz os satélites de radioamador já organizados por grupos.",
          "Shows where the satellites are, predicts passes and corrects Doppler and the rotator during a pass. The "
          "amateur radio satellites come already sorted in groups.",
          "Muestra dónde están los satélites, predice los pasos y corrige el Doppler y el rotor durante el paso. Trae "
          "los satélites de radioaficionado ya organizados en grupos.",
          "Montre où sont les satellites, prévoit les passages et corrige le Doppler et le rotor pendant le passage. "
          "Les satellites radioamateurs sont déjà classés par groupes."),
       "https://oz9aec.dk/gpredict/", pacotes=["gpredict"], comando="gpredict"),
    # --- APRS, packet and Winlink
    _p("direwolf", "Dire Wolf", "aprs", "apt",
       _t("TNC por software para APRS e pacote", "Software TNC for APRS and packet",
          "TNC por software para APRS y paquetes", "TNC logiciel pour l'APRS et le paquet"),
       _t("Modem e TNC por software para APRS e pacote AX.25, com digipeater e IGate. O LogBeamOS cria a "
          "configuração na primeira vez.",
          "A software modem and TNC for APRS and AX.25 packet, with digipeater and IGate. LogBeamOS creates the "
          "configuration the first time.",
          "Módem y TNC por software para APRS y paquetes AX.25, con digipetidor e IGate. LogBeamOS crea la "
          "configuración la primera vez.",
          "Modem et TNC logiciel pour l'APRS et le paquet AX.25, avec digipeater et IGate. LogBeamOS crée la "
          "configuration la première fois."),
       "https://github.com/wb2osz/direwolf", pacotes=["direwolf"], comando="x-terminal-emulator -e logbeamos-direwolf"),
    _p("xastir", "Xastir", "aprs", "apt",
       _t("Mapa APRS", "APRS map", "Mapa APRS", "Carte APRS"),
       _t("Mostra no mapa as estações APRS e envia a sua posição e mensagens. No LogBeamOS abre ligado ao Dire Wolf.",
          "Shows APRS stations on a map and sends your position and messages. On LogBeamOS it opens connected to Dire "
          "Wolf.",
          "Muestra en el mapa las estaciones APRS y envía su posición y mensajes. En LogBeamOS se abre conectado a Dire "
          "Wolf.",
          "Affiche les stations APRS sur une carte et envoie votre position et vos messages. Sous LogBeamOS il s'ouvre "
          "relié à Dire Wolf."),
       "https://xastir.org", pacotes=["xastir"], comando="logbeamos-xastir"),
    _p("pat", "Pat (Winlink)", "aprs", "github",
       _t("Correio Winlink por rádio", "Winlink e-mail over radio", "Correo Winlink por radio",
          "Courrier Winlink par radio"),
       _t("Cliente Winlink para enviar e receber correio por rádio (pacote, ARDOP, VARA) ou pela Internet, com a "
          "interface no navegador.",
          "A Winlink client to send and receive e-mail over radio (packet, ARDOP, VARA) or the Internet, with its "
          "interface in the browser.",
          "Cliente Winlink para enviar y recibir correo por radio (paquetes, ARDOP, VARA) o por Internet, con la "
          "interfaz en el navegador.",
          "Client Winlink pour envoyer et recevoir du courrier par radio (paquet, ARDOP, VARA) ou par Internet, avec "
          "l'interface dans le navigateur."),
       "https://getpat.io", github="pat", comando="pat-web"),
    # --- Digital voice and linking
    _p("qdmr", "qdmr", "voz", "github",
       _t("Programação de rádios DMR (codeplugs)", "Programming DMR radios (codeplugs)",
          "Programación de radios DMR (codeplugs)", "Programmation des radios DMR (codeplugs)"),
       _t("Prepara e grava os codeplugs de vários rádios DMR (Anytone, Radioddity, TYT, Baofeng e outros), com "
          "listas de contactos e de repetidores.",
          "Prepares and writes the codeplugs of many DMR radios (Anytone, Radioddity, TYT, Baofeng and others), with "
          "contact and repeater lists.",
          "Prepara y graba los codeplugs de varias radios DMR (Anytone, Radioddity, TYT, Baofeng y otras), con listas "
          "de contactos y de repetidores.",
          "Prépare et écrit les codeplugs de nombreuses radios DMR (Anytone, Radioddity, TYT, Baofeng et autres), avec "
          "les listes de contacts et de relais."),
       "https://dm3mat.darc.de/qdmr/", github="qdmr", comando="qdmr", a_pedido=True),
    _p("voxdmr", "VoxDMR", "voz", "github",
       _t("Grupos DMR do BrandMeister sem rádio", "DMR talkgroups on BrandMeister without a radio",
          "Grupos DMR de BrandMeister sin radio", "Groupes DMR de BrandMeister sans radio"),
       _t("Ouve e fala nos grupos DMR do BrandMeister pelo computador, sem rádio. Feito por CT7BLE; gratuito, mas sem "
          "licença declarada, por isso não vem na imagem.",
          "Listens and talks on BrandMeister DMR talkgroups from the computer, without a radio. Made by CT7BLE; free "
          "of charge but without a declared licence, so it is not in the image.",
          "Escucha y habla en los grupos DMR de BrandMeister desde el ordenador, sin radio. Hecho por CT7BLE; gratuito "
          "pero sin licencia declarada, por eso no viene en la imagen.",
          "Écoute et parle dans les groupes DMR de BrandMeister depuis l'ordinateur, sans radio. Réalisé par CT7BLE ; "
          "gratuit mais sans licence déclarée, il n'est donc pas dans l'image."),
       "https://voxdmr.com", github="voxdmr", comando="voxdmr", a_pedido=True),
    _p("wiresx", "WIRES-X", "voz", "wine",
       _t("Nó WIRES-X da Yaesu (Windows, pelo Wine)", "Yaesu WIRES-X node (Windows, through Wine)",
          "Nodo WIRES-X de Yaesu (Windows, mediante Wine)", "Nœud WIRES-X de Yaesu (Windows, via Wine)"),
       _t("Nó WIRES-X com a HRI-200 ou com um rádio em modo PDN. A Yaesu exige o ID de cada um para descarregar o "
          "programa: o lançador pede o ficheiro descarregado e instala-o no Wine.",
          "A WIRES-X node with the HRI-200 or a radio in PDN mode. Yaesu requires each user's ID to download the "
          "program: the launcher asks for the downloaded file and installs it into Wine.",
          "Nodo WIRES-X con la HRI-200 o con una radio en modo PDN. Yaesu exige el ID de cada uno para descargar el "
          "programa: el lanzador pide el archivo descargado y lo instala en Wine.",
          "Nœud WIRES-X avec la HRI-200 ou une radio en mode PDN. Yaesu exige l'identifiant de chacun pour télécharger "
          "le logiciel : le lanceur demande le fichier téléchargé et l'installe dans Wine."),
       "https://www.yaesu.com", lancadores=["wires-x"], comando="wires-x"),
    _p("freedv", "FreeDV", "voz", "apt",
       _t("Voz digital em HF", "Digital voice on HF", "Voz digital en HF", "Voix numérique en HF"),
       _t("Voz digital aberta para HF e VHF, com a placa de som e um rádio SSB normal.",
          "Open digital voice for HF and VHF, with the sound card and an ordinary SSB radio.",
          "Voz digital abierta para HF y VHF, con la tarjeta de sonido y una radio SSB normal.",
          "Voix numérique ouverte pour la HF et la VHF, avec la carte son et une radio BLU ordinaire."),
       "https://freedv.org", pacotes=["freedv"], comando="freedv"),
    _p("qtel", "Qtel (EchoLink)", "voz", "apt",
       _t("Cliente EchoLink", "EchoLink client", "Cliente EchoLink", "Client EchoLink"),
       _t("Liga-se a estações, repetidores e conferências EchoLink pela Internet.",
          "Connects to EchoLink stations, repeaters and conferences over the Internet.",
          "Se conecta a estaciones, repetidores y conferencias EchoLink por Internet.",
          "Se connecte aux stations, relais et conférences EchoLink par Internet."),
       "https://www.svxlink.org", pacotes=["qtel"], comando="qtel"),
    # --- Radio control and utilities
    _p("flrig", "Flrig", "radio", "apt",
       _t("Controlo do rádio por CAT", "Radio control through CAT", "Control de la radio por CAT",
          "Contrôle de la radio par CAT"),
       _t("Painel de controlo do rádio pelo cabo CAT (frequência, modo, filtros, potência), partilhado com o Fldigi "
          "e outros programas.",
          "A control panel for the radio through the CAT cable (frequency, mode, filters, power), shared with Fldigi "
          "and other programs.",
          "Panel de control de la radio por el cable CAT (frecuencia, modo, filtros, potencia), compartido con Fldigi "
          "y otros programas.",
          "Panneau de contrôle de la radio par le câble CAT (fréquence, mode, filtres, puissance), partagé avec Fldigi "
          "et d'autres logiciels."),
       "http://www.w1hkj.org", pacotes=["flrig"], comando="flrig"),
    _p("wfview", "wfview", "radio", "github",
       _t("Controlo de rádios Icom e Kenwood", "Control of Icom and Kenwood radios", "Control de radios Icom y Kenwood",
          "Contrôle des radios Icom et Kenwood"),
       _t("Controla os rádios Icom e Kenwood com cascata, áudio e operação remota pela rede.",
          "Controls Icom and Kenwood radios with waterfall, audio and remote operation over the network.",
          "Controla las radios Icom y Kenwood con cascada, audio y operación remota por la red.",
          "Contrôle les radios Icom et Kenwood avec chute d'eau, audio et exploitation à distance par le réseau."),
       "https://wfview.org", github="wfview", comando="wfview", a_pedido=True),
    _p("xnec2c", "xnec2c", "radio", "apt",
       _t("Modelação de antenas", "Antenna modelling", "Modelado de antenas", "Modélisation d'antennes"),
       _t("Calcula o diagrama, o ganho, a impedância e a ROE de antenas a partir de modelos NEC2.",
          "Computes the pattern, gain, impedance and SWR of antennas from NEC2 models.",
          "Calcula el diagrama, la ganancia, la impedancia y la ROE de antenas a partir de modelos NEC2.",
          "Calcule le diagramme, le gain, l'impédance et le ROS d'antennes à partir de modèles NEC2."),
       "https://www.xnec2c.org", pacotes=["xnec2c"], comando="xnec2c"),
]

POR_CHAVE = {p["chave"]: p for p in PROGRAMAS}

# System packages that programs installed outside apt use (and so apt does not know they are needed): marked as
# manually installed before any removal, so that "apt-get autoremove" never takes them with a removed program.
# Measured in the 0.9.0 image tree (22/11/2026): removing Gqrx with GNU Radio would have taken python3-scipy,
# python3-jsonschema and their dependencies, which 4ham imports from the system (its environment uses the system site
# packages), and libiio0/libad9361-0, which SDR++ loads; the rest are the other 4ham modules and their libraries.
PROTEGIDOS = [
    "python3-numpy", "python3-scipy", "python3-matplotlib", "python3-yaml", "python3-jsonschema", "python3-attr",
    "python3-json-pointer", "python3-pyrsistent", "python3-cryptography", "python3-psutil", "python3-soapysdr",
    "libiio0", "libad9361-0", "libpulse0", "libproxy1v5",
]
NOME_PACOTE = re.compile(r"^[a-z0-9][a-z0-9+.\-]+$")


# Approximate space each program takes once installed, with the dependencies that only it uses (measured in the 0.9.0
# image tree, 22/11/2026). Shown before installing; apt programs show the exact figure apt gives when there is one.
TAMANHOS_MB = {
    "qdmr": 2500, "satdump": 423, "not1mm": 396, "gqrx": 330, "gnuradio": 330, "gridtracker2": 319, "decodium": 301,
    "wsjtx": 266, "js8call": 181, "wfview": 115, "uplink": 105, "4ham": 79, "sdrpp": 56, "cqrlog": 51, "klog": 33,
    "tqsl": 31, "voxdmr": 120, "pat": 18, "xastir": 2, "jtdx": 12, "waveloggate": 15, "fldigi": 10, "gpredict": 1,
    "flrig": 6, "flmsg": 3, "xnec2c": 4, "direwolf": 2, "freedv": 3, "qsstv": 2, "flamp": 1, "qtel": 1, "tlf": 1,
}
# The on-demand programs that "Install all" installs (to get a USB drive ready at home before going out without a
# network): the a_pedido ones, without the optional VoxDMR (no declared licence) and without WIRES-X (Yaesu file)
INSTALAR_TUDO = [p["chave"] for p in PROGRAMAS if p["a_pedido"] and p["chave"] not in ("voxdmr", "wiresx")]

MODELOS = "/usr/share/logbeamos/programas/lancadores"   # launcher templates kept by the package
WINE_MODELO = "/opt/ham/wine"
WINE_PROGRAMAS = {
    # program: (folder in "Program Files (x86)", executable, name in the Windows uninstall list, quiet uninstall)
    "n1mm": ("N1MM Logger+", "N1MMLogger.net.exe", "N1MM Logger+", ["Uninstall.exe", "/S"]),
    "log4om": ("IW3HMH/Log4OM NextGen", "L4ONG.exe", "Log4OM", ["unins000.exe", "/VERYSILENT", "/SUPPRESSMSGBOXES",
                                                                "/NORESTART"]),
    "wiresx": ("YAESUMUSEN/WIRES-X", "Wires-X.exe", "WIRES-X", None),
}
# Where each Windows installer comes from (the user downloads it: the sites need a click, and Yaesu a login), and the
# options that install it without questions
WINE_INSTALADORES = {
    "n1mm": ("https://n1mmwp.hamdocs.com/mmfiles/", ["/S"]),
    "log4om": ("https://www.log4om.com/l4ong/", ["/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/SP-"]),
}


def lingua():
    return (os.environ.get("LANGUAGE") or os.environ.get("LANG") or "en")[:2]


def texto(d, ling=None):
    """The text of a {pt, en, es, fr} dictionary in the session language (English for any other language)."""
    return d.get(ling or lingua()) or d["en"]


def icone(p):
    """The icon copy of a program, kept by the LogBeamOS Update package so that it shows while not installed."""
    caminho = os.path.join(ICONES, p["chave"] + ".png")
    return caminho if os.path.exists(caminho) else "/usr/share/logbeamos/logbeam.png"


def _gh(p):
    """The lb_actualizar.GITHUB item of a "github" program."""
    import lb_actualizar as lb
    return {g[0]: g for g in lb.GITHUB}[p["github"]]


def pacotes_estado(nomes):
    """{package: version} of the installed ones among nomes (one dpkg-query for all of them)."""
    if not nomes:
        return {}
    r = subprocess.run(["dpkg-query", "-W", "-f=${Package} ${db:Status-Abbrev} ${Version}\n", *nomes],
                       capture_output=True, text=True)
    d = {}
    for l in r.stdout.splitlines():
        partes = l.split()
        if len(partes) >= 3 and partes[1][1:2] == "i":   # ii, hi (held, like Wine)
            d[partes[0]] = partes[2]
    return d


def pacotes_de(p):
    """The apt packages a program is made of (empty for the other kinds)."""
    if p["tipo"] in ("apt", "logbeamos"):
        return list(p.get("pacotes", []))
    if p["tipo"] == "deb":
        return [p["pacote"]]
    if p["tipo"] == "github" and _gh(p)[5] == "deb":
        return [_gh(p)[6]]
    return []


def prefixo_wine():
    """The Wine prefix of this user, as wine-env.sh chooses it: the owner of /opt/ham/wine uses it, the others get
    their own copy the first time (until then the model tells what they will get)."""
    try:
        if os.stat(WINE_MODELO).st_uid == os.getuid():
            return WINE_MODELO
    except OSError:
        return WINE_MODELO
    proprio = os.path.expanduser("~/.local/share/logbeamos/wine")
    return proprio if os.path.isdir(os.path.join(proprio, "drive_c")) else WINE_MODELO


def wine_exe(chave, prefixo=None):
    pasta, exe, _, _ = WINE_PROGRAMAS[chave]
    return os.path.join(prefixo or prefixo_wine(), "drive_c", "Program Files (x86)", pasta, exe)


def instalado(p, estado_pacotes=None):
    """Is the program installed? estado_pacotes: the result of pacotes_estado for many programs at once."""
    t = p["tipo"]
    pac = pacotes_de(p)
    if pac:
        est = estado_pacotes if estado_pacotes is not None else pacotes_estado(pac)
        return all(x in est for x in pac)
    if t == "github":
        _, _, _, _, _, tipo, alvo = _gh(p)
        if tipo in ("appimage", "makeself"):
            return os.path.isfile(os.path.join(alvo, "AppRun"))
        if tipo == "flatpak":
            import lb_actualizar as lb
            return lb.flatpak_instalado(alvo)
        if tipo == "fonte":
            return os.path.isdir(os.path.join(alvo, "backend"))
    if t == "pipx":
        return os.path.exists("/opt/pipx/venvs/not1mm/bin/python")
    if t == "wine":
        return os.path.isfile(wine_exe(p["chave"]))
    return False


def versao(p, estado_pacotes=None):
    """The installed version to show ("" when it is not known or not installed)."""
    import lb_actualizar as lb
    pac = pacotes_de(p)
    if pac:
        est = estado_pacotes if estado_pacotes is not None else pacotes_estado(pac)
        v = est.get(pac[0], "")
        return v.split(":")[-1].split("-")[0].split("+")[0].split("~")[0]
    if p["tipo"] == "github":
        return lb.instalada_github(_gh(p)) if instalado(p) else ""
    if p["tipo"] == "pipx":
        return lb.versao_not1mm()
    if p["tipo"] == "wine" and instalado(p):
        return versao_wine(p["chave"])
    return ""


def versao_wine(chave, prefixo=None):
    """DisplayVersion of the program in the Windows uninstall list of the prefix ("" if not there)."""
    nome = WINE_PROGRAMAS[chave][2]
    try:
        with open(os.path.join(prefixo or prefixo_wine(), "system.reg"), encoding="utf-8", errors="replace") as f:
            bloco = ""
            for l in list(f) + ["["]:
                if l.startswith("["):
                    if f'"DisplayName"="{nome}' in bloco:
                        m = re.search(r'"DisplayVersion"="([^"]+)"', bloco)
                        if m:
                            return m.group(1)
                    bloco = ""
                bloco += l
    except OSError:
        pass
    return ""


def chave_desinstalar(chave, prefixo=None):
    """The key of the program in the Windows uninstall list of the prefix (an MSI product code such as {…}), for
    "wine uninstaller --remove" ("" if not there)."""
    nome = WINE_PROGRAMAS[chave][2]
    try:
        with open(os.path.join(prefixo or prefixo_wine(), "system.reg"), encoding="utf-8", errors="replace") as f:
            atual = ""
            for l in f:
                m = re.match(r"^\[Software\\\\(?:Wow6432Node\\\\)?Microsoft\\\\Windows\\\\CurrentVersion\\\\Uninstall\\\\([^\]]+)\]", l)
                if m:
                    atual = m.group(1)
                elif l.startswith("["):
                    atual = ""
                elif atual and l.startswith(f'"DisplayName"="{nome}'):
                    return atual
    except OSError:
        pass
    return ""


def por_lancador(caminho):
    """The catalogue program a menu launcher (.desktop path, with or without .desktop) belongs to, or None."""
    ident = os.path.basename(caminho)
    if ident.endswith(".desktop"):
        ident = ident[:-len(".desktop")]
    for p in PROGRAMAS:
        if ident in p["lancadores"]:
            return p
    return None


def a_pedido_por_instalar(chaves=None):
    """The programs of "Install all" that are not installed yet."""
    return [k for k in (chaves or INSTALAR_TUDO) if not instalado(POR_CHAVE[k])]


# --- Launchers (as root, by the helper): a program removed through the manager takes its menu entry and its icon in
# the radio programs folder of every user with it; one installed again gets them back. The on-demand ones always stay
# (their launcher asks to install, logbeamos-abrir).
def pastas_radio():
    """(folder, user, group) of the radio programs folder of each user and of /etc/skel. The folder is found by its
    marker file, because its name follows the session language."""
    import glob
    import grp
    import pwd
    lista = []
    for m in glob.glob("/home/*/*/*/.logbeamos-radio") + glob.glob("/etc/skel/*/*/.logbeamos-radio"):
        d = os.path.dirname(m)
        st = os.stat(d)
        try:
            u, g = pwd.getpwuid(st.st_uid).pw_name, grp.getgrgid(st.st_gid).gr_name
        except KeyError:
            continue
        lista.append((d, u, g))
    return lista


def poe_lancadores(p, registo=print):
    import shutil
    for ident in p["lancadores"]:
        modelo = os.path.join(MODELOS, ident + ".desktop")
        if not os.path.isfile(modelo):
            continue
        destino = os.path.join(APLICACOES, ident + ".desktop")
        if not os.path.exists(destino):
            shutil.copyfile(modelo, destino)
            os.chmod(destino, 0o644)
        for d, u, g in pastas_radio():
            f = os.path.join(d, ident + ".desktop")
            if not os.path.exists(f):
                shutil.copyfile(modelo, f)
                os.chmod(f, 0o755)
                shutil.chown(f, u, g)
    subprocess.run(["update-desktop-database", "-q", APLICACOES], capture_output=True)
    registo(f"launchers in place: {', '.join(p['lancadores']) or '-'}")


def tira_lancadores(p, registo=print):
    if p["a_pedido"]:
        return   # stays: it asks to install again
    for ident in p["lancadores"]:
        for f in [os.path.join(APLICACOES, ident + ".desktop")] + \
                 [os.path.join(d, ident + ".desktop") for d, _, _ in pastas_radio()]:
            try:
                os.remove(f)
            except FileNotFoundError:
                pass
    subprocess.run(["update-desktop-database", "-q", APLICACOES], capture_output=True)
    registo(f"launchers removed: {', '.join(p['lancadores']) or '-'}")


# --- Installation and removal of what is not apt (as root, by the helper; apt is done by the helper itself)
def descarrega_deb(p, pasta, registo):
    """The newest .deb listed on the program's official downloads page (GridTracker2): the file, for apt to install.
    It must be the package of the program (dpkg-deb), and its SHA-256 goes to the details."""
    import urllib.request
    import lb_actualizar as lb
    pedido = urllib.request.Request(p["pagina"], headers={"User-Agent": lb.AGENTE})
    with urllib.request.urlopen(pedido, timeout=30) as r:
        html = r.read().decode("utf-8", "replace")
    achados = {m.group(0): m.group(1) for m in re.finditer(p["padrao"], html)}
    if not achados:
        raise RuntimeError(f"no package found on {p['pagina']}")
    url = max(achados, key=lambda u: lb.numeros(achados[u]))
    f = lb.descarrega({"name": os.path.basename(url), "browser_download_url": url}, pasta, registo)
    r = subprocess.run(["dpkg-deb", "-f", f, "Package"], capture_output=True, text=True)
    if r.stdout.strip() != p["pacote"]:
        raise RuntimeError(f"{os.path.basename(url)} is not the {p['pacote']} package")
    os.chmod(pasta, 0o755)
    os.chmod(f, 0o644)
    return f


def instala_not1mm(registo):
    import lb_actualizar as lb
    env = dict(os.environ, **lb.PIPX)
    lb.corre_registo(["pipx", "install", "not1mm"], registo, env=env)
    lb.corre_registo(["python3", "-I", lb.AJUSTES_NOT1MM], registo)
    lb.corre_registo(["/opt/pipx/venvs/not1mm/bin/python", "-m", "compileall", "-q", "/opt/pipx/venvs/not1mm/lib"],
                     registo)
    subprocess.run(["chmod", "-R", "a+rX", "/opt/pipx"], check=True)
    return lb.versao_not1mm()


ENV_4HAM = """# LogBeamOS: only this computer can reach it (for the local network: APP_HOST=0.0.0.0, after creating the account
# in the Admin panel)
APP_HOST=127.0.0.1
APP_PORT=8000
FT_EXTERNAL_ENABLE=1
FT_EXTERNAL_MODES=FT8,FT4
FT_EXTERNAL_COMMAND=/opt/ham/wsjtx/usr/bin/jt9 {mode_flag} -p {period_int} -d 3 -a . -t . {wav_path}
FT_EXTERNAL_COMMAND_WSPR=/opt/ham/wsjtx/usr/bin/wsprd -d -f {frequency_mhz} {wav_path}
DIREWOLF_KISS_ENABLE=0
DIREWOLF_AUTOSTART=0
"""


def instala_4ham_novo(registo, uid, gid):
    """4ham where there is none (it was removed through the manager): what the image build does (script 47d), for the
    user who asked. The launcher, the user service and the command stay in the system when 4ham is removed."""
    import shutil
    import tarfile
    import tempfile
    import lb_actualizar as lb
    item = {g[0]: g for g in lb.GITHUB}["4ham"]
    alvo = item[6]
    versao_nova, asset = lb.info_github(item)
    with tempfile.TemporaryDirectory(prefix="lb-programas-") as pasta:
        f = lb.descarrega(asset, pasta, registo)
        x = os.path.join(pasta, "fonte")
        os.makedirs(x)
        with tarfile.open(f) as t:
            t.extractall(x, filter="data")
        pastas = [e.path for e in os.scandir(x) if e.is_dir()]
        if len(pastas) != 1 or not os.path.isfile(os.path.join(pastas[0], "backend", "requirements.txt")):
            raise RuntimeError("4ham archive with an unexpected layout")
        shutil.rmtree(alvo, ignore_errors=True)
        shutil.copytree(pastas[0], alvo, symlinks=True)
    with open(os.path.join(alvo, ".env"), "w", encoding="utf-8") as f:
        f.write(ENV_4HAM)
    lb.corre_registo(["python3", "-m", "venv", "--system-site-packages", os.path.join(alvo, ".venv")], registo)
    py = os.path.join(alvo, ".venv", "bin", "python")
    lb.corre_registo([py, "-m", "pip", "install", "-q", "--no-cache-dir", "--disable-pip-version-check", "-r",
                      os.path.join(alvo, "backend", "requirements.txt")], registo)
    lb.corre_registo([py, "-m", "compileall", "-q", os.path.join(alvo, "backend")], registo)
    subprocess.run(["chown", "-R", f"{uid}:{gid}", alvo], check=True)
    lb.grava_estado("4ham", versao_nova)
    return versao_nova


def remove_not1mm(registo):
    import lb_actualizar as lb
    lb.corre_registo(["pipx", "uninstall", "not1mm"], registo, env=dict(os.environ, **lb.PIPX))


def remove_github(p, registo):
    """Removes a GitHub program that is not a .deb (the .deb ones go through apt): AppImage and makeself folders, the
    flatpak with its platform when nothing else uses it, the 4ham code (its data are kept aside)."""
    import shutil
    import time
    import lb_actualizar as lb
    _, _, _, _, _, tipo, alvo = _gh(p)
    if tipo in ("appimage", "makeself"):
        shutil.rmtree(alvo)
    elif tipo == "flatpak":
        # on the pen flatpak fails to move the folders of the image away: lb_actualizar.flatpak_desinstala handles it
        lb.flatpak_desinstala(alvo, registo)
        lb.flatpak_desinstala(None, registo, nao_usados=True)
        try:
            os.remove(f"/etc/udev/rules.d/60-{alvo.rsplit('.', 1)[-1]}.rules")
            subprocess.run(["udevadm", "control", "--reload-rules"], capture_output=True)
        except FileNotFoundError:
            pass
    elif tipo == "fonte":
        # 4ham: the code goes; the user's data (database, exports, settings) are kept in /var/lib/logbeamos
        st = os.stat(alvo)
        lb.servico_utilizador(st.st_uid, "stop", lb.SERVICO_4HAM)
        guarda = f"/var/lib/logbeamos/guardado/{p['chave']}-{time.strftime('%Y%m%d-%H%M%S')}"
        os.makedirs(guarda)
        for x in ("data", "logs", ".env", "config"):
            if os.path.exists(os.path.join(alvo, x)):
                shutil.move(os.path.join(alvo, x), os.path.join(guarda, x))
        shutil.rmtree(alvo)
        registo(f"4ham: data and settings kept in {guarda}")
    d = lb.estado()
    if p["github"] in d:
        del d[p["github"]]
        with open(lb.ESTADO + ".novo", "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
        os.replace(lb.ESTADO + ".novo", lb.ESTADO)
