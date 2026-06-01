API_BRANCHES=f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/branches"
API_COMMITS=f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/commits?per_page=4" # <-- NUEVO RADAR DE NOVEDADES
API_CONTENTS=f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents?ref={{branch}}"
GITHUB_REPO="Lynds-Wallpapers"
GITHUB_USER="Monojo-Project"
INSTALL_BASE=os.path.expanduser("~/.local/share/wallpapers")
RAW_RECOMENDACIONES=f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/RECOMENDACIONES"
ZIP_URL="https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
activebackground=self.c_primary, relief="flat", bd=3,
app=LyndsExecutive()
b64_data=self.gallery_images.get(file_name)
base_img=tk.PhotoImage(data=b64_data)
branch=self.selected_branch
btn=tk.Button(self.thumbs_frame, image=thumb_img, bg=self.c_side,
btn.bind("<Button-1>", lambda e, f=file_name: self.handle_thumb_click(f, False))
btn.bind("<Shift-Button-1>", lambda e, f=file_name: self.handle_thumb_click(f, True))
btn.config(bg=self.c_side, highlightbackground="#333")
btn.pack(fill="x", padx=5, pady=3)
btn.pack(side="left", padx=6, pady=2)
clean_branch=branch.replace("-", " ")
clean_item=item.replace("-", " ")
clean_name=b.replace("-", " ")
command=lambda name=item: self.select_branch(name))
commits_data=json.loads(res.read().decode())
content=res.read().decode('utf-8')
count=0
count +=1
dest=os.path.join(INSTALL_BASE, branch)
dest_path=os.path.join(single_dest_dir, file_name)
dirs=[d for d in os.listdir(tmp) if os.path.isdir(os.path.join(tmp, d))]
download_url=img_meta.get("download_url")
extracted_dir=os.path.join(tmp, f"{GITHUB_REPO}-{branch}")
fallback=["Sin-Vida", "Cosmos-Legendario", "Fin-Del-Mundo"]
file_name=img_meta.get("name")
files_left=os.listdir(os.path.join(INSTALL_BASE, branch))
files_list=json.loads(res.read().decode())
filtered=[b for b in self.all_branches if query in b.lower() or query in b.replace("-", " ").lower()]
final_text="\n".join(news_lines) if news_lines else "• Sin actividad reciente en el mercado."
font=("Courier", 10, "bold"), anchor="w", padx=12, pady=5,
highlightbackground="#333")
if __name__== "__main__":
if len(msg) > 40: msg=msg[:37] + "..."
if not query or query== "buscar paquete...":
if self.selected_branch== branch:
image_files=[f for f in files_list if f.get("type") == "file" and f.get("name", "").lower().endswith(('.png', '.jpg', '.jpeg'))]
insertbackground=self.c_primary, font=("Courier", 11), relief="flat",
last_selected=list(self.selected_files)[-1]
lbl_empty=tk.Label(self.scroll_frame, text="Sin resultados", fg=self.c_alert, bg=self.c_side, font=("Courier", 10, "italic"))
lbl_empty.pack(pady=10)
lbl_galeria=tk.Label(self.main_area, text="▼ COLECCIÓN DEL PACK (SHIFT+CLIC PARA MARCAR VARIOS) ▼", fg=self.c_primary, bg=self.c_bg, font=("Courier", 9, "bold"))
lbl_galeria.pack(pady=(10, 2))
lbl_loading_rec=tk.Label(self.rec_list_frame, text="Sincronizando índice...", fg="#52525b", bg=self.c_side, font=("Courier", 9, "italic"), anchor="w")
lbl_loading_rec.pack(fill="x", padx=5)
lbl_news=tk.Label(self.news_frame, text="📢 NOVEDADES (LIVE GITHUB)", bg=self.c_side, fg=self.c_primary, font=("Courier", 10, "bold"), anchor="w")
lbl_news.pack(fill="x", padx=5, pady=(0, 4))
lbl_rec=tk.Label(self.rec_frame, text="⚡ RECOMENDADOS (MAIN)", bg=self.c_side, fg=self.c_primary, font=("Courier", 10, "bold"), anchor="w")
lbl_rec.pack(fill="x", padx=5, pady=(0, 4))
lbl_search_icon=tk.Label(self.search_frame, text="🔍", bg=self.c_side, fg=self.c_primary, font=("Courier", 10))
lbl_search_icon.pack(side="left", padx=(2, 5))
lbl_side=tk.Label(self.sidebar, text="MERCADO DE ACTIVOS", bg=self.c_side, fg=self.c_primary, font=("Courier", 12, "bold"))
lbl_side.pack(pady=(20, 5), fill="x")
lines=[line.strip() for line in content.split("\n") if line.strip()]
msg=item.get("commit", {}).get("message", "Actualización del sistema").split("\n")[0]
news_lines=[]
os.makedirs(INSTALL_BASE, exist_ok=True)
os.makedirs(single_dest_dir, exist_ok=True)
p_factor=max(1, max(w // 640, h // 360))
path_branch=os.path.join(INSTALL_BASE, branch, file_name)
path_individual=os.path.join(INSTALL_BASE, "Individual", file_name)
query=self.search_var.get().lower().strip()
raw_bytes=response.read()
removed=True
req=urllib.request.Request(url, headers={"User-Agent": "Lynds-Exec"})
req_folder=urllib.request.Request(url_contents, headers={"User-Agent": "Lynds-Exec"})
req_img=urllib.request.Request(download_url, headers={"User-Agent": "Lynds-Exec"})
self.after(0, lambda f=file_name, d=b64_data: self._add_thumbnail_to_ui(f, d))
self.after(0, lambda: self.lbl_news_box.config(text="• Modo Offline\n• Fallo al conectar con el servidor", fg=self.c_alert))
self.after(0, lambda: self.preview_label.config(text=f"[ ERROR AL CARGAR LA GALERÍA ]: {e}"))
self.after(0, lambda: self.status_label.config(text=f"FALLO CRÍTICO EN DESCARGA: {e}"))
self.all_branches=[b['name'] for b in json.loads(res.read().decode()) if b['name'] not in ["main", "master"]]
self.btn_install=tk.Button(self.control_frame, text="⚡ INSTALAR PACK COMPLETO", bg=self.c_btn, fg=self.c_primary, activebackground=self.c_primary, activeforeground=self.c_bg, font=("Courier", 10, "bold"), height=2, command=self.install_package, state="disabled", relief="flat")
self.btn_install.config(state="normal")
self.btn_install.grid(row=0, column=0, padx=5, sticky="ew")
self.btn_install_selected=tk.Button(self.control_frame, text="🖼️ ADQUIRIR SELECCIÓN", bg=self.c_btn, fg=self.c_primary, activebackground=self.c_primary, activeforeground=self.c_bg, font=("Courier", 10, "bold"), height=2, command=self.install_selected_images, state="disabled", relief="flat")
self.btn_install_selected.config(state="disabled", text="🖼️ ADQUIRIR SELECCIÓN")
self.btn_install_selected.grid(row=0, column=1, padx=5, sticky="ew")
self.btn_uninstall=tk.Button(self.control_frame, text="❌ LIQUIDAR PACK", bg=self.c_alert_bg, fg=self.c_alert, activebackground=self.c_alert, activeforeground="white", font=("Courier", 10, "bold"), height=2, command=self.uninstall_package, state="disabled", relief="flat")
self.btn_uninstall.config(state="disabled", text="NO INSTALADO", bg=self.c_alert_bg)
self.btn_uninstall.grid(row=0, column=3, padx=5, sticky="ew")
self.btn_uninstall_selected=tk.Button(self.control_frame, text="🗑️ ELIMINAR SELECCIÓN", bg=self.c_alert_bg, fg=self.c_alert, activebackground=self.c_alert, activeforeground="white", font=("Courier", 10, "bold"), height=2, command=self.uninstall_selected_images, state="disabled", relief="flat")
self.btn_uninstall_selected.config(state="disabled", text="🗑️ ELIMINAR SELECCIÓN")
self.btn_uninstall_selected.grid(row=0, column=2, padx=5, sticky="ew")
self.c_alert="#ef4444"
self.c_alert_bg="#2d1616"
self.c_bg="#121412"
self.c_btn="#14532d"
self.c_primary="#16a34a"
self.c_side="#141614"
self.c_text="#e2e8f0"
self.configure(bg="#121412")
self.control_frame=tk.Frame(self.main_area, bg=self.c_bg)
self.control_frame.grid_columnconfigure(0, weight=1)
self.control_frame.grid_columnconfigure(1, weight=1)
self.control_frame.grid_columnconfigure(2, weight=1)
self.control_frame.grid_columnconfigure(3, weight=1)
self.control_frame.pack(pady=15, fill="x")
self.gallery_images={}
self.gallery_images[file_name]=b64_data
self.hint_label=tk.Label(self.main_area, text="[ SHIFT + CLIC PARA SELECCIÓN MÚLTIPLE ]", fg=self.c_primary, bg=self.c_bg, font=("Courier", 10, "bold"))
self.hint_label.pack(anchor="ne")
self.lbl_news_box=tk.Label(self.news_frame, text="Sincronizando feed del mercado...", bg="#0d0f0d", fg="#a1a1aa",
self.lbl_news_box.pack(fill="x")
self.main_area=tk.Frame(self, bg=self.c_bg)
self.main_area.pack(side="right", expand=True, fill="both", padx=25, pady=20)
self.news_frame=tk.Frame(self.sidebar, bg=self.c_side)
self.news_frame.pack(fill="x", side="bottom", padx=10, pady=(5, 15))
self.preview_frame=tk.Frame(self.main_area, bg=self.c_side, width=640, height=360, highlightbackground=self.c_primary, highlightthickness=1)
self.preview_frame.pack(pady=10)
self.preview_img=base_img.subsample(p_factor, p_factor)
self.preview_label=tk.Label(self.preview_frame, text="[ SELECCIONA UN COMPONENTE PARA PREVISUALIZAR ]", fg=self.c_primary, bg=self.c_side, font=("Courier", 11))
self.preview_label.config(image=self.preview_img, text="")
self.preview_label.config(text=f"[ ERROR AL CARGAR FOTO EN GRANDE ]: {e}")
self.preview_label.pack(expand=True, fill="both")
self.rec_frame=tk.Frame(self.sidebar, bg=self.c_side)
self.rec_frame.pack(fill="x", side="bottom", padx=10, pady=10)
self.rec_list_frame=tk.Frame(self.rec_frame, bg=self.c_side)
self.rec_list_frame.pack(fill="x")
self.scroll_frame=tk.Frame(self.sidebar, bg=self.c_side)
self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
self.search_entry=tk.Entry(self.search_frame, textvariable=self.search_var, bg="#0d0f0d", fg=self.c_text,
self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, tk.END) if self.search_var.get()== "Buscar paquete..." else None)
self.search_entry.pack(side="left", fill="x", expand=True)
self.search_frame=tk.Frame(self.sidebar, bg=self.c_side)
self.search_frame.pack(fill="x", padx=15, pady=(0, 10))
self.search_var=tk.StringVar()
self.selected_branch=branch
self.selected_files={file_name}
self.sidebar=tk.Frame(self, bg=self.c_side, width=320)
self.sidebar.pack(side="left", fill="y")
self.status_label=tk.Label(self.main_area, text="SISTEMA PROFESIONAL OPERATIVO", fg=self.c_primary, bg=self.c_bg, font=("Courier", 10, "bold"))
self.status_label.config(text="EL LOTE OBJETIVO YA NO EXISTE.")
self.status_label.pack(side="bottom", fill="x", pady=5)
self.thumb_btns={}
self.thumb_btns[file_name]=btn
self.thumb_refs={}
self.thumb_refs[file_name]=thumb_img
self.thumbs_frame=tk.Frame(self.thumbs_outer_frame, bg=self.c_side)
self.thumbs_frame.pack(expand=True, fill="both", padx=5, pady=5)
self.thumbs_outer_frame=tk.Frame(self.main_area, bg=self.c_side, height=105, highlightbackground="#222", highlightthickness=1)
self.thumbs_outer_frame.pack(fill="x", padx=10, pady=5)
self.title_label=tk.Label(self.main_area, text="SELECCIONA UN PAQUETE DE LA LISTA", fg=self.c_primary, bg=self.c_bg, font=("Courier", 14, "bold"))
self.title_label.config(text=f"COMPONENTE: {clean_branch.upper()}")
self.title_label.pack(pady=5)
single_dest_dir=os.path.join(INSTALL_BASE, "Individual")
t_factor=max(1, max(w // 110, h // 65))
temp_img=tk.PhotoImage(data=b64_data)
threading.Thread(target=self._download_task, args=(branch,), daemon=True).start()
thumb_img=temp_img.subsample(t_factor, t_factor)
url=ZIP_URL.format(user=GITHUB_USER, repo=GITHUB_REPO, branch=branch)
url_contents=API_CONTENTS.format(branch=branch)
w, h=base_img.width(), base_img.height()
zip_path=os.path.join(tmp, "pack.zip")

[Desktop Entry]
Name[gl_ES]=Lynds_Wallpaper_Installer.py
Name=Lynds_Wallpaper_Installer.py
