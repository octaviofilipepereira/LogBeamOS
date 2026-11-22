# Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
# © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
# Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
# LogBeamOS: o que o "Actualizar LogBeamOS" sabe de cada programa: de onde vem, como se lê a versão instalada,
# como se procura a mais recente e como se instala. Usado pela janela (como utilizador) e pelo ajudante (como root).
# O ajudante nunca recebe endereços da janela: procura-os ele próprio, a partir desta tabela.
import errno
import glob
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import tarfile
import tempfile
import urllib.request

ESTADO = "/var/lib/logbeamos/versoes.json"   # versões dos programas que não vêm por pacote
AGENTE = "LogBeamOS-Actualizar"
PIPX = {"PIPX_HOME": "/opt/pipx", "PIPX_BIN_DIR": "/usr/local/bin"}
AJUSTES_NOT1MM = "/usr/local/lib/logbeamos/ajustes-not1mm.py"

# Programas publicados no GitHub: chave, nome, repositório, etiqueta fixa (None = a mais recente), ficheiro, instalação
GITHUB = [
    ("wsjtx", "WSJT-X", "WSJTX/wsjtx", None, r"^wsjtx-.*-linux-x86_64\.AppImage$", "appimage", "/opt/ham/wsjtx"),
    ("js8call", "JS8Call", "JS8Call-improved/JS8Call-improved", None, r"^JS8Call-.*-x86_64\.AppImage$", "appimage", "/opt/ham/js8call"),
    ("wfview", "wfview", "wf-group/wfview", None, r"^wfview-linux-installer\.sh$", "makeself", "/opt/ham/wfview"),
    ("pat", "Pat (Winlink)", "la5nta/pat", None, r"^pat_.*_linux_amd64\.deb$", "deb", "pat"),
    ("satdump", "SatDump", "SatDump/SatDump", None, r"^satdump_.*_ubuntu_24\.04_amd64\.deb$", "deb", "satdump"),
    ("sdrpp", "SDR++", "AlexandreRouma/SDRPlusPlus", "nightly", r"^sdrpp_ubuntu_noble_amd64\.deb$", "deb", "sdrpp"),
    ("waveloggate", "WaveLogGate", "wavelog/WaveLogGate", None, r"^wavelog-gate_.*_webkit4\.1_amd64\.deb$", "deb", "wavelog-gate"),
    ("decodium", "Decodium", "iu8lmc/Decodium-4.0-Core-Shannon", None, r"^decodium.*-linux-x86_64\.AppImage$", "appimage", "/opt/ham/decodium"),
    # Flatpak publicado no GitHub (não está no Flathub): a base KDE vem do Flathub quando o flatpak a pede
    ("qdmr", "qdmr", "hmatuschek/qdmr", None, r"^qdmr.*x86_64\.flatpak\.zip$", "flatpak", "de.darc.dm3mat.qdmr"),
    # Opcional (ver OPCIONAIS): não vem na imagem, instala-se pelo Actualizar quando o utilizador o marcar
    ("voxdmr", "VoxDMR", "jcalado/voxdmr-site", None, r"^VoxDMR-linux-x86_64\.AppImage$", "appimage", "/opt/ham/voxdmr"),
    # Publicado só como código: substitui-se o código e mantêm-se os dados e as definições (ver instala_fonte)
    ("4ham", "4ham Spectrum Analysis", "octaviofilipepereira/4ham-spectrum-analysis", None, None, "fonte", "/opt/ham/4ham"),
]
SERVICO_4HAM = "4ham-spectrum-analysis.service"

# Programas que não vêm na imagem: enquanto não estiverem instalados aparecem como opcionais, desmarcados, fora dos
# atalhos "Rádio" e "Tudo" e do aviso do arranque. O VoxDMR é gratuito mas não declara licença (autor, 09/11/2026).
OPCIONAIS = {"voxdmr"}

# Pacotes de rádio do sistema que aparecem na lista com nome próprio; os restantes contam como "sistema operativo"
PACOTES_RADIO = {
    "fldigi": "Fldigi", "flrig": "Flrig", "flamp": "Flamp", "flmsg": "Flmsg", "gpredict": "Gpredict", "jtdx": "JTDX",
    "cqrlog": "CQRLOG", "klog": "KLog", "direwolf": "Dire Wolf", "freedv": "FreeDV", "gnuradio": "GNU Radio",
    "gqrx-sdr": "Gqrx", "xastir": "Xastir", "qsstv": "QSSTV", "xnec2c": "xnec2c",
    "gridtracker2": "GridTracker2", "shutter": "Shutter", "libhamlib4t64": "Hamlib", "libhamlib-utils": "Hamlib",
    "wine-stable": "Wine", "qtel": "Qtel (EchoLink)",
    # Repositório apt do LogBeamOS (https://logbeam.org/apt, desde a 0.3.11): as ferramentas e o Uplink. The tools
    # package is shown to the user as "LogBeamOS Update" (author's decision of 16/11/2026, tools 0.3.23)
    "logbeamos-ferramentas": "LogBeamOS Update", "logbeam-uplink": "LogBeam Uplink",
    "logbeamos-tqsl": "TQSL",   # since tools 0.3.18 (14/11/2026), from the same repository
}

