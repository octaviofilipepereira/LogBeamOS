# Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
# © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
# Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
# LogBeamOS: o que o "Actualizar LogBeamOS" sabe de cada programa: de onde vem, como se lê a versão instalada,
# como se procura a mais recente e como se instala. Usado pela janela (como utilizador) e pelo ajudante (como root).
# O ajudante nunca recebe endereços da janela: procura-os ele próprio, a partir desta tabela.
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
    # Repositório apt do LogBeamOS (https://logbeam.org/apt, desde a 0.3.11): as ferramentas e o Uplink
    "logbeamos-ferramentas": "LogBeamOS", "logbeam-uplink": "LogBeam Uplink",
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


def apt_pendentes(pasta=None):
    """Lista (pacote, instalada, nova) do que o apt actualizaria. Sem root: usa uma cópia própria das listas."""
    env = dict(os.environ, LC_ALL="C")
    if pasta:
        os.makedirs(f"{pasta}/lists/partial", exist_ok=True)
        r = subprocess.run(["apt-get", "-q", *apt_opcoes(pasta), "update"], capture_output=True, text=True, env=env)
        if r.returncode:
            raise RuntimeError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "apt-get update")
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
        os.rename(alvo, velho)
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
