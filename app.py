import os
from pydub import AudioSegment
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# === APP INFO ===
APP_NAME = "Audio Converter PRO"
APP_VERSION = "1.0.0"
DEVELOPER_NAME = "Murod Primov"  # o'zgartirsa bo'ladi

# === STATE ===
input_path = ""
output_folder = ""

SUPPORTED_INPUTS = [("Audio files", "*.wav *.mp3 *.flac *.ogg")]
FORMATS = ["mp3", "wav", "flac", "ogg"]

def choose_audio():
    global input_path
    path = filedialog.askopenfilename(
        title="Audio faylni tanlang",
        filetypes=SUPPORTED_INPUTS
    )
    if path:
        input_path = path
        file_value.config(text=os.path.basename(path))

def choose_output_folder():
    global output_folder
    folder = filedialog.askdirectory(title="Saqlash papkasini tanlang")
    if folder:
        output_folder = folder
        folder_value.config(text=folder)

def convert_audio():
    if not input_path:
        messagebox.showerror("Xato", "Audio fayl tanlanmadi!")
        return
    if not output_folder:
        messagebox.showerror("Xato", "Saqlash papkasi tanlanmadi!")
        return

    new_name = name_entry.get().strip()
    if not new_name:
        messagebox.showerror("Xato", "Yangi nom kiriting!")
        return

    out_format = format_var.get()
    output_path = os.path.join(output_folder, f"{new_name}.{out_format}")

    try:
        audio = AudioSegment.from_file(input_path)
        export_args = {"bitrate": "320k"} if out_format == "mp3" else {}
        audio.export(output_path, format=out_format, **export_args)
        messagebox.showinfo("Tayyor 🎉", f"Fayl saqlandi:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Xato", str(e))

def show_info():
    info_win = ttk.Toplevel(app)
    info_win.title(f"{APP_NAME} — Info")
    info_win.geometry("420x520")
    info_win.resizable(False, False)

    frame = ttk.Frame(info_win, padding=20)
    frame.pack(fill=BOTH, expand=True)

    # Developer image
    try:
        img_path = os.path.join("assets", "dev.png")
        img = Image.open(img_path)
        img = img.resize((160, 160))
        photo = ImageTk.PhotoImage(img)
        img_label = ttk.Label(frame, image=photo)
        img_label.image = photo
        img_label.pack(pady=10)
    except Exception:
        ttk.Label(frame, text="(Rasm topilmadi)").pack(pady=10)

    ttk.Label(frame, text=DEVELOPER_NAME, font=("Segoe UI", 14, "bold")).pack(pady=(10, 2))
    ttk.Label(frame, text="Dasturchi").pack(pady=(0, 10))

    info_text = (
        "Audio Converter PRO — audio fayllarni turli formatlar orasida "
        "tez va sifatli konvertatsiya qilish uchun mo'ljallangan dastur.\n\n"
        "Qo'llab-quvvatlanadi: WAV, MP3, FLAC, OGG\n"
        "MP3 eksport: 320kbps\n\n"
        f"Versiya: {APP_VERSION}"
    )

    ttk.Label(frame, text=info_text, wraplength=360, justify=CENTER).pack(pady=10)
    ttk.Button(frame, text="Yopish", bootstyle=SECONDARY, command=info_win.destroy).pack(pady=12)

# === WINDOW ===
app = ttk.Window(themename="darkly")
app.title(f"{APP_NAME} | v{APP_VERSION}")
app.geometry("640x460")
app.resizable(False, False)

# === HEADER ===
header = ttk.Frame(app, padding=(20, 16))
header.pack(fill=X)
ttk.Label(header, text=APP_NAME, font=("Segoe UI", 20, "bold")).pack(anchor=W)
ttk.Label(header, text="Any format → WAV / MP3 / FLAC / OGG / M4A", foreground="#9aa0a6").pack(anchor=W)

# === CONTENT ===
content = ttk.Frame(app, padding=20)
content.pack(fill=BOTH, expand=True)

ttk.Label(content, text="1) Audio fayl:").grid(row=0, column=0, sticky=W, pady=(0, 6))
ttk.Button(content, text="Tanlash", bootstyle=PRIMARY, command=choose_audio).grid(row=0, column=1, sticky=EW, padx=8, pady=(0, 6))
file_value = ttk.Label(content, text="Tanlanmadi")
file_value.grid(row=0, column=2, sticky=W, pady=(0, 6))

ttk.Label(content, text="2) Saqlash papkasi:").grid(row=1, column=0, sticky=W, pady=(0, 6))
ttk.Button(content, text="Tanlash", bootstyle=INFO, command=choose_output_folder).grid(row=1, column=1, sticky=EW, padx=8, pady=(0, 6))
folder_value = ttk.Label(content, text="Tanlanmadi")
folder_value.grid(row=1, column=2, sticky=W, pady=(0, 6))

ttk.Label(content, text="3) Yangi nom:").grid(row=2, column=0, sticky=W, pady=(10, 6))
name_entry = ttk.Entry(content)
name_entry.grid(row=2, column=1, columnspan=2, sticky=EW, pady=(10, 6))

ttk.Label(content, text="4) Chiqish formati:").grid(row=3, column=0, sticky=W, pady=(0, 6))
format_var = ttk.StringVar(value="mp3")
format_combo = ttk.Combobox(content, textvariable=format_var, values=FORMATS, state="readonly")
format_combo.grid(row=3, column=1, sticky=EW, padx=(0, 8))
ttk.Label(content, text="(mp3 – 320kbps)").grid(row=3, column=2, sticky=W)

ttk.Separator(content).grid(row=4, column=0, columnspan=3, sticky=EW, pady=14)
ttk.Button(content, text="▶️ Konvert qilish", bootstyle=SUCCESS, command=convert_audio).grid(row=5, column=0, columnspan=3, sticky=EW)

# === FOOTER ===
footer = ttk.Frame(app, padding=(20, 0, 20, 16))
footer.pack(fill=X, side=BOTTOM)
ttk.Label(footer, text=f"v{APP_VERSION}", foreground="#9aa0a6").pack(side=LEFT)
ttk.Button(footer, text="ℹ️ Info", bootstyle=SECONDARY, command=show_info).pack(side=RIGHT)

content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=2)

app.mainloop()
