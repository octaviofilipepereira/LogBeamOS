# wininet · LogBeamOS

[English](#english) · [Português](#português) · [Español](#español) · [Français](#français)

---

## English

Since LogBeamOS Update 0.3.28, LogBeamOS brings, for **WIRES-X** alone, the `wininet.dll` of Wine 11.0 (the Wine of LogBeamOS) with a correction. Without it, WIRES-X 2.010 stayed **OFFLINE** under Wine, and the ID activation answered "Server or ID Not Found.".

WIRES-X reads the reply headers of the Yaesu servers with `HttpQueryInfo(HTTP_QUERY_RAW_HEADERS_CRLF)` and an index, adding 1 to the index until the call fails. On Windows the call with an index above 0 fails (`ERROR_HTTP_HEADER_NOT_FOUND`). Wine 11.0 ignored the index for the raw headers and returned them every time, so the loop never ended and WIRES-X never read its first file (`UpdateInfoX_New.bin`). [wininet-indice.patch](wininet-indice.patch) makes Wine behave as Windows; with it WIRES-X goes **ONLINE(IPv4)**.

- File: `usr/local/lib/logbeamos/wires-x/wininet.dll`, built by [construir-wininet.sh](construir-wininet.sh) from the Wine 11.0 source with this patch only. The "Wine builtin DLL" mark is removed, so that Wine loads it as a native DLL.
- The `wires-x` launcher copies it into the WIRES-X folder of the Wine prefix and starts WIRES-X with `wininet=n,b` in `WINEDLLOVERRIDES`. Every other program keeps the wininet of the installed Wine.
- Source, as the LGPL asks: `wine-11.0.tar.xz` (SHA-256 `c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701`) and `wine-11.0-wininet-indice.patch`, in the apt repository (`https://logbeam.org/apt/`). Wine is under the GNU Lesser General Public License, version 2.1 or later.

## Português

Desde o LogBeamOS Update 0.3.28, o LogBeamOS traz, só para o **WIRES-X**, a `wininet.dll` do Wine 11.0 (o Wine do LogBeamOS) com uma correcção. Sem ela, o WIRES-X 2.010 ficava **OFFLINE** no Wine e a activação do ID respondia «Server or ID Not Found.».

O WIRES-X lê os cabeçalhos das respostas dos servidores da Yaesu com `HttpQueryInfo(HTTP_QUERY_RAW_HEADERS_CRLF)` e um índice, somando 1 ao índice até o pedido falhar. No Windows o pedido com índice maior que 0 falha (`ERROR_HTTP_HEADER_NOT_FOUND`). O Wine 11.0 ignorava o índice nos cabeçalhos completos e devolvia-os sempre: o ciclo nunca acabava e o WIRES-X nunca lia o seu primeiro ficheiro (`UpdateInfoX_New.bin`). O [wininet-indice.patch](wininet-indice.patch) faz o Wine comportar-se como o Windows; com ele o WIRES-X fica **ONLINE(IPv4)**.

- Ficheiro: `usr/local/lib/logbeamos/wires-x/wininet.dll`, construído pelo [construir-wininet.sh](construir-wininet.sh) a partir do código-fonte do Wine 11.0, só com esta alteração. Sem a marca «Wine builtin DLL», para o Wine a carregar como DLL nativa.
- O lançador `wires-x` copia-a para a pasta do WIRES-X no prefixo do Wine e abre o WIRES-X com `wininet=n,b` no `WINEDLLOVERRIDES`. Todos os outros programas continuam com a wininet do Wine instalado.
- Código-fonte, como pede a LGPL: `wine-11.0.tar.xz` (SHA-256 `c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701`) e `wine-11.0-wininet-indice.patch`, no repositório apt (`https://logbeam.org/apt/`). O Wine está sob a GNU Lesser General Public License, versão 2.1 ou posterior.

## Español

Desde LogBeamOS Update 0.3.28, LogBeamOS trae, solo para **WIRES-X**, la `wininet.dll` de Wine 11.0 (el Wine de LogBeamOS) con una corrección. Sin ella, WIRES-X 2.010 se quedaba **OFFLINE** en Wine y la activación del ID respondía «Server or ID Not Found.».

WIRES-X lee las cabeceras de las respuestas de los servidores de Yaesu con `HttpQueryInfo(HTTP_QUERY_RAW_HEADERS_CRLF)` y un índice, sumando 1 al índice hasta que la llamada falla. En Windows la llamada con un índice mayor que 0 falla (`ERROR_HTTP_HEADER_NOT_FOUND`). Wine 11.0 ignoraba el índice en las cabeceras completas y las devolvía siempre: el bucle no terminaba nunca y WIRES-X nunca leía su primer archivo (`UpdateInfoX_New.bin`). [wininet-indice.patch](wininet-indice.patch) hace que Wine se comporte como Windows; con él WIRES-X queda **ONLINE(IPv4)**.

- Archivo: `usr/local/lib/logbeamos/wires-x/wininet.dll`, construido por [construir-wininet.sh](construir-wininet.sh) a partir del código fuente de Wine 11.0, solo con este cambio. Sin la marca «Wine builtin DLL», para que Wine la cargue como DLL nativa.
- El lanzador `wires-x` la copia a la carpeta de WIRES-X en el prefijo de Wine y abre WIRES-X con `wininet=n,b` en `WINEDLLOVERRIDES`. Todos los demás programas siguen con la wininet del Wine instalado.
- Código fuente, como pide la LGPL: `wine-11.0.tar.xz` (SHA-256 `c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701`) y `wine-11.0-wininet-indice.patch`, en el repositorio apt (`https://logbeam.org/apt/`). Wine está bajo la GNU Lesser General Public License, versión 2.1 o posterior.

## Français

Depuis LogBeamOS Update 0.3.28, LogBeamOS apporte, pour **WIRES-X** seulement, la `wininet.dll` de Wine 11.0 (le Wine de LogBeamOS) avec une correction. Sans elle, WIRES-X 2.010 restait **OFFLINE** sous Wine et l'activation de l'ID répondait « Server or ID Not Found. ».

WIRES-X lit les en-têtes des réponses des serveurs de Yaesu avec `HttpQueryInfo(HTTP_QUERY_RAW_HEADERS_CRLF)` et un index, en ajoutant 1 à l'index jusqu'à ce que l'appel échoue. Sous Windows, l'appel avec un index supérieur à 0 échoue (`ERROR_HTTP_HEADER_NOT_FOUND`). Wine 11.0 ignorait l'index pour les en-têtes complets et les renvoyait à chaque fois : la boucle ne se terminait jamais et WIRES-X ne lisait jamais son premier fichier (`UpdateInfoX_New.bin`). [wininet-indice.patch](wininet-indice.patch) fait se comporter Wine comme Windows ; avec lui WIRES-X passe **ONLINE(IPv4)**.

- Fichier : `usr/local/lib/logbeamos/wires-x/wininet.dll`, construit par [construir-wininet.sh](construir-wininet.sh) à partir du code source de Wine 11.0, avec ce seul changement. Sans la marque « Wine builtin DLL », pour que Wine la charge comme DLL native.
- Le lanceur `wires-x` la copie dans le dossier de WIRES-X du préfixe Wine et ouvre WIRES-X avec `wininet=n,b` dans `WINEDLLOVERRIDES`. Tous les autres logiciels gardent la wininet du Wine installé.
- Code source, comme le demande la LGPL : `wine-11.0.tar.xz` (SHA-256 `c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701`) et `wine-11.0-wininet-indice.patch`, dans le dépôt apt (`https://logbeam.org/apt/`). Wine est sous la GNU Lesser General Public License, version 2.1 ou ultérieure.
