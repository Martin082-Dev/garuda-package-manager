# Garuda Package Manager

Un gestore grafico di pacchetti per Garuda Linux, basato su PyQt6. 
Supporta pacman, AUR (paru) e Flatpak, con un'interfaccia completa per la ricerca, l'installazione, gli aggiornamenti e la manutenzione sicura del sistema.

## Caratteristiche principali
- Ricerca e installazione pacchetti da repository ufficiali, AUR e Flatpak.
- Gestione avanzata degli aggiornamenti con cache offline e multi-selezione.
- Gestione dei pacchetti ignorati (`IgnorePkg`) direttamente dall'interfaccia.
- Strumenti di manutenzione (Garuda Health, pulizia cache, pacchetti orfani, pacdiff).
- Interfaccia bilingue (Italiano / Inglese) con rilevamento automatico della lingua per i dettagli dei pacchetti.
- Icona nella system tray con stati visivi reattivi.
- Ottimizzazione dei mirror integrata.

## Requisiti
- Garuda Linux (o Arch Linux con gli strumenti Garuda)
- Python 3.10+
- `python-pyqt6`
- `paru` (o un altro helper AUR)
- `flatpak` (opzionale, per la gestione Flatpak)
- `pacman-contrib` (opzionale, per `checkupdates`)

## Installazione

Clona il repository:
```bash
git clone https://github.com/Martin082-Dev/garuda-package-manager.git
cd garuda-package-manager