# Programas que se actualizam sozinhos: só aparecem na lista
SOZINHOS = [("n1mm", "N1MM Logger+"), ("log4om", "Log4OM 2"), ("gridtracker2", "GridTracker2")]

# Na pen o arranque vem sempre da imagem: estes pacotes não se actualizam lá (no disco instalado, sim)
PEN_FIXOS = ("linux-image-*", "linux-headers-*", "linux-modules-*", "linux-generic*", "linux-signed-*",
             "grub-*", "grub2-*", "shim*", "casper", "ubiquity*")


def na_pen():
    with open("/proc/cmdline") as f:
        return "boot=casper" in f.read().split()


def fixo_na_pen(pacote):
    import fnmatch
    return any(fnmatch.fnmatch(pacote, p) for p in PEN_FIXOS)


# --- Utilitários
CACHE_MINUTOS = 15


def obter_json(url, tempo=20):
    """A API do GitHub sem conta aceita 60 pedidos por hora por endereço e cada procura faz um por programa (até
    os pedidos condicionais com ETag contam, sem conta). Por isso cada resposta fica guardada: durante
    CACHE_MINUTOS volta a usar-se sem perguntar; se o limite se esgotar, usa-se a última que houver (0.3.11)."""
    import time
    import urllib.error
    pasta = os.path.join(os.path.expanduser("~"), ".cache", "logbeamos-actualizar", "http")
    nome = os.path.join(pasta, hashlib.sha256(url.encode()).hexdigest()[:32] + ".json")
    guardado = None
    try:
        with open(nome, encoding="utf-8") as f:
            guardado = json.load(f)
        if time.time() - os.path.getmtime(nome) < CACHE_MINUTOS * 60:
            return guardado
    except (OSError, ValueError):
        pass
    p = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(p, timeout=tempo) as r:
            dados = json.load(r)
    except urllib.error.HTTPError as e:
        if guardado is not None and limite_github(e):
            return guardado
        raise
    try:
        os.makedirs(pasta, exist_ok=True)
        with open(nome + ".novo", "w", encoding="utf-8") as f:
            json.dump(dados, f)
        os.replace(nome + ".novo", nome)
    except OSError:
        pass
    return dados


def limite_github(e):
    """O pedido falhou por se ter esgotado o limite de pedidos do GitHub?"""
    h = getattr(e, "headers", None)
    return getattr(e, "code", 0) in (403, 429) and h is not None and h.get("X-RateLimit-Remaining") == "0"


def numeros(v):
    """'v2.6.0' → (2, 6, 0); serve para comparar versões simples."""
    return tuple(int(n) for n in re.findall(r"\d+", v or "")[:4])


def mais_recente(disponivel, instalada):
    if not disponivel:
        return False
    if not instalada:
        return True
    a, b = numeros(disponivel), numeros(instalada)
    return a > b if a and b else disponivel != instalada


