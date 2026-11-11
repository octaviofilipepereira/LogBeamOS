<!--
  Code & Powered by: Octávio Filipe Pereira Gonçalves / CT7BFV
  © 2026 Octávio Filipe Pereira Gonçalves — Todos os direitos reservados
  Licença GPL v3 (https://www.gnu.org/licenses/gpl-3.0.pt-br.html | https://www.gnu.org/licenses/gpl-3.0.html.en)
-->

# LogBeamOS Manual

*Linux distribution for radio amateurs*

This is the manual that comes with LogBeamOS (tools 0.3.13).

[Português](manual-pt.md) · **English** · [Español](manual-es.md) · [Français](manual-fr.md)

- [1. First steps](#1-first-steps)
- [2. Connecting the radio](#2-connecting-the-radio)
- [3. Which program for what](#3-which-program-for-what)
- [4. Updating](#4-updating)
- [5. Alongside Windows](#5-installing-alongside-windows)
- [6. Common problems](#6-common-problems)

## 1. First steps

- LogBeamOS starts from the USB drive without installing anything on the computer. On the first start you are asked whether you want your own user and password; without them, the session opens by itself.
- What you do on the USB drive (settings, logs, files) is kept on it and is still there the next time you start.
- On the desktop: the **Ham Radio Programs** folder (every program), **Radio and Equipment**, **Update LogBeamOS**, **LogBeam Uplink** and this manual. The programs are also in the menu, in the *Hamradio* group.
- To switch off: menu → red button. Do not remove the USB drive while LogBeamOS is running.

## 2. Connecting the radio

1. **Connect the radio by USB.** For most radios there is no driver to install: Linux already has it.
2. **Open Radio and Equipment.** It shows the radio, the CAT port, the radio's sound card and the matching COM port for N1MM+ and Log4OM.
3. **Test CAT:** choose the model; with the speed set to *Automatic*, it looks for the speed the radio answers at. The test only reads the frequency: it never transmits.
4. **Set up the programs…:** choose the radio from the list and press *Set up*. WSJT-X, JTDX, Fldigi, Not1MM and Direwolf then use the radio at the same time, with the radio's sound and PTT by CAT. A copy of each program's settings is kept before changing them.
5. **N1MM+ and Log4OM:** in each one's CAT settings, choose the COM port shown in Radio and Equipment. While N1MM+ is open, the other programs have no CAT; when it closes, they get it back.

> The CAT speed must be the same in the radio's menu (for example, *CAT RATE* on Yaesu radios).

## 3. Which program for what

| For… | Program |
|---|---|
| FT8, FT4, WSPR | WSJT-X or JTDX · with FT2: Decodium · map of the stations heard: GridTracker2 |
| Weak-signal keyboard messaging | JS8Call |
| RTTY, PSK, Olivia and other digital modes | Fldigi (with Flrig, Flmsg and Flamp) |
| Contests | N1MM+ (the Windows one, through Wine) or Not1MM |
| Logbook | Log4OM (through Wine), CQRLOG or KLog · upload to logbeam.org: LogBeam Uplink · upload to Wavelog: WaveLogGate |
| APRS | Direwolf (the sound card modem) and Xastir (the map); Xastir starts Direwolf by itself and connects to it |
| Winlink (e-mail over radio) | Pat |
| Satellites | Gpredict (predictions and tracking) · weather satellite images: SatDump |
| SDR receivers | Gqrx or SDR++ · experiments: GNU Radio |
| Digital voice and pictures | FreeDV · SSTV: QSSTV |
| Remote Icom and Kenwood radios | wfview |
| Programming DMR radios | qdmr |
| DMR without a radio (BrandMeister) | VoxDMR (optional: installed by *Update LogBeamOS*; asks for your DMR ID and BrandMeister hotspot password) |
| EchoLink | Qtel (the router must let UDP ports 5198–5199 and TCP port 5200 through, or use an EchoLink proxy) |
| Antenna modelling | xnec2c |
| Band analysis | 4ham Spectrum Analysis |

> In Xastir, before transmitting: enter your callsign (Xastir asks for it the first time), change *MYCALL* in the `direwolf.conf` file in your home folder and turn transmitting on under *Interfaces*. By default, Xastir only receives.

## 4. Updating

- **Update LogBeamOS** lists the radio programs and the operating system, with the installed version, the available one and the download size.
- The LogBeamOS tools (this updater, **Radio and Equipment** and this manual) and **LogBeam Uplink** are also updated here. They come from the LogBeamOS repository at logbeam.org, which is signed.
- Tick what you want to update. Each program has its own box; *Operating system* opens with the arrow and each package can be chosen too. Shortcuts: *Radio*, *System*, *All*, *None*.
- Press *Update selected*. While updating, it shows what is being downloaded, the MB, the speed and the time left.
- N1MM+, Log4OM and GridTracker2 update themselves.
- On the USB drive no password is asked; on an installed LogBeamOS, the user's password is asked.
- Ten minutes after logging in, a notice appears if there are updates.

## 5. Installing alongside Windows

### First, in Windows

1. **Back up your data.**
2. **Run "Preparar o Windows.cmd"** with right-click → *Run as administrator*. It is on the LOGBEAMOS drive that the USB drive shows in Windows, and also at the root of the ISO (double-click the ISO). The USB drive also shows a small 5 MB drive with the "boot" and "EFI" folders: do not change it, the USB drive needs it to start. It turns off fast startup and, if drive C: is encrypted, starts decrypting it; before installing, wait until the percentage encrypted reaches 0 %. It can also be done by hand: *Before installing*.

### Installing

3. Start from the USB drive and open *Install LogBeamOS*. For the installation type, choose to install alongside Windows and drag the divider: 40 GB is enough for LogBeamOS.
4. Afterwards, when the computer starts, a menu with LogBeamOS and Windows is shown for 10 seconds. The last choice is remembered.

### Removing LogBeamOS

5. In Windows, in an administrator console: `bcdedit /set {fwbootmgr} displayorder {bootmgr} /addfirst`. The computer then starts straight into Windows.
6. Disk Management: delete the LogBeamOS partitions (the ones after C: without a drive letter; never the EFI or recovery partition). Then right-click C: → *Extend Volume*.
7. Optional, to also delete LogBeamOS's boot files, in the same console:
   - `bcdedit /enum firmware` lists the boot entries; delete the ones with `\EFI\ubuntu` in the path with `bcdedit /delete {identifier}`;
   - `mountvol S: /S` and `rmdir /S /Q S:\EFI\ubuntu`;
   - if `S:\EFI\Boot\fbx64.efi` exists, the installer replaced the disk's fallback boot file: `copy /Y S:\EFI\Microsoft\Boot\bootmgfw.efi S:\EFI\Boot\bootx64.efi` and `del S:\EFI\Boot\fbx64.efi S:\EFI\Boot\mmx64.efi`;
   - finally, `mountvol S: /D`.

## 6. Common problems

**The USB drive does not start: "Unable to find a medium containing a live file system"**  
Remove the USB drive, wait 5 seconds, plug it back in and start again.

**Windows asks to format the USB drive**  
Always cancel. It is the part of the USB drive where your LogBeamOS data is kept, which Windows cannot read.

**A program is stuck**  
Open the System Monitor (icon on the panel), *Processes* tab, right-click the program → *End*.

**The desktop crashed ("fallback mode")**  
Press Ctrl+Alt+Esc to restart it, or log out and log back in.

**The radio does not answer CAT**  
In Radio and Equipment, check the model and use the *Automatic* speed; check that CAT is enabled in the radio's menu and close the programs using the port.

**No radio sound in WSJT-X or Direwolf**  
In Radio and Equipment → *Set up the programs…*, choose the radio sound.

**Direwolf closes straight away**  
The window stays open with the explanation. The settings are in the `direwolf.conf` file in your home folder.
