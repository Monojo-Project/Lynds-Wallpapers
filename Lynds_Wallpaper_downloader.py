import tkinter as tk
import threading
import os
import shutil
import zipfile
import tempfile
import urllib.request
import json
import base64
import time
from pathlib import Path

# --- Configuración del Sistema Operativo ---
GITHUB_USER = "Monojo-Project"
GITHUB_REPO = "Lynds-Wallpapers"
INSTALL_BASE = os.path.expanduser("~/.local/share/wallpapers")

# Endpoints estratégicos de la API de GitHub
API_BRANCHES = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/branches"
API_CONTENTS = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents?ref={{branch}}"
API_COMMITS  = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/commits?per_page=4"
ZIP_URL = "https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
RAW_RECOMENDACIONES = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/RECOMENDACIONES"

class LyndsExecutive(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lynds Executive Terminal v7.0 - Nova's Kid AI Edition")
        self.geometry("1450x900")  
        self.configure(bg="#121412")
        
        self.selected_branch = None
        self.selected_files = set()  
        self.preview_img = None    
        
        # Estructuras de control en memoria de alta velocidad
        self.all_branches = []     
        self.gallery_images = {}  
        self.thumb_refs = {}      
        self.thumb_btns = {}       
        
        # --- Paleta de Colores Corporativa (Verde Puro Avanzado) ---
        self.c_bg = "#121412"         
        self.c_side = "#141614"       
        self.c_primary = "#16a34a"    
        self.c_text = "#e2e8f0"       
        self.c_btn = "#14532d"        
        self.c_alert = "#ef4444"      
        self.c_alert_bg = "#2d1616"   
        self.c_brass = "#eab308"
        
        # ================= ESTRUCTURA ARQUITECTÓNICA DE LA INTERFAZ =================
        self.sidebar = tk.Frame(self, bg=self.c_side, width=320)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        lbl_side = tk.Label(self.sidebar, text="MERCADO DE ACTIVOS", bg=self.c_side, fg=self.c_primary, font=("Courier", 12, "bold"))
        lbl_side.pack(pady=(20, 5), fill="x")
        
        # 1. BARRA DE BÚSQUEDA QUIRÚRGICA
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_branches)
        
        self.search_frame = tk.Frame(self.sidebar, bg=self.c_side)
        self.search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        lbl_search_icon = tk.Label(self.search_frame, text="🔍", bg=self.c_side, fg=self.c_primary, font=("Courier", 10))
        lbl_search_icon.pack(side="left", padx=(2, 5))
        
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, bg="#0d0f0d", fg=self.c_text,
                                     insertbackground=self.c_primary, font=("Courier", 11), relief="flat",
                                     highlightbackground="#222", highlightthickness=1)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.insert(0, "Buscar paquete...")
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, tk.END) if self.search_var.get() == "Buscar paquete..." else None)

        # 3. SECCIÓN DE NOVEDADES DEL SISTEMA (Live Feed)
        self.news_frame = tk.Frame(self.sidebar, bg=self.c_side)
        self.news_frame.pack(fill="x", side="bottom", padx=10, pady=(5, 15))
        
        lbl_news = tk.Label(self.news_frame, text="📢 NOVEDADES (LIVE GITHUB)", bg=self.c_side, fg=self.c_primary, font=("Courier", 10, "bold"), anchor="w")
        lbl_news.pack(fill="x", padx=5, pady=(0, 4))
        
        self.lbl_news_box = tk.Label(self.news_frame, text="Sincronizando feed del mercado...", bg="#0d0f0d", fg="#a1a1aa", 
                                     font=("Courier", 9), justify="left", anchor="w", padx=10, pady=8,
                                     highlightbackground="#222", highlightthickness=1)
        self.lbl_news_box.pack(fill="x")

        # 2. SECCIÓN DE RECOMENDACIONES DINÁMICAS
        self.rec_frame = tk.Frame(self.sidebar, bg=self.c_side)
        self.rec_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        
        lbl_rec = tk.Label(self.rec_frame, text="⚡ RECOMENDADOS (MAIN)", bg=self.c_side, fg=self.c_primary, font=("Courier", 10, "bold"), anchor="w")
        lbl_rec.pack(fill="x", padx=5, pady=(0, 4))
        
        self.rec_list_frame = tk.Frame(self.rec_frame, bg=self.c_side)
        self.rec_list_frame.pack(fill="x")
        
        lbl_loading_rec = tk.Label(self.rec_list_frame, text="Sincronizando índice...", fg="#52525b", bg=self.c_side, font=("Courier", 9, "italic"), anchor="w")
        lbl_loading_rec.pack(fill="x", padx=5)

        # Contenedor central scrollable
        self.scroll_frame = tk.Frame(self.sidebar, bg=self.c_side)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # ================= LIENZO DE ACCIONES PRINCIPAL =================
        self.main_area = tk.Frame(self, bg=self.c_bg)
        self.main_area.pack(side="right", expand=True, fill="both", padx=25, pady=20)
        
        self.hint_label = tk.Label(self.main_area, text="[ SHIFT + CLIC PARA SELECCIÓN MÚLTIPLE ]", fg=self.c_primary, bg=self.c_bg, font=("Courier", 10, "bold"))
        self.hint_label.pack(anchor="ne")

        self.title_label = tk.Label(self.main_area, text="SELECCIONA UN PAQUETE DE LA LISTA", fg=self.c_primary, bg=self.c_bg, font=("Courier", 14, "bold"))
        self.title_label.pack(pady=5)
        
        # --- ARQUITECTURA SIDE-BY-SIDE VISTA PREVIA + IA ---
        self.split_frame = tk.Frame(self.main_area, bg=self.c_bg)
        self.split_frame.pack(fill="x", pady=10)
        
        # Panel Izquierdo: Vista Previa
        self.preview_frame = tk.Frame(self.split_frame, bg=self.c_side, width=640, height=360, highlightbackground=self.c_primary, highlightthickness=1)
        self.preview_frame.pack_propagate(False)
        self.preview_frame.pack(side="left")
        
        self.preview_label = tk.Label(self.preview_frame, text="[ SELECCIONA UN COMPONENTE PARA PREVISUALIZAR ]", fg=self.c_primary, bg=self.c_side, font=("Courier", 11))
        self.preview_label.pack(expand=True, fill="both")
        
        # Panel Derecho: Módulo de IA Nova's Kid
        self.ai_frame = tk.Frame(self.split_frame, bg=self.c_side, width=420, height=360, highlightbackground="#1e3a1e", highlightthickness=1)
        self.ai_frame.pack_propagate(False)
        self.ai_frame.pack(side="right", padx=(15, 0), fill="both", expand=True)
        
        lbl_ai_title = tk.Label(self.ai_frame, text="🧠 ASSISTANT NODE: NOVA'S KID", bg="#111827", fg="#10b981", font=("Courier", 10, "bold"), pady=4)
        lbl_ai_title.pack(fill="x")
        
        self.ai_chatlog = tk.Text(self.ai_frame, bg="#090a0f", fg="#a7f3d0", font=("Courier", 9), state="disabled", wrap="word", relief="flat", padx=8, pady=8)
        self.ai_chatlog.pack(fill="both", expand=True)
        
        ai_input_frame = tk.Frame(self.ai_frame, bg=self.c_side)
        ai_input_frame.pack(fill="x", padx=5, pady=5)
        
        self.ai_entry = tk.Entry(ai_input_frame, bg="#0d0f0d", fg=self.c_text, insertbackground="#10b981", font=("Courier", 10), relief="flat", highlightbackground="#222", highlightthickness=1)
        self.ai_entry.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=3)
        self.ai_entry.bind("<Return>", lambda e: self.send_ai_message())
        
        btn_ai_send = tk.Button(ai_input_frame, text="ASK", bg=self.c_btn, fg=self.c_primary, font=("Courier", 9, "bold"), relief="flat", padx=10, command=self.send_ai_message)
        btn_ai_send.pack(side="right")
        
        # Activar el saludo corporativo
        self.trigger_ai_greeting()

        # Galería inferior de miniaturas
        lbl_galeria = tk.Label(self.main_area, text="▼ COLECCIÓN DEL PACK (SHIFT+CLIC PARA MARCAR VARIOS) ▼", fg=self.c_primary, bg=self.c_bg, font=("Courier", 9, "bold"))
        lbl_galeria.pack(pady=(10, 2))
        
        self.thumbs_outer_frame = tk.Frame(self.main_area, bg=self.c_side, height=105, highlightbackground="#222", highlightthickness=1)
        self.thumbs_outer_frame.pack(fill="x", padx=10, pady=5)
        self.thumbs_outer_frame.pack_propagate(False)
        
        self.thumbs_frame = tk.Frame(self.thumbs_outer_frame, bg=self.c_side)
        self.thumbs_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Panel de Control de Accionesobre Lotes
        self.control_frame = tk.Frame(self.main_area, bg=self.c_bg)
        self.control_frame.pack(pady=15, fill="x")
        
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)
        self.control_frame.grid_columnconfigure(3, weight=1)

        self.btn_install = tk.Button(self.control_frame, text="⚡ INSTALAR PACK COMPLETO", bg=self.c_btn, fg=self.c_primary, activebackground=self.c_primary, activeforeground=self.c_bg, font=("Courier", 10, "bold"), height=2, command=self.install_package, state="disabled", relief="flat")
        self.btn_install.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.btn_install_selected = tk.Button(self.control_frame, text="🖼️ ADQUIRIR SELECCIÓN", bg=self.c_btn, fg=self.c_primary, activebackground=self.c_primary, activeforeground=self.c_bg, font=("Courier", 10, "bold"), height=2, command=self.install_selected_images, state="disabled", relief="flat")
        self.btn_install_selected.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.btn_uninstall_selected = tk.Button(self.control_frame, text="🗑️ ELIMINAR SELECCIÓN", bg=self.c_alert_bg, fg=self.c_alert, activebackground=self.c_alert, activeforeground="white", font=("Courier", 10, "bold"), height=2, command=self.uninstall_selected_images, state="disabled", relief="flat")
        self.btn_uninstall_selected.grid(row=0, column=2, padx=5, sticky="ew")

        self.btn_uninstall = tk.Button(self.control_frame, text="❌ LIQUIDAR PACK", bg=self.c_alert_bg, fg=self.c_alert, activebackground=self.c_alert, activeforeground="white", font=("Courier", 10, "bold"), height=2, command=self.uninstall_package, state="disabled", relief="flat")
        self.btn_uninstall.grid(row=0, column=3, padx=5, sticky="ew")
        
        self.status_label = tk.Label(self.main_area, text="SISTEMA PROFESIONAL OPERATIVO", fg=self.c_primary, bg=self.c_bg, font=("Courier", 10, "bold"))
        self.status_label.pack(side="bottom", fill="x", pady=5)

        self.refresh_data()

    def refresh_data(self):
        threading.Thread(target=self._fetch_branches_thread, daemon=True).start()
        threading.Thread(target=self._fetch_recommendations_thread, daemon=True).start()
        threading.Thread(target=self._fetch_news_thread, daemon=True).start()

    # ================= INTERFAZ Y PROCESAMIENTO DE NOVA'S KID =================
    def print_ai_text(self, sender, text):
        self.ai_chatlog.config(state="normal")
        self.ai_chatlog.insert(tk.END, f"[{sender}]: {text}\n\n")
        self.ai_chatlog.see(tk.END)
        self.ai_chatlog.config(state="disabled")

    def trigger_ai_greeting(self):
        greeting = ("¡Hola, estimado usuario! Permítame presentarme, mi nombre es Nova's Kid, su asistente de "
                    "Inteligencia Artificial integrado. Me complace enormemente asistirle con absoluta cortesía. "
                    "I can speak English, fano un pouco de galego, et je comprends aussi le français! "
                    "Pregúnteme libremente cuáles son los packs 'más instalados' o plantéeme cualquier duda.")
        self.print_ai_text("Nova's Kid", greeting)

    def send_ai_message(self):
        query = self.ai_entry.get().strip()
        if not query: return
        self.ai_entry.delete(0, tk.END)
        
        self.print_ai_text("Usted", query)
        threading.Thread(target=self._process_ai_query_thread, args=(query.lower(),), daemon=True).start()

    def _process_ai_query_thread(self, query):
        time.sleep(0.3) 
        
        if any(w in query for w in ["instalado", "popular", "top", "descarga", "más usado", "most installed"]):
            reply = ("Con sumo gusto le informo que, analizando la telemetría global de nuestros servidores, "
                     "los componentes más solicitados por los usuarios en el mercado son los siguientes:\n\n"
                     " 1º 🔥 COSMOS LEGENDARIO — Con un récord total de 4,890 despliegues.\n"
                     " 2º 🔥 SIN VIDA — Registrando 3,540 instalaciones activas.\n"
                     " 3º 🔥 FIN DEL MUNDO — Asegurando 2,910 descargas en terminales.\n\n"
                     "¿Desea que localicemos alguno de estos paquetes en su barra de búsqueda?")
            
        elif any(w in query for w in ["hello", "hi", "welcome", "english"]):
            reply = ("It is an absolute honor to serve you, sir. I am Nova's Kid, your polite digital partner. "
                     "Please let me know if you want me to list the top trends or help you clear any assets.")
            
        elif any(w in query for w in ["ola", "galego", "gallego", "fala"]):
            reply = ("Ola! É un pracer enorme saudarche. Son Nova's Kid, a túa intelixencia artificial de confianza. "
                     "Estou aquí para axudarche de xeito amable a xestionar todos os fondos da túa distribución.")
            
        elif any(w in query for w in ["bonjour", "salut", "français", "frances"]):
            reply = ("Bonjour, mon cher ami! Je suis Nova's Kid, votre dévoué assistant IA. C'est un réel plaisir "
                     "de vous offrir mon aide cordiale aujourd'hui. Comment puis-je vous assister?")
            
        elif any(w in query for w in ["gracias", "thank", "grazas", "merci"]):
            reply = ("Al contrario, las gracias se las debo dar yo a usted. Es un auténtico privilegio "
                     "acompañarle en sus operaciones diarias. Quedo a sus enteras órdenes.")
        else:
            reply = ("Entendido perfectamente. Como Nova's Kid, me comprometo a atenderle siempre con la mayor amabilidad "
                     "y respeto posible. Si desea ver las tendencias de descarga globales, recuerde que puede consultarme "
                     "por los activos 'más instalados'. ¿En qué otra cosa puedo serle útil?")
            
        self.after(0, lambda: self.print_ai_text("Nova's Kid", reply))

    # --- RADAR DE NOVEDADES EN DIRECTO ---
    def _fetch_news_thread(self):
        try:
            req = urllib.request.Request(API_COMMITS, headers={"User-Agent": "Lynds-Exec"})
            with urllib.request.urlopen(req) as res:
                commits_data = json.loads(res.read().decode())
                news_lines = []
                for item in commits_data:
                    msg = item.get("commit", {}).get("message", "Actualización del sistema").split("\n")[0]
                    if len(msg) > 40: msg = msg[:37] + "..."
                    news_lines.append(f"• {msg}")
                final_text = "\n".join(news_lines) if news_lines else "• Sin actividad reciente en el mercado."
                self.after(0, lambda: self.lbl_news_box.config(text=final_text, fg="#10b981"))
        except Exception as e:
            self.after(0, lambda: self.lbl_news_box.config(text="• Modo Offline\n• Fallo al conectar con el servidor", fg=self.c_alert))

    # --- MOTOR DE FILTRADO Y BÚSQUEDA ---
    def filter_branches(self, *args):
        query = self.search_var.get().lower().strip()
        if not query or query == "buscar paquete...":
            filtered = self.all_branches
        else:
            filtered = [b for b in self.all_branches if query in b.lower() or query in b.replace("-", " ").lower()]
        self._render_list(filtered)

    def _fetch_branches_thread(self):
        try:
            req = urllib.request.Request(API_BRANCHES, headers={"User-Agent": "Lynds-Exec"})
            with urllib.request.urlopen(req) as res:
                self.all_branches = [b['name'] for b in json.loads(res.read().decode()) if b['name'] not in ["main", "master"]]
                self.after(0, lambda: self._render_list(self.all_branches))
        except Exception as e:
            print(f"Error de conexión al listar ramas: {e}")

    def _render_list(self, branches):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        if not branches:
            lbl_empty = tk.Label(self.scroll_frame, text="Sin resultados", fg=self.c_alert, bg=self.c_side, font=("Courier", 10, "italic"))
            lbl_empty.pack(pady=10)
            return
        for b in branches:
            clean_name = b.replace("-", " ")
            btn = tk.Button(self.scroll_frame, text=f"• {clean_name}", bg=self.c_btn, fg=self.c_text, 
                            font=("Courier", 11, "bold"), anchor="w", padx=15, pady=8,
                            activebackground=self.c_primary, activeforeground=self.c_bg, relief="flat",
                            command=lambda name=b: self.select_branch(name))
            btn.pack(fill="x", padx=10, pady=4)

    def _fetch_recommendations_thread(self):
        try:
            req = urllib.request.Request(RAW_RECOMENDACIONES, headers={"User-Agent": "Lynds-Exec"})
            with urllib.request.urlopen(req) as res:
                content = res.read().decode('utf-8')
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                self.after(0, lambda: self._render_recommendations(lines))
        except Exception as e:
            fallback = ["Sin-Vida", "Cosmos-Legendario", "Fin-Del-Mundo"]
            self.after(0, lambda: self._render_recommendations(fallback))

    def _render_recommendations(self, lines):
        for widget in self.rec_list_frame.winfo_children():
            widget.destroy()
        for item in lines:
            clean_item = item.replace("-", " ")
            btn = tk.Button(self.rec_list_frame, text=f"🔥 {clean_item.upper()}", bg="#0d0f0d", fg="#10b981",
                            font=("Courier", 10, "bold"), anchor="w", padx=12, pady=5,
                            activebackground=self.c_primary, activeforeground=self.c_bg, relief="flat",
                            highlightbackground="#222", highlightthickness=1,
                            command=lambda name=item: self.select_branch(name))
            btn.pack(fill="x", padx=5, pady=3)

    # --- DESPLIEGUE EXECUTIVO DE CONTENIDO ---
    def select_branch(self, branch):
        self.selected_branch = branch
        clean_branch = branch.replace("-", " ")
        self.title_label.config(text=f"COMPONENTE: {clean_branch.upper()}")
        
        self.btn_install.config(state="normal")
        self.btn_install_selected.config(state="disabled", text="🖼️ ADQUIRIR SELECCIÓN") 
        self.btn_uninstall_selected.config(state="disabled", text="🗑️ ELIMINAR SELECCIÓN") 
        self._update_uninstall_button_status(branch)
        
        self.preview_label.config(image="", text="⚙️ SOLICITANDO ÍNDICE DE IMÁGENES A GITHUB...")
        for widget in self.thumbs_frame.winfo_children():
            widget.destroy()
            
        self.gallery_images.clear()
        self.thumb_refs.clear()
        self.thumb_btns.clear()
        self.selected_files.clear()
        self.preview_img = None
            
        threading.Thread(target=self._load_branch_gallery_thread, args=(branch,), daemon=True).start()

    def _update_uninstall_button_status(self, branch):
        dest = os.path.join(INSTALL_BASE, branch)
        if os.path.exists(dest):
            self.btn_uninstall.config(state="normal", text="❌ LIQUIDAR PACK", bg="#451a1a")
        else:
            self.btn_uninstall.config(state="disabled", text="NO INSTALADO", bg=self.c_alert_bg)

    def _load_branch_gallery_thread(self, branch):
        url_contents = API_CONTENTS.format(branch=branch)
        try:
            req_folder = urllib.request.Request(url_contents, headers={"User-Agent": "Lynds-Exec"})
            with urllib.request.urlopen(req_folder) as res:
                files_list = json.loads(res.read().decode())
            
            image_files = [f for f in files_list if f.get("type") == "file" and f.get("name", "").lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if not image_files:
                self.after(0, lambda: self.preview_label.config(text="[ NO SE ENCONTRARON IMÁGENES EN ESTA RAMA ]"))
                return

            self.after(0, lambda: self.preview_label.config(text="📥 DESCARGANDO MINIATURAS A LA VOLANTE RAM..."))

            for img_meta in image_files:
                file_name = img_meta.get("name")
                download_url = img_meta.get("download_url")
                
                try:
                    req_img = urllib.request.Request(download_url, headers={"User-Agent": "Lynds-Exec"})
                    with urllib.request.urlopen(req_img) as response:
                        raw_bytes = response.read()
                    b64_data = base64.b64encode(raw_bytes)
                    self.after(0, lambda f=file_name, d=b64_data: self._add_thumbnail_to_ui(f, d))
                except Exception as img_err:
                    print(f"Error descargando {file_name}: {img_err}")
        except Exception as e:
            self.after(0, lambda: self.preview_label.config(text=f"[ ERROR AL CARGAR LA GALERÍA ]: {e}"))

    def _add_thumbnail_to_ui(self, file_name, b64_data):
        try:
            self.gallery_images[file_name] = b64_data
            temp_img = tk.PhotoImage(data=b64_data)
            w, h = temp_img.width(), temp_img.height()
            
            t_factor = max(1, max(w // 110, h // 65))
            thumb_img = temp_img.subsample(t_factor, t_factor)
            self.thumb_refs[file_name] = thumb_img
            
            btn = tk.Button(self.thumbs_frame, image=thumb_img, bg=self.c_side, 
                            activebackground=self.c_primary, relief="flat", bd=3,
                            highlightbackground="#333")
            
            btn.bind("<Button-1>", lambda e, f=file_name: self.handle_thumb_click(f, False))
            btn.bind("<Shift-Button-1>", lambda e, f=file_name: self.handle_thumb_click(f, True))
            
            btn.pack(side="left", padx=6, pady=2)
            self.thumb_btns[file_name] = btn
            
            if self.preview_img is None:
                self.handle_thumb_click(file_name, False)
        except Exception as e:
            print(f"Error de renderizado en miniatura {file_name}: {e}")

    def handle_thumb_click(self, file_name, is_shift):
        if is_shift:
            if file_name in self.selected_files:
                self.selected_files.remove(file_name)
            else:
                self.selected_files.add(file_name)
        else:
            self.selected_files = {file_name}

        for fname, btn in self.thumb_btns.items():
            if fname in self.selected_files:
                btn.config(bg=self.c_primary, highlightbackground=self.c_primary)
            else:
                btn.config(bg=self.c_side, highlightbackground="#333")

        if self.selected_files:
            count = len(self.selected_files)
            self.btn_install_selected.config(state="normal", text=f"🖼️ ADQUIRIR SELECCIÓN ({count})")
            self.btn_uninstall_selected.config(state="normal", text=f"🗑️ ELIMINAR SELECCIÓN ({count})")
            last_selected = list(self.selected_files)[-1]
            self.display_full_preview(last_selected)
        else:
            self.btn_install_selected.config(state="disabled", text="🖼️ ADQUIRIR SELECCIÓN")
            self.btn_uninstall_selected.config(state="disabled", text="🗑️ ELIMINAR SELECCIÓN")
            self.preview_label.config(image="", text="[ SELECCIÓN VACÍA ]")

    def display_full_preview(self, file_name):
        try:
            b64_data = self.gallery_images.get(file_name)
            if not b64_data: return
            base_img = tk.PhotoImage(data=b64_data)
            w, h = base_img.width(), base_img.height()
            
            p_factor = max(1, max(w // 640, h // 360))
            self.preview_img = base_img.subsample(p_factor, p_factor)
            self.preview_label.config(image=self.preview_img, text="")
            self.status_label.config(text=f"VISUALIZANDO ACTIVO: {file_name.upper()} ({w}x{h} px)")
        except Exception as e:
            self.preview_label.config(text=f"[ ERROR AL CARGAR FOTO EN GRANDE ]: {e}")

    # ================= LOGICA DE DESPLIEGUE INDIVIDUAL =================
    def install_selected_images(self):
        branch = self.selected_branch
        if not branch or not self.selected_files: return
        try:
            single_dest_dir = os.path.join(INSTALL_BASE, "Individual")
            os.makedirs(single_dest_dir, exist_ok=True)
            count = 0
            for file_name in self.selected_files:
                b64_data = self.gallery_images.get(file_name)
                if b64_data:
                    dest_path = os.path.join(single_dest_dir, file_name)
                    with open(dest_path, "wb") as f:
                        f.write(base64.b64decode(b64_data))
                    count += 1
            clean_branch = branch.replace("-", " ")
            self.status_label.config(text=f"ÉXITO: {count} ACTIVOS EXTRAÍDOS DE '{clean_branch.upper()}' A TU CARTERA INDIVIDUAL.")
        except Exception as e:
            self.status_label.config(text=f"FALLO CRÍTICO AL EXTRAER IMÁGENES: {e}")

    def uninstall_selected_images(self):
        branch = self.selected_branch
        if not branch or not self.selected_files: return
        count = 0
        for file_name in self.selected_files:
            path_branch = os.path.join(INSTALL_BASE, branch, file_name)
            path_individual = os.path.join(INSTALL_BASE, "Individual", file_name)
            removed = False
            if os.path.exists(path_branch):
                os.remove(path_branch)
                removed = True
            if os.path.exists(path_individual):
                os.remove(path_individual)
                removed = True
            if removed: count += 1
                
        self.status_label.config(text=f"OPERACIÓN DE ELIMINACIÓN: {count} ACTIVOS ELIMINADOS DEL DISCO.")
        if os.path.exists(os.path.join(INSTALL_BASE, branch)):
            files_left = os.listdir(os.path.join(INSTALL_BASE, branch))
            if not files_left: shutil.rmtree(os.path.join(INSTALL_BASE, branch))
        self._update_uninstall_button_status(branch)

    # ================= LOGICA DE LOTE COMPLETO =================
    def install_package(self):
        branch = self.selected_branch
        if not branch: return
        clean_branch = branch.replace("-", " ")
        self.status_label.config(text=f"EJECUTANDO DESCARGA EN LOTE ASÍNCRONA: {clean_branch.upper()}...")
        threading.Thread(target=self._download_task, args=(branch,), daemon=True).start()

    def _download_task(self, branch):
        url = ZIP_URL.format(user=GITHUB_USER, repo=GITHUB_REPO, branch=branch)
        dest = os.path.join(INSTALL_BASE, branch)
        try:
            os.makedirs(INSTALL_BASE, exist_ok=True)
            with tempfile.TemporaryDirectory() as tmp:
                zip_path = os.path.join(tmp, "pack.zip")
                req = urllib.request.Request(url, headers={"User-Agent": "Lynds-Exec"})
                with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                with zipfile.ZipFile(zip_path) as zf:
                    zf.extractall(tmp)
                    if os.path.exists(dest): shutil.rmtree(dest)
                    extracted_dir = os.path.join(tmp, f"{GITHUB_REPO}-{branch}")
                    if os.path.exists(extracted_dir): shutil.move(extracted_dir, dest)
                    else:
                        dirs = [d for d in os.listdir(tmp) if os.path.isdir(os.path.join(tmp, d))]
                        if dirs: shutil.move(os.path.join(tmp, dirs[0]), dest)
            self.after(0, lambda: self._on_install_complete(branch))
        except Exception as e:
            self.after(0, lambda: self.status_label.config(text=f"FALLO CRÍTICO EN DESCARGA: {e}"))

    def _on_install_complete(self, branch):
        clean_branch = branch.replace("-", " ")
        self.status_label.config(text=f"ÉXITO: LOTE {clean_branch.upper()} INSTALADO EN EL SISTEMA.")
        if self.selected_branch == branch: self._update_uninstall_button_status(branch)

    def uninstall_package(self):
        branch = self.selected_branch
        if not branch: return
        dest = os.path.join(INSTALL_BASE, branch)
        clean_branch = branch.replace("-", " ")
        if os.path.exists(dest):
            try:
                shutil.rmtree(dest)
                self.status_label.config(text=f"ELIMINADO: LOTE {clean_branch.upper()} COMPLETAMENTE LIQUIDADO.")
                self._update_uninstall_button_status(branch)
            except Exception as e:
                self.status_label.config(text=f"ERROR EN ELIMINACIÓN DE ARCHIVOS MASIVA: {e}")
        else:
            self.status_label.config(text="EL LOTE OBJETIVO YA NO EXISTE.")

if __name__ == "__main__":
    app = LyndsExecutive()
    app.mainloop()