def estado():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def grava_estado(chave, versao):
    d = estado()
    d[chave] = versao
    os.makedirs(os.path.dirname(ESTADO), exist_ok=True)
    with open(ESTADO + ".novo", "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)
    os.replace(ESTADO + ".novo", ESTADO)


def versao_pacote(nome):
    r = subprocess.run(["dpkg-query", "-W", "-f=${Status} ${Version}", nome], capture_output=True, text=True)
    if r.returncode or "installed" not in r.stdout:
        return ""
    return r.stdout.split()[-1]


# --- Versões disponíveis e instaladas
def info_github(item):
    """Devolve (versão, ficheiro) da publicação no GitHub; ficheiro é o dicionário do 'asset'."""
    chave, _, repo, etiqueta, padrao, tipo, _ = item
    url = f"https://api.github.com/repos/{repo}/releases/" + (f"tags/{etiqueta}" if etiqueta else "latest")
    rel = obter_json(url)
    if tipo == "fonte":
        tag = rel["tag_name"]
        return tag.lstrip("vV"), {"name": f"{chave}-{tag}.tar.gz",
                                  "browser_download_url": f"https://github.com/{repo}/archive/refs/tags/{tag}.tar.gz"}
    for a in rel.get("assets", []):
        if re.search(padrao, a["name"]):
            versao = a["updated_at"][:10] if etiqueta else rel["tag_name"].lstrip("vV")
            return versao, a
    return None, None


def instalada_github(item):
    chave, _, _, etiqueta, _, tipo, alvo = item
    if tipo == "deb" and not etiqueta:
        return versao_pacote(alvo).split("-")[0].split("+")[0]
    if tipo == "deb" and not versao_pacote(alvo):
        return ""
    if tipo == "flatpak" and not os.path.isdir(f"/var/lib/flatpak/app/{alvo}"):
        return ""
    return estado().get(chave, "")


def versao_not1mm():
    py = "/opt/pipx/venvs/not1mm/bin/python"
    if not os.path.exists(py):
        return ""
    r = subprocess.run([py, "-c", "import importlib.metadata as m; print(m.version('not1mm'))"],
                       capture_output=True, text=True)
    return r.stdout.strip()


def disponivel_not1mm():
    return obter_json("https://pypi.org/pypi/not1mm/json")["info"]["version"]


def apt_fontes(pasta):
    """Na pen o casper junta a própria pen às fontes do apt (deb cdrom:…), e o apt falharia a actualizá-la.
    Devolve as opções que usam uma cópia da lista de fontes sem essas linhas (vazio se não houver nenhuma)."""
    try:
        with open("/etc/apt/sources.list", encoding="utf-8") as f:
            linhas = f.read().splitlines()
    except OSError:
        return []
    if not any(l.lstrip().startswith("deb cdrom:") for l in linhas):
        return []
    os.makedirs(pasta, exist_ok=True)
    copia = os.path.join(pasta, "sources.list")
    with open(copia, "w", encoding="utf-8") as f:
        f.write("\n".join(l for l in linhas if not l.lstrip().startswith("deb cdrom:")) + "\n")
    return ["-o", f"Dir::Etc::SourceList={copia}"]


def apt_opcoes(pasta):
    return ["-o", "Debug::NoLocking=true", "-o", f"Dir::State::Lists={pasta}/lists",
            "-o", "Dir::Cache::pkgcache=", "-o", "Dir::Cache::srcpkgcache=", *apt_fontes(pasta)]


class SemRede(RuntimeError):
    """No package source answered apt-get update: there is no Internet connection. "falhas" lists (source, reason)."""

    def __init__(self, falhas):
        super().__init__("; ".join(f"{f}: {m}" for f, m in falhas))
        self.falhas = falhas


def falhas_apt(texto):
    """From the output of apt-get update (LC_ALL=C): (how many indexes were reached, [(source, reason)] of the sources
    that failed). Each failed source is an "Err:N URL SUITE …" line, followed by the reason, indented."""
    ok, falhas, actual = 0, {}, None
    for l in texto.splitlines():
        m = re.match(r"^(Hit|Get|Err|Ign):\d+ (\S+ \S+)", l)
        if m:
            actual = None
            if m.group(1) in ("Hit", "Get"):
                ok += 1
            elif m.group(1) == "Err":
                actual = m.group(2)
                falhas.setdefault(actual, "")
        elif actual and l.startswith("  ") and not falhas[actual]:
            falhas[actual] = l.strip()
    return ok, list(falhas.items())


def apt_actualiza_listas(pasta):
    """apt-get update into this user's own copy of the package lists. Returns the sources that failed, as
    [(source, reason)]: the others are updated and used. Raises SemRede when no source answered at all, and
    RuntimeError when apt itself failed (a broken sources file, for example).
    Until 0.9.0 any error here showed "No Internet connection" and hid every apt line, the LogBeamOS Update one
    included: one source of another program without its signing key was enough (Google Earth, reported by Bráulio
    Sousa, CT7APZ, 22/11/2026). apt 2.8 also ends with 0 when there is no network at all (the failures are warnings),
    so the exit code tells neither case apart: the "Hit/Get/Err" lines do."""
    env = dict(os.environ, LC_ALL="C")
    os.makedirs(f"{pasta}/lists/partial", exist_ok=True)
    r = subprocess.run(["apt-get", "-q", *apt_opcoes(pasta), "update"], capture_output=True, text=True, env=env)
    ok, falhas = falhas_apt(r.stdout + "\n" + r.stderr)
    if falhas and not ok:
        raise SemRede(falhas)
    if r.returncode and not falhas:
        erros = [l for l in r.stderr.splitlines() if l.startswith("E: ")] or r.stderr.strip().splitlines()
        raise RuntimeError(erros[-1] if erros else "apt-get update")
    return falhas


# Network problems in the messages of flatpak and cinnamon-spice-updater, so that they are not shown as errors
_REDE = re.compile(r"(?i)could not resolve|temporary failure|could not connect|failed to connect|network is unreachable|"
                   r"no route to host|timed? ?out|name or service not known|unable to load summary|urlopen error")


def e_rede(texto):
    """Does this error message say that the network could not be reached?"""
    return bool(_REDE.search(texto or ""))


def apt_pendentes(pasta=None, listas=True):
    """Lista (pacote, instalada, nova) do que o apt actualizaria. Sem root: usa uma cópia própria das listas.
    With listas=False the lists in pasta are not updated first (apt_actualiza_listas already did it)."""
    env = dict(os.environ, LC_ALL="C")
    if pasta:
        if listas:
            apt_actualiza_listas(pasta)
        extra = apt_opcoes(pasta)
    else:
        extra = []
    r = subprocess.run(["apt-get", "-s", "-q", *extra, "dist-upgrade"], capture_output=True, text=True, env=env)
    lista = []
    for linha in r.stdout.splitlines():
        m = re.match(r"^Inst (\S+) \[([^\]]+)\] \((\S+)", linha)
        if m:
            lista.append(m.groups())
    return lista


def apt_tamanhos(pasta=None):
    """Bytes a descarregar por pacote (só os que ainda não estão na cache do apt). Usa as listas de apt_pendentes."""
    import urllib.parse
    env = dict(os.environ, LC_ALL="C")
    extra = apt_opcoes(pasta) if pasta else []
    r = subprocess.run(["apt-get", "-qq", "--print-uris", *extra, "dist-upgrade"], capture_output=True, text=True,
                       env=env)
    d = {}
    for linha in r.stdout.splitlines():
        m = re.match(r"^'[^']+' ([^_\s]+)_\S+ (\d+) ", linha)
        if m:
            d[urllib.parse.unquote(m.group(1))] = int(m.group(2))
    return d


# --- Flatpak, Cinnamon extensions and old kernels: what the Mint Update Manager also did. LogBeamOS no longer ships
# it and "Update LogBeamOS" does everything (author's decision, 14/11/2026).
FLATPAK_GITHUB = {g[6] for g in GITHUB if g[5] == "flatpak"}  # these have their own line (qdmr)
TIPOS_CINNAMON = ("applet", "desklet", "extension", "theme")


def corre_registo(cmd, registo, env=None, tempo=None):
    """Runs a command and sends each line of its output to registo; raises with the last line if it fails."""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    ultima = ""
    for linha in p.stdout:
        for parte in linha.replace("\r", "\n").split("\n"):
            parte = parte.rstrip()
            if parte:
                ultima = parte
                registo(parte)
    if p.wait(tempo):
        raise RuntimeError(ultima or " ".join(cmd))


def flatpak_pendentes(instalacao):
    """What "flatpak update" would do in one installation ("--system" or "--user"): list of (ref, bytes to download
    or None). None if flatpak is not installed, or if there is no user installation.
    libflatpak prepares the same transaction as "flatpak update" and it is stopped before anything is downloaded.
    The shortcuts disagreed with "flatpak update" in the workshop (14/11/2026): "flatpak remote-ls --updates" leaves
    out the bases that Flathub marked end-of-life, and list_installed_refs_for_update() listed a KDE base (395 MB)
    that "flatpak update" did not touch, so the notice would never go away."""
    if not shutil.which("flatpak"):
        return None
    if instalacao == "--user" and not os.path.isdir(os.path.expanduser("~/.local/share/flatpak/repo")):
        return None
    import gi
    gi.require_version("Flatpak", "1.0")
    from gi.repository import Flatpak, GLib
    inst = Flatpak.Installation.new_system(None) if instalacao == "--system" else Flatpak.Installation.new_user(None)
    t = Flatpak.Transaction.new_for_installation(inst, None)
    t.set_no_interaction(True)
    for r in inst.list_installed_refs(None):
        if r.get_name() not in FLATPAK_GITHUB:  # qdmr has its own line
            try:
                t.add_update(r.format_ref(), None, None)
            except GLib.Error:
                pass
    ops = []

    def pronto(tr):
        ops.extend((op.get_ref(), op.get_download_size() or None) for op in tr.get_operations()
                   if not op.get_is_skipped())
        return False  # stop: nothing is downloaded or deployed

    t.connect("ready", pronto)
    try:
        t.run(None)
    except GLib.Error as e:
        if not e.matches(Flatpak.error_quark(), Flatpak.Error.ABORTED):
            raise RuntimeError(e.message)
    return ops


def actualiza_flatpak(instalacao, registo):
    """"flatpak update" of the whole installation, as the Mint Update Manager did, when flatpak_pendentes finds
    something (worked out here, never received from the window)."""
    pend = flatpak_pendentes(instalacao) or []
    if not pend:
        return "0"
    corre_registo(["flatpak", "update", instalacao, "-y", "--noninteractive"], registo, env=dict(os.environ, LC_ALL="C"))
    return str(len(pend))


def cinnamon_pendentes():
    """Cinnamon extensions of this user (applets, desklets, extensions, themes) with a new version: list of
    (type, uuid). None outside Cinnamon. Only as the user: cinnamon-spice-updater refuses to run as root."""
    if not shutil.which("cinnamon-spice-updater"):
        return None
    lista = []
    for tipo in TIPOS_CINNAMON:
        r = subprocess.run(["cinnamon-spice-updater", "--list-json", tipo], capture_output=True, text=True, timeout=180)
        try:
            d = json.loads(r.stdout)
        except ValueError:  # it prints "Cinnamon updates failed: …" (no network, for example) and still exits with 0
            raise RuntimeError((r.stdout.strip() or r.stderr.strip() or "cinnamon-spice-updater").splitlines()[-1])
        lista += [(tipo, uuid) for uuid in sorted(d)]
    return lista


def actualiza_cinnamon(registo):
    pend = cinnamon_pendentes() or []
    if not pend:
        return "0"
    texto = []

    def guarda(linha):
        texto.append(linha)
        registo(linha)
    corre_registo(["cinnamon-spice-updater", "--update-all"], guarda, tempo=1800)
    falhou = [l for l in texto if l.startswith("Cinnamon updates failed")]
    if falhou:
        raise RuntimeError(falhou[-1])
    return str(len(pend))


def actualiza_utilizador(tarefa, registo):
    """What the window updates itself, as the user (no password): Cinnamon extensions and the user's flatpaks."""
    if tarefa == "cinnamon":
        return actualiza_cinnamon(registo)
    if tarefa == "flatpak-utilizador":
        return actualiza_flatpak("--user", registo)
    raise RuntimeError(tarefa)


def nucleos_a_retirar(instalados, em_uso):
    """Kernel versions (e.g. '6.14.0-37-generic') to remove: all but the one in use and the newest. If the one in
    use is not among them, the two newest stay."""
    ordem = sorted(instalados, key=numeros)
    fica = set(ordem[-1:])
    if em_uso in ordem:
        fica.add(em_uso)
    else:
        fica.update(ordem[-2:])
    return [v for v in ordem if v not in fica]


def pacotes_do_nucleo(versao, pacotes):
    """Installed packages of one kernel version: linux-image-6.14.0-37-generic, linux-modules(-extra)-…,
    linux-headers-…, linux-hwe-6.14-headers-6.14.0-37, … (never the meta packages, such as linux-generic-hwe-24.04)."""
    abi = re.sub(r"-[a-z][a-z0-9\-]*$", "", versao)  # 6.14.0-37-generic → 6.14.0-37
    padrao = re.compile(r"^linux-[a-z0-9.\-]*-" + re.escape(abi) + r"(-[a-z][a-z0-9\-]*)?$")
    return [p for p in pacotes if padrao.match(p)]


def nucleos_velhos():
    """Packages of the old kernels of an installed system (on the pen the kernel always comes from the image)."""
    if na_pen():
        return []
    r = subprocess.run(["dpkg-query", "-W", "-f=${Package} ${Status}\n"], capture_output=True, text=True)
    pacotes = [l.split()[0] for l in r.stdout.splitlines() if l.endswith(" installed")]
    versoes = [p[len("linux-image-"):] for p in pacotes if re.match(r"^linux-image-\d", p)]
    return sorted({p for v in nucleos_a_retirar(versoes, os.uname().release) for p in pacotes_do_nucleo(v, pacotes)})


# --- System identity (tools 0.3.18, author's decision of 14/11/2026). A LogBeamOS that is updated through "Update
# LogBeamOS" gets everything a new image brings to the system itself, including its name and version: the description
# ("LogBeamOS 0.3.17"), the GRUB title, the installer minimum of 50 GB and, since tools 0.3.19 (author, 15/11/2026),
# the "System information" screen (mintreport), which writes "Linux Mint" in its code. Some of these files belong to
# other packages (base-files, mint-info-cinnamon, ubiquity, mintreport), whose updates can put the original text back,
# so this is applied by the package scripts and again at the end of every run of the helper.
VERSAO_SISTEMA = "usr/share/logbeamos/versao-sistema"   # the LogBeamOS version these tools bring the system to
# The version of these tools, shown to the user as "LogBeamOS Update" (tools 0.3.23, author's decision of 16/11/2026)
VERSAO_UPDATE = "usr/share/logbeamos/versao-update"
INSTALADOR = "usr/lib/ubiquity/ubiquity/misc.py"
MINIMO_50GB = "    min_disk_size = max(size * 3 // 2, 50 * 1000 ** 3)  # LogBeamOS: pelo menos 50 GB"
MINIMOS_ANTIGOS = ("    min_disk_size = size * 2  # fudge factor", "    min_disk_size = size * 3 // 2  # LogBeamOS: 1,5x (era 2x)")
# mintreport 1.6.0 shows f"{distribution} {release} - {edition} {architecture}" under a banner with the Linux Mint logo
# on green; the version is read when the screen opens, so it follows the system version without patching again. The
# banner gets the LogBeam logo (installed by these tools as the icon logbeamos-logo) on the dark blue of logbeam.org.
INFORMACOES = "usr/lib/linuxmint/mintreport/app.py"
INFORMACOES_UI = "usr/share/linuxmint/mintreport/mintreport.ui"
_VS = "/" + VERSAO_SISTEMA
_VU = "/" + VERSAO_UPDATE
# Since tools 0.3.23 the screen also shows the LogBeamOS Update version: "LogBeamOS 0.3.17 · LogBeamOS Update 0.3.23".
# Since 0.9.0-1 a single number when both are the same (single version number since 0.9.0): "LogBeamOS 0.9.0-1".
# The other keys are the lines written by tools 0.3.19 to 0.3.22 ("release = open(") and 0.3.23 to 0.9.0
# ("release = (open("), so that systems already patched get the new one; the new line starts differently, so a second
# run leaves it as it is
_RELEASE = (f"        release = (lambda s, u: s if u in ('', s) else s + ' · LogBeamOS Update ' + u)(open({_VS!r}).read()"
            f".strip(), open({_VU!r}).read().strip() if os.path.exists({_VU!r}) else '') if os.path.exists({_VS!r}) "
            f"else config['RELEASE']  # LogBeamOS")
INFORMACOES_TROCAS = {
    '        distribution = "Linux Mint"': '        distribution = "LogBeamOS"  # LogBeamOS',
    "        release = config['RELEASE']": _RELEASE,
    "        release = open(": _RELEASE,
    "        release = (open(": _RELEASE,
    "                background-color: #86be43;": "                background-color: #0d1117; /* LogBeamOS */",
}
INFORMACOES_UI_TROCAS = {
    '                                <property name="icon-name">linuxmint-logo-filled-ring</property>':
        '                                <property name="icon-name">logbeamos-logo</property>',
}
# The Cinnamon "Backgrounds" settings name each collection after its XML file and keep only the first capital letter:
# the LogBeamOS background (logbeamos.xml, tools 0.3.24) would be listed as "Logbeamos" (author's decision of
# 18/11/2026: show "LogBeamOS"). A Cinnamon update puts the original line back, so it is applied with the identity.
FUNDOS = "usr/share/cinnamon/cinnamon-settings/modules/cs_backgrounds.py"
_NOME_COLECCAO = ('                    display_name = i.replace(".xml", "").replace("-", " ").replace("_", " ")'
                  '.split(" ")[-1].capitalize()')
FUNDOS_TROCAS = {_NOME_COLECCAO: _NOME_COLECCAO + '.replace("Logbeamos", "LogBeamOS")  # LogBeamOS'}


def versao_sistema(raiz="/"):
    try:
        with open(os.path.join(raiz, VERSAO_SISTEMA), encoding="utf-8") as f:
            v = f.read().strip()
    except OSError:
        return None
    # Since 0.9.0 (author, 21/11/2026) the updates after an image are numbered from it: 0.9.0-1, 0.9.0-2, ...
    return v if re.fullmatch(r"\d+(\.\d+)+(-\d+)?", v) else None


def versao_update(raiz="/"):
    try:
        with open(os.path.join(raiz, VERSAO_UPDATE), encoding="utf-8") as f:
            v = f.read().strip()
    except OSError:
        return None
    return v if re.fullmatch(r"\d+(\.\d+)+(-\d+)?([~+][\w.]+)?", v) else None


def versoes_logbeamos():
    """'LogBeamOS 0.3.17 · LogBeamOS Update 0.3.23' (what the Update window shows under its title), or '' if unknown.
    Since 0.9.0 LogBeamOS has a single version number (system = LogBeamOS Update): then only 'LogBeamOS 0.9.0'."""
    s, u = versao_sistema(), versao_update()
    if s and s == u:
        return f"LogBeamOS {s}"
    return " · ".join(x for x in (f"LogBeamOS {s}" if s else "", f"LogBeamOS Update {u}" if u else "") if x)


def _caminho_real(raiz, relativo):
    """Follows a symbolic link inside raiz (/etc/os-release points to ../usr/lib/os-release)."""
    p = os.path.join(raiz, relativo)
    for _ in range(8):
        if not os.path.islink(p):
            return p
        alvo = os.readlink(p)
        p = os.path.join(raiz, alvo.lstrip("/")) if alvo.startswith("/") else os.path.normpath(
            os.path.join(os.path.dirname(p), alvo))
    return p


def _troca_linhas(caminho, trocas):
    """trocas: {line that starts with this: new line}. Only lines that exist are replaced; the file is written only
    if it changes, keeping its permissions. Returns True when it changed."""
    try:
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
    except OSError:
        return False
    linhas = texto.split("\n")
    novas = []
    for l in linhas:
        for inicio, nova in trocas.items():
            if l.startswith(inicio):
                l = nova
                break
        novas.append(l)
    novo = "\n".join(novas)
    if novo == texto:
        return False
    tmp = caminho + ".logbeamos-novo"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(novo)
    shutil.copymode(caminho, tmp)
    os.replace(tmp, caminho)
    return True


def identidade(raiz="/"):
    """Applies the LogBeamOS identity. Returns what changed: 'descricao', 'versao', 'grub' (the GRUB title: an installed
    system then needs update-grub), 'instalador', 'informacoes' (the "System information" screen) and 'fundos' (the
    name of the LogBeamOS collection in the Cinnamon "Backgrounds" settings)."""
    v = versao_sistema(raiz)
    if not v:
        return []
    mudou = []
    if _troca_linhas(os.path.join(raiz, "etc/lsb-release"), {"DISTRIB_DESCRIPTION=": f'DISTRIB_DESCRIPTION="LogBeamOS {v}"'}) | \
            _troca_linhas(_caminho_real(raiz, "etc/os-release"), {"PRETTY_NAME=": f'PRETTY_NAME="LogBeamOS {v}"'}):
        mudou.append("descricao")
    if _troca_linhas(os.path.join(raiz, "etc/logbeamos-release"), {"VERSION=": f'VERSION="{v}"'}):
        mudou.append("versao")
    if _troca_linhas(os.path.join(raiz, "etc/linuxmint/info"), {"GRUB_TITLE=": f"GRUB_TITLE=LogBeamOS v{v}"}):
        mudou.append("grub")
    if _troca_linhas(os.path.join(raiz, INSTALADOR), {a: MINIMO_50GB for a in MINIMOS_ANTIGOS}):
        mudou.append("instalador")
    if _troca_linhas(os.path.join(raiz, INFORMACOES), INFORMACOES_TROCAS) | \
            _troca_linhas(os.path.join(raiz, INFORMACOES_UI), INFORMACOES_UI_TROCAS):
        mudou.append("informacoes")
    if _troca_linhas(os.path.join(raiz, FUNDOS), FUNDOS_TROCAS):
        mudou.append("fundos")
    return mudou


# --- Instalação (só no ajudante, como root)
def descarrega(asset, pasta, registo):
    """Descarrega e confere o SHA-256. Vai dizendo à janela o progresso, como o apt ("@baixar …", ver actualizar-raiz)."""
    import time
    destino = os.path.join(pasta, asset["name"])
    p = urllib.request.Request(asset["browser_download_url"], headers={"User-Agent": AGENTE})
    h = hashlib.sha256()
    with urllib.request.urlopen(p, timeout=60) as r, open(destino, "wb") as f:
        total = int(r.headers.get("Content-Length") or asset.get("size") or 0)
        feito, inicio, enviado = 0, time.monotonic(), 0.0
        while True:
            b = r.read(1 << 18)
            if not b:
                break
            h.update(b)
            f.write(b)
            feito += len(b)
            agora = time.monotonic()
            if agora - enviado >= 0.25:
                enviado = agora
                vel = int(feito / (agora - inicio)) if agora > inicio else -1
                eta = int((total - feito) / vel) if vel > 0 and total else -1
                pct = 100 * feito / total if total else 0
                registo(f"@baixar {pct:.1f} {feito} {total or -1} {vel} {eta} 1 1 {asset['name']}")
    soma = (asset.get("digest") or "").removeprefix("sha256:")
    if soma:
        if soma != h.hexdigest():
            raise RuntimeError(f"SHA-256 não confere: {asset['name']}")
        registo(f"SHA-256 verificado: {asset['name']}")
    else:
        registo(f"Sem SHA-256 publicado: {asset['name']} {h.hexdigest()}")
    return destino


def extrai_appimage(ficheiro, alvo):
    """Extrai o AppImage sem o executar: o sistema de ficheiros começa onde acaba o ELF."""
    with open(ficheiro, "rb") as f:
        d = f.read(64)
    inicio = struct.unpack("<Q", d[40:48])[0] + struct.unpack("<H", d[58:60])[0] * struct.unpack("<H", d[60:62])[0]
    novo = alvo + ".novo"
    shutil.rmtree(novo, ignore_errors=True)
    subprocess.run(["unsquashfs", "-q", "-n", "-d", novo, "-o", str(inicio), ficheiro], check=True,
                   stdout=subprocess.DEVNULL)
    subprocess.run(["chmod", "-R", "a+rX", novo], check=True)
    velho = alvo + ".velho"
    shutil.rmtree(velho, ignore_errors=True)
    if os.path.exists(alvo):
        try:
            os.rename(alvo, velho)
        except OSError as e:
            # On the pen the old folder may come from the system image (overlayfs), and a directory from there
            # cannot be renamed (EXDEV). The new version is already complete in .novo, so the old one is removed
            # instead (tools 0.3.23, 16/11/2026: Decodium did not update on the pen).
            if e.errno != errno.EXDEV:
                raise
            shutil.rmtree(alvo)
    os.rename(novo, alvo)
    shutil.rmtree(velho, ignore_errors=True)


def extrai_makeself(ficheiro, alvo, pasta):
    """Instalador Makeself (wfview): o arquivo começa depois do cabeçalho; lá dentro está um AppImage."""
    with open(ficheiro, "rb") as f:
        texto = f.read(200000).decode("latin-1")
    m = re.search(r'head -n (\d+) "\$\{?0', texto) or re.search(r"head -n (\d+)", texto)
    linhas = int(m.group(1)) if m else 714
    with open(ficheiro, "rb") as f:
        for _ in range(linhas):
            f.readline()
        x = os.path.join(pasta, "makeself")
        os.makedirs(x, exist_ok=True)
        with tarfile.open(fileobj=f, mode="r|*") as t:
            t.extractall(x, filter="data")
    app = [p for p in glob.glob(os.path.join(x, "**", "*.AppImage"), recursive=True)]
    if not app:
        raise RuntimeError("AppImage não encontrado no instalador")
    extrai_appimage(app[0], alvo)


def instala_github(item, registo):
    chave, nome, _, _, _, tipo, alvo = item
    versao, asset = info_github(item)
    if not asset:
        raise RuntimeError("publicação sem ficheiro para Linux")
    with tempfile.TemporaryDirectory(prefix="lb-actualizar-") as pasta:
        f = descarrega(asset, pasta, registo)
        if tipo == "deb":
            os.chmod(pasta, 0o755)
            os.chmod(f, 0o644)
            r = subprocess.run(["apt-get", "install", "-y", "-q", f], capture_output=True, text=True,
                               env=dict(os.environ, DEBIAN_FRONTEND="noninteractive"))
            registo(r.stdout[-2000:])
            if r.returncode:
                raise RuntimeError(r.stderr.strip()[-300:])
        elif tipo == "appimage":
            extrai_appimage(f, alvo)
        elif tipo == "flatpak":
            instala_flatpak(f, alvo, pasta, registo)
        elif tipo == "fonte":
            instala_fonte(f, alvo, pasta, registo)
        else:
            extrai_makeself(f, alvo, pasta)
    grava_estado(chave, versao)
    return versao


def instala_flatpak(ficheiro, alvo, pasta, registo):
    """Flatpak dentro de um .zip (qdmr): instala-se para todos os utilizadores. Um flatpak avulso não se instala por
    cima de outro (nem com --reinstall nem com --or-update, flatpak 1.14): primeiro garante-se a base que a versão nova
    pede, depois sai a anterior (as definições do utilizador ficam) e entra a nova. As regras USB dos cabos de
    programação vêm no próprio flatpak (files/OFF) e copiam-se para o sistema, que o flatpak não o faz."""
    import zipfile
    with zipfile.ZipFile(ficheiro) as z:
        nomes = [n for n in z.namelist() if n.endswith(".flatpak")]
        if len(nomes) != 1:
            raise RuntimeError("arquivo sem o ficheiro .flatpak")
        bundle = os.path.join(pasta, "programa.flatpak")
        with z.open(nomes[0]) as o, open(bundle, "wb") as d:
            shutil.copyfileobj(o, d)
    env = dict(os.environ, LC_ALL="C")

    def flatpak(*args):
        r = subprocess.run(["flatpak", *args], capture_output=True, text=True, env=env)
        registo((r.stdout + r.stderr)[-2000:])
        if r.returncode:
            raise RuntimeError((r.stderr.strip() or "flatpak " + args[0]).splitlines()[-1])

    with open(bundle, "rb") as f:
        m = re.search(rb"\nruntime=([\w.\-]+/[\w.\-]+/[\w.\-]+)\n", f.read(1 << 20))
    base = "runtime/" + m.group(1).decode() if m else None
    if base and not os.path.isdir("/var/lib/flatpak/" + base):
        flatpak("install", "--system", "-y", "--noninteractive", "flathub", base)
    # Ao sair a versão anterior, o flatpak apagaria também a base (1,5 GB com as extensões), por já não ter quem a
    # use: fica fixada durante a troca
    if base:
        flatpak("pin", "--system", base)
    try:
        if os.path.isdir(f"/var/lib/flatpak/app/{alvo}"):
            flatpak("uninstall", "--system", "-y", "--noninteractive", alvo)
        flatpak("install", "--system", "-y", "--noninteractive", "--bundle", bundle)
    finally:
        if base:
            flatpak("pin", "--system", "--remove", base)
    flatpak("uninstall", "--system", "-y", "--noninteractive", "--unused")  # a base antiga, se a nova mudou
    regras = glob.glob(f"/var/lib/flatpak/app/{alvo}/current/active/files/OFF/*.rules")
    if regras:  # de.darc.dm3mat.qdmr → /etc/udev/rules.d/60-qdmr.rules (o mesmo nome que o pacote antigo do sistema usava)
        shutil.copyfile(regras[0], f"/etc/udev/rules.d/60-{alvo.rsplit('.', 1)[-1]}.rules")
        subprocess.run(["udevadm", "control", "--reload-rules"], capture_output=True)


def instala_fonte(ficheiro, alvo, pasta, registo):
    """4ham: troca o código pelo da versão nova e mantém o que é do utilizador (base de dados e exportações em data/,
    registos, .env, config/direwolf.conf) e o ambiente Python, que só recebe as dependências novas."""
    x = os.path.join(pasta, "fonte")
    os.makedirs(x)
    with tarfile.open(ficheiro) as t:
        t.extractall(x, filter="data")
    pastas = [e.path for e in os.scandir(x) if e.is_dir()]
    if len(pastas) != 1 or not os.path.isfile(os.path.join(pastas[0], "backend", "requirements.txt")):
        raise RuntimeError("arquivo do 4ham com estrutura inesperada")
    nova = pastas[0]
    st = os.stat(alvo)
    servico_utilizador(st.st_uid, "stop", SERVICO_4HAM)
    subprocess.run(["rsync", "-a", "--delete", "--exclude=/data/", "--exclude=/logs/", "--exclude=/.env",
                    "--exclude=/.venv/", "--exclude=/config/direwolf.conf", nova + "/", alvo + "/"], check=True)
    subprocess.run(["rsync", "-a", nova + "/data/", alvo + "/data/"], check=True)  # ficheiros novos de data/, sem apagar
    py = os.path.join(alvo, ".venv", "bin", "python")
    r = subprocess.run([py, "-m", "pip", "install", "-q", "--no-cache-dir", "--disable-pip-version-check",
                        "-r", os.path.join(alvo, "backend", "requirements.txt")], capture_output=True, text=True)
    registo((r.stdout + r.stderr)[-2000:])
    if r.returncode:
        raise RuntimeError("dependências do 4ham: " + (r.stderr.strip().splitlines() or ["pip"])[-1])
    subprocess.run(["chown", "-R", f"{st.st_uid}:{st.st_gid}", alvo], check=True)
    registo("4ham: dados e definições mantidos; se estava ligado, volte a abri-lo")


def servico_utilizador(uid, accao, unidade):
    """Pára ou reinicia um serviço da sessão do utilizador (se a sessão estiver aberta)."""
    import pwd
    run = f"/run/user/{uid}"
    if not os.path.isdir(run):
        return
    try:
        nome = pwd.getpwuid(uid).pw_name
    except KeyError:
        return
    subprocess.run(["runuser", "-u", nome, "--", "env", f"XDG_RUNTIME_DIR={run}", "systemctl", "--user", accao, unidade],
                   capture_output=True)
