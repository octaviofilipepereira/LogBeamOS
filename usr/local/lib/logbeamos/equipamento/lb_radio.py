# Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
# © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
# Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
# LogBeamOS: "Configurar" do "Rádio e Equipamento".
# O rádio fica num só sítio: o rigctld (Hamlib), como serviço do utilizador, em 127.0.0.1:4532. O WSJT-X, o JTDX,
# o Fldigi, o Not1MM e o Direwolf ligam-se a ele ao mesmo tempo ("Hamlib NET rigctl").
# N1MM+ and Log4OM (Windows programs, through Wine) use the radio the way the user chooses, each one on its own: alone
# (the program opens the radio port and the sharing stops while it is open) or shared with the others (0.3.22; see
# "N1MM+ and Log4OM" below).
# RTS e DTR ficam desligados na porta do rádio (nenhum cabo transmite por engano; o RTS fica com o controlo de fluxo
# nos rádios que o usam, ver opcoes_serie); o PTT é por CAT.
# Antes de alterar a configuração de um programa, guarda-se uma cópia (*.antes-logbeamos).
import glob
import json
import os
import re
import shutil
import subprocess
import time

CASA = os.path.expanduser("~")
CONF = os.path.join(CASA, ".config", "logbeamos", "radio.json")
SERVICO = "logbeamos-rigctld.service"
UNIDADE = os.path.join(CASA, ".config", "systemd", "user", SERVICO)
ENDERECO = "127.0.0.1:4532"
RIG_REDE = 2              # "Hamlib NET rigctl"
NOME_REDE = "Hamlib NET rigctl"

# Programas que ficam ligados à partilha: chave, nome, processo (para saber se está aberto)
# (o processo do Decodium chama-se AppRun.decodium-real; o "ps" mostra só os primeiros 15 caracteres)
PROGRAMAS = [("wsjtx", "WSJT-X", "wsjtx"), ("jtdx", "JTDX", "jtdx"), ("decodium", "Decodium", "AppRun.decodiu"),
             ("fldigi", "Fldigi", "fldigi"), ("not1mm", "Not1MM", "not1mm"), ("direwolf", "Direwolf", "direwolf")]
# Velocidades do CAT, pela ordem em que se experimentam quando a velocidade é automática
VELOCIDADES = [38400, 19200, 9600, 4800, 57600, 115200]


# --- Rádio e porta
def porta_fixa(dev):
    """/dev/ttyUSB0 → /dev/serial/by-id/…: o nome não muda quando se liga o cabo noutra USB."""
    real = os.path.realpath(dev)
    for p in sorted(glob.glob("/dev/serial/by-id/*")):
        if os.path.realpath(p) == real:
            return p
    return dev


def modelos_hamlib():
    """Lista (número, "Fabricante Modelo") de todos os rádios que o Hamlib conhece."""
    r = subprocess.run(["rigctl", "-l"], capture_output=True, text=True)
    lista = []
    for linha in r.stdout.splitlines()[1:]:
        m = re.match(r"\s*(\d+)\s{2,}(\S.*?)\s{2,}(\S.*?)\s{2,}", linha)
        if m:
            lista.append((int(m.group(1)), f"{m.group(2).strip()} {m.group(3).strip()}"))
    return lista


def nome_hamlib(numero):
    for n, nome in modelos_hamlib():
        if n == numero:
            return nome
    return str(numero)


_SERIE = {}


def opcoes_serie(modelo):
    """RTS e DTR desligados para nenhum cabo transmitir por engano. Excepto o RTS nos rádios em que o Hamlib usa
    controlo de fluxo por hardware (CTS/RTS, como o FT-991): aí o RTS é do controlo de fluxo e o Hamlib recusa
    abrir o rádio se lhe for imposto um estado."""
    if modelo not in _SERIE:
        r = subprocess.run(["rigctl", "-m", str(modelo), "-u"], capture_output=True, text=True)
        linha = next((l for l in r.stdout.splitlines() if l.startswith("Serial speed")), "")
        _SERIE[modelo] = "CTS/RTS" in linha
    return ["-C", "dtr_state=OFF"] if _SERIE[modelo] else ["-C", "rts_state=OFF", "-C", "dtr_state=OFF"]


