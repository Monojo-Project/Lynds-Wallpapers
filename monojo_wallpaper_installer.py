#!/usr/bin/env python3
"""
Lynds Wallpaper Installer
Descarga ramas de github.com/Monojo-Project/Lynds-Wallpapers e instala los wallpapers en ~/.local/share/wallpapers/
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import urllib.request
import urllib.error
import json
import os
import shutil
import zipfile
import tempfile


# ── Configuración ────────────────────────────────────────────────────────────
GITHUB_USER = "Monojo-Project"
GITHUB_REPO = "Lynds-Wallpapers"
INSTALL_BASE = os.path.expanduser("~/.local/share/wallpapers")
API_BRANCHES  = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/branches"
ZIP_URL       = "https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
# ─────────────────────────────────────────────────────────────────────────────


def fetch_branches():
    """Obtiene la lista de ramas del repositorio via la API de GitHub."""
    req = urllib.request.Request(
        API_BRANCHES,
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "MonojoWallpaperInstaller/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    return [b["name"] for b in data]


def is_installed(branch_name):
    path = os.path.join(INSTALL_BASE, branch_name)
    return os.path.isdir(path) and bool(os.listdir(path))


def download_and_install(branch, progress_cb, status_cb):
    """
    Descarga el ZIP de la rama y lo extrae en ~/.local/share/wallpapers/<branch>.
    progress_cb(value)  → actualiza la barra (0–100)
    status_cb(text)     → actualiza la etiqueta de estado
    """
    url = ZIP_URL.format(user=GITHUB_USER, repo=GITHUB_REPO, branch=branch)
    dest_dir = os.path.join(INSTALL_BASE, branch)

    status_cb(f"Conectando con GitHub…")
    os.makedirs(INSTALL_BASE, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, f"{branch}.zip")

        # ── Descarga con progreso ────────────────────────────────────────────
        status_cb(f"Descargando '{branch}'…")

        def _reporthook(block_num, block_size, total_size):
            if total_size > 0:
                pct = min(block_num * block_size / total_size * 90, 90)
                progress_cb(int(pct))

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "MonojoWallpaperInstaller/1.0"}
            )
            # urllib.request.urlretrieve no soporta headers; usamos urlopen manual
            with urllib.request.urlopen(req, timeout=60) as resp:
                total = int(resp.getheader("Content-Length", 0))
                downloaded = 0
                chunk = 65536
                with open(zip_path, "wb") as f:
                    while True:
                        buf = resp.read(chunk)
                        if not buf:
                            break
                        f.write(buf)
                        downloaded += len(buf)
                        if total:
                            progress_cb(int(downloaded / total * 90))
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP {e.code}: no se pudo descargar la rama '{branch}'.\n"
                               f"Verifica que el repositorio exista y la rama sea correcta.")

        # ── Extracción ───────────────────────────────────────────────────────
        status_cb("Descomprimiendo…")
        extract_dir = os.path.join(tmp, "extracted")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)
        progress_cb(95)

        # El ZIP de GitHub crea una carpeta raíz tipo "Repo-branch/"
        entries = os.listdir(extract_dir)
        if len(entries) == 1 and os.path.isdir(os.path.join(extract_dir, entries[0])):
            source = os.path.join(extract_dir, entries[0])
        else:
            source = extract_dir

        # ── Copia al destino ─────────────────────────────────────────────────
        status_cb(f"Instalando en {dest_dir}…")
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        shutil.copytree(source, dest_dir)
        progress_cb(100)
        status_cb(f"✅  Instalado en {dest_dir}")


# ── GUI ───────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lynds Wallpaper Installer")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self._build_ui()
        self._load_branches()

    # ── Construcción de la interfaz ──────────────────────────────────────────
    def _build_ui(self):
        PAD = 18
        BG      = "#1e1e2e"
        FG      = "#cdd6f4"
        ACCENT  = "#89b4fa"
        BTN_BG  = "#313244"
        BTN_ACT = "#45475a"
        SEL_BG  = "#313244"

        # Cabecera
        hdr = tk.Frame(self, bg="#181825", pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🖼  Lynds Wallpaper Installer",
                 font=("Sans", 15, "bold"), fg=ACCENT, bg="#181825").pack()
        tk.Label(hdr,
                 text=f"github.com/{GITHUB_USER}/{GITHUB_REPO}",
                 font=("Mono", 9), fg="#6c7086", bg="#181825").pack()

        # Cuerpo
        body = tk.Frame(self, bg=BG, padx=PAD, pady=PAD)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Ramas disponibles:", fg=FG, bg=BG,
                 font=("Sans", 10, "bold")).pack(anchor="w")

        # Lista de ramas con scrollbar
        list_frame = tk.Frame(body, bg=BG)
        list_frame.pack(fill="both", expand=True, pady=(6, 12))

        scrollbar = tk.Scrollbar(list_frame, bg=BTN_BG, troughcolor=BG,
                                 highlightbackground=BG)
        scrollbar.pack(side="right", fill="y")

        self.branch_list = tk.Listbox(
            list_frame,
            selectmode="single",
            bg=SEL_BG, fg=FG, selectbackground=ACCENT,
            selectforeground="#1e1e2e",
            font=("Mono", 11), height=10, width=38,
            highlightthickness=0, bd=0,
            yscrollcommand=scrollbar.set
        )
        self.branch_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.branch_list.yview)
        self.branch_list.bind("<<ListboxSelect>>", self._on_select)

        # Etiqueta de estado de instalación
        self.install_label = tk.Label(body, text="", fg="#a6e3a1", bg=BG,
                                      font=("Sans", 9), wraplength=340, justify="left")
        self.install_label.pack(anchor="w")

        # Barra de progreso
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("custom.Horizontal.TProgressbar",
                        troughcolor=BTN_BG, background=ACCENT,
                        thickness=14, borderwidth=0)
        self.progress = ttk.Progressbar(body, style="custom.Horizontal.TProgressbar",
                                        orient="horizontal", length=340, mode="determinate")
        self.progress.pack(pady=(4, 10))

        # Botones
        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack()

        btn_cfg = dict(font=("Sans", 10, "bold"), relief="flat",
                       activebackground=BTN_ACT, activeforeground=FG,
                       cursor="hand2", padx=14, pady=6)

        self.btn_refresh = tk.Button(
            btn_row, text="🔄  Actualizar", bg=BTN_BG, fg=FG,
            command=self._load_branches, **btn_cfg)
        self.btn_refresh.pack(side="left", padx=(0, 8))

        self.btn_install = tk.Button(
            btn_row, text="⬇  Instalar", bg=ACCENT, fg="#1e1e2e",
            command=self._start_install, state="disabled", **btn_cfg)
        self.btn_install.pack(side="left")

        # Footer
        tk.Label(self, text=f"Destino: {INSTALL_BASE}",
                 fg="#6c7086", bg=BG, font=("Mono", 8)).pack(pady=(0, 8))

    # ── Lógica ───────────────────────────────────────────────────────────────
    def _load_branches(self):
        self.branch_list.delete(0, "end")
        self.branch_list.insert("end", "  Cargando ramas…")
        self.btn_install.config(state="disabled")
        self.install_label.config(text="")
        threading.Thread(target=self._fetch_branches_thread, daemon=True).start()

    def _fetch_branches_thread(self):
        try:
            branches = fetch_branches()
            self.after(0, self._populate_list, branches)
        except Exception as e:
            self.after(0, self._populate_list, None, str(e))

    def _populate_list(self, branches, error=None):
        self.branch_list.delete(0, "end")
        if error:
            messagebox.showerror("Error al obtener ramas",
                                 f"No se pudieron cargar las ramas:\n{error}\n\n"
                                 f"Comprueba la URL del repositorio en la configuración del script.")
            self.branch_list.insert("end", "  (sin datos)")
            return
        if not branches:
            self.branch_list.insert("end", "  (no hay ramas)")
            return
        for b in branches:
            marker = " ✓" if is_installed(b) else ""
            self.branch_list.insert("end", f"  {b}{marker}")

    def _on_select(self, _event=None):
        sel = self.branch_list.curselection()
        if sel:
            self.btn_install.config(state="normal")

    def _start_install(self):
        sel = self.branch_list.curselection()
        if not sel:
            return
        raw = self.branch_list.get(sel[0]).strip()
        branch = raw.rstrip(" ✓")  # quitar marcador si existe

        self.btn_install.config(state="disabled")
        self.btn_refresh.config(state="disabled")
        self.progress["value"] = 0
        self.install_label.config(text="Iniciando…", fg="#cba6f7")

        threading.Thread(
            target=self._install_thread,
            args=(branch,),
            daemon=True
        ).start()

    def _install_thread(self, branch):
        def progress_cb(val):
            self.after(0, lambda: self.progress.configure(value=val))

        def status_cb(text):
            self.after(0, lambda: self.install_label.config(text=text))

        try:
            download_and_install(branch, progress_cb, status_cb)
            self.after(0, self._on_install_done, branch, True)
        except Exception as e:
            self.after(0, self._on_install_done, branch, False, str(e))

    def _on_install_done(self, branch, success, error_msg=None):
        self.btn_install.config(state="normal")
        self.btn_refresh.config(state="normal")
        if success:
            self.install_label.config(
                text=f"✅  '{branch}' instalado en\n{INSTALL_BASE}/{branch}",
                fg="#a6e3a1")
            self._load_branches()   # refrescar lista (con ✓ actualizado)
        else:
            self.install_label.config(
                text=f"❌  Error: {error_msg}", fg="#f38ba8")
            messagebox.showerror("Error en la instalación", error_msg)


# ── Entrada ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
