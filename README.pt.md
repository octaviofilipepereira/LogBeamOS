<p align="center"><img src="usr/share/logbeamos/manual/logbeam.png" width="96" alt="LogBeamOS"></p>

<h1 align="center">LogBeamOS</h1>

<p align="center"><b>LogBeamOS, a distribuição Linux para radioamadores.</b></p>

<p align="center">
  <a href="https://logbeam.org"><img alt="logbeam.org" src="https://img.shields.io/badge/site-logbeam.org-2f81f7"></a>
  <img alt="Linux Mint 22" src="https://img.shields.io/badge/base-Linux%20Mint%2022-87cf3e">
  <a href="https://www.gnu.org/licenses/gpl-3.0.html"><img alt="Licença GPL v3" src="https://img.shields.io/badge/licen%C3%A7a-GPL%20v3-blue"></a>
</p>

<p align="center"><b>Português</b> · <a href="README.md">English</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a></p>

---

O LogBeamOS é uma distribuição para radioamadores, baseada no Linux Mint. Arranca de uma pen, guardando os dados, ou instala-se ao lado do Windows, já com os programas de radioamador instalados: programas nativos de Linux e, através do Wine, o N1MM Logger+ e o Log4OM.

Esses programas são dos respectivos autores e vêm dos sítios habituais: os repositórios do Linux Mint e do Ubuntu, as publicações dos próprios autores e o Flathub. **Este repositório tem só o que foi escrito para o LogBeamOS**: as ferramentas abaixo. O LogBeam Uplink, que envia os QSOs para o [LogBeam](https://logbeam.org), tem repositório próprio: [LogBeam-Uplink](https://github.com/octaviofilipepereira/LogBeam-Uplink).

## As ferramentas

| Ferramenta | O que faz |
|---|---|
| **Actualizar LogBeamOS** | Uma janela para actualizar os programas de radioamador e o sistema operativo. Mostra a versão instalada, a disponível e o tamanho a descarregar, e actualiza só o que estiver marcado, com o progresso em MB, a velocidade e o tempo que falta. Abrange os pacotes do sistema, os programas publicados no GitHub (WSJT-X, JS8Call, wfview, SatDump, SDR++, Decodium, qdmr e outros), o Not1MM e as próprias ferramentas do LogBeamOS. Dez minutos depois de entrar na sessão, aparece um aviso se houver actualizações. |
| **Rádio e Equipamento** | Detecta rádios, cabos de CAT, placas de som e receptores SDR. Partilha o rádio entre os programas através do `rigctld` do Hamlib, com detecção automática da velocidade, e configura o WSJT-X, o JTDX, o Decodium, o Fldigi, o Not1MM e o Direwolf para o usarem. |
| **Manual do LogBeamOS** | Primeiros passos, ligar o rádio, que programa para quê, actualizar, instalar ao lado do Windows e retirar o LogBeamOS. Em janela própria, na língua da sessão. |
| **Lançadores** | O N1MM Logger+ através do Wine, a receber o rádio partilhado enquanto está aberto; o Direwolf, com uma configuração criada se faltar; o Xastir, ligado ao Direwolf. |

Todas as janelas estão em português, inglês, espanhol e francês.

## Instalar e actualizar

As ferramentas vêm com o LogBeamOS. São distribuídas pelo repositório apt do LogBeamOS, em `https://logbeam.org/apt`, que traz também o LogBeam Uplink. No LogBeamOS, actualizam-se pelo **Actualizar LogBeamOS**, como qualquer outro programa.

O índice do repositório é assinado. Impressão digital da chave:

```
A6D0 1419 9FF3 D8B0 4D6D  000A 9621 41CF 2D04 1E07
```

Para juntar o repositório à mão no Linux Mint 22 ou no Ubuntu 24.04:

```sh
sudo curl -fsSL -o /usr/share/keyrings/logbeamos.gpg https://logbeam.org/apt/logbeamos.gpg
printf 'Types: deb\nURIs: https://logbeam.org/apt/\nSuites: ./\nSigned-By: /usr/share/keyrings/logbeamos.gpg\n' \
  | sudo tee /etc/apt/sources.list.d/logbeamos.sources
sudo apt update
sudo apt install logbeamos-ferramentas
```

As ferramentas foram feitas para o LogBeamOS. Noutro sistema, as partes que dependem dos programas que o LogBeamOS instala (o WSJT-X em `/opt/ham`, o N1MM+ no Wine, etc.) não funcionam.

## Organização do repositório

Cada ficheiro está na pasta onde é instalado:

| Pasta | Conteúdo |
|---|---|
| `usr/local/bin/` | Os programas: `logbeamos-actualizar`, `logbeamos-equipamento`, `logbeamos-manual` e os lançadores |
| `usr/local/lib/logbeamos/` | O que o Actualizar (`actualizar/`) e o Rádio e Equipamento (`equipamento/`) usam |
| `usr/share/logbeamos/` | Os ícones e o manual nas quatro línguas |
| `usr/local/share/applications/` | As entradas do menu |
| `usr/share/polkit-1/actions/` | A autorização do ajudante do Actualizar, que corre como administrador |
| `etc/` | O aviso de actualizações ao entrar na sessão e a regra que afasta os receptores RTL-SDR do controlador de TV do Linux |

As ferramentas estão escritas em Python 3 com GTK 3; a janela do manual usa o WebKitGTK.

## Contribuir e segurança

As contribuições são bem-vindas: ver o [CONTRIBUTING.md](CONTRIBUTING.md). As falhas de segurança comunicam-se em privado: ver o [SECURITY.md](SECURITY.md).

## Licença

As ferramentas do LogBeamOS são software livre, distribuído com a [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). O texto completo está no ficheiro [LICENSE](LICENSE).

## Exclusão de responsabilidade

- As ferramentas do LogBeamOS são distribuídas sem qualquer garantia, nos termos da GPL v3 (secções 15 e 16). O autor não é responsável por danos ou perdas resultantes do seu uso, seja na versão oficial, seja numa versão modificada.
- Quem modificar e distribuir uma versão é o único responsável por ela.
- As versões oficiais são só as distribuídas pelo repositório em `https://logbeam.org/apt`, assinadas com a chave acima.

## Autor

Octávio Filipe Pereira Gonçalves, CT7BFV · [logbeam.org](https://logbeam.org)
