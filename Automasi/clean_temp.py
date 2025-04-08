import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import psutil
import subprocess
from datetime import datetime
import ctypes
import sys

# Fungsi untuk menulis log ke GUI dan file
def tulis_log(pesan):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text.insert(tk.END, f"[{waktu}] {pesan}\n")
    log_text.see(tk.END)  # Auto-scroll ke bawah
    with open("log.txt", "a") as log_file:
        log_file.write(f"[{waktu}] {pesan}\n")

# Mengecek apakah program sudah berjalan sebagai admin
def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return  # Jika sudah admin, lanjutkan eksekusi

    # Jika bukan admin, restart sebagai admin
    script = sys.argv[0]
    params = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    sys.exit()

# Jalankan pemeriksaan admin
run_as_admin()

# Fungsi untuk membersihkan temporary files
def bersihkan_temp():
    temp_folder = os.getenv("TEMP")
    if not os.path.exists(temp_folder):
        messagebox.showerror("Error", "Folder temp tidak ditemukan!")
        return

    tulis_log("Memulai pembersihan temporary files...")

    for item in os.listdir(temp_folder):
        item_path = os.path.join(temp_folder, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)
            tulis_log(f"File dihapus: {item_path}")
        except Exception as e:
            tulis_log(f"Gagal menghapus {item_path}: {e}")

    messagebox.showinfo("Sukses", "Temporary files berhasil dibersihkan!")
    tulis_log("Pembersihan temporary files selesai.")

# Fungsi untuk membersihkan Recycle Bin
def bersihkan_recycle_bin():
    tulis_log("Mengosongkan Recycle Bin...")
    try:
        subprocess.run(["cmd", "/c", "rd /s /q C:\\$Recycle.Bin"], shell=True)
        messagebox.showinfo("Sukses", "Recycle Bin berhasil dikosongkan!")
        tulis_log("Recycle Bin berhasil dikosongkan.")
    except Exception as e:
        tulis_log(f"Gagal mengosongkan Recycle Bin: {e}")

# Fungsi untuk membersihkan Prefetch
def bersihkan_prefetch():
    prefetch_folder = r"C:\Windows\Prefetch"
    if not os.path.exists(prefetch_folder):
        messagebox.showerror("Error", "Folder Prefetch tidak ditemukan!")
        return

    tulis_log("Memulai pembersihan Prefetch...")

    for item in os.listdir(prefetch_folder):
        item_path = os.path.join(prefetch_folder, item)
        try:
            os.unlink(item_path)
            tulis_log(f"File dihapus: {item_path}")
        except Exception as e:
            tulis_log(f"Gagal menghapus {item_path}: {e}")

    messagebox.showinfo("Sukses", "Prefetch berhasil dibersihkan!")
    tulis_log("Pembersihan Prefetch selesai.")

# Fungsi untuk membersihkan Recent Files
def bersihkan_recent_files():
    recent_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Recent")
    if not os.path.exists(recent_folder):
        messagebox.showerror("Error", "Folder Recent Files tidak ditemukan!")
        return

    tulis_log("Memulai pembersihan Recent Files...")

    for item in os.listdir(recent_folder):
        item_path = os.path.join(recent_folder, item)
        try:
            os.unlink(item_path)
            tulis_log(f"File dihapus: {item_path}")
        except Exception as e:
            tulis_log(f"Gagal menghapus {item_path}: {e}")

    messagebox.showinfo("Sukses", "Recent Files berhasil dibersihkan!")
    tulis_log("Pembersihan Recent Files selesai.")

# Fungsi untuk membersihkan cache browser berdasarkan pilihan
def bersihkan_cache_browser():
    selected_browsers = []
    if var_chrome.get():
        selected_browsers.append("Google Chrome")
    if var_edge.get():
        selected_browsers.append("Microsoft Edge")
    if var_firefox.get():
        selected_browsers.append("Mozilla Firefox")

    if not selected_browsers:
        messagebox.showwarning("Pilih Browser", "Silakan pilih minimal satu browser untuk dibersihkan.")
        return

    tulis_log("Menutup browser sebelum membersihkan cache...")
    for browser in ["chrome", "edge", "firefox"]:
        for proc in psutil.process_iter():
            try:
                if browser.lower() in proc.name().lower():
                    proc.terminate()
                    tulis_log(f"Menutup {browser}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    browser_paths = {
        "Google Chrome": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Cache"),
        "Microsoft Edge": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "Cache"),
        "Mozilla Firefox": os.path.join(os.getenv("LOCALAPPDATA"), "Mozilla", "Firefox", "Profiles"),
    }

    tulis_log("Memulai pembersihan cache browser...")

    for browser in selected_browsers:
        path = browser_paths[browser]
        if os.path.exists(path):
            try:
                shutil.rmtree(path, ignore_errors=True)
                tulis_log(f"Cache dihapus: {path}")
            except Exception as e:
                tulis_log(f"Gagal menghapus cache {browser}: {e}")

    messagebox.showinfo("Sukses", "Cache browser berhasil dibersihkan!")
    tulis_log("Pembersihan cache browser selesai.")

# Membuat jendela utama
root = tk.Tk()
root.title("Pembersih File Sampah")
root.geometry("500x600")

# Tombol pembersihan utama
tk.Button(root, text="Bersihkan Temp Files", command=bersihkan_temp).pack(pady=5)
tk.Button(root, text="Kosongkan Recycle Bin", command=bersihkan_recycle_bin).pack(pady=5)
tk.Button(root, text="Bersihkan Prefetch", command=bersihkan_prefetch).pack(pady=5)
tk.Button(root, text="Bersihkan Recent Files", command=bersihkan_recent_files).pack(pady=5)

# Label Pilihan Browser
tk.Label(root, text="Pilih browser yang ingin dibersihkan:").pack()

# Checkbox untuk memilih browser
var_chrome = tk.BooleanVar()
var_edge = tk.BooleanVar()
var_firefox = tk.BooleanVar()

tk.Checkbutton(root, text="Google Chrome", variable=var_chrome).pack(anchor="w")
tk.Checkbutton(root, text="Microsoft Edge", variable=var_edge).pack(anchor="w")
tk.Checkbutton(root, text="Mozilla Firefox", variable=var_firefox).pack(anchor="w")

# Tombol untuk membersihkan cache browser
tk.Button(root, text="Bersihkan Cache Browser", command=bersihkan_cache_browser).pack(pady=5)

# Progress Bar
# progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
# progress.pack(pady=10)

# Log Aktivitas dengan Scroll
log_text = scrolledtext.ScrolledText(root, height=10, width=60)
log_text.pack(pady=10)
log_text.insert(tk.END, "=== Log Aktivitas ===\n")

root.mainloop()