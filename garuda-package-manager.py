import sys
import os
import subprocess
import re
import html
import tempfile
import shutil
import socket
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QLabel, QTextEdit, QHeaderView, QMessageBox,
    QSystemTrayIcon, QMenu, QStyle, QGroupBox, QGridLayout, QDialog,
    QTextBrowser, QButtonGroup, QListWidget, QToolButton, QCheckBox
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer, QSettings
from PyQt6.QtGui import QIcon, QFont
from PyQt6 import sip
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

TRANSLATIONS = {
    "it": {
        "window_title": "Garuda Package Manager (Paru + Flatpak + Manutenzione Sicura)",
        "tab_packages": "Gestione Pacchetti",
        "tab_updates": "Aggiornamenti",
        "tab_maintenance": "Manutenzione",
        "search_placeholder": "Cerca pacchetto (es. firefox, vlc)... Premi Invio per cercare online.",
        "btn_search": "Cerca",
        "btn_show_all": "Azzera Ricerca",
        "filter_state": "Stato:",
        "filter_all": "Tutti",
        "filter_inst": "Installati",
        "filter_not_inst": "Non Installati",
        "filter_repo": "Repository:",
        "repo_all": "Tutti i Repository",
        "repo_official": "Repo Ufficiali",
        "repo_aur": "AUR",
        "repo_flatpak": "Flatpak",
        "th_package": "Pacchetto",
        "th_version": "Versione",
        "th_repo": "Repo / Sorgente",
        "th_desc": "Descrizione",
        "console_placeholder": "Box di Sistema. Informazioni dettagliate sui pacchetti selezionati...",
        "btn_install": "Installa Selezionato",
        "btn_remove": "Rimuovi Selezionato",
        "btn_files": "Mostra File Installati",
        "btn_refresh_updates": "Verifica Aggiornamenti",
        "btn_system_update": "Aggiornamento Sistema (Official)",
        "btn_full_update": "Aggiornamento Completo (Official + AUR)",
        "btn_update_flatpak": "Aggiorna Flatpak",
        "chk_skip_mirrors": "Salta ottimizzazione mirror",
        "chk_skip_mirrors_tooltip": "Usa --skip-mirrorlist durante l'aggiornamento (consigliato solo se hai appena ottimizzato i mirror)",
        "th_up_package": "Pacchetto",
        "th_up_old_ver": "Versione Attuale",
        "th_up_new_ver": "Nuova Versione",
        "th_up_repo": "Repository",
        "th_up_action": "Azione",
        "btn_ignore": "Ignora",
        "btn_unignore": "Non ignorare",
        "btn_ignore_selected": "Ignora Selezionati",
        "btn_unignore_selected": "Non Ignorare Selezionati",
        "maint_garuda": "Strumenti e Riparazione Garuda",
        "btn_garuda_health": "Esegui Garuda Health (--fix)",
        "btn_optimize_mirrors": "Ottimizza Mirror (Velocità)",
        "maint_ignored": "Gestione Pacchetti Ignorati",
        "btn_manage_ignored": "Apri Gestione Pacchetti Ignorati (Visualizza, Rimuovi, Aggiungi)",
        "maint_cache": "Pulizia Cache e Spazio su Disco",
        "btn_clean_pacman": "Pulisci Cache Pacman (paccache)",
        "btn_clean_paru": "Pulisci Cache Paru (AUR)",
        "btn_clean_yay": "Pulisci Cache Yay (AUR)",
        "btn_clean_orphans": "Gestisci Pacchetti Orfani (Elenca & Rimuovi)",
        "maint_repo": "Gestione Repository e Configurazione",
        "btn_edit_pacman": "Modifica pacman.conf",
        "btn_edit_mirrors": "Modifica Mirrorlist",
        "btn_pacdiff": "Gestisci file .pacnew (pacdiff)",
        "btn_refresh_keys": "Aggiorna Keyring PGP",
        "btn_view_logs": "Visualizza Log Pacman (/var/log/pacman.log)",
        "tray_check": "Verifica aggiornamenti",
        "tray_sys_update": "Aggiorna sistema",
        "tray_full_update": "Aggiornamento Completo",
        "tray_quit": "Esci",
        "lang_btn": "🌐 EN / ITA",
        "tray_tooltip_updates": "Garuda Package Manager - {n} aggiornamenti disponibili",
        "tray_tooltip_updated": "Garuda Package Manager - Sistema aggiornato",
        "tray_tooltip_sys_updating": "Aggiornamento Sistema in corso ({n} pacchetti)...",
        "tray_tooltip_full_updating": "Aggiornamento Completo in corso ({n} pacchetti)...",
        "tray_tooltip_flatpak_updating": "Aggiornamento Flatpak in corso ({n} app + runtime)...",
        "tray_tooltip_checking": "Verifica aggiornamenti in corso...",
        "tray_check_title": "Verifica Aggiornamenti",
        "tray_check_msg": "Controllo avviato in background...",
        "tray_running_title": "Garuda Package Manager",
        "tray_running_msg": "L'applicazione è attiva nella barra di sistema.",
        "flatpak_no_updates": "Nessun aggiornamento Flatpak da eseguire.",
        "status_ready": "Pronto.",
        "updates_checking": "Controllo aggiornamenti in corso ...",
        "updates_offline_partial": "Connessione assente. Visualizzazione di {n} aggiornamenti pendenti.",
        "updates_offline_none": "Impossibile verificare gli aggiornamenti: Connessione Internet assente.",
        "updates_all_updated": "Il sistema è completamente aggiornato.",
        "updates_found": "Trovati {n} aggiornamenti disponibili{size}{ignored}.",
        "ignored_suffix": " ({n} ignorati)",
        "loading_installed": "Caricamento pacchetti installati in corso...",
        "loading_all": "Caricamento in corso di tutti i pacchetti...",
        "searching": "Ricerca di '{q}' in corso online...",
        "status_totals": "Totale: {t} | Installati: {i}",
        "status_filtered": "Visualizzati: {v} pacchetti  |  Totale: {t}  |  Installati: {i}",
        "loading_details": "Caricamento dettagli per {name}...",
        "dlg_ignored_title": "Gestione Pacchetti Ignorati",
        "dlg_ignored_list_lbl": "Pacchetti attualmente ignorati in pacman.conf:",
        "dlg_ignored_btn_remove": "Rimuovi Selezionati (Non ignorare)",
        "dlg_ignored_add_lbl": "Aggiungi nuovo pacchetto da ignorare:",
        "dlg_ignored_add_ph": "Nome esatto del pacchetto (es. firefox)...",
        "dlg_ignored_btn_add": "Aggiungi",
        "dlg_btn_close": "Chiudi",
        "msg_warning_title": "Attenzione",
        "msg_info_title": "Info",
        "msg_error_title": "Errore",
        "warn_select_pkg": "Seleziona un pacchetto dalla lista da rimuovere.",
        "info_already_ignored": "Il pacchetto '{name}' è già nella lista degli ignorati.",
        "err_terminal": "Impossibile aprire il terminale: {e}",
        "err_read_conf": "Impossibile leggere {path}:\n{e}",
        "details_name": "Nome",
        "details_repo": "Repository",
        "details_desc": "Descrizione",
        "details_flatpak_unavail": "Dettagli Flatpak non disponibili.",
        "details_unavail": "Dettagli non disponibili.",
        "details_error": "Errore nel recupero dettagli: {e}",
        "logs_dialog_title": "Log di Pacman (/var/log/pacman.log) - ultime 5000 righe",
        "logs_read_error": "Impossibile leggere il log:\n{e}",
        "logs_empty": "Il log è vuoto o non leggibile.",
        "locale_missing_warning": "⚠ Locale italiana non installata sul sistema: i dettagli dei pacchetti saranno mostrati in inglese. Esegui 'sudo locale-gen' per abilitarla.",
    },
    "en": {
        "window_title": "Garuda Package Manager (Paru + Flatpak + Safe Maintenance)",
        "tab_packages": "Package Management",
        "tab_updates": "Updates",
        "tab_maintenance": "Maintenance",
        "search_placeholder": "Search package (e.g. firefox, vlc)... Press Enter to search online.",
        "btn_search": "Search",
        "btn_show_all": "Clear Search",
        "filter_state": "State:",
        "filter_all": "All",
        "filter_inst": "Installed",
        "filter_not_inst": "Not Installed",
        "filter_repo": "Repository:",
        "repo_all": "All Repositories",
        "repo_official": "Official Repos",
        "repo_aur": "AUR",
        "repo_flatpak": "Flatpak",
        "th_package": "Package",
        "th_version": "Version",
        "th_repo": "Repo / Source",
        "th_desc": "Description",
        "console_placeholder": "System Box. Detailed information about selected packages...",
        "btn_install": "Install Selected",
        "btn_remove": "Remove Selected",
        "btn_files": "Show Installed Files",
        "btn_refresh_updates": "Check for Updates",
        "btn_system_update": "System Update (Official)",
        "btn_full_update": "Full Update (Official + AUR)",
        "btn_update_flatpak": "Update Flatpak",
        "chk_skip_mirrors": "Skip mirror optimization",
        "chk_skip_mirrors_tooltip": "Use --skip-mirrorlist during update (recommended only if you just optimized mirrors)",
        "th_up_package": "Package",
        "th_up_old_ver": "Current Version",
        "th_up_new_ver": "New Version",
        "th_up_repo": "Repository",
        "th_up_action": "Action",
        "btn_ignore": "Ignore",
        "btn_unignore": "Unignore",
        "btn_ignore_selected": "Ignore Selected",
        "btn_unignore_selected": "Unignore Selected",
        "maint_garuda": "Garuda Tools & Repair",
        "btn_garuda_health": "Run Garuda Health (--fix)",
        "btn_optimize_mirrors": "Optimize Mirrors (Speed)",
        "maint_ignored": "Ignored Packages Management",
        "btn_manage_ignored": "Open Ignored Packages (View, Remove, Add)",
        "maint_cache": "Cache Cleaning & Disk Space",
        "btn_clean_pacman": "Clean Pacman Cache (paccache)",
        "btn_clean_paru": "Clean Paru Cache (AUR)",
        "btn_clean_yay": "Clean Yay Cache (AUR)",
        "btn_clean_orphans": "Manage Orphan Packages (List & Remove)",
        "maint_repo": "Repository & Configuration Management",
        "btn_edit_pacman": "Edit pacman.conf",
        "btn_edit_mirrors": "Edit Mirrorlist",
        "btn_pacdiff": "Manage .pacnew files (pacdiff)",
        "btn_refresh_keys": "Refresh PGP Keyring",
        "btn_view_logs": "View Pacman Log (/var/log/pacman.log)",
        "tray_check": "Check for updates",
        "tray_sys_update": "System update",
        "tray_full_update": "Full update",
        "tray_quit": "Quit",
        "lang_btn": "🌐 ITA / EN",
        "tray_tooltip_updates": "Garuda Package Manager - {n} updates available",
        "tray_tooltip_updated": "Garuda Package Manager - System up to date",
        "tray_tooltip_sys_updating": "System Update in progress ({n} packages)...",
        "tray_tooltip_full_updating": "Full Update in progress ({n} packages)...",
        "tray_tooltip_flatpak_updating": "Flatpak Update in progress ({n} apps + runtimes)...",
        "tray_tooltip_checking": "Checking for updates...",
        "tray_check_title": "Check for Updates",
        "tray_check_msg": "Background check started...",
        "tray_running_title": "Garuda Package Manager",
        "tray_running_msg": "The application is running in the system tray.",
        "flatpak_no_updates": "No Flatpak updates to perform.",
        "status_ready": "Ready.",
        "updates_checking": "Checking for updates ...",
        "updates_offline_partial": "No connection. Showing {n} pending updates.",
        "updates_offline_none": "Unable to check for updates: no Internet connection.",
        "updates_all_updated": "The system is fully up to date.",
        "updates_found": "Found {n} updates available{size}{ignored}.",
        "ignored_suffix": " ({n} ignored)",
        "loading_installed": "Loading installed packages...",
        "loading_all": "Loading all packages...",
        "searching": "Searching for '{q}' online...",
        "status_totals": "Total: {t} | Installed: {i}",
        "status_filtered": "Displayed: {v} packages  |  Total: {t}  |  Installed: {i}",
        "loading_details": "Loading details for {name}...",
        "dlg_ignored_title": "Ignored Packages Management",
        "dlg_ignored_list_lbl": "Packages currently ignored in pacman.conf:",
        "dlg_ignored_btn_remove": "Remove Selected Items (Unignore)",
        "dlg_ignored_add_lbl": "Add new package to ignore:",
        "dlg_ignored_add_ph": "Exact package name (e.g. firefox)...",
        "dlg_ignored_btn_add": "Add",
        "dlg_btn_close": "Close",
        "msg_warning_title": "Warning",
        "msg_info_title": "Info",
        "msg_error_title": "Error",
        "warn_select_pkg": "Select a package from the list to remove.",
        "info_already_ignored": "Package '{name}' is already in the ignored list.",
        "err_terminal": "Cannot open terminal: {e}",
        "err_read_conf": "Cannot read {path}:\n{e}",
        "details_name": "Name",
        "details_repo": "Repository",
        "details_desc": "Description",
        "details_flatpak_unavail": "Flatpak details not available.",
        "details_unavail": "Details not available.",
        "details_error": "Error retrieving details: {e}",
        "logs_dialog_title": "Pacman Log (/var/log/pacman.log) - last 5000 lines",
        "logs_read_error": "Unable to read the log:\n{e}",
        "logs_empty": "The log is empty or unreadable.",
        "locale_missing_warning": "⚠ Italian locale not installed: package details will be shown in English. Run 'sudo locale-gen' to enable it.",
    }
}

