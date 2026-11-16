# Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
# © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
# Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
# LogBeamOS: what the n1mm and log4om commands do with the shared radio before and after the program runs.
# The user chooses in "Radio and Equipment" how each of the two programs uses the radio; the choice is in
# ~/.config/logbeamos/radio.json (keys "n1mm" and "log4om"):
#   "partilhado": the program uses the sharing (rigctld) like the others; N1MM+ through the bridge that
#                 "Radio and Equipment" keeps running (logbeamos-ponte-n1mm.service). Nothing to stop.
#   "exclusivo":  the program opens the radio port itself. The port cannot be opened twice, so the sharing stops
#                 while the program is open and comes back when the last program that had the radio to itself closes.
#   not chosen:   as before the choice existed: N1MM+ has the radio to itself; nothing is done for Log4OM.
# Sourced by /usr/local/bin/n1mm and /usr/local/bin/log4om:  radio_antes PROGRAM … radio_depois
LB_PARTILHA=logbeamos-rigctld.service
LB_PONTE=logbeamos-ponte-n1mm.service
LB_MARCAS="${XDG_RUNTIME_DIR:-/tmp}/logbeamos-radio-exclusivo"
LB_MARCA=

modo_radio() {
  sed -n 's/^ *"'"$1"'": *"\([a-z]*\)".*/\1/p' "$HOME/.config/logbeamos/radio.json" 2>/dev/null | head -n 1
}

# Marks left by programs that are no longer running (a session that ended badly) do not count
limpa_marcas() {
  local m
  for m in "$LB_MARCAS"/*.[0-9]*; do
    [ -e "$m" ] || continue
    kill -0 "${m##*.}" 2>/dev/null || rm -f "$m"
  done
}

# Wine numbers the serial ports by itself: the 32 ports of the motherboard first, so the first USB cable would be
# COM33, and it puts its own numbers back at every start (the links wine-env.sh makes in dosdevices do not last).
# What Wine does respect is its registry: the radio cables are declared there as COM3, COM4…, in the order
# "Radio and Equipment" shows them. Only when the cables changed, and only with no other Wine program open (the
# registry is read when Wine starts).
portas_wine() {
  local n=3 t quer="" tem f
  for t in /dev/ttyUSB[0-9]* /dev/ttyACM[0-9]*; do
    [ -e "$t" ] || continue
    quer="$quer\"COM$n\"=\"$t\"
"
    n=$((n + 1)); [ $n -gt 12 ] && break
  done
  tem=$(awk '/^\[Software\\\\Wine\\\\Ports\]/ {p = 1; next} /^\[/ {p = 0} p && /^"COM/' "$WINEPREFIX/system.reg" 2>/dev/null | sort)
  [ "$(printf '%s' "$quer" | sort)" = "$tem" ] && return 0
  pgrep -u "$(id -u)" -x wineserver >/dev/null 2>&1 && return 0
  f=$(mktemp --suffix=.reg) || return 0
  printf 'REGEDIT4\r\n\r\n[-HKEY_LOCAL_MACHINE\\Software\\Wine\\Ports]\r\n\r\n[HKEY_LOCAL_MACHINE\\Software\\Wine\\Ports]\r\n' > "$f"
  printf '%s' "$quer" | sed 's/$/\r/' >> "$f"
  wine regedit /S "$f" >/dev/null 2>&1
  "$(dirname "$(readlink -f "$(command -v wine)")")/wineserver" -w 2>/dev/null   # Wine closed: the ports are read anew
  rm -f "$f"
}

radio_antes() {
  local modo
  portas_wine
  modo=$(modo_radio "$1")
  case "$modo" in
    partilhado)
      [ "$1" = n1mm ] && systemctl --user start "$LB_PONTE" 2>/dev/null
      return 0 ;;
    exclusivo) ;;
    *) [ "$1" = n1mm ] || return 0 ;;
  esac
  mkdir -p "$LB_MARCAS"
  limpa_marcas
  if systemctl --user -q is-active "$LB_PARTILHA" 2>/dev/null; then
    systemctl --user stop "$LB_PARTILHA" && : > "$LB_MARCAS/retoma"
  fi
  LB_MARCA="$LB_MARCAS/$1.$$"
  : > "$LB_MARCA"
}

radio_depois() {
  [ -n "$LB_MARCA" ] || return 0
  rm -f "$LB_MARCA"
  LB_MARCA=
  limpa_marcas
  if [ -e "$LB_MARCAS/retoma" ] && [ -z "$(ls "$LB_MARCAS" | grep -v '^retoma$')" ]; then
    rm -f "$LB_MARCAS/retoma"
    systemctl --user start "$LB_PARTILHA"
  fi
}
