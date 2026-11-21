# WIRES-X · Wine DLLs · LogBeamOS

[English](#english) · [Português](#português) · [Español](#español) · [Français](#français)

---

## English

For **WIRES-X** alone, LogBeamOS brings two DLLs of Wine 11.0 (the Wine of LogBeamOS), each with one correction. The corrections are by **Octávio Filipe Pereira Gonçalves, CT7BFV**. Both errors were found and reported by **Bráulio Sousa, CT7APZ**, in November 2026, with a Yaesu radio and WIRES-X 2.010 on LogBeamOS.

| DLL | Correction | Since | Without it |
|---|---|---|---|
| `wininet.dll` | [wininet-indice.patch](wininet-indice.patch) | LogBeamOS Update 0.3.28 | WIRES-X stayed **OFFLINE** and the ID activation answered "Server or ID Not Found." |
| `msgsm32.acm` | [msgsm32-cbsize.patch](msgsm32-cbsize.patch) | LogBeamOS Update 0.3.29 | WIRES-X closed, without any message, on the first voice frame of a radio in PDN mode |

**wininet.dll.** WIRES-X reads the reply headers of the Yaesu servers with `HttpQueryInfo(HTTP_QUERY_RAW_HEADERS_CRLF)` and an index, adding 1 to the index until the call fails. On Windows the call with an index above 0 fails (`ERROR_HTTP_HEADER_NOT_FOUND`). Wine 11.0 ignored the index for the raw headers and returned them every time, so the loop never ended and WIRES-X never read its first file (`UpdateInfoX_New.bin`). With the correction WIRES-X goes **ONLINE(IPv4)**.

**msgsm32.acm.** WIRES-X converts the voice (PCM 8 kHz, 16 bits, mono) to GSM 6.10 and back with the Audio Compression Manager, and asks for the GSM 6.10 format with `acmFormatSuggest` on a zeroed destination; on Windows the codec fills in the format, `cbSize` included. Wine 11.0's codec refused a destination whose `cbSize` was not already 2, so the conversion was never opened and WIRES-X crashed when it copied the first voice frame into the conversion buffer. With the correction the codec fills in `cbSize` and every conversion opens.

- Files: `usr/local/lib/logbeamos/wires-x/wininet.dll` and `usr/local/lib/logbeamos/wires-x/msgsm32.acm`, built by [construir-dlls.sh](construir-dlls.sh) from the Wine 11.0 source with these two patches only. The "Wine builtin DLL" mark is removed, so that Wine loads them as native DLLs.
- The `wires-x` launcher copies them into the WIRES-X folder of the Wine prefix and starts WIRES-X with `wininet=n,b` and `msgsm32.acm=n,b` in `WINEDLLOVERRIDES`. Every other program keeps the DLLs of the installed Wine.
- Source, as the LGPL asks: `wine-11.0.tar.xz` (SHA-256 `c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701`), `wine-11.0-wininet-indice.patch` and `wine-11.0-msgsm32-cbsize.patch`, in the apt repository (`https://logbeam.org/apt/`). Wine is under the GNU Lesser General Public License, version 2.1 or later.

## Português

Só para o **WIRES-X**, o LogBeamOS traz duas DLLs do Wine 11.0 (o Wine do LogBeamOS), cada uma com uma correcção. As correcções são de **Octávio Filipe Pereira Gonçalves, CT7BFV**. Os dois erros foram descobertos e relatados por **Bráulio Sousa, CT7APZ**, em Novembro de 2026, com um rádio Yaesu e o WIRES-X 2.010 no LogBeamOS.

| DLL | Correcção | Desde | Sem ela |
|---|---|---|---|
| `wininet.dll` | [wininet-indice.patch](wininet-indice.patch) | LogBeamOS Update 0.3.28 | o WIRES-X ficava **OFFLINE** e a activação do ID respondia «Server or ID Not Found.» |
| `msgsm32.acm` | [msgsm32-cbsize.patch](msgsm32-cbsize.patch) | LogBeamOS Update 0.3.29 | o WIRES-X fechava, sem mensagem nenhuma, na primeira trama de voz de um rádio em modo PDN |

**wininet.dll.** O WIRES-X lê os cabeçalhos das respostas dos servidores da Yaesu com `HttpQueryInfo(HTTP_QUERY_RAW_HEADERS_CRLF)` e um índice, somando 1 ao índice até o pedido falhar. No Windows o pedido com índice maior que 0 falha (`ERROR_HTTP_HEADER_NOT_FOUND`). O Wine 11.0 ignorava o índice nos cabeçalhos completos e devolvia-os sempre: o ciclo nunca acabava e o WIRES-X nunca lia o seu primeiro ficheiro (`UpdateInfoX_New.bin`). Com a correcção o WIRES-X fica **ONLINE(IPv4)**.

**msgsm32.acm.** O WIRES-X converte a voz (PCM 8 kHz, 16 bits, mono) para GSM 6.10 e de volta com o Audio Compression Manager, e pede o formato GSM 6.10 com `acmFormatSuggest` sobre um destino a zeros; no Windows é o codec que preenche o formato, `cbSize` incluído. O codec do Wine 11.0 recusava um destino cujo `cbSize` não fosse já 2: a conversão nunca se abria e o WIRES-X ia abaixo ao copiar a primeira trama de voz para o buffer da conversão. Com a correcção o codec preenche o `cbSize` e todas as conversões se abrem.

- Ficheiros: `usr/local/lib/logbeamos/wires-x/wininet.dll` e `usr/local/lib/logbeamos/wires-x/msgsm32.acm`, construídos pelo [construir-dlls.sh](construir-dlls.sh) a partir do código-fonte do Wine 11.0, só com estas duas alterações. Sem a marca «Wine builtin DLL», para o Wine as carregar como DLLs nativas.
- O lançador `wires-x` copia-as para a pasta do WIRES-X no prefixo do Wine e abre o WIRES-X com `wininet=n,b` e `msgsm32.acm=n,b` no `WINEDLLOVERRIDES`. Todos os outros programas continuam com as DLLs do Wine instalado.
- Código-fonte, como pede a LGPL: `wine-11.0.tar.xz` (SHA-256 `c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701`), `wine-11.0-wininet-indice.patch` e `wine-11.0-msgsm32-cbsize.patch`, no repositório apt (`https://logbeam.org/apt/`). O Wine está sob a GNU Lesser General Public License, versão 2.1 ou posterior.

## Español

Solo para **WIRES-X**, LogBeamOS trae dos DLL de Wine 11.0 (el Wine de LogBeamOS), cada una con una corrección. Las correcciones son de **Octávio Filipe Pereira Gonçalves, CT7BFV**. Los dos errores los descubrió y comunicó **Bráulio Sousa, CT7APZ**, en noviembre de 2026, con una radio Yaesu y WIRES-X 2.010 en LogBeamOS.

| DLL | Corrección | Desde | Sin ella |
|---|---|---|---|
| `wininet.dll` | [wininet-indice.patch](wininet-indice.patch) | LogBeamOS Update 0.3.28 | WIRES-X se quedaba **OFFLINE** y la activación del ID respondía «Server or ID Not Found.» |
| `msgsm32.acm` | [msgsm32-cbsize.patch](msgsm32-cbsize.patch) | LogBeamOS Update 0.3.29 | WIRES-X se cerraba, sin ningún mensaje, con la primera trama de voz de una radio en modo PDN |

**wininet.dll.** WIRES-X lee las cabeceras de las respuestas de los servidores de Yaesu con `HttpQueryInfo(HTTP_QUERY_RAW_HEADERS_CRLF)` y un índice, sumando 1 al índice hasta que la llamada falla. En Windows la llamada con un índice mayor que 0 falla (`ERROR_HTTP_HEADER_NOT_FOUND`). Wine 11.0 ignoraba el índice en las cabeceras completas y las devolvía siempre: el bucle no terminaba nunca y WIRES-X nunca leía su primer archivo (`UpdateInfoX_New.bin`). Con la corrección WIRES-X queda **ONLINE(IPv4)**.

**msgsm32.acm.** WIRES-X convierte la voz (PCM 8 kHz, 16 bits, mono) a GSM 6.10 y de vuelta con el Audio Compression Manager, y pide el formato GSM 6.10 con `acmFormatSuggest` sobre un destino a ceros; en Windows es el códec el que rellena el formato, `cbSize` incluido. El códec de Wine 11.0 rechazaba un destino cuyo `cbSize` no fuera ya 2: la conversión nunca se abría y WIRES-X se caía al copiar la primera trama de voz al búfer de la conversión. Con la corrección el códec rellena `cbSize` y todas las conversiones se abren.

- Archivos: `usr/local/lib/logbeamos/wires-x/wininet.dll` y `usr/local/lib/logbeamos/wires-x/msgsm32.acm`, construidos por [construir-dlls.sh](construir-dlls.sh) a partir del código fuente de Wine 11.0, solo con estos dos cambios. Sin la marca «Wine builtin DLL», para que Wine las cargue como DLL nativas.
- El lanzador `wires-x` las copia a la carpeta de WIRES-X en el prefijo de Wine y abre WIRES-X con `wininet=n,b` y `msgsm32.acm=n,b` en `WINEDLLOVERRIDES`. Todos los demás programas siguen con las DLL del Wine instalado.
- Código fuente, como pide la LGPL: `wine-11.0.tar.xz` (SHA-256 `c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701`), `wine-11.0-wininet-indice.patch` y `wine-11.0-msgsm32-cbsize.patch`, en el repositorio apt (`https://logbeam.org/apt/`). Wine está bajo la GNU Lesser General Public License, versión 2.1 o posterior.

## Français

Pour **WIRES-X** seulement, LogBeamOS apporte deux DLL de Wine 11.0 (le Wine de LogBeamOS), chacune avec une correction. Les corrections sont de **Octávio Filipe Pereira Gonçalves, CT7BFV**. Les deux erreurs ont été découvertes et signalées par **Bráulio Sousa, CT7APZ**, en novembre 2026, avec une radio Yaesu et WIRES-X 2.010 sous LogBeamOS.

| DLL | Correction | Depuis | Sans elle |
|---|---|---|---|
| `wininet.dll` | [wininet-indice.patch](wininet-indice.patch) | LogBeamOS Update 0.3.28 | WIRES-X restait **OFFLINE** et l'activation de l'ID répondait « Server or ID Not Found. » |
| `msgsm32.acm` | [msgsm32-cbsize.patch](msgsm32-cbsize.patch) | LogBeamOS Update 0.3.29 | WIRES-X se fermait, sans aucun message, à la première trame vocale d'une radio en mode PDN |

**wininet.dll.** WIRES-X lit les en-têtes des réponses des serveurs de Yaesu avec `HttpQueryInfo(HTTP_QUERY_RAW_HEADERS_CRLF)` et un index, en ajoutant 1 à l'index jusqu'à ce que l'appel échoue. Sous Windows, l'appel avec un index supérieur à 0 échoue (`ERROR_HTTP_HEADER_NOT_FOUND`). Wine 11.0 ignorait l'index pour les en-têtes complets et les renvoyait à chaque fois : la boucle ne se terminait jamais et WIRES-X ne lisait jamais son premier fichier (`UpdateInfoX_New.bin`). Avec la correction, WIRES-X passe **ONLINE(IPv4)**.

**msgsm32.acm.** WIRES-X convertit la voix (PCM 8 kHz, 16 bits, mono) en GSM 6.10 et inversement avec l'Audio Compression Manager, et demande le format GSM 6.10 avec `acmFormatSuggest` sur une destination remise à zéro ; sous Windows, c'est le codec qui remplit le format, `cbSize` compris. Le codec de Wine 11.0 refusait une destination dont le `cbSize` ne valait pas déjà 2 : la conversion ne s'ouvrait jamais et WIRES-X plantait en copiant la première trame vocale dans le tampon de la conversion. Avec la correction, le codec remplit `cbSize` et toutes les conversions s'ouvrent.

- Fichiers : `usr/local/lib/logbeamos/wires-x/wininet.dll` et `usr/local/lib/logbeamos/wires-x/msgsm32.acm`, construits par [construir-dlls.sh](construir-dlls.sh) à partir du code source de Wine 11.0, avec ces deux seuls changements. Sans la marque « Wine builtin DLL », pour que Wine les charge comme DLL natives.
- Le lanceur `wires-x` les copie dans le dossier de WIRES-X du préfixe Wine et ouvre WIRES-X avec `wininet=n,b` et `msgsm32.acm=n,b` dans `WINEDLLOVERRIDES`. Tous les autres logiciels gardent les DLL du Wine installé.
- Code source, comme le demande la LGPL : `wine-11.0.tar.xz` (SHA-256 `c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701`), `wine-11.0-wininet-indice.patch` et `wine-11.0-msgsm32-cbsize.patch`, dans le dépôt apt (`https://logbeam.org/apt/`). Wine est sous la GNU Lesser General Public License, version 2.1 ou ultérieure.