SOCKET_NAME = "garuda-package-manager-single-instance"

REPO_CODES = ["all", "official", "aur", "flatpak"]
REPO_KEYS = {
    "all": "repo_all",
    "official": "repo_official",
    "aur": "repo_aur",
    "flatpak": "repo_flatpak",
}

_ITALIAN_LOCALE_CACHE = None


def _italian_locale_available():
    global _ITALIAN_LOCALE_CACHE
    if _ITALIAN_LOCALE_CACHE is not None:
        return _ITALIAN_LOCALE_CACHE
    try:
        res = subprocess.run(["locale", "-a"], capture_output=True, text=True, check=False, timeout=5)
        found = False
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                l = line.strip().lower()
                if l.startswith("it_it.utf-8") or l.startswith("it_it.utf8"):
                    found = True
                    break
        _ITALIAN_LOCALE_CACHE = found
        return found
    except Exception:
        _ITALIAN_LOCALE_CACHE = False
        return False


def _get_locale_env(lang):
    env = os.environ.copy()
    if lang == "en":
        env["LC_ALL"] = "C"
    elif lang == "it":
        if _italian_locale_available():
            env["LC_ALL"] = "it_IT.UTF-8"
        else:
            env["LC_ALL"] = "C"
    return env


def _translate(lang, key, **kwargs):
    s = TRANSLATIONS.get(lang, TRANSLATIONS["it"]).get(key, key)
    if kwargs:
        try:
            return s.format(**kwargs)
        except Exception:
            return s
    return s


class PackageLoaderThread(QThread):
    finished = pyqtSignal(list, set)

    def __init__(self, search_query="", show_all=False):
        super().__init__()
        self.search_query = search_query.lower()
        self.show_all = show_all

    def run(self):
        try:
            all_packages = []
            installed_packages = set()
            seen_pkgs = set()

            def run_cmd(args):
                try:
                    return subprocess.run(args, capture_output=True, text=True, check=False)
                except FileNotFoundError:
                    class Dummy:
                        returncode = 1
                        stdout = ""
                    return Dummy()

            def add_pkg(name, version, repo, desc, p_type):
                ident = str(name).lower()
                if ident not in seen_pkgs:
                    all_packages.append({
                        "name": str(name),
                        "version": str(version),
                        "repo": str(repo),
                        "desc": str(desc),
                        "type": str(p_type),
                        "installed": ident in installed_packages
                    })
                    seen_pkgs.add(ident)

            for cmd in [["pacman", "-Q"], ["paru", "-Qm"]]:
                res = run_cmd(cmd)
                if res.returncode == 0:
                    for line in res.stdout.splitlines():
                        if line.strip():
                            installed_packages.add(line.split()[0].lower())

            res_fp = run_cmd(["flatpak", "list", "--app", "--columns=application"])
            if res_fp.returncode == 0:
                for line in res_fp.stdout.splitlines():
                    if line.strip():
                        installed_packages.add(line.strip().lower())

            def parse_pacman_output(output, is_aur=False):
                c_name, c_ver, c_repo = "", "", ""
                for line in output.splitlines():
                    if not line.startswith(" "):
                        parts = line.split()
                        if len(parts) >= 2:
                            repo_pkg = parts[0].split("/")
                            if is_aur:
                                c_repo = "AUR"
                                c_name = repo_pkg[1] if len(repo_pkg) > 1 else repo_pkg[0]
                                c_ver = parts[1]
                            else:
                                c_repo = repo_pkg[0] if len(repo_pkg) > 1 else "extra"
                                if c_repo.lower() == "aur":
                                    continue
                                c_name = repo_pkg[1] if len(repo_pkg) > 1 else repo_pkg[0]
                                c_ver = parts[1]
                    elif c_name and line.strip():
                        add_pkg(c_name, c_ver, c_repo, line.strip(), "aur" if is_aur else "pacman")
                        c_name = ""

            if self.search_query:
                res_pac = run_cmd(["pacman", "-Ss", self.search_query])
                if not res_pac.stdout.strip():
                    escaped_query = re.escape(self.search_query)
                    res_pac = run_cmd(["pacman", "-Ss", escaped_query])
                parse_pacman_output(res_pac.stdout)

                                # Cerca anche nei pacchetti installati (per pacchetti non più nei repo)
                res_local = run_cmd(["pacman", "-Qs", self.search_query])
                parse_pacman_output(res_local.stdout)

                # Risolve il vero repository dei pacchetti trovati solo localmente
                local_names = [p["name"] for p in all_packages if p["repo"] == "local"]
                if local_names:
                    env_c = os.environ.copy()
                    env_c["LC_ALL"] = "C"
                    res_si = subprocess.run(["pacman", "-Si"] + local_names, capture_output=True, text=True, check=False, timeout=20, env=env_c)
                    cur_repo = None
                    for line in res_si.stdout.splitlines():
                        if line.startswith("Repository"):
                            cur_repo = line.split(":", 1)[-1].strip()
                        elif line.startswith("Name") and cur_repo:
                            pkg_name = line.split(":", 1)[-1].strip()
                            for p in all_packages:
                                if p["repo"] == "local" and p["name"] == pkg_name:
                                    p["repo"] = cur_repo
                                    break
                            cur_repo = None
                res_aur = run_cmd(["paru", "-Ss", self.search_query])
                if not res_aur.stdout.strip():
                    escaped_query = re.escape(self.search_query)
                    res_aur = run_cmd(["paru", "-Ss", escaped_query])
                parse_pacman_output(res_aur.stdout, is_aur=True)

                res_fp_search = run_cmd(["flatpak", "search", self.search_query, "--columns=application,version,description"])
                if res_fp_search.returncode == 0:
                    for line in res_fp_search.stdout.splitlines():
                        if not line.strip():
                            continue
                        parts = [p.strip() for p in line.split("\t") if p.strip()]
                        if len(parts) < 2:
                            parts = [p.strip() for p in line.split("  ") if p.strip()]
                        if len(parts) >= 1 and parts[0].lower() != "no matches found":
                            add_pkg(parts[0], parts[1] if len(parts) > 1 else "latest", "Flatpak", " ".join(parts[2:]) if len(parts) > 2 else "", "flatpak")
            else:
                res_pac = run_cmd(["pacman", "-Sl"])
                if res_pac.returncode == 0:
                    for line in res_pac.stdout.splitlines():
                        parts = line.split()
                        if len(parts) >= 3:
                            add_pkg(parts[1], parts[2], parts[0], "Pacchetto repository ufficiale", "pacman")

                res_fpr = run_cmd(["flatpak", "remote-ls", "--app", "--columns=application,version,description"])
                if res_fpr.returncode == 0:
                    for line in res_fpr.stdout.splitlines():
                        if not line.strip():
                            continue
                        parts = [p.strip() for p in line.split("\t") if p.strip()]
                        if len(parts) < 2:
                            parts = [p.strip() for p in line.split("  ") if p.strip()]
                        if len(parts) >= 1:
                            add_pkg(parts[0], parts[1] if len(parts) > 1 else "latest", "Flatpak", " ".join(parts[2:]) if len(parts) > 2 else "", "flatpak")

                res_aur = run_cmd(["paru", "-Qm"])
                if res_aur.returncode == 0:
                    for line in res_aur.stdout.splitlines():
                        parts = line.split()
                        if len(parts) >= 2:
                            add_pkg(parts[0], parts[1], "AUR", "Pacchetto AUR installato localmente", "aur")

            for pkg in all_packages:
                pkg["installed"] = pkg["name"].lower() in installed_packages

            self.finished.emit(all_packages, installed_packages)
        except Exception as e:
            print(f"Errore fatale nel thread loader: {e}")
            self.finished.emit([], set())


