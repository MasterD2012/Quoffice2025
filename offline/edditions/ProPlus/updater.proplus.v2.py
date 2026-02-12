import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import json
import shutil
import requests
from datetime import datetime

# ================= CONFIG =================

MANIFEST_URL = "https://masterd2012.github.io/Quoffice2025/offline/edditions/ProPlus/manifest.json"
ACTIVATION_URL = "https://masterd2012.github.io/Quoffice2025/offline/edditions/ProPlus/activation.txt"

INSTALL_DIR = os.getcwd()
LOG_FILE = "install.log"
INFO_FILE = "install.info"
ACTIVATION_FILE = "activation.key"

# =========================================

# ---------- Utilities ----------

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def set_status(text):
    status_var.set(text)
    root.update_idletasks()

# ---------- Activation ----------

def is_activated():
    return os.path.exists(ACTIVATION_FILE)

def check_activation_online(key):
    r = requests.get(ACTIVATION_URL)
    r.raise_for_status()
    valid_keys = r.text.splitlines()
    return key.strip() in valid_keys

def activate():
    key = simpledialog.askstring("Activation", "Enter activation key:")
    if not key:
        return

    set_status("Checking activation key...")
    try:
        if check_activation_online(key):
            with open(ACTIVATION_FILE, "w") as f:
                f.write(key)
            log("Activated successfully")
            messagebox.showinfo("Activated", "Activation successful.")
        else:
            messagebox.showerror("Error", "Invalid activation key.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- Safe JSON Loader ----------

def safe_get_json(url, error_title="Download Error"):
    try:
        r = requests.get(url)
        r.raise_for_status()

        if not r.text.strip():
            raise ValueError("Empty response")

        return r.json()
    except Exception as e:
        messagebox.showerror(
            error_title,
            f"Failed to load JSON from:\n{url}\n\n{e}"
        )
        log(f"JSON error from {url}: {e}")
        return None

# ---------- Manifest ----------

def load_manifest():
    data = safe_get_json(MANIFEST_URL, "Manifest Error")
    if not data:
        raise RuntimeError("Manifest could not be loaded")
    return data

# ---------- File Downloader ----------

def download_file(url, dest, progress=None):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    total = int(r.headers.get("content-length", 1))
    downloaded = 0

    with open(dest, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if progress:
                    progress.set((downloaded / total) * 100)
                    root.update_idletasks()

# ---------- Install Single App ----------

def install_single_app():
    if not is_activated():
        activate()
        if not is_activated():
            return

    manifest = load_manifest()
    if not manifest or "apps" not in manifest:
        return

    names = [app["name"] for app in manifest["apps"]]
    app_name = simpledialog.askstring(
        "Install App",
        "Available apps:\n\n" + "\n".join(names) + "\n\nEnter app name:"
    )

    app = next((a for a in manifest["apps"] if a["name"] == app_name), None)
    if not app:
        return

    set_status(f"Installing {app['name']}...")
    log(f"Installing {app['name']}")

    filelist_url = app["source_url"].rstrip("/") + "/filelist.json"
    filelist = safe_get_json(filelist_url, "File List Error")
    if not filelist:
        set_status("Install failed.")
        return

    total_files = len(filelist.get("files", []))

    for i, file in enumerate(filelist.get("files", []), start=1):
        progress_var.set((i / total_files) * 100)
        download_file(
            f"{app['source_url']}/{file}",
            os.path.join(INSTALL_DIR, app["install_dir"], file)
        )

    write_install_info()
    set_status("Install completed.")
    log(f"{app['name']} installed")

# ---------- Repair All ----------

def repair_all():
    if not is_activated():
        activate()
        if not is_activated():
            return

    set_status("Repairing installation...")
    log("Repair started")

    manifest = load_manifest()
    if not manifest or "apps" not in manifest:
        return

    apps = manifest["apps"]
    count = len(apps)

    for i, app in enumerate(apps, start=1):
        progress_var.set((i / count) * 100)
        filelist_url = app["source_url"].rstrip("/") + "/filelist.json"
        filelist = safe_get_json(filelist_url, "Repair Error")
        if not filelist:
            continue

        for file in filelist.get("files", []):
            download_file(
                f"{app['source_url']}/{file}",
                os.path.join(INSTALL_DIR, app["install_dir"], file)
            )

    set_status("Repair completed.")
    log("Repair completed")

# ---------- Uninstall Everything ----------

def uninstall_all():
    if not messagebox.askyesno("Uninstall", "Remove all installed apps?"):
        return

    set_status("Uninstalling everything...")
    log("Uninstall started")

    manifest = load_manifest()
    if not manifest or "apps" not in manifest:
        return

    for app in manifest["apps"]:
        path = os.path.join(INSTALL_DIR, app["install_dir"])
        if os.path.exists(path):
            shutil.rmtree(path)

    for f in [ACTIVATION_FILE, INFO_FILE]:
        if os.path.exists(f):
            os.remove(f)

    set_status("Uninstall completed.")
    log("Uninstall completed")

# ---------- Install Info ----------

def write_install_info():
    info = {
        "installed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(INFO_FILE, "w") as f:
        json.dump(info, f, indent=2)

# ---------- View Logs ----------

def view_logs():
    if not os.path.exists(LOG_FILE):
        messagebox.showinfo("Logs", "No logs yet.")
        return

    win = tk.Toplevel(root)
    win.title("Update Logs")
    text = tk.Text(win, width=80, height=25)
    text.pack(fill="both", expand=True)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        text.insert("1.0", f.read())

# ================= UI ====================

root = tk.Tk()
root.title("Software Update Manager")
root.geometry("700x400")

status_var = tk.StringVar(value="Ready.")
progress_var = tk.DoubleVar(value=0)

# Menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Activate", command=activate)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

actions_menu = tk.Menu(menu, tearoff=0)
actions_menu.add_command(label="Install Single App", command=install_single_app)
actions_menu.add_command(label="Repair All", command=repair_all)
actions_menu.add_command(label="Uninstall Everything", command=uninstall_all)

help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(label="View Logs", command=view_logs)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Actions", menu=actions_menu)
menu.add_cascade(label="Help", menu=help_menu)

# Main
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)

title = tk.Label(frame, text="Software Update Manager", font=("Segoe UI", 16, "bold"))
title.pack(pady=10)

status_label = tk.Label(frame, textvariable=status_var, font=("Segoe UI", 10))
status_label.pack(pady=10)

# Bottom bar
bottom = tk.Frame(root)
bottom.pack(fill="x", side="bottom")

progress = ttk.Progressbar(bottom, variable=progress_var, maximum=100)
progress.pack(fill="x", padx=10, pady=5)

root.mainloop()
