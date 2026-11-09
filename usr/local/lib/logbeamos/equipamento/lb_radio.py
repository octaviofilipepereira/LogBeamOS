# Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
# © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
# Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
# LogBeamOS: "Configurar" do "Rádio e Equipamento".
# O rádio fica num só sítio: o rigctld (Hamlib), como serviço do utilizador, em 127.0.0.1:4532. O WSJT-X, o JTDX,
# o Fldigi, o Not1MM e o Direwolf ligam-se a ele ao mesmo tempo ("Hamlib NET rigctl"). O N1MM+ só fala por uma COM:
# o comando n1mm desliga o rigctld enquanto o N1MM+ está aberto e volta a ligá-lo no fim.
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


def liga_partilha(modelo, porta, velocidade):
    """Escreve a configuração e o serviço, e (re)arranca o rigctld."""
    nome = nome_hamlib(modelo)
    porta = porta_fixa(porta)
    os.makedirs(os.path.dirname(CONF), exist_ok=True)
    with open(CONF, "w", encoding="utf-8") as f:
        json.dump({"modelo": modelo, "nome": nome, "porta": porta, "velocidade": velocidade}, f, indent=2)
    escreve_servico(modelo, porta, velocidade, nome)
    systemctl("daemon-reload")
    systemctl("enable", SERVICO)
    systemctl("restart", SERVICO)
    return nome, porta


def desliga_partilha():
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


CAMINHOS = {
    "wsjtx": os.path.join(CASA, ".config", "WSJT-X.ini"),
    "jtdx": os.path.join(CASA, ".config", "JTDX.ini"),
    "decodium": os.path.join(CASA, ".config", "Decodium", "Decodium3.ini"),
    "fldigi": os.path.join(CASA, ".fldigi", "fldigi_def.xml"),
    "not1mm": os.path.join(CASA, ".config", "not1mm", "not1mm.json"),
    "direwolf": os.path.join(CASA, "direwolf.conf"),
}


def configura(modelo, porta, velocidade, programas, carta_som=None):
    """Liga a partilha e configura os programas escolhidos. Devolve (nome, porta fixa, frequência, resultados),
    em que resultados é uma lista (chave, ok, detalhe)."""
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
    return nome, fixa, frequencia_partilha(), res