class UpdateLoaderThread(QThread):
    finished = pyqtSignal(list, bool, bool)

    def __init__(self, ignored_packages=None):
        super().__init__()
        self.ignored_packages = list(ignored_packages) if ignored_packages else []

    def run(self):
        has_conn = False
        updates = []
        try:
            env_en = os.environ.copy()
            env_en["LC_ALL"] = "C"

            # Verifica reale della connessione prima di tutto il resto
            def _check_conn():
                # Prova più server/porte per essere robusto su reti con firewall
                targets = [
                    ("1.1.1.1", 443),
                    ("8.8.8.8", 443),
                    ("1.1.1.1", 53),
                    ("8.8.8.8", 53),
                    ("9.9.9.9", 53),
                ]
                for host, port in targets:
                    try:
                        socket.create_connection((host, port), timeout=2).close()
                        return True
                    except OSError:
                        continue
                return False

            if not _check_conn():
                self.finished.emit([], False, False)
                return
            has_conn = True

            raw_updates = []
            seen_names = set()
            scan_ok = False

            # 0. checkupdates → dati freschi dai mirror, rispetta IgnorePkg
            if shutil.which("checkupdates"):
                try:
                    res_chk = subprocess.run(["checkupdates"], capture_output=True, text=True, check=False, timeout=30, env=env_en)
                    # checkupdates: 0 = ci sono update, 2 = nessun update (scansione OK)
                    if res_chk.returncode in (0, 2):
                        scan_ok = True
                    if res_chk.stdout.strip():
                        for line in res_chk.stdout.splitlines():
                            parts = line.split()
                            if len(parts) >= 4:
                                pkg_name = parts[0]
                                if pkg_name not in seen_names:
                                    raw_updates.append({
                                        "name": pkg_name,
                                        "old_version": parts[1],
                                        "version": parts[3]
                                    })
                                    seen_names.add(pkg_name)
                except subprocess.TimeoutExpired:
                    pass

            # 1. pacman -Qu → update ufficiali secondo il DB LOCALE.
            #    Mostra solo cio' che pacman -Syu puo' davvero installare
            #    con il mirror corrente → zero falsi positivi.
            #    Non rispetta IgnorePkg, quindi mostra anche gli ignorati.
            try:
                res_qu = subprocess.run(["pacman", "-Qu"], capture_output=True, text=True, check=False, timeout=20, env=env_en)
                if res_qu.stdout.strip():
                    for line in res_qu.stdout.splitlines():
                        parts = line.split()
                        if len(parts) >= 4:
                            full_name = parts[0]
                            name = full_name.split("/")[-1] if "/" in full_name else full_name
                            if name not in seen_names:
                                raw_updates.append({
                                    "name": name,
                                    "old_version": parts[1],
                                    "version": parts[3]
                                })
                                seen_names.add(name)
            except subprocess.TimeoutExpired:
                pass
            # 1b. Controllo esplicito dei pacchetti ignorati ufficiali
            for ignored_name in self.ignored_packages:
                if ignored_name in seen_names:
                    continue
                try:
                    res_q = subprocess.run(["pacman", "-Q", ignored_name], capture_output=True, text=True, check=False, timeout=5, env=env_en)
                    if res_q.returncode != 0:
                        continue
                    q_parts = res_q.stdout.split()
                    if len(q_parts) < 2:
                        continue
                    installed_ver = q_parts[1]
                    res_si = subprocess.run(["pacman", "-Si", ignored_name], capture_output=True, text=True, check=False, timeout=10, env=env_en)
                    if res_si.returncode != 0:
                        continue
                    repo_ver = None
                    repo_name = "unknown"
                    for line in res_si.stdout.splitlines():
                        if line.startswith("Version"):
                            repo_ver = line.split(":", 1)[-1].strip()
                        elif line.startswith("Repository"):
                            repo_name = line.split(":", 1)[-1].strip()
                    if repo_ver and repo_ver != installed_ver:
                        raw_updates.append({
                            "name": ignored_name,
                            "old_version": installed_ver,
                            "version": repo_ver,
                            "repo": repo_name
                        })
                        seen_names.add(ignored_name)
                except (subprocess.TimeoutExpired, Exception):
                    pass
            # 2. paru -Qua → tutti gli update AUR (richiede rete)
            if shutil.which("paru"):
                try:
                    res_paru = subprocess.run(["paru", "-Qua"], capture_output=True, text=True, check=False, timeout=30, env=env_en)
                    has_conn = True
                    # paru -Qua: 0 = ci sono update, 1 = nessun update (scansione OK)
                    if res_paru.returncode in (0, 1):
                        scan_ok = True
                    if res_paru.returncode == 0 and res_paru.stdout.strip():
                        for line in res_paru.stdout.splitlines():
                            parts = line.split()
                            if len(parts) >= 4:
                                full_name = parts[0]
                                name = full_name.split("/")[-1] if "/" in full_name else full_name
                                if name not in seen_names:
                                    raw_updates.append({
                                        "name": name,
                                        "old_version": parts[1],
                                        "version": parts[3]
                                    })
                                    seen_names.add(name)
                except subprocess.TimeoutExpired:
                    pass

            if raw_updates:
                repo_map = {}
                sizes = {}

                try:
                    res_sl = subprocess.run(["pacman", "-Sl"], capture_output=True, text=True, check=False, timeout=20, env=env_en)
                    if res_sl.returncode == 0:
                        for line in res_sl.stdout.splitlines():
                            parts = line.split()
                            if len(parts) >= 2:
                                repo_map[parts[1]] = parts[0]
                except subprocess.TimeoutExpired:
                    pass

                official_pkg_names = [u["name"] for u in raw_updates if u["name"] in repo_map]

                if official_pkg_names:
                    try:
                        res_si = subprocess.run(["pacman", "-Si"] + official_pkg_names, capture_output=True, text=True, check=False, env=env_en, timeout=20)
                        current_pkg = None
                        for line in res_si.stdout.splitlines():
                            if line.startswith("Name"):
                                current_pkg = line.split(":", 1)[-1].strip()
                            elif ":" in line and current_pkg:
                                key, val = line.split(":", 1)
                                key = key.strip().lower()
                                if "download size" in key:
                                    size_str = val.strip()
                                    try:
                                        parts_sz = size_str.split()
                                        if len(parts_sz) >= 2:
                                            val_num = float(parts_sz[0].replace(',', '.'))
                                            unit = parts_sz[1].lower()
                                            mult = 1
                                            if 'k' in unit: mult = 1024
                                            elif 'm' in unit: mult = 1024 * 1024
                                            elif 'g' in unit: mult = 1024 * 1024 * 1024
                                            sizes[current_pkg] = int(val_num * mult)
                                    except (ValueError, IndexError):
                                        pass
                    except subprocess.TimeoutExpired:
                        pass

                for u in raw_updates:
                    name = u["name"]
                    repo_name = repo_map.get(name, u.get("repo", "AUR"))
                    updates.append({
                        "name": name,
                        "old_version": u["old_version"],
                        "version": u["version"],
                        "repo": repo_name,
                        "size": sizes.get(name, 0)
                    })
            has_flatpak = shutil.which("flatpak") is not None
            try:
                if not has_flatpak:
                    raise subprocess.TimeoutExpired("flatpak", 0)
                res_flatpak = subprocess.run(["flatpak", "remote-ls", "--app", "--updates", "--columns=application,download-size"], capture_output=True, text=True, check=False, timeout=20, env=env_en)
                has_conn = True
                if res_flatpak.returncode == 0 and res_flatpak.stdout.strip():
                    for line in res_flatpak.stdout.splitlines():
                        parts = line.split(None, 1)
                        if parts:
                            app_id = parts[0].strip()
                            flatpak_bytes = 0
                            if len(parts) > 1:
                                size_str = parts[1].strip()
                                try:
                                    sz_parts = size_str.split()
                                    if len(sz_parts) >= 2:
                                        val_num = float(sz_parts[0].replace(',', '.'))
                                        unit = sz_parts[1].lower()
                                        mult = 1
                                        if 'k' in unit: mult = 1024
                                        elif 'm' in unit: mult = 1024 * 1024
                                        elif 'g' in unit: mult = 1024 * 1024 * 1024
                                        flatpak_bytes = int(val_num * mult)
                                except (ValueError, IndexError):
                                    pass

                            updates.append({
                                "name": app_id,
                                "old_version": "-",
                                "version": "Disponibile",
                                "repo": "Flatpak",
                                "size": flatpak_bytes
                            })
            except subprocess.TimeoutExpired:
                pass
        except Exception as e:
            print(f"Errore caricamento aggiornamenti: {e}")

        self.finished.emit(updates, has_conn, scan_ok)


class ConsoleRunnerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            full_cmd = f"{self.command}; echo ''; echo '========================================='; echo 'Operazione completata. Premi Invio per chiudere...'; read"

            term_cmd = None
            for term in ["konsole", "alacritty", "kitty", "gnome-terminal", "xfce4-terminal", "foot"]:
                if shutil.which(term):
                    if term == "konsole":
                        term_cmd = ["konsole", "--nofork", "-e"]
                    elif term in ["alacritty", "kitty", "foot"]:
                        term_cmd = [term, "-e"]
                    elif term == "gnome-terminal":
                        term_cmd = [term, "--wait", "--"]
                    elif term == "xfce4-terminal":
                        term_cmd = [term, "--disable-server", "--"]
                    break

            if term_cmd is None:
                term_cmd = ["x-terminal-emulator", "-e"]

            p = subprocess.Popen(term_cmd + ["sh", "-c", full_cmd])
            p.wait()
        except Exception as e:
            print(f"Errore esecuzione terminale: {e}")
        self.finished.emit()


class PackageDetailThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, name, repo, desc, lang="it"):
        super().__init__()
        self.name = name
        self.repo = repo
        self.desc = desc
        self.lang = lang

    def tr(self, key, **kwargs):
        return _translate(self.lang, key, **kwargs)

    def _env(self):
        return _get_locale_env(self.lang)

    def run(self):
        details = ""
        try:
            repo_lower = self.repo.lower()
            env = self._env()

            if repo_lower == "flatpak":
                res = subprocess.run(["flatpak", "info", self.name], capture_output=True, text=True, check=False, env=env)
                if res.returncode == 0:
                    raw_text = res.stdout
                else:
                    raw_text = (
                        f"{self.tr('details_name')}: {self.name}\n"
                        f"{self.tr('details_repo')}: {self.repo}\n"
                        f"{self.tr('details_desc')}: {self.desc}\n\n"
                        f"{self.tr('details_flatpak_unavail')}"
                    )
            else:
                res_local = subprocess.run(["pacman", "-Qi", self.name], capture_output=True, text=True, check=False, env=env)

                if res_local.returncode == 0 and res_local.stdout.strip():
                    raw_text = res_local.stdout
                else:
                    if repo_lower == "aur":
                        res_remote = subprocess.run(["paru", "-Si", self.name], capture_output=True, text=True, check=False, env=env)
                    else:
                        res_remote = subprocess.run(["pacman", "-Si", self.name], capture_output=True, text=True, check=False, env=env)
                        if res_remote.returncode != 0 or not res_remote.stdout.strip():
                            res_remote = subprocess.run(["paru", "-Si", self.name], capture_output=True, text=True, check=False, env=env)

                    if res_remote.returncode == 0 and res_remote.stdout.strip():
                        raw_text = res_remote.stdout
                    else:
                        raw_text = (
                            f"{self.tr('details_name')}: {self.name}\n"
                            f"{self.tr('details_repo')}: {self.repo}\n"
                            f"{self.tr('details_desc')}: {self.desc}\n\n"
                            f"{self.tr('details_unavail')}"
                        )

            safe_text = html.escape(raw_text)
            linked_text = re.sub(r'(https?://[^\s<]+)', r'<a href="\1">\1</a>', safe_text)

            details = f"<pre style='font-family: monospace;'>{linked_text}</pre>"

        except Exception as e:
            details = f"<pre>{self.tr('details_error', e=e)}</pre>"

        self.finished.emit(details)


class IgnoredPackagesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.lang = parent.current_lang if parent and hasattr(parent, 'current_lang') else "it"
        self.setWindowTitle(self.tr("dlg_ignored_title"))
        self.resize(450, 420)
        self.init_ui()

    def tr(self, key, **kwargs):
        return _translate(self.lang, key, **kwargs)

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.lbl_title = QLabel(f"**{self.tr('dlg_ignored_list_lbl')}**")
        layout.addWidget(self.lbl_title)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.refresh_list()
        layout.addWidget(self.list_widget)

        self.btn_remove = QPushButton(self.tr("dlg_ignored_btn_remove"))
        self.btn_remove.setStyleSheet("background-color: #c62828; color: white; font-weight: bold;")
        self.btn_remove.clicked.connect(self.remove_selected)
        layout.addWidget(self.btn_remove)

        self.lbl_add = QLabel(f"**{self.tr('dlg_ignored_add_lbl')}**")
        layout.addWidget(self.lbl_add)

        add_layout = QHBoxLayout()
        self.input_add = QLineEdit()
        self.input_add.setPlaceholderText(self.tr("dlg_ignored_add_ph"))
        self.input_add.returnPressed.connect(self.add_package)

        self.btn_add = QPushButton(self.tr("dlg_ignored_btn_add"))
        self.btn_add.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold;")
        self.btn_add.clicked.connect(self.add_package)

        add_layout.addWidget(self.input_add)
        add_layout.addWidget(self.btn_add)
        layout.addLayout(add_layout)

        self.btn_close = QPushButton(self.tr("dlg_btn_close"))
        self.btn_close.clicked.connect(self.accept)
        layout.addWidget(self.btn_close)

    def refresh_list(self):
        self.list_widget.clear()
        if self.parent_window and hasattr(self.parent_window, 'ignored_packages'):
            for pkg in sorted(self.parent_window.ignored_packages):
                self.list_widget.addItem(pkg)

    def remove_selected(self):
        items = self.list_widget.selectedItems()
        if not items:
            QMessageBox.warning(self, self.tr("msg_warning_title"), self.tr("warn_select_pkg"))
            return
        pkg_names = [item.text() for item in items]
        if self.parent_window and hasattr(self.parent_window, 'ignored_packages'):
            removed = []
            for pkg_name in pkg_names:
                if pkg_name in self.parent_window.ignored_packages:
                    self.parent_window.ignored_packages.remove(pkg_name)
                    removed.append(pkg_name)
            if not removed:
                return
            self.refresh_list()

            def on_success():
                if self.parent_window:
                    self.parent_window.load_updates()

            if not self.parent_window.sync_ignored_to_pacman_conf(callback=on_success):
                for pkg_name in removed:
                    self.parent_window.ignored_packages.append(pkg_name)
                self.refresh_list()

    def add_package(self):
        pkg_name = self.input_add.text().strip()
        if not pkg_name:
            return
        if self.parent_window and hasattr(self.parent_window, 'ignored_packages'):
            if pkg_name not in self.parent_window.ignored_packages:
                self.parent_window.ignored_packages.append(pkg_name)
                self.input_add.clear()
                self.refresh_list()

                def on_success():
                    if self.parent_window:
                        self.parent_window.load_updates()

                if not self.parent_window.sync_ignored_to_pacman_conf(callback=on_success):
                    self.parent_window.ignored_packages.remove(pkg_name)
                    self.refresh_list()
            else:
                QMessageBox.information(self, self.tr("msg_info_title"), self.tr("info_already_ignored", name=pkg_name))


class GarudaPackageManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("Garuda", "GarudaManager")
        self.current_lang = self.settings.value("language", "it")

        self.setWindowTitle(self.tr("window_title"))
        self.resize(1000, 650)
        self.cached_updates = []
        self.is_quitting = False
        self._load_cache_from_disk()

        self.ignored_packages = self.load_ignored_from_pacman()

        app_icon = QIcon.fromTheme("system-software-update")
        if app_icon.isNull():
            app_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        self.setWindowIcon(app_icon)

        self.all_packages_cache = []
        self.installed_packages_cache = set()

        self.loader_thread = None
        self.update_thread = None
        self.detail_thread = None
        self.console_thread = None

        self.init_ui()
        self.init_tray()
        self._setup_single_instance_server()

        geometry = self.settings.value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
        current_tab = self.settings.value("current_tab", 0, type=int)
        self.tabs.setCurrentIndex(current_tab)

        self.load_installed_only()
        QTimer.singleShot(3500, self.load_updates)

        self.auto_update_timer = QTimer(self)
        self.auto_update_timer.setInterval(3 * 60 * 60 * 1000)
        self.auto_update_timer.timeout.connect(self.load_updates)
        self.auto_update_timer.start()

        if self.current_lang == "it" and not _italian_locale_available():
            QTimer.singleShot(800, self._check_locale_warning)

        # Se Flatpak non è installato, disabilita i controlli relativi
        if not self._flatpak_available():
            self.btn_update_flatpak.setEnabled(False)
            self.btn_update_flatpak.setToolTip("Flatpak non installato sul sistema")
            for i in range(self.repo_combo.count()):
                if self.repo_combo.itemData(i) == "flatpak":
                    self.repo_combo.model().item(i).setEnabled(False)
                    break

    def _check_locale_warning(self):
        if self.current_lang == "it" and not _italian_locale_available():
            self.status_label.setText(self.tr("locale_missing_warning"))

    def tr(self, key, **kwargs):
        return _translate(self.current_lang, key, **kwargs)

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "it" else "it"
        self.settings.setValue("language", self.current_lang)
        self.retranslate_ui()

    def _populate_repo_combo(self):
        self.repo_combo.blockSignals(True)
        current_code = self.repo_combo.currentData() if self.repo_combo.count() > 0 else "all"
        self.repo_combo.clear()
        for code in REPO_CODES:
            self.repo_combo.addItem(self.tr(REPO_KEYS[code]), code)
        idx = 0
        for i, code in enumerate(REPO_CODES):
            if code == current_code:
                idx = i
                break
        self.repo_combo.setCurrentIndex(idx)
        self.repo_combo.blockSignals(False)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("window_title"))

        self.tabs.setTabText(0, self.tr("tab_packages"))
        self.tabs.setTabText(1, self.tr("tab_updates"))
        self.tabs.setTabText(2, self.tr("tab_maintenance"))

        self.search_input.setPlaceholderText(self.tr("search_placeholder"))
        self.btn_search.setText(self.tr("btn_search"))
        self.btn_clear_search.setText(self.tr("btn_show_all"))
        self.btn_filter_all.setText(self.tr("filter_all"))
        self.btn_filter_inst.setText(self.tr("filter_inst"))
        self.btn_filter_not_inst.setText(self.tr("filter_not_inst"))

        self.lbl_filter_state.setText(self.tr("filter_state"))
        self.lbl_filter_repo.setText(self.tr("filter_repo"))

        self._populate_repo_combo()

        self.table.setHorizontalHeaderLabels([self.tr("th_package"), self.tr("th_version"), self.tr("th_repo"), self.tr("th_desc")])
        self.console_output.setPlaceholderText(self.tr("console_placeholder"))

        self.btn_install.setText(self.tr("btn_install"))
        self.btn_remove.setText(self.tr("btn_remove"))
        self.btn_files.setText(self.tr("btn_files"))

        self.btn_refresh_updates.setText(self.tr("btn_refresh_updates"))
        self.btn_system_update.setText(self.tr("btn_system_update"))
        self.btn_full_update.setText(self.tr("btn_full_update"))
        self.btn_update_flatpak.setText(self.tr("btn_update_flatpak"))
        self.updates_table.setHorizontalHeaderLabels([self.tr("th_up_package"), self.tr("th_up_old_ver"), self.tr("th_up_new_ver"), self.tr("th_up_repo"), self.tr("th_up_action")])

        self.group_garuda.setTitle(self.tr("maint_garuda"))
        self.btn_garuda_health.setText(self.tr("btn_garuda_health"))
        self.btn_optimize_mirrors.setText(self.tr("btn_optimize_mirrors"))

        self.group_ignored.setTitle(self.tr("maint_ignored"))
        self.btn_manage_ignored.setText(self.tr("btn_manage_ignored"))

        self.group_cache.setTitle(self.tr("maint_cache"))
        self.btn_clean_pacman.setText(self.tr("btn_clean_pacman"))
        self.btn_clean_paru.setText(self.tr("btn_clean_paru"))
        self.btn_clean_yay.setText(self.tr("btn_clean_yay"))
        self.btn_clean_orphans.setText(self.tr("btn_clean_orphans"))

        self.group_repo.setTitle(self.tr("maint_repo"))
        self.btn_edit_pacman.setText(self.tr("btn_edit_pacman"))
        self.btn_edit_mirrors.setText(self.tr("btn_edit_mirrors"))
        self.btn_pacdiff.setText(self.tr("btn_pacdiff"))
        self.btn_refresh_keys.setText(self.tr("btn_refresh_keys"))
        self.btn_view_logs.setText(self.tr("btn_view_logs"))

        self.btn_lang_toggle.setText(self.tr("lang_btn"))

        self.update_tray_menu()

        active_count = sum(
            1 for pkg in self.cached_updates
            if pkg.get("name") not in self.ignored_packages
        )
        self.update_tray_icon_state(active_count)

        if self.current_lang == "it" and not _italian_locale_available():
            self.status_label.setText(self.tr("locale_missing_warning"))

    def _setup_single_instance_server(self):
        QLocalServer.removeServer(SOCKET_NAME)
        self.local_server = QLocalServer(self)
        self.local_server.newConnection.connect(self._on_new_instance_connection)
        self.local_server.listen(SOCKET_NAME)

    def _on_new_instance_connection(self):
        while self.local_server.hasPendingConnections():
            conn = self.local_server.nextPendingConnection()
            if conn:
                conn.readyRead.connect(lambda c=conn: self._handle_instance_message(c))
                conn.disconnected.connect(conn.deleteLater)

    def _handle_instance_message(self, conn):
        try:
            data = bytes(conn.readAll()).decode(errors="ignore")
            if "SHOW" in data:
                self.show()
                self.raise_()
                self.activateWindow()
        except Exception:
            pass

    def _flatpak_available(self):
        return shutil.which("flatpak") is not None

    def _cache_file_path(self):
        cache_dir = os.path.expanduser("~/.cache/garuda-package-manager")
        os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, "updates.json")

    def _save_cache_to_disk(self):
        try:
            with open(self._cache_file_path(), "w") as f:
                json.dump(self.cached_updates, f)
        except Exception as e:
            print(f"Errore salvataggio cache: {e}")

    def _load_cache_from_disk(self):
        try:
            path = self._cache_file_path()
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self.cached_updates = data

        except Exception as e:
            print(f"Errore caricamento cache: {e}")

    def _open_in_terminal(self, command):
        term_cmd = None
        for term in ["konsole", "alacritty", "kitty", "gnome-terminal", "xfce4-terminal", "foot"]:
            if shutil.which(term):
                if term == "konsole":
                    term_cmd = ["konsole", "-e"]
                elif term in ["alacritty", "kitty", "foot"]:
                    term_cmd = [term, "-e"]
                elif term in ["gnome-terminal", "xfce4-terminal"]:
                    term_cmd = [term, "--"]
                break
        if term_cmd is None:
            term_cmd = ["x-terminal-emulator", "-e"]
        try:
            subprocess.Popen(term_cmd + ["sh", "-c", command])
        except Exception as e:
            QMessageBox.warning(self, self.tr("msg_error_title"), self.tr("err_terminal", e=str(e)))

    def load_ignored_from_pacman(self):
        ignored = []
        try:
            with open("/etc/pacman.conf", "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "#" in line:
                        line = line.split("#", 1)[0].strip()
                    if line.startswith("IgnorePkg") and "=" in line:
                        val = line.split("=", 1)[1]
                        ignored.extend([p.strip() for p in val.split() if p.strip()])
        except Exception as e:
            print(f"Errore lettura pacman.conf: {e}")
        return list(set(ignored))

    def sync_ignored_to_pacman_conf(self, callback=None):
        conf_path = "/etc/pacman.conf"
        try:
            with open(conf_path, "r") as f:
                lines = f.readlines()
        except IOError as e:
            QMessageBox.critical(self, self.tr("msg_error_title"), self.tr("err_read_conf", path=conf_path, e=str(e)))
            return False

        new_lines = []
        for line in lines:
            if line.strip().startswith("IgnorePkg") and not line.strip().startswith("#"):
                continue
            new_lines.append(line)
            if line.strip() == "[options]":
                if self.ignored_packages:
                    pkg_str = " ".join(self.ignored_packages)
                    new_lines.append(f"IgnorePkg = {pkg_str}\n")

        fd, temp_path = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as f:
            f.writelines(new_lines)

        full_cmd = (
            f"sudo cp {temp_path} {conf_path}.new && "
            f"sudo mv {conf_path}.new {conf_path} && "
            f"sudo chmod 644 {conf_path} && "
            f"rm -f {temp_path}"
        )

        def on_finished():
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            self.ignored_packages = self.load_ignored_from_pacman()
            if callback:
                callback()

        self.run_in_konsole(full_cmd, callback=on_finished)
        return True

    def set_tray_actions_enabled(self, enabled):
        if hasattr(self, 'action_check_updates') and self.action_check_updates:
            self.action_check_updates.setEnabled(enabled)
        if hasattr(self, 'action_system_update') and self.action_system_update:
            self.action_system_update.setEnabled(enabled)
        if hasattr(self, 'action_full_update') and self.action_full_update:
            self.action_full_update.setEnabled(enabled)

    def set_execution_controls_enabled(self, enabled):
        self.set_tray_actions_enabled(enabled)

        update_buttons_info = [
            (getattr(self, 'btn_refresh_updates', None), ""),
            (getattr(self, 'btn_system_update', None), "background-color: #2e7d32; color: white; font-weight: bold;"),
            (getattr(self, 'btn_full_update', None), "background-color: #fbc02d; color: black; font-weight: bold;"),
            (getattr(self, 'btn_update_flatpak', None), "background-color: #0277bd; color: white; font-weight: bold;")
        ]

        always_active_buttons = [
            getattr(self, 'btn_filter_all', None),
            getattr(self, 'btn_filter_inst', None),
            getattr(self, 'btn_filter_not_inst', None),
            getattr(self, 'btn_search', None),
            getattr(self, 'btn_clear_search', None),
            getattr(self, 'btn_lang_toggle', None)
        ]

        for btn, original_style in update_buttons_info:
            if btn is not None and not sip.isdeleted(btn):
                btn.setEnabled(enabled)
                if not enabled:
                    btn.setStyleSheet("background-color: #555555; color: #aaaaaa; font-weight: bold;")
                else:
                    btn.setStyleSheet(original_style)

        excluded_buttons = [b[0] for b in update_buttons_info if b[0] is not None] + [b for b in always_active_buttons if b is not None]

        all_buttons = []
        all_buttons.extend(self.findChildren(QPushButton))
        all_buttons.extend(self.findChildren(QToolButton))

        search_input = getattr(self, 'search_input', None)

        for btn in all_buttons:
            if search_input is not None and search_input.isAncestorOf(btn):
                continue

            if btn not in excluded_buttons and not sip.isdeleted(btn):
                btn.setEnabled(enabled)
                if not enabled:
                    if btn.property("original_style") is None:
                        btn.setProperty("original_style", btn.styleSheet())
                    btn.setStyleSheet("background-color: #555555; color: #aaaaaa; font-weight: bold;")
                else:
                    orig_style = btn.property("original_style")
                    if orig_style is not None:
                        btn.setStyleSheet(orig_style)
                    else:
                        btn.setStyleSheet("")

    def start_system_update(self):
        count = 0
        for pkg in self.cached_updates:
            repo = pkg.get("repo", "").lower()
            if repo != "flatpak" and repo != "aur" and pkg.get("name") not in self.ignored_packages:
                count += 1

        self.cached_updates = []
        self.set_execution_controls_enabled(False)
        if self.tray_icon is not None:
            spinner = QIcon.fromTheme("process-working")
            if spinner.isNull():
                spinner = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
            self.tray_icon.setIcon(spinner)
            self.tray_icon.setToolTip(self.tr("tray_tooltip_sys_updating", n=count))
            skip_flag = " --skip-mirrorlist" if hasattr(self, 'chk_skip_mirrors') and self.chk_skip_mirrors.isChecked() else ""
            self.run_in_konsole(f"garuda-update{skip_flag}", callback=self.load_updates)

    def run_full_update_aur(self):
        count = 0
        for pkg in self.cached_updates:
            if pkg.get("repo", "").lower() != "flatpak" and pkg.get("name") not in self.ignored_packages:
                count += 1

        self.cached_updates = []
        self.set_execution_controls_enabled(False)
        if self.tray_icon is not None:
            spinner = QIcon.fromTheme("process-working")
            if spinner.isNull():
                spinner = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
            self.tray_icon.setIcon(spinner)
            self.tray_icon.setToolTip(self.tr("tray_tooltip_full_updating", n=count))
            skip_flag = " --skip-mirrorlist" if hasattr(self, 'chk_skip_mirrors') and self.chk_skip_mirrors.isChecked() else ""
            self.run_in_konsole(f"garuda-update -a{skip_flag}", callback=self.load_updates)

    def run_flatpak_update(self):
        if not self._flatpak_available():
            QMessageBox.information(self, "Flatpak", "Flatpak non è installato su questo sistema.")
            return
        self.set_execution_controls_enabled(False)
        flatpaks_to_update = []
        for pkg in self.cached_updates:
            if pkg.get("repo", "").lower() == "flatpak" and pkg.get("name") not in self.ignored_packages:
                flatpaks_to_update.append(pkg.get("name"))

        if not flatpaks_to_update:
            QMessageBox.information(self, "Flatpak", self.tr("flatpak_no_updates"))
            self.set_execution_controls_enabled(True)
            return

        count = len(flatpaks_to_update)
        self.cached_updates = []
        if self.tray_icon is not None:
            spinner = QIcon.fromTheme("process-working")
            if spinner.isNull():
                spinner = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
            self.tray_icon.setIcon(spinner)
            self.tray_icon.setToolTip(self.tr("tray_tooltip_flatpak_updating", n=count))
        self.run_in_konsole("flatpak update -y", callback=self.load_updates)

    def init_ui(self):
        self.status_label = QLabel(self.tr("status_ready"))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()
        self.btn_lang_toggle = QPushButton(self.tr("lang_btn"))
        self.btn_lang_toggle.setStyleSheet("font-weight: bold; padding: 4px 10px;")
        self.btn_lang_toggle.clicked.connect(self.toggle_language)
        top_bar_layout.addWidget(self.btn_lang_toggle)
        main_layout.addLayout(top_bar_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tab_packages = QWidget()
        self.tabs.addTab(self.tab_packages, self.tr("tab_packages"))
        packages_layout = QVBoxLayout(self.tab_packages)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr("search_placeholder"))
        self.search_input.setClearButtonEnabled(True)
        self.search_input.returnPressed.connect(self.start_search)

        self.btn_search = QPushButton(self.tr("btn_search"))
        self.btn_search.clicked.connect(self.start_search)

        self.btn_clear_search = QPushButton(self.tr("btn_show_all"))
        self.btn_clear_search.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.btn_search)
        search_layout.addWidget(self.btn_clear_search)
        packages_layout.addLayout(search_layout)

        filter_layout = QHBoxLayout()
        self.btn_filter_all = QPushButton(self.tr("filter_all"))
        self.btn_filter_all.setCheckable(True)
        self.btn_filter_all.setChecked(True)

        self.btn_filter_inst = QPushButton(self.tr("filter_inst"))
        self.btn_filter_inst.setCheckable(True)

        self.btn_filter_not_inst = QPushButton(self.tr("filter_not_inst"))
        self.btn_filter_not_inst.setCheckable(True)

        self.filter_group = QButtonGroup(self)
        self.filter_group.setExclusive(True)
        self.filter_group.addButton(self.btn_filter_all)
        self.filter_group.addButton(self.btn_filter_inst)
        self.filter_group.addButton(self.btn_filter_not_inst)
        self.filter_group.buttonClicked.connect(self.on_filter_button_clicked)

        self.current_state_filter = "all"

        self.lbl_filter_state = QLabel(self.tr("filter_state"))
        filter_layout.addWidget(self.lbl_filter_state)
        filter_layout.addWidget(self.btn_filter_all)
        filter_layout.addWidget(self.btn_filter_inst)
        filter_layout.addWidget(self.btn_filter_not_inst)

        self.lbl_filter_repo = QLabel(self.tr("filter_repo"))
        filter_layout.addWidget(self.lbl_filter_repo)

        self.repo_combo = QComboBox()
        for code in REPO_CODES:
            self.repo_combo.addItem(self.tr(REPO_KEYS[code]), code)
        self.repo_combo.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.repo_combo)
        filter_layout.addStretch()

        packages_layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([self.tr("th_package"), self.tr("th_version"), self.tr("th_repo"), self.tr("th_desc")])

        self.table.horizontalHeader().setSectionsMovable(True)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_row_selected)
        packages_layout.addWidget(self.table)

        header_state = self.settings.value("packages_header_state")
        if header_state:
            self.table.horizontalHeader().restoreState(header_state)

        self.console_output = QTextBrowser()
        self.console_output.setReadOnly(True)
        self.console_output.setOpenExternalLinks(True)
        self.console_output.setMaximumHeight(130)
        self.console_output.setPlaceholderText(self.tr("console_placeholder"))
        packages_layout.addWidget(self.console_output)

        action_layout = QHBoxLayout()
        self.btn_install = QPushButton(self.tr("btn_install"))
        self.btn_install.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold;")
        self.btn_install.clicked.connect(self.install_selected)

        self.btn_remove = QPushButton(self.tr("btn_remove"))
        self.btn_remove.setStyleSheet("background-color: #c62828; color: white; font-weight: bold;")
        self.btn_remove.clicked.connect(self.remove_selected)

        self.btn_files = QPushButton(self.tr("btn_files"))
        self.btn_files.setStyleSheet("background-color: #1565c0; color: white; font-weight: bold;")
        self.btn_files.clicked.connect(self.show_installed_files)

        action_layout.addWidget(self.btn_install)
        action_layout.addWidget(self.btn_remove)
        action_layout.addWidget(self.btn_files)
        packages_layout.addLayout(action_layout)

        self.tab_updates = QWidget()
        self.tabs.addTab(self.tab_updates, self.tr("tab_updates"))
        updates_layout = QVBoxLayout(self.tab_updates)

        up_top_layout = QHBoxLayout()
        self.btn_refresh_updates = QPushButton(self.tr("btn_refresh_updates"))
        self.btn_refresh_updates.clicked.connect(self.load_updates)

        self.btn_system_update = QPushButton(self.tr("btn_system_update"))
        self.btn_system_update.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold;")
        self.btn_system_update.clicked.connect(self.start_system_update)

        self.btn_full_update = QPushButton(self.tr("btn_full_update"))
        self.btn_full_update.setStyleSheet("background-color: #fbc02d; color: black; font-weight: bold;")
        self.btn_full_update.clicked.connect(self.run_full_update_aur)

        self.btn_update_flatpak = QPushButton(self.tr("btn_update_flatpak"))
        self.btn_update_flatpak.setStyleSheet("background-color: #0277bd; color: white; font-weight: bold;")
        self.btn_update_flatpak.clicked.connect(self.run_flatpak_update)

        up_top_layout.addWidget(self.btn_refresh_updates)
        up_top_layout.addWidget(self.btn_system_update)
        up_top_layout.addWidget(self.btn_full_update)
        up_top_layout.addWidget(self.btn_update_flatpak)
        up_top_layout.addStretch()
        updates_layout.addLayout(up_top_layout)

        opt_layout = QHBoxLayout()
        self.chk_skip_mirrors = QCheckBox(self.tr("chk_skip_mirrors"))
        self.chk_skip_mirrors.setToolTip(self.tr("chk_skip_mirrors_tooltip"))
        opt_layout.addWidget(self.chk_skip_mirrors)
        opt_layout.addStretch()
        updates_layout.addLayout(opt_layout)

        self.updates_table = QTableWidget()
        self.updates_table.setColumnCount(4)
        self.updates_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.updates_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.updates_table.setHorizontalHeaderLabels([self.tr("th_up_package"), self.tr("th_up_old_ver"), self.tr("th_up_new_ver"), self.tr("th_up_repo")])

        self.updates_table.horizontalHeader().setSectionsMovable(True)
        self.updates_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        updates_layout.addWidget(self.updates_table)

        # Pulsanti di azione sotto la tabella (come nella sezione Pacchetti)
        updates_action_layout = QHBoxLayout()

        self.btn_ignore_selected = QPushButton(self.tr("btn_ignore_selected"))
        self.btn_ignore_selected.setStyleSheet("background-color: #c62828; color: white; font-weight: bold;")
        self.btn_ignore_selected.clicked.connect(self.ignore_selected_updates)

        self.btn_unignore_selected = QPushButton(self.tr("btn_unignore_selected"))
        self.btn_unignore_selected.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold;")
        self.btn_unignore_selected.clicked.connect(self.unignore_selected_updates)

        updates_action_layout.addWidget(self.btn_ignore_selected)
        updates_action_layout.addWidget(self.btn_unignore_selected)

        updates_layout.addLayout(updates_action_layout)

        updates_header_state = self.settings.value("updates_header_state_v2")
        if updates_header_state:
            self.updates_table.horizontalHeader().restoreState(updates_header_state)

        self.updates_status_label = QLabel(self.tr("status_ready"))
        updates_layout.addWidget(self.updates_status_label)

        self.tab_maintenance = QWidget()
        self.tabs.addTab(self.tab_maintenance, self.tr("tab_maintenance"))
        maint_layout = QVBoxLayout(self.tab_maintenance)

        self.group_garuda = QGroupBox(self.tr("maint_garuda"))
        garuda_layout = QHBoxLayout(self.group_garuda)

        self.btn_garuda_health = QPushButton(self.tr("btn_garuda_health"))
