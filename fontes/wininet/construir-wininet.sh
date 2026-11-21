#!/bin/bash
# Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
# © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
# Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
# LogBeamOS: builds the wininet.dll that WIRES-X uses under Wine (LogBeamOS Update 0.3.28), from the source of Wine 11.0
# (the Wine of LogBeamOS) with one correction, wininet-indice.patch: HttpQueryInfo with the raw headers and an index
# above 0 fails with ERROR_HTTP_HEADER_NOT_FOUND, as on Windows. WIRES-X 2.010 reads the reply headers of the Yaesu
# servers with that index until the call fails; Wine returned the headers every time, so WIRES-X never got past its
# first file and stayed OFFLINE (CT7APZ, 20/11/2026).
# The DLL then loses the "Wine builtin DLL" mark (offset 0x40): with it, Wine loads its own installed wininet in its
# place; without it, the file is loaded as a native DLL from the WIRES-X folder (the wires-x launcher sets wininet=n,b).
# If LogBeamOS moves to another Wine version, build it again from that version (and check that the patch still applies).
# Needs: gcc-mingw-w64-i686, flex, bison, gcc, make, curl, patch (Ubuntu 24.04). Usage: construir-wininet.sh WORK-FOLDER
set -e
mkdir -p "${1:?pasta de trabalho em falta}"; W=$(cd "$1" && pwd)
AQUI=$(cd "$(dirname "$0")" && pwd)
V=11.0
SHA=c07a6857933c1fc60dff5448d79f39c92481c1e9db5aa628db9d0358446e0701
cd "$W"
[ -f "wine-$V.tar.xz" ] || curl -fsSLO "https://dl.winehq.org/wine/source/$V/wine-$V.tar.xz"
echo "$SHA  wine-$V.tar.xz" | sha256sum -c --quiet -
rm -rf "wine-$V" build
tar xf "wine-$V.tar.xz"
tr -d '\r' < "$AQUI/wininet-indice.patch" | patch -s -d "wine-$V" -p1
mkdir build; cd build
"../wine-$V/configure" --enable-archs=i386 --without-x --without-freetype --disable-tests > configure.log 2>&1
make -j"$(nproc)" __tooldeps__ > make.log 2>&1
make -j"$(nproc)" dlls/wininet/i386-windows/wininet.dll >> make.log 2>&1
cp dlls/wininet/i386-windows/wininet.dll "$W/wininet.dll"
[ "$(dd if="$W/wininet.dll" bs=1 skip=64 count=16 status=none)" = "Wine builtin DLL" ] || { echo "ERRO: marca não encontrada"; exit 1; }
head -c 17 /dev/zero | dd of="$W/wininet.dll" bs=1 seek=64 conv=notrunc status=none
sha256sum "$W/wininet.dll"
