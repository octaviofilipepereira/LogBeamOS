#!/bin/bash
# Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
# © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
# Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
# LogBeamOS: builds the two Wine DLLs that WIRES-X uses under Wine (LogBeamOS Update 0.3.29), from the source of
# Wine 11.0 (the Wine of LogBeamOS), each with one correction. Both errors were found and reported by Bráulio Sousa,
# CT7APZ (LogBeamOS tester), in November 2026:
# - wininet.dll (0.3.28), wininet-indice.patch: HttpQueryInfo with the raw headers and an index above 0 fails with
#   ERROR_HTTP_HEADER_NOT_FOUND, as on Windows. WIRES-X 2.010 reads the reply headers of the Yaesu servers with that
#   index until the call fails; Wine returned the headers every time, so WIRES-X never got past its first file and
#   stayed OFFLINE.
# - msgsm32.acm (0.3.29), msgsm32-cbsize.patch: acmFormatSuggest to GSM 6.10 fills in the cbSize of the destination,
#   as on Windows. WIRES-X asks for PCM 8 kHz to GSM 6.10 with a zeroed destination; Wine refused it, the conversion
#   was never opened and WIRES-X closed on the first voice frame of a radio in PDN mode.
# Each DLL then loses the "Wine builtin DLL" mark (offset 0x40): with it, Wine loads its own installed DLL in its
# place; without it, the file is loaded as a native DLL from the WIRES-X folder (the wires-x launcher sets wininet=n,b
# and msgsm32.acm=n,b).
# If LogBeamOS moves to another Wine version, build them again from that version (and check that the patches apply).
# Needs: gcc-mingw-w64-i686, flex, bison, gcc, make, curl, patch (Ubuntu 24.04). Usage: construir-dlls.sh WORK-FOLDER
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
for p in wininet-indice msgsm32-cbsize; do
  tr -d '\r' < "$AQUI/$p.patch" | patch -s -d "wine-$V" -p1
done
mkdir build; cd build
"../wine-$V/configure" --enable-archs=i386 --without-x --without-freetype --disable-tests > configure.log 2>&1
make -j"$(nproc)" __tooldeps__ > make.log 2>&1
for d in dlls/wininet/i386-windows/wininet.dll dlls/msgsm32.acm/i386-windows/msgsm32.acm; do
  make -j"$(nproc)" "$d" >> make.log 2>&1
  f="$W/${d##*/}"
  cp "$d" "$f"
  [ "$(dd if="$f" bs=1 skip=64 count=16 status=none)" = "Wine builtin DLL" ] || { echo "ERRO: marca não encontrada em ${d##*/}"; exit 1; }
  head -c 17 /dev/zero | dd of="$f" bs=1 seek=64 conv=notrunc status=none
  sha256sum "$f"
done