#       self.btn_garuda_health.setStyleSheet("background-color: #0277bd; color: white; font-weight: bold;")
        self.btn_garuda_health.clicked.connect(lambda: self.run_in_konsole("garuda-health --fix"))

        self.btn_optimize_mirrors = QPushButton(self.tr("btn_optimize_mirrors"))
        self.btn_optimize_mirrors.clicked.connect(lambda: self.run_in_konsole("garuda-optimize-mirrors"))

        garuda_layout.addWidget(self.btn_garuda_health)
        garuda_layout.addWidget(self.btn_optimize_mirrors)
        maint_layout.addWidget(self.group_garuda)

        self.group_ignored = QGroupBox(self.tr("maint_ignored"))
        ignored_layout = QHBoxLayout(self.group_ignored)
        self.btn_manage_ignored = QPushButton(self.tr("btn_manage_ignored"))
#       self.btn_manage_ignored.setStyleSheet("background-color: #0277bd; color: white; font-weight: bold;")
        self.btn_manage_ignored.clicked.connect(self.open_ignored_packages_dialog)
        ignored_layout.addWidget(self.btn_manage_ignored)
        maint_layout.addWidget(self.group_ignored)

        self.group_cache = QGroupBox(self.tr("maint_cache"))
        cache_layout = QGridLayout(self.group_cache)

        self.btn_clean_pacman = QPushButton(self.tr("btn_clean_pacman"))
        self.btn_clean_pacman.clicked.connect(lambda: self.run_in_konsole("sudo paccache -r; echo 'Fatto!'; read"))

        self.btn_clean_paru = QPushButton(self.tr("btn_clean_paru"))
        self.btn_clean_paru.clicked.connect(lambda: self.run_in_konsole("paru -Sc --noconfirm; rm -rf ~/.cache/paru/*; echo 'Fatto!'; read"))

        self.btn_clean_yay = QPushButton(self.tr("btn_clean_yay"))
        self.btn_clean_yay.clicked.connect(lambda: self.run_in_konsole("yay -Sc --noconfirm; rm -rf ~/.cache/yay/*; echo 'Fatto!'; read"))

        self.btn_clean_orphans = QPushButton(self.tr("btn_clean_orphans"))
