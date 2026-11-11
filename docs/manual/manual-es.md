<!--
  Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
  © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
  Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
-->

# Manual de LogBeamOS

*Distribución Linux para radioaficionados*

Este es el manual que acompaña a LogBeamOS (herramientas 0.3.13).

[Português](manual-pt.md) · [English](manual-en.md) · **Español** · [Français](manual-fr.md)

- [1. Primeros pasos](#1-primeros-pasos)
- [2. Conectar la radio](#2-conectar-la-radio)
- [3. Qué programa para qué](#3-qué-programa-para-qué)
- [4. Actualizar](#4-actualizar)
- [5. Junto a Windows](#5-instalar-junto-a-windows)
- [6. Problemas frecuentes](#6-problemas-frecuentes)

## 1. Primeros pasos

- LogBeamOS arranca desde la memoria USB sin instalar nada en el ordenador. En el primer arranque se pregunta si quiere un usuario y una contraseña propios; sin ellos, la sesión se abre sola.
- Lo que haga en la memoria USB (ajustes, registros, archivos) queda guardado en ella y sigue allí en el arranque siguiente.
- En el escritorio: la carpeta **Programas de Radioaficionado** (todos los programas), **Radio y Equipo**, **Actualizar LogBeamOS**, **LogBeam Uplink** y este manual. Los programas también están en el menú, en el grupo *Radio-aficionados*.
- Para apagar: menú → botón rojo. No retire la memoria USB con LogBeamOS en marcha.

## 2. Conectar la radio

1. **Conecte la radio por USB.** En la mayoría de las radios no hace falta instalar ningún controlador: Linux ya lo tiene.
2. **Abra Radio y Equipo.** Aparecen la radio, el puerto CAT, la tarjeta de sonido de la radio y el COM correspondiente para N1MM+ y Log4OM.
3. **Probar CAT:** elija el modelo; con la velocidad *Automática*, se busca la velocidad a la que responde la radio. La prueba solo lee la frecuencia: nunca transmite.
4. **Configurar los programas…:** elija la radio en la lista y pulse *Configurar*. WSJT-X, JTDX, Fldigi, Not1MM y Direwolf pasan a usar la radio al mismo tiempo, con el sonido de la radio y el PTT por CAT. Antes de cambiar, se guarda una copia de la configuración de cada programa.
5. **N1MM+ y Log4OM:** en los ajustes CAT de cada uno, elija el COM indicado en Radio y Equipo. Mientras N1MM+ esté abierto, los demás programas no tienen CAT; al cerrarlo, lo recuperan.

> La velocidad CAT tiene que ser la misma en el menú de la radio (por ejemplo, *CAT RATE* en las Yaesu).

## 3. Qué programa para qué

| Para… | Programa |
|---|---|
| FT8, FT4, WSPR | WSJT-X o JTDX · con FT2: Decodium · mapa de las estaciones oídas: GridTracker2 |
| Mensajes por teclado con señal débil | JS8Call |
| RTTY, PSK, Olivia y otros modos digitales | Fldigi (con Flrig, Flmsg y Flamp) |
| Concursos | N1MM+ (el de Windows, a través de Wine) o Not1MM |
| Libro de guardia (logbook) | Log4OM (a través de Wine), CQRLOG o KLog · envío a logbeam.org: LogBeam Uplink · envío a Wavelog: WaveLogGate |
| APRS | Direwolf (el módem por la tarjeta de sonido) y Xastir (el mapa); Xastir abre Direwolf solo y se conecta a él |
| Winlink (correo por radio) | Pat |
| Satélites | Gpredict (predicciones y seguimiento) · imágenes de satélites meteorológicos: SatDump |
| Receptores SDR | Gqrx o SDR++ · experimentos: GNU Radio |
| Voz digital e imagen | FreeDV · SSTV: QSSTV |
| Radios Icom y Kenwood a distancia | wfview |
| Programación de radios DMR | qdmr |
| DMR sin radio (BrandMeister) | VoxDMR (opcional: se instala con *Actualizar LogBeamOS*; pide su ID DMR y la contraseña de hotspot de BrandMeister) |
| EchoLink | Qtel (el router debe dejar pasar los puertos UDP 5198–5199 y TCP 5200, o use un proxy EchoLink) |
| Simulación de antenas | xnec2c |
| Análisis de las bandas | 4ham Spectrum Analysis |

> En Xastir, antes de transmitir: indique su indicativo (Xastir lo pregunta la primera vez), cambie *MYCALL* en el archivo `direwolf.conf` de su carpeta personal y active la transmisión en *Interfaces*. Por defecto, Xastir solo recibe.

## 4. Actualizar

- **Actualizar LogBeamOS** muestra los programas de radio y el sistema operativo, con la versión instalada, la disponible y el tamaño a descargar.
- Las herramientas de LogBeamOS (este Actualizar, **Radio y Equipo** y este manual) y **LogBeam Uplink** también se actualizan aquí. Vienen del repositorio de LogBeamOS en logbeam.org, que está firmado.
- Marque lo que quiere actualizar. Cada programa tiene su casilla; el *Sistema operativo* se abre con la flecha y cada paquete también se puede elegir. Atajos: *Radio*, *Sistema*, *Todo*, *Nada*.
- Pulse *Actualizar los marcados*. Durante la actualización se muestra lo que se está descargando, los MB, la velocidad y el tiempo que falta.
- N1MM+, Log4OM y GridTracker2 se actualizan solos.
- En la memoria USB no se pide contraseña; en LogBeamOS instalado, se pide la del usuario.
- Diez minutos después de entrar en la sesión, si hay actualizaciones, aparece un aviso.

## 5. Instalar junto a Windows

### Antes, en Windows

1. **Copie sus datos.**
2. **Ejecute "Preparar o Windows.cmd"** con el botón derecho → *Ejecutar como administrador*. Está en la unidad LOGBEAMOS que la memoria USB muestra en Windows, y también en la raíz de la ISO (doble clic en la ISO). La memoria USB muestra también una unidad pequeña, de 5 MB, con las carpetas "boot" y "EFI": no la modifique, porque la memoria USB la necesita para arrancar. Desactiva el inicio rápido y, si la unidad C: está cifrada, empieza a descifrarla; antes de instalar, espere a que el porcentaje cifrado llegue al 0 %. También se puede hacer a mano: *Antes de instalar*.

### Instalar

3. Arranque desde la memoria USB y abra *Instalar LogBeamOS*. En el tipo de instalación, elija instalar junto a Windows y arrastre el divisor: 40 GB bastan para LogBeamOS.
4. Después, al encender el ordenador, aparece durante 10 segundos un menú con LogBeamOS y Windows. Se recuerda la última elección.

### Quitar LogBeamOS

5. En Windows, en una consola de administrador: `bcdedit /set {fwbootmgr} displayorder {bootmgr} /addfirst`. El ordenador pasa a arrancar directamente en Windows.
6. Administración de discos: elimine las particiones de LogBeamOS (las que están después de C: y no tienen letra; nunca la partición EFI ni la de recuperación). Después, botón derecho en C: → *Extender volumen*.
7. Opcional, para borrar también el arranque de LogBeamOS, en la misma consola:
   - `bcdedit /enum firmware` muestra las entradas de arranque; borre las que tienen `\EFI\ubuntu` en la ruta con `bcdedit /delete {identificador}`;
   - `mountvol S: /S` y `rmdir /S /Q S:\EFI\ubuntu`;
   - si existe `S:\EFI\Boot\fbx64.efi`, el instalador cambió el arranque de reserva del disco: `copy /Y S:\EFI\Microsoft\Boot\bootmgfw.efi S:\EFI\Boot\bootx64.efi` y `del S:\EFI\Boot\fbx64.efi S:\EFI\Boot\mmx64.efi`;
   - al final, `mountvol S: /D`.

## 6. Problemas frecuentes

**La memoria USB no arranca: "Unable to find a medium containing a live file system"**  
Retire la memoria USB, espere 5 segundos, vuelva a conectarla y arranque de nuevo.

**Windows pide formatear la memoria USB**  
Cancele siempre. Es la parte de la memoria USB donde se guardan sus datos de LogBeamOS, que Windows no sabe leer.

**Un programa se ha quedado colgado**  
Abra el Monitor del sistema (icono en la barra), pestaña *Procesos*, botón derecho en el programa → *Terminar*.

**El escritorio se ha caído ("modo de emergencia")**  
Pulse Ctrl+Alt+Esc para reiniciarlo, o cierre la sesión y vuelva a entrar.

**La radio no responde al CAT**  
En Radio y Equipo, compruebe el modelo y use la velocidad *Automática*; compruebe que el CAT está activado en el menú de la radio y cierre los programas que estén usando el puerto.

**Sin sonido de la radio en WSJT-X o Direwolf**  
En Radio y Equipo → *Configurar los programas…*, elija el sonido de la radio.

**Direwolf se cierra enseguida**  
La ventana queda abierta con la explicación. La configuración está en el archivo `direwolf.conf` de su carpeta personal.