def configuracao():
    try:
        with open(CONF, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


# --- Partilha (rigctld)
def systemctl(*args):
    return subprocess.run(["systemctl", "--user", *args], capture_output=True, text=True)


def escreve_servico(modelo, porta, velocidade, nome):
    os.makedirs(os.path.dirname(UNIDADE), exist_ok=True)
    texto = f"""# LogBeamOS: rádio partilhado ({nome}). Escrito pelo "Rádio e Equipamento"; altere-o por lá.
[Unit]
Description=LogBeamOS: rádio partilhado ({nome})
StartLimitIntervalSec=0

[Service]
# Sem o rádio ligado não arranca; tenta de novo a cada 10 segundos
ExecStartPre=/usr/bin/test -e {porta}
ExecStart=/usr/bin/rigctld -m {modelo} -r {porta} -s {velocidade} -T 127.0.0.1 -t 4532 {" ".join(opcoes_serie(modelo))}
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
"""
    with open(UNIDADE, "w", encoding="utf-8") as f:
        f.write(texto)


def _guarda_configuracao(d):
    os.makedirs(os.path.dirname(CONF), exist_ok=True)
    with open(CONF, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)


def liga_partilha(modelo, porta, velocidade):
    """Escreve a configuração e o serviço, e (re)arranca o rigctld."""
    nome = nome_hamlib(modelo)
    porta = porta_fixa(porta)
    d = {"modelo": modelo, "nome": nome, "porta": porta, "velocidade": velocidade}
    d.update(modos())  # the choice made for N1MM+ and Log4OM stays
    _guarda_configuracao(d)
    escreve_servico(modelo, porta, velocidade, nome)
    systemctl("daemon-reload")
    systemctl("enable", SERVICO)
    systemctl("restart", SERVICO)
    return nome, porta


def desliga_partilha():
    desliga_ponte()
    systemctl("disable", "--now", SERVICO)
    for f in (UNIDADE, CONF):
        try:
            os.remove(f)
        except OSError:
            pass
    systemctl("daemon-reload")


def partilha_activa():
    return systemctl("is-active", SERVICO).stdout.strip() == "active"


def frequencia_partilha(espera=12):
    """Lê a frequência através da partilha (o que os programas vão ver). Só leitura."""
    fim = time.time() + espera
    while True:
        try:
            r = subprocess.run(["rigctl", "-m", str(RIG_REDE), "-r", ENDERECO, "f"], capture_output=True, text=True,
                               timeout=6)
            m = re.search(r"^(\d{4,})$", r.stdout, re.M)
            if m and r.returncode == 0:
                return int(m.group(1))
        except subprocess.TimeoutExpired:
            pass
        if time.time() > fim:
            return None
        time.sleep(1)


# --- Som do rádio (nomes do PulseAudio/PipeWire, os que o WSJT-X e o JTDX mostram)
def som_pulse(carta):
    """Devolve (entrada, saída) do som com o número de carta ALSA indicado, ou (None, None)."""
    entrada = saida = None
    for tipo in ("sources", "sinks"):
        r = subprocess.run(["pactl", "-f", "json", "list", tipo], capture_output=True, text=True)
        try:
            lista = json.loads(r.stdout or "[]")
        except ValueError:
            lista = []
        for d in lista:
            prop = d.get("properties", {})
            if str(prop.get("alsa.card", "")) != str(carta) or d.get("name", "").endswith(".monitor"):
                continue
            if tipo == "sources" and not entrada:
                entrada = d["name"]
            elif tipo == "sinks" and not saida:
                saida = d["name"]
    return entrada, saida


# --- Cópia de segurança
def guarda(caminho):
    if os.path.exists(caminho) and not os.path.exists(caminho + ".antes-logbeamos"):
        shutil.copy2(caminho, caminho + ".antes-logbeamos")


def abertos():
    """Programas da lista que estão abertos (gravariam a configuração antiga ao fechar)."""
    r = subprocess.run(["ps", "-eo", "comm="], capture_output=True, text=True)
    nomes = r.stdout.split()
    return [nome for chave, nome, proc in PROGRAMAS if any(n.startswith(proc) for n in nomes)]


# --- WSJT-X e JTDX: QSettings (.ini). Os valores de lista vão em @Variant, como o próprio programa os grava.
def _escapa_ini(texto):
    """Mesmas regras do QSettings (iniEscapedString)."""
    r, a_seguir = [], False
    especiais = {"\a": "\\a", "\b": "\\b", "\f": "\\f", "\n": "\\n", "\r": "\\r", "\t": "\\t", "\v": "\\v",
                 '"': '\\"', "\\": "\\\\"}
    for ch in texto:
        o = ord(ch)
        if a_seguir and ch in "0123456789abcdefABCDEF":
            r.append("\\x%x" % o)
            continue
        a_seguir = False
        if ch == "\0":
            r.append("\\0")
            a_seguir = True
        elif ch in especiais:
            r.append(especiais[ch])
        elif o <= 0x1F or o >= 0x7F:
            r.append("\\x%x" % o)
            a_seguir = True
        else:
            r.append(ch)
    return "".join(r)


def qvariant(tipo, valor):
    """Enumerado do WSJT-X gravado pelo QSettings: tipo do utilizador (127), nome do tipo, valor como texto."""
    def bloco(s):
        b = s.encode("latin-1") + b"\0"
        return len(b).to_bytes(4, "big") + b
    dados = (127).to_bytes(4, "big") + bloco(tipo) + bloco(valor)
    return "@Variant(" + _escapa_ini(dados.decode("latin-1")) + ")"


def altera_ini(caminho, seccao, valores):
    """Altera ou acrescenta chaves numa secção de um .ini do QSettings, sem tocar no resto."""
    linhas = []
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8", errors="surrogateescape") as f:
            linhas = f.read().splitlines()
    cab = f"[{seccao}]"
    if cab not in linhas:
        if linhas and linhas[-1].strip():
            linhas.append("")
        linhas.append(cab)
    i = linhas.index(cab) + 1
    fim = i
    while fim < len(linhas) and not linhas[fim].startswith("["):
        fim += 1
    falta = dict(valores)
    for j in range(i, fim):
        k = linhas[j].split("=", 1)[0]
        if k in falta:
            linhas[j] = f"{k}={falta.pop(k)}"
    pos = fim
    while pos > i and not linhas[pos - 1].strip():
        pos -= 1
    for k, v in falta.items():
        linhas.insert(pos, f"{k}={v}")
        pos += 1
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    guarda(caminho)
    with open(caminho, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write("\n".join(linhas) + "\n")


def configura_wsjt(caminho, entrada=None, saida=None):
    v = {"Rig": NOME_REDE, "CATNetworkPort": ENDERECO,
         "PTTMethod": qvariant("TransceiverFactory::PTTMethod", "PTT_method_CAT"), "Polling": "1"}
    if entrada:
        v["SoundInName"] = entrada
    if saida:
        v["SoundOutName"] = saida
    altera_ini(caminho, "Configuration", v)


# --- Decodium (0.3.11): derivado do WSJT-X, mas com configuração própria em ~/.config/Decodium/Decodium3.ini:
# o rádio na secção [Transceiver] e o "CAT backend" e o som em [General] (visto no próprio ficheiro que o programa grava)
def configura_decodium(caminho, entrada=None, saida=None):
    altera_ini(caminho, "Transceiver", {"rigName": NOME_REDE, "networkPort": ENDERECO, "pttMethod": "CAT",
                                        "pttPort": "CAT", "pollInterval": "1", "catAutoConnect": "true"})
    g = {"catBackend": "hamlib"}
    if entrada:
        g["SoundInName"] = entrada
    if saida:
        g["SoundOutName"] = saida
    altera_ini(caminho, "General", g)


# --- Fldigi: fldigi_def.xml
def configura_fldigi(caminho):
    valores = {"CHKUSEHAMLIBIS": "1", "CHKUSERIGCATIS": "0", "CHKUSEXMLRPCIS": "0", "HAMRIGMODEL": str(RIG_REDE),
               "HAMRIGNAME": "NET rigctl (Hamlib)", "HAMRIGDEVICE": ENDERECO, "HAMLIBCMDPTT": "1"}
    texto = ""
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8", errors="surrogateescape") as f:
            texto = f.read()
    if "<FLDIGI_DEFS>" not in texto:
        texto = '<?xml version="1.0" encoding="UTF-8"?>\n<FLDIGI_DEFS>\n</FLDIGI_DEFS>\n'
    for k, v in valores.items():
        novo = f"<{k}>{v}</{k}>"
        texto, n = re.subn(rf"<{k}>.*?</{k}>", lambda _m: novo, texto, flags=re.S)
        if not n:
            texto = texto.replace("</FLDIGI_DEFS>", novo + "\n</FLDIGI_DEFS>")
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    guarda(caminho)
    with open(caminho, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(texto)


# --- Not1MM: preferências em JSON
def configura_not1mm(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError):
        d = {}
    d.update({"userigctld": True, "useflrig": False, "CAT_ip": "127.0.0.1", "CAT_port": 4532})
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    guarda(caminho)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=4)


# --- Direwolf: ~/direwolf.conf (o Direwolf procura-a na pasta pessoal). Sem ela, o Direwolf fecha-se logo ao abrir.
EXEMPLO_DIREWOLF = "/usr/share/doc/direwolf/conf/direwolf.conf.gz"
CABECALHO_DIREWOLF = """\
# LogBeamOS: Direwolf configuration, made from Direwolf's own example.
# "Radio and Equipment" > "Set up the programs..." writes the radio sound (ADEVICE) and PTT by shared CAT here.
# Before transmitting, change MYCALL to your callsign.
# LogBeamOS: configuração do Direwolf, feita a partir do exemplo do próprio Direwolf.
# O "Rádio e Equipamento" > "Configurar os programas..." escreve aqui o som do rádio (ADEVICE) e o PTT pelo CAT.
# Antes de transmitir, mude o MYCALL para o seu indicativo.

"""


def direwolf_base(caminho):
    """Cria a configuração do Direwolf a partir do exemplo, se ainda não existir. Devolve True se a criou."""
    if os.path.exists(caminho):
        return False
    import gzip
    with gzip.open(EXEMPLO_DIREWOLF, "rt", encoding="utf-8", errors="replace") as f:
        texto = f.read()
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(CABECALHO_DIREWOLF + texto)
    return True


def _activa(linha, chave):
    """A linha (não comentada) começa pela palavra-chave do Direwolf indicada (ADEVICE também apanha ADEVICE0)."""
    p = linha.split()
    return bool(p) and (p[0].upper() == chave or (chave == "ADEVICE" and p[0].upper() == "ADEVICE0"))


# Som do rádio com um nome curto no ALSA: o Direwolf corta os nomes de dispositivo aos 30 caracteres, e os do
# PipeWire são muito maiores. O bloco vai para ~/.config/alsa/asoundrc (lido pelo ALSA a seguir ao ~/.asoundrc),
# entre marcas, sem tocar no resto do ficheiro.
ALSA_UTILIZADOR = os.path.join(CASA, ".config", "alsa", "asoundrc")
ALSA_NOME = "logbeamos-radio"
_ALSA_INICIO = "# >>> LogBeamOS: radio sound / som do rádio (Rádio e Equipamento) >>>"
_ALSA_FIM = "# <<< LogBeamOS <<<"


def som_alsa(entrada, saida):
    """Escreve (ou troca) o dispositivo ALSA "logbeamos-radio": entrada e saída do rádio no PipeWire."""
    texto = ""
    if os.path.exists(ALSA_UTILIZADOR):
        with open(ALSA_UTILIZADOR, encoding="utf-8", errors="surrogateescape") as f:
            texto = f.read()
        guarda(ALSA_UTILIZADOR)
    texto = re.sub(re.escape(_ALSA_INICIO) + r".*?" + re.escape(_ALSA_FIM) + r"\n?", "", texto, flags=re.S)
    bloco = (f'{_ALSA_INICIO}\npcm.{ALSA_NOME} {{\n    type pipewire\n    capture_node "{entrada}"\n'
             f'    playback_node "{saida}"\n    hint {{\n        show on\n        description "LogBeamOS: radio sound"\n'
             f'    }}\n}}\n{_ALSA_FIM}\n')
    if texto and not texto.endswith("\n"):
        texto += "\n"
    os.makedirs(os.path.dirname(ALSA_UTILIZADOR), exist_ok=True)
    with open(ALSA_UTILIZADOR, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(texto + bloco)


def configura_direwolf(caminho, entrada=None, saida=None):
    """Som do rádio (o dispositivo ALSA "logbeamos-radio", ver som_alsa) e PTT pelo CAT partilhado (rigctld).
    Troca as linhas activas ADEVICE e PTT; se não existirem, o ADEVICE vai antes do 1.º CHANNEL e o PTT a seguir
    ao 1.º MODEM (canal 0). Não transmite nada: o exemplo do Direwolf não tem balizas nem digipeater ligados."""
    direwolf_base(caminho)
    with open(caminho, encoding="utf-8", errors="surrogateescape") as f:
        linhas = f.read().splitlines()
    guarda(caminho)
    novas = {"PTT": f"PTT RIG {RIG_REDE} {ENDERECO}"}
    if entrada and saida:
        som_alsa(entrada, saida)
        novas["ADEVICE"] = f"ADEVICE {ALSA_NOME}"
    for chave, nova in novas.items():
        i = next((j for j, l in enumerate(linhas) if _activa(l, chave)), None)
        if i is not None:
            linhas[i] = nova
            continue
        ref = "CHANNEL" if chave == "ADEVICE" else "MODEM"
        j = next((j for j, l in enumerate(linhas) if _activa(l, ref)), None)
        if j is None:
            linhas.append(nova)
        elif chave == "ADEVICE":
            linhas.insert(j, nova)
        else:
            linhas.insert(j + 1, nova)
    with open(caminho, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write("\n".join(linhas) + "\n")


# --- N1MM+ and Log4OM (Windows programs, through Wine): each one uses the radio the way the user chose (0.3.22).
#   "exclusivo":  the program opens the radio port itself (a COM port of Wine). The port cannot be opened twice, so the
#                 n1mm and log4om commands stop the sharing while the program is open and start it again at the end;
#   "partilhado": the program uses the sharing, like the others. Log4OM speaks Hamlib and attaches to rigctld directly.
#                 N1MM+ does not: it connects over the network (its "TCP" port) to ponte-ts2000, which answers like a
#                 Kenwood TS-2000 and passes everything on to the sharing.
# The choice is kept in the radio configuration (keys "n1mm" and "log4om"), where the two commands read it.
WINE = [("n1mm", "N1MM+", "N1MMLogger.net.exe"), ("log4om", "Log4OM", "L4ONG.exe")]
PONTE = "logbeamos-ponte-n1mm.service"
UNIDADE_PONTE = os.path.join(CASA, ".config", "systemd", "user", PONTE)
PONTE_PROGRAMA = "/usr/local/lib/logbeamos/equipamento/ponte-ts2000"
PONTE_PORTA = 4533
HAMLIB_LOG4OM = 10        # "CATSoftware" of the Hamlib driver in the Log4OM settings
LOG4OM_PORTA = 4534       # where the rigctld that Log4OM starts for itself answers ("only Log4OM uses the radio")


class FaltaAbrir(Exception):
    """The program has to be opened once before it can be set up here: its settings do not exist yet."""


def modos():
    """The choice already made for N1MM+ and Log4OM: {"n1mm": "partilhado" | "exclusivo", "log4om": …}."""
    cfg = configuracao() or {}
    return {k: cfg[k] for k, _n, _e in WINE if cfg.get(k) in ("partilhado", "exclusivo")}


def prefixo_wine():
    """The Wine prefix of this user, as /usr/local/lib/logbeamos/wine-env.sh decides it."""
    modelo = "/opt/ham/wine"
    try:
        if os.stat(modelo).st_uid == os.getuid():
            return modelo
    except OSError:
        pass
    return os.path.join(CASA, ".local", "share", "logbeamos", "wine")


def abertos_wine():
    """N1MM+ and Log4OM that are open (they would save their old settings when closing)."""
    r = subprocess.run(["ps", "-eo", "args="], capture_output=True, text=True)
    return [nome for _k, nome, exe in WINE if exe.lower() in r.stdout.lower()]


def liga_ponte():
    os.makedirs(os.path.dirname(UNIDADE_PONTE), exist_ok=True)
    texto = f"""# LogBeamOS: N1MM+ shares the radio through this bridge. Written by "Radio and Equipment"; change it there.
[Unit]
Description=LogBeamOS: N1MM+ on the shared radio
After={SERVICO}

[Service]
ExecStart=/usr/bin/python3 -I {PONTE_PROGRAMA} {PONTE_PORTA} {ENDERECO}
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
"""
    with open(UNIDADE_PONTE, "w", encoding="utf-8") as f:
        f.write(texto)
    systemctl("daemon-reload")
    systemctl("enable", PONTE)
    systemctl("restart", PONTE)


def desliga_ponte():
    if not os.path.exists(UNIDADE_PONTE):
        return
    systemctl("disable", "--now", PONTE)
    try:
        os.remove(UNIDADE_PONTE)
    except OSError:
        pass
    systemctl("daemon-reload")


def formato_serie(modelo):
    """Data bits, parity and stop bits of the radio, as Hamlib knows them ("8", "N", "2"), and whether it uses
    hardware flow control."""
    r = subprocess.run(["rigctl", "-m", str(modelo), "-u"], capture_output=True, text=True)
    linha = next((l for l in r.stdout.splitlines() if l.startswith("Serial speed")), "")
    m = re.search(r"\b([5-8])([NEO])([12])\b", linha)
    return (m.groups() if m else ("8", "N", "1")), "CTS/RTS" in linha


# N1MM+ radio for each Hamlib model: the name and the number N1MM+ keeps in its ini (its Configurer list, version
# 1.0.11364). The FT-818 and the KX2 use the entries N1MM+ points them to (FT-817 and KX3); the older Kenwoods use
# "TS-940" or the generic "Kenwood", as its Configurer says.
N1MM_RADIOS = {
    1001: ("FT-847", 220), 1003: ("FT-1000", 255), 1004: ("FT-1000MP", 256), 1007: ("FT-757GXII", 205),
    1011: ("FT-840", 215), 1013: ("FT-900", 235), 1014: ("FT-920", 237), 1015: ("FT-890", 230), 1016: ("FT-990", 242),
    1020: ("FT-817", 210), 1021: ("FT-100", 200), 1022: ("FT-857", 225), 1023: ("FT-897", 233),
    1024: ("FT-1000MP", 256), 1025: ("FT-1000MP", 256), 1027: ("FT-450", 202), 1028: ("FT-950", 240),
    1029: ("FT-2000", 272), 1030: ("FTDX-9000", 290), 1032: ("FTDX-5000", 285), 1034: ("FTDX-1200", 270),
    1035: ("FT-991", 243), 1036: ("FT-891", 231), 1037: ("FTDX-3000", 283), 1040: ("FTDX101D", 250),
    1041: ("FT-817", 210), 1042: ("FTDX10", 201), 1043: ("FT-897", 233), 1044: ("FTDX101D", 250),
    1046: ("FT-450", 202), 1049: ("FT-710", 206),
    2001: ("TS-940", 140), 2002: ("TS-940", 140), 2003: ("Kenwood", 100), 2004: ("Kenwood", 100),
    2005: ("Kenwood", 100), 2009: ("Kenwood", 100), 2010: ("Kenwood", 100), 2011: ("TS-940", 140),
    2012: ("Kenwood", 100), 2013: ("Kenwood", 100), 2014: ("TS-2000", 130), 2016: ("Kenwood", 100),
    2021: ("Elecraft K2", 180), 2024: ("TS-940", 140), 2025: ("TS-940", 140), 2028: ("TS-480", 118),
    2029: ("Elecraft K3", 181), 2031: ("TS-590", 120), 2037: ("TS-590", 120), 2039: ("TS-990", 145),
    2041: ("TS-890", 125), 2043: ("Elecraft K3", 181), 2044: ("Elecraft KX3", 182), 2045: ("Elecraft KX3", 182),
    2047: ("Elecraft K4", 183),
    3002: ("IC-1275", 398), 3004: ("IC-275", 303), 3007: ("IC-475", 305), 3009: ("IC-706", 300),
    3010: ("IC-706MKII", 301), 3011: ("IC-706MKIIG", 304), 3012: ("IC-707", 307), 3013: ("IC-718", 302),
    3014: ("IC-725", 308), 3015: ("IC-726", 309), 3016: ("IC-728", 310), 3019: ("IC-735", 320), 3020: ("IC-736", 330),
    3021: ("IC-737", 340), 3022: ("IC-738", 341), 3023: ("IC-746", 344), 3024: ("IC-751", 350), 3026: ("IC-756", 360),
    3027: ("IC-756PRO", 370), 3028: ("IC-761", 376), 3029: ("IC-765", 380), 3030: ("IC-775", 390),
    3031: ("IC-781", 395), 3034: ("IC-821", 331), 3044: ("IC-910", 391), 3045: ("IC-78", 312),
    3046: ("IC-746PRO", 345), 3047: ("IC-756PROII", 373), 3055: ("IC-703", 306), 3056: ("IC-7800", 397),
    3057: ("IC-756PROIII", 374), 3060: ("IC-7000", 396), 3061: ("IC-7200", 393), 3062: ("IC-7700", 381),
    3063: ("IC-7600", 394), 3067: ("IC-7410", 346), 3068: ("IC-9100", 325), 3070: ("IC-7100", 392),
    3073: ("IC-7300", 335), 3075: ("IC-7850-7851", 410), 3078: ("IC-7610", 399), 3081: ("IC-9700", 460),
    3085: ("IC-705", 311), 3088: ("Xiegu G90", 498),
}
# N1MM+ radios for which its own Configurer suggests "Handshake" on the serial lines (flow control by RTS/CTS): the
# Kenwoods and the Yaesus that use it. The Hamlib of the system does not always agree (4.5.5 opens the TS-2000 without
# flow control), and N1MM+ is the one that speaks to the radio here.
N1MM_FLUXO = {100, 101, 118, 120, 125, 130, 140, 145, 201, 202, 240, 243, 244, 250, 270, 272, 283, 285, 290}
# CI-V address N1MM+ uses for each of its Icom radios (its own defaults). Its Configurer fills it in when the radio is
# chosen there; written straight into the ini, it has to go with it.
N1MM_ICOM = {
    300: 72, 301: 78, 302: 94, 303: 16, 304: 88, 305: 20, 306: 104, 307: 62, 308: 40, 309: 48, 310: 56, 311: 164,
    312: 98, 320: 4, 325: 124, 330: 64, 331: 76, 335: 148, 340: 60, 341: 68, 344: 86, 345: 102, 346: 128, 350: 28,
    360: 80, 370: 92, 373: 100, 374: 110, 376: 30, 380: 44, 381: 116, 390: 70, 391: 96, 392: 136, 393: 118, 394: 122,
    395: 38, 396: 112, 397: 106, 398: 24, 399: 152, 410: 142, 460: 162, 498: 112,
}


def ini_n1mm():
    """N1MM+ keeps its settings in the Documents folder of Wine (which wine-env.sh links to the user's own)."""
    docs = os.path.join(prefixo_wine(), "drive_c", "users", "logbeam", "Documents")
    return os.path.join(os.path.realpath(docs), "N1MM Logger+", "N1MM Logger.ini")


def _seccao_ini(linhas, nome):
    """Start and end (exclusive) of the lines of a section, after its header; (None, None) if it does not exist."""
    cab = f"[{nome}]"
    for i, l in enumerate(linhas):
        if l.strip() == cab:
            fim = i + 1
            while fim < len(linhas) and not linhas[fim].startswith("["):
                fim += 1
            return i + 1, fim
    return None, None


def _porta_n1mm(linhas):
    """N1MM+ has eight COM port lines ([Port1] to [Port8]). Returns the one that holds radio 1 or, when there is none,
    the first one that is not in use (no port, or a port with no radio that is not kept for digital modes, CW or
    PTT either)."""
    livres = []
    for n in range(1, 9):
        i, fim = _seccao_ini(linhas, f"Port{n}")
        v = {k: x.strip() for k, x in (l.split("=", 1) for l in linhas[i:fim] if "=" in l)} if i is not None else {}
        com = v.get(f"ComPortNum{n}") or "0"
        tipo = v.get(f"RadioType{n}") or "0"
        if com != "0" and tipo != "0" and v.get(f"AssociatedRadioNr{n}", "1") in ("0", "1"):
            return n
        if com == "0" or (tipo == "0" and "True" not in (v.get(f"IsDigitalPort{n}"), v.get(f"IsOtherPort{n}"))):
            livres.append(n)
    return livres[0] if livres else 1


def _le_ini_n1mm(caminho):
    """The lines of the N1MM+ ini (empty when it does not exist yet) and how it is encoded."""
    bruto = b""
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            bruto = f.read()
    cod = "utf-16" if bruto[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
    linhas = bruto.decode(cod, errors="surrogateescape" if cod == "utf-8" else "replace").replace("\r\n", "\n").split("\n")
    while linhas and not linhas[-1].strip():
        linhas.pop()
    return linhas, cod


def modo_presumido(chave):
    """How the program is set up today, for the first time the choice is shown to someone who set it up by hand:
    "exclusivo" when it already opens the radio port itself, "partilhado" when it already uses the sharing, None when
    its settings do not tell. The choice comes selected accordingly, so that nothing changes without being asked."""
    try:
        if chave == "n1mm":
            linhas, _cod = _le_ini_n1mm(ini_n1mm())
            n = _porta_n1mm(linhas)
            i, fim = _seccao_ini(linhas, f"Port{n}")
            v = {k: x.strip() for k, x in (l.split("=", 1) for l in linhas[i:fim] if "=" in l)} if i is not None else {}
            com, tipo = int(v.get(f"ComPortNum{n}") or 0), v.get(f"RadioType{n}") or "0"
            if tipo == "0" or com == 0:
                return None
            return "partilhado" if com >= 1000 and v.get(f"TCPRadioAddr{n}", "").endswith(f":{PONTE_PORTA}") else "exclusivo"
        with open(json_log4om(), "rb") as f:
            c = _cat_log4om(json.loads(f.read().decode("utf-8-sig"))) or {}
        h = next((x for x in c.get("CATDrivers", []) if isinstance(x, dict) and x.get("CATSoftware") == HAMLIB_LOG4OM), None)
        if c.get("CatEngine") != HAMLIB_LOG4OM or h is None:
            return None
        return "partilhado" if h.get("AttachExisting") else ("exclusivo" if h.get("COMPort") else None)
    except (OSError, ValueError):
        return None


def configura_n1mm(modo, com=None, velocidade=None, modelo=None):
    """Writes the radio port of N1MM+ in its ini; PTT in voice and in the digital modes goes by CAT. Returns
    "partilhado", "exclusivo" or, when N1MM+ has no radio of its own for the model, "exclusivo-sem-radio" (the port
    and the speed are written; the radio is left to be chosen in the N1MM+ Configurer)."""
    if not os.path.isdir(os.path.join(prefixo_wine(), "drive_c")):
        raise FaltaAbrir()
    caminho = ini_n1mm()
    linhas, cod = _le_ini_n1mm(caminho)
    n = _porta_n1mm(linhas)
    v = {f"AssociatedRadioNr{n}": "1", f"DTRFunction{n}": "Always Off", f"RTSFunction{n}": "Always Off",
         f"IsPTTviaRadioSsb{n}": "True", f"IsPTTviaRadioDigital{n}": "True", f"IcomCode{n}": "0"}
    if modo == "partilhado":
        v.update({f"ComPortNum{n}": "1000", f"TCPRadioAddr{n}": f"127.0.0.1:{PONTE_PORTA}", f"TCPInitString{n}": "",
                  f"RadioName{n}": "TS-2000", f"RadioType{n}": "130", f"IsRadioPort{n}": "True"})
        feito = "partilhado"
    else:
        m = re.fullmatch(r"COM(\d+)", com or "")
        if not m:
            raise ValueError("COM")
        (bits, paridade, paragem), fluxo = formato_serie(modelo)
        v.update({f"ComPortNum{n}": m.group(1), f"PortSpeed{n}": str(velocidade), f"PortDataBits{n}": bits,
                  f"PortParity{n}": paridade, f"PortStopBits{n}": paragem, f"TCPRadioAddr{n}": "",
                  f"TCPInitString{n}": ""})
        radio = N1MM_RADIOS.get(modelo)
        # DTR stays off; the RTS line goes to the flow control where the radio uses it (see opcoes_serie), as Hamlib
        # or N1MM+ itself knows the radio
        if fluxo or (radio and radio[1] in N1MM_FLUXO):
            v[f"RTSFunction{n}"] = "Handshake"
        if radio:
            v.update({f"RadioName{n}": radio[0], f"RadioType{n}": str(radio[1]), f"IsRadioPort{n}": "True"})
            if radio[1] in N1MM_ICOM:
                v[f"IcomCode{n}"] = str(N1MM_ICOM[radio[1]])
            feito = "exclusivo"
        else:       # never leave another radio's commands going to this one
            v.update({f"RadioName{n}": "None", f"RadioType{n}": "0", f"IsRadioPort{n}": "False"})
            feito = "exclusivo-sem-radio"
    i, fim = _seccao_ini(linhas, f"Port{n}")
    if i is None:
        if linhas:
            linhas.append("")
        linhas.append(f"[Port{n}]")
        i = fim = len(linhas)
    resto = [l for l in linhas[i:fim] if l.strip() and l.split("=", 1)[0] not in v]
    linhas[i:fim] = sorted(resto + [f"{k}={x}" for k, x in v.items()], key=str.lower) + ([""] if fim < len(linhas) else [])
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    guarda(caminho)
    texto = "\r\n".join(linhas) + "\r\n"
    with open(caminho, "wb") as f:
        f.write(texto.encode(cod, errors="surrogateescape" if cod == "utf-8" else "replace"))
    return feito


def json_log4om():
    return os.path.join(prefixo_wine(), "drive_c", "users", "logbeam", "AppData", "Roaming", "Log4OM2", "user",
                        "config.json")


def _cat_log4om(d):
    """The CATConfiguration object, wherever the Log4OM profile keeps it."""
    if isinstance(d, dict):
        if isinstance(d.get("CATConfiguration"), dict):
            return d["CATConfiguration"]
        d = list(d.values())
    if isinstance(d, list):
        for x in d:
            r = _cat_log4om(x)
            if r is not None:
                return r
    return None


def opcoes_serie_log4om(modelo):
    """The rule of opcoes_serie (RTS and DTR off, except the RTS of the flow control), asked to the Hamlib that Log4OM
    brings with it: a newer version than the one of the system, which may know the radio differently, and which
    refuses to start when a state is imposed on a line it uses for flow control."""
    prefixo = prefixo_wine()
    exe = os.path.join(prefixo, "drive_c", "users", "logbeam", "AppData", "Roaming", "Log4OM2", "hamlib", "rigctl.exe")
    linha = ""
    try:
        r = subprocess.run(["wine", exe, "-m", str(modelo), "-u"], capture_output=True, text=True, errors="replace",
                           timeout=60, env=dict(os.environ, WINEPREFIX=prefixo, WINEDEBUG="-all",
                                                WINEDLLOVERRIDES="winemenubuilder.exe=d"))
        linha = next((l for l in r.stdout.splitlines() if l.startswith("Serial speed")), "")
    except (OSError, subprocess.TimeoutExpired):
        pass
    if not linha:
        return opcoes_serie(modelo)
    return ["-C", "dtr_state=OFF"] if "CTS/RTS" in linha else ["-C", "rts_state=OFF", "-C", "dtr_state=OFF"]


def configura_log4om(modo, com=None, velocidade=None, modelo=None):
    """Writes the CAT of Log4OM 2 in its config.json: the Hamlib driver, started with Log4OM, PTT by CAT.
    "partilhado": Log4OM attaches to the rigctld that is already running (the sharing).
    "exclusivo":  Log4OM starts its own rigctld on the radio port; it runs it with the "Parameters" exactly as written,
                  so they are the same the sharing uses, with the COM port of Wine."""
    caminho = json_log4om()
    if not os.path.exists(caminho):
        raise FaltaAbrir()
    with open(caminho, "rb") as f:
        bruto = f.read()
    marca = bruto.startswith(b"\xef\xbb\xbf")
    d = json.loads(bruto.decode("utf-8-sig"))
    c = _cat_log4om(d)
    if c is None or not isinstance(c.get("CATDrivers"), list):
        raise ValueError("CATConfiguration")
    h = next((x for x in c["CATDrivers"] if isinstance(x, dict) and x.get("CATSoftware") == HAMLIB_LOG4OM), None)
    if h is None:   # a new profile has no Hamlib driver until its CAT screen is used: the same fields Log4OM writes
        h = {"CATSoftware": HAMLIB_LOG4OM, "DisconnectAtFirstMessage": False, "AttachExisting": False,
             "Parameters": "", "TcpPort": 4532, "Address": "127.0.0.1", "Delay": 500, "Radio": 0, "COMPTTPort": "",
             "COMPort": "", "DataCarrier": "NONE", "RTS": False, "DTR": False, "BaudRate": 0, "StopBits": "1",
             "PTTMode": "RIG", "CIV": "", "DebugMode": "", "RadioNetworkAddress": "127.0.0.1",
             "RadioNetworkPort": 7820, "SerialConnected": True, "Hide": False, "VfoMode": False, "SpotColor": "Red",
             "ShowSpot": True, "ExecutablePath": "", "AutostartExecutable": False, "ConnectionUser": "",
             "ConnectionPassword": ""}
        c["CATDrivers"].insert(0, h)
    h.update({"Address": "127.0.0.1", "TcpPort": 4532, "PTTMode": "RIG"})
    if modo == "partilhado":
        h["AttachExisting"] = True
    else:
        # Its own rigctld answers on a port of its own (4534), not on the one of the sharing: on 4532 the other
        # programs would find it and go on using the radio through Log4OM, which is not what "only Log4OM" says
        m = re.fullmatch(r"COM(\d+)", com or "")
        if not m:
            raise ValueError("COM")
        porta = com if int(m.group(1)) < 10 else "\\\\.\\" + com
        (_bits, _paridade, paragem), _fluxo = formato_serie(modelo)
        h.update({"AttachExisting": False, "TcpPort": LOG4OM_PORTA, "Radio": modelo, "COMPort": com,
                  "BaudRate": velocidade, "StopBits": paragem, "RTS": False, "DTR": False, "SerialConnected": True,
                  "Hide": True,
                  "Parameters": " ".join(["-m", str(modelo), "-r", porta, "-s", str(velocidade), "-T", "127.0.0.1",
                                          "-t", str(LOG4OM_PORTA), *opcoes_serie_log4om(modelo)])})
    c["CatEngine"] = HAMLIB_LOG4OM
    c["CatAutostart"] = True
    guarda(caminho)
    with open(caminho, "wb") as f:
        f.write((b"\xef\xbb\xbf" if marca else b"") + json.dumps(d, indent=2, ensure_ascii=False).encode("utf-8"))
    return modo


def configura_wine(escolha, com, velocidade, modelo):
    """Sets up N1MM+ and Log4OM as chosen ({"n1mm": "partilhado" | "exclusivo", "log4om": …}) and keeps the choice of
    the ones that were set up. The bridge runs only while N1MM+ shares the radio. Returns a list (key, ok, detail)."""
    res = []
    feitos = {}
    for chave, _nome, _exe in WINE:
        modo = escolha.get(chave)
        if modo not in ("partilhado", "exclusivo"):
            continue
        try:
            f = configura_n1mm if chave == "n1mm" else configura_log4om
            res.append((chave, True, f(modo, com, velocidade, modelo)))
            feitos[chave] = modo
        except FaltaAbrir:
            res.append((chave, False, "falta"))
        except Exception as e:  # one program with a problem does not stop the other
            res.append((chave, False, str(e)))
    cfg = configuracao() or {}
    cfg.update(feitos)
    _guarda_configuracao(cfg)
    if cfg.get("n1mm") == "partilhado":
        liga_ponte()
    else:
        desliga_ponte()
    return res


CAMINHOS = {
    "wsjtx": os.path.join(CASA, ".config", "WSJT-X.ini"),
    "jtdx": os.path.join(CASA, ".config", "JTDX.ini"),
    "decodium": os.path.join(CASA, ".config", "Decodium", "Decodium3.ini"),
    "fldigi": os.path.join(CASA, ".fldigi", "fldigi_def.xml"),
    "not1mm": os.path.join(CASA, ".config", "not1mm", "not1mm.json"),
    "direwolf": os.path.join(CASA, "direwolf.conf"),
}


def configura(modelo, porta, velocidade, programas, carta_som=None, wine=None, com=None):
    """Liga a partilha e configura os programas escolhidos. Devolve (nome, porta fixa, frequência, resultados),
    em que resultados é uma lista (chave, ok, detalhe).
    wine: how N1MM+ and Log4OM use the radio ({"n1mm": "partilhado" | "exclusivo", "log4om": …}); com: the COM port
    the radio has in Wine, for the ones that use it alone."""
    nome, fixa = liga_partilha(modelo, porta, velocidade)
    entrada = saida = None
    if carta_som is not None:
        entrada, saida = som_pulse(carta_som)
    res = []
    for chave in programas:
        try:
            if chave in ("wsjtx", "jtdx"):
                configura_wsjt(CAMINHOS[chave], entrada, saida)
                res.append((chave, True, "som" if (entrada or saida) else ""))
            elif chave == "decodium":
                configura_decodium(CAMINHOS[chave], entrada, saida)
                res.append((chave, True, "som" if (entrada or saida) else ""))
            elif chave == "fldigi":
                configura_fldigi(CAMINHOS[chave])
                res.append((chave, True, ""))
            elif chave == "not1mm":
                configura_not1mm(CAMINHOS[chave])
                res.append((chave, True, ""))
            elif chave == "direwolf":
                configura_direwolf(CAMINHOS[chave], entrada, saida)
                res.append((chave, True, "som" if (entrada and saida) else ""))
        except Exception as e:  # um programa com problemas não impede os outros
            res.append((chave, False, str(e)))
    if wine:
        res += configura_wine(wine, com, velocidade, modelo)
    return nome, fixa, frequencia_partilha(), res
