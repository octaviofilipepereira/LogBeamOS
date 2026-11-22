<!--
  Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
  © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
  Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
-->

# Manual do LogBeamOS

*Distribuição Linux para radioamadores*

Este é o manual que acompanha o LogBeamOS (LogBeamOS Update 0.9.0-1).

**Português** · [English](manual-en.md) · [Español](manual-es.md) · [Français](manual-fr.md)

- [1. Primeiros passos](#1-primeiros-passos)
- [2. Ligar o rádio](#2-ligar-o-rádio)
- [3. Que programa para quê](#3-que-programa-para-quê)
- [4. Actualizar](#4-actualizar)
- [5. Ao lado do Windows](#5-instalar-ao-lado-do-windows)
- [6. Problemas comuns](#6-problemas-comuns)
- [7. Relatar um problema](#7-relatar-um-problema)

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
5. **N1MM+ e Log4OM:** no mesmo ecrã, escolha como cada um usa o rádio. *Só o N1MM+ (ou o Log4OM) usa o rádio*: o programa fala directamente com o rádio; enquanto estiver aberto, os outros programas ficam sem CAT e, quando fecha, voltam a tê-lo. *Usa o rádio com os outros programas*: todos usam o rádio ao mesmo tempo; o N1MM+ passa a ver um «Kenwood TS-2000» e as funções próprias do seu rádio podem não funcionar. A escolha pode ser mudada quando quiser, voltando a *Configurar os programas…*. O Log4OM tem de ser aberto uma vez antes de poder ser configurado.

> A velocidade do CAT tem de ser a mesma no menu do rádio (por exemplo, *CAT RATE* nos Yaesu).

## 3. Que programa para quê

| Para… | Programa |
|---|---|
| FT8, FT4, WSPR | WSJT-X ou JTDX · com FT2: Decodium · mapa das estações ouvidas: GridTracker2 |
| Mensagens por teclado em sinal fraco | JS8Call |
| RTTY, PSK, Olivia e outros modos digitais | Fldigi (com Flrig, Flmsg e Flamp) |
| Concursos | N1MM+ (o do Windows, através do Wine) ou Not1MM |
| Registo de contactos (logbook) | Log4OM (através do Wine), CQRLOG ou KLog · envio para o logbeam.org: LogBeam Uplink · envio para o Wavelog: WaveLogGate |
| Confirmações no Logbook of The World (LoTW) | TQSL, da ARRL: assina os QSOs e envia-os para o LoTW |
| APRS | Direwolf (o modem pela placa de som) e Xastir (o mapa); o Xastir abre o Direwolf sozinho e liga-se a ele |
| Winlink (correio por rádio) | Pat |
| Satélites | Gpredict (previsões e seguimento) · imagens de satélites meteorológicos: SatDump |
| Receptores SDR | Gqrx ou SDR++ · experiências: GNU Radio |
| Voz digital e imagem | FreeDV · SSTV: QSSTV |
| Rádios Icom e Kenwood à distância | wfview |
| Programação de rádios DMR | qdmr |
| DMR sem rádio (BrandMeister) | VoxDMR (opcional: instala-se pelo *Actualizar LogBeamOS*; pede o ID DMR e a password de hotspot do BrandMeister) |
| EchoLink | Qtel (o router tem de deixar passar as portas UDP 5198–5199 e TCP 5200, ou use um proxy EchoLink) |
| WIRES-X (Yaesu) | WIRES-X, através do Wine. Não vem com o LogBeamOS: descarregue-o no site WIRES-X da Yaesu (é preciso entrar com o seu ID), abra o *WIRES-X* e indique o ficheiro .zip descarregado. Depois é indicada a porta COM da HRI-200 ou do rádio (modo PDN), para escolher no ecrã *COM port setting* do WIRES-X. |
| Simulação de antenas | xnec2c |
| Análise de espectro e análises académicas do espectro radioeléctrico | 4ham Spectrum Analysis |

> No Xastir, antes de transmitir: indique o seu indicativo (o Xastir pergunta-o na primeira vez), mude o *MYCALL* no ficheiro `direwolf.conf` da pasta pessoal e ligue a transmissão em *Interfaces*. Por omissão, o Xastir só recebe.

## 4. Actualizar

- O **Actualizar LogBeamOS** mostra os programas de rádio e o sistema operativo, com a versão instalada, a disponível e o tamanho a descarregar.
- O **LogBeamOS Update** (este Actualizar, o **Rádio e Equipamento** e este manual) e o **LogBeam Uplink** também se actualizam aqui. Vêm do repositório do LogBeamOS em logbeam.org, que é assinado. A versão do LogBeamOS e a do LogBeamOS Update aparecem no topo da janela.
- Também actualiza as aplicações Flatpak e as extensões do Cinnamon. No LogBeamOS instalado no disco, retira os núcleos (kernels) antigos: ficam o que está em uso e o mais recente.
- Cada versão nova do LogBeamOS chega também por aqui, sem ser preciso reinstalar. Só o que faz parte do arranque da pen exige gravá-la de novo. As novidades de cada versão estão em [logbeam.org/logbeamos/novidades](https://logbeam.org/logbeamos/novidades/).
- Marque o que quer actualizar. Cada programa tem a sua caixa; o *Sistema operativo* abre-se na seta e cada pacote também se escolhe. Atalhos: *Rádio*, *Sistema*, *Tudo*, *Nada*.
- Carregue em *Actualizar os marcados*. Durante a actualização é mostrado o que está a ser descarregado, os MB, a velocidade e o tempo que falta.
- O N1MM+, o Log4OM e o GridTracker2 actualizam-se sozinhos.
- Na pen não é pedida password; no LogBeamOS instalado, é pedida a do utilizador.
- Dez minutos depois de entrar na sessão, se houver actualizações, aparece um aviso.

## 5. Instalar ao lado do Windows

### Antes, no Windows

1. **Copie os seus dados.**
2. **Corra o "Preparar o Windows.cmd"** com o botão direito → *Executar como administrador*. Está na raiz da ISO: no Windows, faça duplo clique no ficheiro ISO para a abrir. Desliga o arranque rápido e, se o disco C: estiver encriptado, começa a desencriptação; antes de instalar, espere que a percentagem encriptada chegue a 0 %. Também se pode fazer à mão: *Antes de instalar*.

### Instalar

3. Arranque pela pen e abra *Instalar LogBeamOS*. No tipo de instalação, escolha instalar ao lado do Windows e arraste a divisória para dar ao LogBeamOS pelo menos 50 GB; o instalador não aceita menos.
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

**N1MM+: "The given port name is invalid… not a serial port" ou "Radio … is not responding"**  
A porta COM escolhida no N1MM+ não é a do cabo do rádio. No Rádio e Equipamento, carregue em *Configurar os programas…* e escolha como o N1MM+ usa o rádio: a porta certa é escrita no N1MM+. A COM de cada cabo aparece no Rádio e Equipamento ("no N1MM+ e no Log4OM: COM…").

**O LogBeam Uplink avisa "a porta 2333 está ocupada por outro programa"**  
Normalmente é o WaveLogGate, que também recebe QSOs nessa porta. O LogBeamOS passa o WaveLogGate para a porta 2335 ao entrar na sessão; se a voltou a pôr em 2333, mude-a no WaveLogGate: *Configuration* → *Advanced* → *UDP Port* 2335 → *Save*. Depois feche e abra o LogBeam Uplink. Se algum programa enviava QSOs para o WaveLogGate, mude nele a porta de destino para 2335.

**WaveLogGate: "HTTPS/WSS require a trusted certificate"**  
O LogBeamOS põe o certificado do WaveLogGate no Firefox sozinho, sem password, logo que o WaveLogGate o cria: não é preciso carregar em *Install Certificate*. Se o aviso continuar, feche o WaveLogGate e abra-o de novo.

**Sem som do rádio no WSJT-X ou no Direwolf**  
No Rádio e Equipamento → *Configurar os programas…*, escolha o som do rádio.

**O Direwolf fecha-se logo**  
A janela fica aberta com a explicação. A configuração está no ficheiro `direwolf.conf` da pasta pessoal.

## 7. Relatar um problema

Quando alguma coisa falhar, um relato com estes três passos chega para se perceber o que aconteceu.

1. **Anote o que aconteceu:** o que estava a fazer, o que esperava e o que apareceu. Se houver uma mensagem de erro, copie o texto ou fotografe o ecrã (tecla *PrtSc*).
2. **Crie o relatório de diagnóstico** logo a seguir à falha, antes de reiniciar: no menu, *Relatório de diagnóstico*; ou, num terminal, `logbeamos-diagnostico`. Fica um ficheiro de texto no ambiente de trabalho. Se o computador bloqueou e teve de ser reiniciado, use `logbeamos-diagnostico --anterior`, que junta também os erros do arranque anterior.
3. **Envie o relato** com o ficheiro em anexo: em [github.com/octaviofilipepereira/LogBeamOS](https://github.com/octaviofilipepereira/LogBeamOS/issues/new/choose), separador *Issues* (é precisa uma conta do GitHub, gratuita).

> O relatório não contém passwords nem chaves, e o nome do utilizador, o nome do computador e os endereços de rede são retirados. Contém as versões, o modelo do computador, os aparelhos USB ligados, a configuração do rádio em cada programa e os avisos e erros do sistema. Pode lê-lo antes de o enviar.
