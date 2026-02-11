import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk, font

# Main window
root = tk.Tk()
root.title("Type 2025")
root.geometry("1000x700")
root.configure(bg="#f4f4f4")

# Dark mode flag
dark_mode = False

# Functions
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.configure(bg="#2e2e2e")
        editor.configure(bg="#444", fg="white")
    else:
        root.configure(bg="#f4f4f4")
        editor.configure(bg="white", fg="black")

def new_document():
    editor.delete("1.0", tk.END)

def save_document():
    file_path = filedialog.asksaveasfilename(defaultextension=".TYP2", filetypes=[("Type 2025 files", "*.TYP2")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", tk.END))

def load_document():
    file_path = filedialog.askopenfilename(filetypes=[("Type 2025 files", "*.TYP2")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            editor.delete("1.0", tk.END)
            editor.insert(tk.END, f.read())

def insert_image():
    url = simpledialog.askstring("Insert Image", "Enter image URL or path:")
    if url:
        try:
            img = tk.PhotoImage(file=url)
            editor.image_create(tk.INSERT, image=img)
            editor.image = img  # prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert image:\n{e}")

def insert_table():
    table_text = "\t".join(["Cell"] * 3) + "\n"
    table_text *= 3
    editor.insert(tk.INSERT, table_text)

def zoom_editor(val):
    size = int(val)
    editor.configure(font=("Segoe UI", size))

# Ribbon setup
ribbon = tk.Frame(root, bg="#e7e7e7")
ribbon.pack(fill=tk.X)

# Tabs
tabs_frame = tk.Frame(ribbon, bg="#f2f2f2")
tabs_frame.pack(fill=tk.X)

active_tab = tk.StringVar(value="home")

def switch_tab(tab_name):
    active_tab.set(tab_name)
    for frame in content_frames.values():
        frame.pack_forget()
    content_frames[tab_name].pack(fill=tk.X, padx=10, pady=5)

tabs = ["file", "home", "insert", "layout", "review"]
tab_buttons = {}
for tab in tabs:
    btn = tk.Button(tabs_frame, text=tab.capitalize(), command=lambda t=tab: switch_tab(t))
    btn.pack(side=tk.LEFT, padx=2, pady=2)
    tab_buttons[tab] = btn

# Ribbon content frames
content_frames = {}
for tab in tabs:
    frame = tk.Frame(ribbon, bg="#ffffff", bd=1, relief=tk.SOLID)
    content_frames[tab] = frame
content_frames["home"].pack(fill=tk.X, padx=10, pady=5)

# File group
file_group = tk.Frame(content_frames["file"], bd=1, relief=tk.SOLID, padx=5, pady=5)
file_group.pack(side=tk.LEFT, padx=5)
tk.Button(file_group, text="New", command=new_document).pack(side=tk.LEFT, padx=2)
tk.Button(file_group, text="Save", command=save_document).pack(side=tk.LEFT, padx=2)
tk.Button(file_group, text="Open", command=load_document).pack(side=tk.LEFT, padx=2)

# Home group (font and style)
home_group = tk.Frame(content_frames["home"], bd=1, relief=tk.SOLID, padx=5, pady=5)
home_group.pack(side=tk.LEFT, padx=5)
font_name = tk.StringVar(value="Segoe UI")
font_size = tk.StringVar(value="12")
ttk.Combobox(home_group, textvariable=font_name, values=["Segoe UI","Arial","Georgia"]).pack(side=tk.LEFT, padx=2)
ttk.Combobox(home_group, textvariable=font_size, values=["8","10","12","14","18"], width=3).pack(side=tk.LEFT, padx=2)

def apply_font(*args):
    f = font.Font(family=font_name.get(), size=int(font_size.get()))
    editor.configure(font=f)
font_name.trace_add("write", apply_font)
font_size.trace_add("write", apply_font)

# Text style buttons
style_group = tk.Frame(content_frames["home"], bd=1, relief=tk.SOLID, padx=5, pady=5)
style_group.pack(side=tk.LEFT, padx=5)
def toggle_bold(): editor.tag_add("bold", "sel.first", "sel.last"); editor.tag_config("bold", font=("Segoe UI", int(font_size.get()), "bold"))
def toggle_italic(): editor.tag_add("italic", "sel.first", "sel.last"); editor.tag_config("italic", font=("Segoe UI", int(font_size.get()), "italic"))
def toggle_underline(): editor.tag_add("underline", "sel.first", "sel.last"); editor.tag_config("underline", font=("Segoe UI", int(font_size.get()), "underline"))
tk.Button(style_group, text="B", command=toggle_bold).pack(side=tk.LEFT)
tk.Button(style_group, text="I", command=toggle_italic).pack(side=tk.LEFT)
tk.Button(style_group, text="U", command=toggle_underline).pack(side=tk.LEFT)

# Insert group
insert_group = tk.Frame(content_frames["insert"], bd=1, relief=tk.SOLID, padx=5, pady=5)
insert_group.pack(side=tk.LEFT, padx=5)
tk.Button(insert_group, text="Insert Image", command=insert_image).pack(side=tk.LEFT, padx=2)
tk.Button(insert_group, text="Insert Table", command=insert_table).pack(side=tk.LEFT, padx=2)

# Layout group
layout_group = tk.Frame(content_frames["layout"], bd=1, relief=tk.SOLID, padx=5, pady=5)
layout_group.pack(side=tk.LEFT, padx=5)
tk.Button(layout_group, text="Toggle Dark Mode", command=toggle_dark_mode).pack(side=tk.LEFT, padx=2)

# Editor
editor = tk.Text(root, wrap=tk.WORD, font=("Segoe UI", 12))
editor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
editor.insert(tk.END, "Type here...")

# Bottom bar (zoom)
bottom_bar = tk.Frame(root, bg="#ddd")
bottom_bar.pack(fill=tk.X, side=tk.BOTTOM)
zoom_slider = tk.Scale(bottom_bar, from_=8, to=48, orient=tk.HORIZONTAL, label="Zoom", command=zoom_editor)
zoom_slider.set(12)
zoom_slider.pack(side=tk.LEFT, padx=10, pady=5)

# Start main loop
root.mainloop()