#       self.btn_clean_orphans.setStyleSheet("background-color: #c62828; color: white; font-weight: bold;")
        orphan_safe_cmd = (
            "echo '=== ANALISI PACCHETTI ORFANI ===';"
            "pacman -Qdt || echo 'Nessun pacchetto orfano trovato.';"
            "echo '----------------------------------';"
            "if [ -n \"$(pacman -Qtdq)\" ]; then"
            "  echo '';"
            "  read -p 'Vuoi procedere alla rimozione di questi pacchetti? (s/N): ' resp;"
            "  if [ \"$resp\" = 's' ] || [ \"$resp\" = 'S' ]; then"
            "    sudo pacman -Rns $(pacman -Qtdq);"
            "  else"
            "    echo \"Operazione di rimozione annullata dall'utente.\";"
            "  fi;"
            "fi;"
            "echo ''; echo 'Operazione completata. Premi Invio per chiudere...'; read"
        )
        self.btn_clean_orphans.clicked.connect(lambda: self.run_in_konsole(orphan_safe_cmd))

        cache_layout.addWidget(self.btn_clean_pacman, 0, 0)
        cache_layout.addWidget(self.btn_clean_paru, 0, 1)
        cache_layout.addWidget(self.btn_clean_yay, 1, 0, 1, 2)
        cache_layout.addWidget(self.btn_clean_orphans, 2, 0, 1, 2)
        maint_layout.addWidget(self.group_cache)

        self.group_repo = QGroupBox(self.tr("maint_repo"))
        repo_layout = QGridLayout(self.group_repo)

        self.btn_edit_pacman = QPushButton(self.tr("btn_edit_pacman"))
        self.btn_edit_pacman.clicked.connect(lambda: self._open_in_terminal("sudo nano /etc/pacman.conf"))

        self.btn_edit_mirrors = QPushButton(self.tr("btn_edit_mirrors"))
        self.btn_edit_mirrors.clicked.connect(lambda: self._open_in_terminal("sudo nano /etc/pacman.d/mirrorlist"))

        self.btn_pacdiff = QPushButton(self.tr("btn_pacdiff"))
        self.btn_pacdiff.clicked.connect(lambda: self._open_in_terminal("sudo pacdiff"))

        self.btn_refresh_keys = QPushButton(self.tr("btn_refresh_keys"))
        self.btn_refresh_keys.clicked.connect(lambda: self._open_in_terminal("sudo pacman -Syu garuda-keyring archlinux-keyring; echo; echo 'Fatto! Premi Invio...'; read"))

        self.btn_view_logs = QPushButton(self.tr("btn_view_logs"))
        self.btn_view_logs.clicked.connect(self.show_pacman_logs)

        repo_layout.addWidget(self.btn_edit_pacman, 0, 0)
        repo_layout.addWidget(self.btn_edit_mirrors, 0, 1)
        repo_layout.addWidget(self.btn_pacdiff, 1, 0)
        repo_layout.addWidget(self.btn_refresh_keys, 1, 1)
        repo_layout.addWidget(self.btn_view_logs, 2, 0, 1, 2)

        maint_layout.addWidget(self.group_repo)
        main_layout.addWidget(self.status_label)

    def open_ignored_packages_dialog(self):
        self.ignored_packages = self.load_ignored_from_pacman()
        dialog = IgnoredPackagesDialog(self)
        dialog.exec()

    def run_in_konsole(self, command, callback=None):
        try:
            if self.console_thread and not sip.isdeleted(self.console_thread) and self.console_thread.isRunning():
                try:
                    self.console_thread.finished.disconnect()
                except Exception:
                    pass

            self.set_execution_controls_enabled(False)

            self.console_thread = ConsoleRunnerThread(command)
            self.console_thread.finished.connect(self.console_thread.deleteLater)

            self.console_thread.finished.connect(lambda: self.set_execution_controls_enabled(True))
            if callback:
                self.console_thread.finished.connect(callback)
            self.console_thread.start()
        except Exception as e:
            self.set_execution_controls_enabled(True)
            QMessageBox.warning(self, self.tr("msg_error_title"), self.tr("err_terminal", e=str(e)))

    def init_tray(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = None
            return

        self.tray_icon = QSystemTrayIcon(self)
        self.update_tray_icon_state(0)

        self.tray_menu = QMenu()
        self.update_tray_menu()

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def update_tray_menu(self):
        if not hasattr(self, 'tray_menu') or self.tray_menu is None:
            return
        self.tray_menu.clear()

        self.action_check_updates = self.tray_menu.addAction(self.tr("tray_check"))
        self.action_check_updates.triggered.connect(self.check_updates)

        self.action_system_update = self.tray_menu.addAction(self.tr("tray_sys_update"))
        self.action_system_update.triggered.connect(self.start_system_update)

        self.action_full_update = self.tray_menu.addAction(self.tr("tray_full_update"))
        self.action_full_update.triggered.connect(self.run_full_update_aur)

        self.tray_menu.addSeparator()

        action_quit = self.tray_menu.addAction(self.tr("tray_quit"))
        action_quit.triggered.connect(self.quit_application)

    def update_tray_icon_state(self, updates_count):
        if self.tray_icon is None:
            return
        if updates_count > 0:
            icon = QIcon.fromTheme("software-update-available")
            if icon.isNull():
                icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
            self.tray_icon.setIcon(icon)
            self.tray_icon.setToolTip(self.tr("tray_tooltip_updates", n=updates_count))
        else:
            icon = QIcon.fromTheme("system-software-update")
            if icon.isNull():
                icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
            self.tray_icon.setIcon(icon)
            self.tray_icon.setToolTip(self.tr("tray_tooltip_updated"))

    def quit_application(self):
        self.is_quitting = True
        self.close()

    def load_updates(self):
        self.ignored_packages = self.load_ignored_from_pacman()
        self.set_execution_controls_enabled(False)

        if self.update_thread and not sip.isdeleted(self.update_thread) and self.update_thread.isRunning():
            try:
                self.update_thread.finished.disconnect()
            except Exception:
                pass
            self.update_thread.quit()
            self.update_thread.wait(200)

        self.btn_refresh_updates.setEnabled(False)
        self.updates_status_label.setText(self.tr("updates_checking"))

        self.update_thread = UpdateLoaderThread(ignored_packages=self.ignored_packages)
        self.update_thread.finished.connect(self.update_thread.deleteLater)
        self.update_thread.finished.connect(self.on_updates_loaded)

        if self.tray_icon is not None:
            checking_icon = QIcon.fromTheme("view-refresh")
            if checking_icon.isNull():
                checking_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
            self.tray_icon.setIcon(checking_icon)
            self.tray_icon.setToolTip(self.tr("tray_tooltip_checking"))

        self.update_thread.start()

    def on_updates_loaded(self, updates, has_conn, scan_ok):
        self.set_execution_controls_enabled(True)
        self.btn_refresh_updates.setEnabled(True)

        # Se la connessione c'è ma la scansione non è affidabile (comandi
        # falliti silenziosamente, tipico al boot), usa la cache persistita
        if has_conn and not scan_ok and self.cached_updates:
            active_updates = [pkg for pkg in self.cached_updates if pkg.get("name") not in self.ignored_packages]
            count = len(active_updates)
            self.populate_updates_table(self.cached_updates)
            self.updates_status_label.setText(self.tr("updates_offline_partial", n=count))
            self.update_tray_icon_state(count)
            return

        if not has_conn:
            if self.cached_updates:
                active_updates = [pkg for pkg in self.cached_updates if pkg.get("name") not in self.ignored_packages]
                count = len(active_updates)
                self.populate_updates_table(self.cached_updates)
                self.updates_status_label.setText(self.tr("updates_offline_partial", n=count))
                self.update_tray_icon_state(count)
            else:
                self.populate_updates_table([])
                self.updates_status_label.setText(self.tr("updates_offline_none"))
                self.update_tray_icon_state(0)
            return

        self.cached_updates = updates
        self._save_cache_to_disk()
        self.populate_updates_table(updates)

        active_updates = [pkg for pkg in updates if pkg.get("name") not in self.ignored_packages]
        count = len(active_updates)
        total_bytes = sum(pkg.get("size", 0) for pkg in active_updates if isinstance(pkg.get("size", 0), (int, float)))

        if total_bytes > 0:
            size_mb = total_bytes / (1024 * 1024)
            size_text = f" (~{size_mb:.1f} MB)" if size_mb < 1024 else f" (~{size_mb / 1024:.2f} GB)"
        else:
            size_text = ""

        ignored_count = len(updates) - count
        ignored_str = self.tr("ignored_suffix", n=ignored_count) if ignored_count > 0 else ""

        if count == 0 and ignored_count == 0:
            self.updates_status_label.setText(self.tr("updates_all_updated"))
        else:
            self.updates_status_label.setText(self.tr("updates_found", n=count, size=size_text, ignored=ignored_str))

        self.update_tray_icon_state(count)

    def populate_updates_table(self, updates):
        self.updates_table.blockSignals(True)
        self.updates_table.setRowCount(len(updates))
        for row, pkg in enumerate(updates):
            pkg_name = pkg.get("name", "")
            is_ignored = pkg_name in self.ignored_packages

            item_name = QTableWidgetItem(pkg_name)
            item_old = QTableWidgetItem(pkg.get("old_version", ""))
            item_new = QTableWidgetItem(pkg.get("version", ""))
            item_repo = QTableWidgetItem(pkg.get("repo", ""))

            if is_ignored:
                gray_color = Qt.GlobalColor.darkGray
                item_name.setForeground(gray_color)
                item_old.setForeground(gray_color)
                item_new.setForeground(gray_color)
                item_repo.setForeground(gray_color)

            self.updates_table.setItem(row, 0, item_name)
            self.updates_table.setItem(row, 1, item_old)
            self.updates_table.setItem(row, 2, item_new)
            self.updates_table.setItem(row, 3, item_repo)
        self.updates_table.blockSignals(False)

    def ignore_selected_updates(self):
        rows = sorted(set(item.row() for item in self.updates_table.selectedItems()))
        if not rows:
            QMessageBox.warning(self, self.tr("msg_warning_title"), self.tr("warn_select_pkg"))
            return

        to_add = []
        for row in rows:
            item_name = self.updates_table.item(row, 0)
            if item_name:
                name = item_name.text()
                if name and name not in self.ignored_packages:
                    to_add.append(name)

        if not to_add:
            return

        for name in to_add:
            self.ignored_packages.append(name)

        def on_success():
            self.load_updates()

        if not self.sync_ignored_to_pacman_conf(callback=on_success):
            for name in to_add:
                if name in self.ignored_packages:
                    self.ignored_packages.remove(name)

    def unignore_selected_updates(self):
        rows = sorted(set(item.row() for item in self.updates_table.selectedItems()))
        if not rows:
            QMessageBox.warning(self, self.tr("msg_warning_title"), self.tr("warn_select_pkg"))
            return

        to_remove = []
        for row in rows:
            item_name = self.updates_table.item(row, 0)
            if item_name:
                name = item_name.text()
                if name and name in self.ignored_packages:
                    to_remove.append(name)

        if not to_remove:
            return

        for name in to_remove:
            self.ignored_packages.remove(name)

        def on_success():
            self.load_updates()

        if not self.sync_ignored_to_pacman_conf(callback=on_success):
            for name in to_remove:
                self.ignored_packages.append(name)

    def set_package_ignored(self, pkg_name, ignore):
        if ignore:
            if pkg_name not in self.ignored_packages:
                self.ignored_packages.append(pkg_name)
                def on_success():
                    self.load_updates()
                if not self.sync_ignored_to_pacman_conf(callback=on_success):
                    self.ignored_packages.remove(pkg_name)
        else:
            if pkg_name in self.ignored_packages:
                self.ignored_packages.remove(pkg_name)
                def on_success():
                    self.load_updates()
                if not self.sync_ignored_to_pacman_conf(callback=on_success):
                    self.ignored_packages.append(pkg_name)

    def check_updates(self):
        self.set_execution_controls_enabled(False)
        self.load_updates()
        if self.tray_icon is not None:
            self.tray_icon.showMessage(
                self.tr("tray_check_title"),
                self.tr("tray_check_msg"),
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )

    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_window()

    def closeEvent(self, event):
        self.settings.setValue("window_geometry", self.saveGeometry())
        self.settings.setValue("packages_header_state", self.table.horizontalHeader().saveState())
        self.settings.setValue("updates_header_state_v2", self.updates_table.horizontalHeader().saveState())
        self.settings.setValue("current_tab", self.tabs.currentIndex())

        for thread in [self.loader_thread, self.update_thread, self.detail_thread, self.console_thread]:
            if thread and not sip.isdeleted(thread) and thread.isRunning():
                try:
                    thread.finished.disconnect()
                except Exception:
                    pass
                thread.quit()
                thread.wait(150)

        tray_ok = (self.tray_icon is not None) and QSystemTrayIcon.isSystemTrayAvailable()

        if getattr(self, 'is_quitting', False) or not tray_ok:
            if self.tray_icon is not None:
                self.tray_icon.hide()
            event.accept()
        else:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                self.tr("tray_running_title"),
                self.tr("tray_running_msg"),
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

    def set_ui_loading_state(self, loading):
        self.btn_search.setEnabled(not loading)
        self.btn_clear_search.setEnabled(not loading)
        self.search_input.setEnabled(not loading)

    def on_filter_button_clicked(self, button):
        if button == self.btn_filter_all:
            self.set_filter_state("all")
        elif button == self.btn_filter_inst:
            self.set_filter_state("installed")
        elif button == self.btn_filter_not_inst:
            self.set_filter_state("not_installed")

    def set_filter_state(self, state):
        self.current_state_filter = state
        if state in ("all", "not_installed"):
            has_uninstalled = any(not p.get("installed", False) for p in self.all_packages_cache)
            if not has_uninstalled:
                self.load_all_packages()
                return
        self.apply_filters()

    def clear_search(self):
        self.search_input.clear()
        self.current_state_filter = "all"
        self.btn_filter_all.setChecked(True)
        self.repo_combo.blockSignals(True)
        self.repo_combo.setCurrentIndex(0)
        self.repo_combo.blockSignals(False)
        self.load_all_packages()

    def load_installed_only(self):
        if self.loader_thread and not sip.isdeleted(self.loader_thread) and self.loader_thread.isRunning():
            try:
                self.loader_thread.finished.disconnect()
            except Exception:
                pass
            self.loader_thread.quit()
            self.loader_thread.wait(200)

        self.set_ui_loading_state(True)
        self.status_label.setText(self.tr("loading_installed"))
        self.loader_thread = PackageLoaderThread(search_query="", show_all=False)
        self.loader_thread.finished.connect(self.loader_thread.deleteLater)
        self.loader_thread.finished.connect(self.on_packages_loaded)
        self.loader_thread.start()

    def load_all_packages(self):
        if self.loader_thread and not sip.isdeleted(self.loader_thread) and self.loader_thread.isRunning():
            try:
                self.loader_thread.finished.disconnect()
            except Exception:
                pass
            self.loader_thread.quit()
            self.loader_thread.wait(200)

        self.set_ui_loading_state(True)
        self.status_label.setText(self.tr("loading_all"))
        self.loader_thread = PackageLoaderThread(search_query="", show_all=True)
        self.loader_thread.finished.connect(self.loader_thread.deleteLater)
        self.loader_thread.finished.connect(self.on_packages_loaded)
        self.loader_thread.start()

    def show_pacman_logs(self):
        log_path = "/var/log/pacman.log"
        try:
            result = subprocess.run(
                ["tail", "-n", "5000", log_path],
                capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                content = result.stdout
            else:
                content = self.tr("logs_read_error", e=result.stderr)

            if not content.strip():
                content = self.tr("logs_empty")

            dialog = QDialog(self)
            dialog.setWindowTitle(self.tr("logs_dialog_title"))
            dialog.resize(850, 600)

            layout = QVBoxLayout(dialog)
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setPlainText(content)

            font = QFont("Monospace")
            font.setStyleHint(QFont.StyleHint.Monospace)
            text_edit.setFont(font)

            cursor = text_edit.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            text_edit.setTextCursor(cursor)

            layout.addWidget(text_edit)

            btn_close = QPushButton(self.tr("dlg_btn_close"))
            btn_close.clicked.connect(dialog.accept)
            layout.addWidget(btn_close)

            dialog.exec()
        except Exception as e:
            self.console_output.setHtml(f"**{self.tr('msg_error_title')}**: {str(e)}")

    def start_search(self):
        query = self.search_input.text().strip()
        if not query:
            self.load_installed_only()
            return

        if self.loader_thread and not sip.isdeleted(self.loader_thread) and self.loader_thread.isRunning():
            try:
                self.loader_thread.finished.disconnect()
            except Exception:
                pass
            self.loader_thread.quit()
            self.loader_thread.wait(200)

        self.set_ui_loading_state(True)
        self.status_label.setText(self.tr("searching", q=query))
        self.loader_thread = PackageLoaderThread(search_query=query, show_all=False)
        self.loader_thread.finished.connect(self.loader_thread.deleteLater)
        self.loader_thread.finished.connect(self.on_packages_loaded)
        self.loader_thread.start()

    def on_packages_loaded(self, all_packages, installed_packages):
        self.set_ui_loading_state(False)
        self.all_packages_cache = all_packages
        self.installed_packages_cache = installed_packages
        self.apply_filters()
        self.status_label.setText(self.tr("status_totals", t=len(all_packages), i=len(installed_packages)))

    def apply_filters(self):
        try:
            selected_repo_code = self.repo_combo.currentData()
            if selected_repo_code is None:
                selected_repo_code = "all"

            filtered = []
            for pkg in self.all_packages_cache:
                is_inst = pkg.get("installed", False)
                repo_str = str(pkg.get("repo", "")).lower()

                if self.current_state_filter == "installed" and not is_inst:
                    continue
                if self.current_state_filter == "not_installed" and is_inst:
                    continue

                if selected_repo_code == "official":
                    if repo_str in ("aur", "flatpak"):
                        continue
                elif selected_repo_code != "all":
                    if repo_str != selected_repo_code:
                        continue

                filtered.append(pkg)

            repo_order = {"core": 0, "extra": 1, "multilib": 2, "aur": 3, "flatpak": 4}
            filtered.sort(key=lambda x: (repo_order.get(str(x.get("repo", "")).lower(), 5), str(x.get("name", "")).lower()))

            self.populate_table(filtered)
            total_pkgs = len(self.all_packages_cache)
            installed_count = len(self.installed_packages_cache)
            self.status_label.setText(self.tr("status_filtered", v=len(filtered), t=total_pkgs, i=installed_count))

        except Exception as e:
            self.console_output.setHtml(f"**{self.tr('msg_error_title')}**: {str(e)}")

    def populate_table(self, packages):
        try:
            self.table.blockSignals(True)
            self.table.setRowCount(len(packages))
            for row, pkg in enumerate(packages):
                item_name = QTableWidgetItem(str(pkg.get("name", "")))
                item_version = QTableWidgetItem(str(pkg.get("version", "")))
                item_repo = QTableWidgetItem(str(pkg.get("repo", "")))
                item_desc = QTableWidgetItem(str(pkg.get("desc", "")))

                if pkg.get("installed", False):
                    item_name.setForeground(Qt.GlobalColor.darkGreen)

                self.table.setItem(row, 0, item_name)
                self.table.setItem(row, 1, item_version)
                self.table.setItem(row, 2, item_repo)
                self.table.setItem(row, 3, item_desc)
            self.table.blockSignals(False)
        except Exception as e:
            self.table.blockSignals(False)
            self.console_output.setHtml(f"**{self.tr('msg_error_title')}**: {str(e)}")

    def on_row_selected(self):
        row = self.table.currentRow()
        if row < 0 or row >= self.table.rowCount():
            return

        item_name = self.table.item(row, 0)
        item_repo = self.table.item(row, 2)
        item_desc = self.table.item(row, 3)

        if not item_name or not item_repo:
            return

        name = item_name.text()
        repo = item_repo.text()
        desc = item_desc.text() if item_desc else ""

        self.console_output.setHtml(f"*{self.tr('loading_details', name=name)}*")

        if self.detail_thread and not sip.isdeleted(self.detail_thread) and self.detail_thread.isRunning():
            try:
                self.detail_thread.finished.disconnect()
                self.detail_thread.quit()
                if not self.detail_thread.wait(2000):
                    # Il thread non risponde: non aspettare, lascialo morire da solo
                    self.detail_thread = None
                    return
            except Exception:
                pass

        self.detail_thread = PackageDetailThread(name, repo, desc, lang=self.current_lang)
        self.detail_thread.finished.connect(self.detail_thread.deleteLater)
        self.detail_thread.finished.connect(self.console_output.setHtml)
        self.detail_thread.start()

    def install_selected(self):
        row = self.table.currentRow()
        if row < 0 or row >= self.table.rowCount():
            return
        item = self.table.item(row, 0)
        repo_item = self.table.item(row, 2)
        if not item or not repo_item:
            return

        name = item.text()
        repo = repo_item.text().lower()
        if repo == "flatpak":
            self.run_in_konsole(f"flatpak install {name}", callback=self.load_installed_only)
        elif repo == "aur":
            self.run_in_konsole(f"paru -S {name}", callback=self.load_installed_only)
        else:
            self.run_in_konsole(f"sudo pacman -S {name}", callback=self.load_installed_only)

    def remove_selected(self):
        row = self.table.currentRow()
        if row < 0 or row >= self.table.rowCount():
            return
        item = self.table.item(row, 0)
        repo_item = self.table.item(row, 2)
        if not item or not repo_item:
            return

        name = item.text()
        repo = repo_item.text().lower()
        if repo == "flatpak":
            self.run_in_konsole(f"flatpak uninstall {name}", callback=self.load_installed_only)
        else:
            self.run_in_konsole(f"sudo pacman -Rns {name}", callback=self.load_installed_only)

    def show_installed_files(self):
        row = self.table.currentRow()
        if row < 0 or row >= self.table.rowCount():
            return
        item = self.table.item(row, 0)
        repo_item = self.table.item(row, 2)
        if not item or not repo_item:
            return

        name = item.text()
        repo = repo_item.text().lower()
        if repo == "flatpak":
            self.run_in_konsole(f"flatpak info {name}; echo ''; read")
        else:
            self.run_in_konsole(f"pacman -Ql {name} | less", callback=None)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("GarudaPackageManager")
    app.setDesktopFileName("garuda-package-manager")

    probe = QLocalSocket()
    probe.connectToServer(SOCKET_NAME)
    if probe.waitForConnected(300):
        probe.write(b"SHOW")
        probe.flush()
        probe.waitForBytesWritten(300)
        probe.disconnectFromServer()
        sys.exit(0)

    window = GarudaPackageManager()
    if "--tray" not in sys.argv:
        window.show()
    sys.exit(app.exec())
