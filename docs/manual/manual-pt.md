<!--
  Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
  © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
  Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
-->

# Manual do LogBeamOS

*Distribuição Linux para radioamadores*

Este é o manual que acompanha o LogBeamOS (ferramentas 0.3.14).

**Português** · [English](manual-en.md) · [Español](manual-es.md) · [Français](manual-fr.md)

- [1. Primeiros passos](#1-primeiros-passos)
- [2. Ligar o rádio](#2-ligar-o-rádio)
- [3. Que programa para quê](#3-que-programa-para-quê)
- [4. Actualizar](#4-actualizar)
- [5. Ao lado do Windows](#5-instalar-ao-lado-do-windows)
- [6. Problemas comuns](#6-problemas-comuns)

## 1. Primeiros passos

- O LogBeamOS arranca da pen sem instalar nada no computador. No primeiro arranque é perguntado se quer um utilizador e uma password próprios; sem eles, a sessão abre sozinha.
- O que fizer na pen (definições, registos, ficheiros) fica guardado nela e continua lá no arranque seguinte.
- No ambiente de trabalho: a pasta **Programas Radioamador** (todos os programas), **Rádio e Equipamento**, **Actualizar LogBeamOS**, **LogBeam Uplink** e este manual. Os programas estão também no menu, no grupo *Rádio Amador*.
- Para desligar: menu → botão vermelho. Não retire a pen com o LogBeamOS ligado.

## 2. Ligar o rádio

1. **Ligue o rádio por USB.** Na maior parte dos rádios não é preciso instalar nenhum controlador: o Linux já o tem.
2. **Abra o Rádio e Equipamento.** Aparecem o rádio, a porta do CAT, a placa de som do rádio e a COM correspondente para o N1MM+ e o Log4OM.
3. **Testar CAT:** escolha o modelo; com a velocidade *Automática*, é procurada a velocidade a que o rádio responde. O teste só lê a frequência: nunca transmite.
4. **Configurar os programas…:** escolha o rádio na lista e carregue em *Configurar*. O WSJT-X, o JTDX, o Fldigi, o Not1MM e o Direwolf ficam a usar o rádio ao mesmo tempo, com o som do rádio e o PTT pelo CAT. Antes de mudar, é guardada uma cópia da configuração de cada programa.
5. **N1MM+ e Log4OM:** nas definições de CAT de cada um, escolha a COM indicada no Rádio e Equipamento. Enquanto o N1MM+ estiver aberto, os outros programas ficam sem CAT; quando fecha, voltam a tê-lo.

> A velocidade do CAT tem de ser a mesma no menu do rádio (por exemplo, *CAT RATE* nos Yaesu).

## 3. Que programa para quê

| Para… | Programa |
|---|---|
| FT8, FT4, WSPR | WSJT-X ou JTDX · com FT2: Decodium · mapa das estações ouvidas: GridTracker2 |
| Mensagens por teclado em sinal fraco | JS8Call |
| RTTY, PSK, Olivia e outros modos digitais | Fldigi (com Flrig, Flmsg e Flamp) |
| Concursos | N1MM+ (o do Windows, através do Wine) ou Not1MM |
| Registo de contactos (logbook) | Log4OM (através do Wine), CQRLOG ou KLog · envio para o logbeam.org: LogBeam Uplink · envio para o Wavelog: WaveLogGate |
| APRS | Direwolf (o modem pela placa de som) e Xastir (o mapa); o Xastir abre o Direwolf sozinho e liga-se a ele |
| Winlink (correio por rádio) | Pat |
| Satélites | Gpredict (previsões e seguimento) · imagens de satélites meteorológicos: SatDump |
| Receptores SDR | Gqrx ou SDR++ · experiências: GNU Radio |
| Voz digital e imagem | FreeDV · SSTV: QSSTV |
| Rádios Icom e Kenwood à distância | wfview |
| Programação de rádios DMR | qdmr |
| DMR sem rádio (BrandMeister) | VoxDMR (opcional: instala-se pelo *Actualizar LogBeamOS*; pede o ID DMR e a password de hotspot do BrandMeister) |
| EchoLink | Qtel (o router tem de deixar passar as portas UDP 5198–5199 e TCP 5200, ou use um proxy EchoLink) |
| Simulação de antenas | xnec2c |
| Análise das bandas | 4ham Spectrum Analysis |

> No Xastir, antes de transmitir: indique o seu indicativo (o Xastir pergunta-o na primeira vez), mude o *MYCALL* no ficheiro `direwolf.conf` da pasta pessoal e ligue a transmissão em *Interfaces*. Por omissão, o Xastir só recebe.

## 4. Actualizar

- O **Actualizar LogBeamOS** mostra os programas de rádio e o sistema operativo, com a versão instalada, a disponível e o tamanho a descarregar.
- As ferramentas do LogBeamOS (este Actualizar, o **Rádio e Equipamento** e este manual) e o **LogBeam Uplink** também se actualizam aqui. Vêm do repositório do LogBeamOS em logbeam.org, que é assinado.
- Marque o que quer actualizar. Cada programa tem a sua caixa; o *Sistema operativo* abre-se na seta e cada pacote também se escolhe. Atalhos: *Rádio*, *Sistema*, *Tudo*, *Nada*.
- Carregue em *Actualizar os marcados*. Durante a actualização é mostrado o que está a ser descarregado, os MB, a velocidade e o tempo que falta.
- O N1MM+, o Log4OM e o GridTracker2 actualizam-se sozinhos.
- Na pen não é pedida password; no LogBeamOS instalado, é pedida a do utilizador.
- Dez minutos depois de entrar na sessão, se houver actualizações, aparece um aviso.

## 5. Instalar ao lado do Windows

### Antes, no Windows

1. **Copie os seus dados.**
2. **Corra o "Preparar o Windows.cmd"** com o botão direito → *Executar como administrador*. Está na unidade LOGBEAMOS que a pen mostra no Windows, e também na raiz da ISO (duplo clique na ISO). A pen mostra também uma unidade pequena, de 5 MB, com as pastas "boot" e "EFI": não mexa nela, porque a pen precisa dela para arrancar. Desliga o arranque rápido e, se o disco C: estiver encriptado, começa a desencriptação; antes de instalar, espere que a percentagem encriptada chegue a 0 %. Também se pode fazer à mão: *Antes de instalar*.

### Instalar

3. Arranque pela pen e abra *Instalar LogBeamOS*. No tipo de instalação, escolha instalar ao lado do Windows e arraste a divisória: 40 GB chegam para o LogBeamOS.
4. Depois, ao ligar o computador, aparece durante 10 segundos um menu com o LogBeamOS e o Windows. É lembrada a última escolha.

### Retirar o LogBeamOS

5. No Windows, numa consola de administrador: `bcdedit /set {fwbootmgr} displayorder {bootmgr} /addfirst`. O computador passa a arrancar directamente no Windows.
6. Gestão de Discos: apague as partições do LogBeamOS (as que estão a seguir ao C: e não têm letra; nunca a partição EFI nem a de recuperação). Depois, botão direito no C: → *Expandir volume*.
7. Opcional, para apagar também o arranque do LogBeamOS, na mesma consola:
   - `bcdedit /enum firmware` mostra as entradas de arranque; apague as que têm `\EFI\ubuntu` no caminho com `bcdedit /delete {identificador}`;
   - `mountvol S: /S` e `rmdir /S /Q S:\EFI\ubuntu`;
   - se existir `S:\EFI\Boot\fbx64.efi`, o instalador trocou o arranque de recurso do disco: `copy /Y S:\EFI\Microsoft\Boot\bootmgfw.efi S:\EFI\Boot\bootx64.efi` e `del S:\EFI\Boot\fbx64.efi S:\EFI\Boot\mmx64.efi`;
   - no fim, `mountvol S: /D`.

## 6. Problemas comuns

**A pen não arranca: "Unable to find a medium containing a live file system"**  
Retire a pen, espere 5 segundos, volte a ligá-la e arranque de novo.

**O Windows pede para formatar a pen**  
Cancele sempre. É a parte da pen onde ficam os seus dados do LogBeamOS, que o Windows não sabe ler.

**Um programa ficou preso**  
Abra o Monitor do sistema (ícone na barra), separador *Processos*, botão direito no programa → *Terminar*.

**O ambiente de trabalho foi abaixo ("modo de recurso")**  
Carregue em Ctrl+Alt+Esc para o reiniciar, ou termine a sessão e volte a entrar.

**O rádio não responde ao CAT**  
No Rádio e Equipamento, confirme o modelo e use a velocidade *Automática*; confirme que o CAT está ligado no menu do rádio e feche os programas que estejam a usar a porta.

**Sem som do rádio no WSJT-X ou no Direwolf**  
No Rádio e Equipamento → *Configurar os programas…*, escolha o som do rádio.

**O Direwolf fecha-se logo**  
A janela fica aberta com a explicação. A configuração está no ficheiro `direwolf.conf` da pasta pessoal.
