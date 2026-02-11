import tkinter as tk
import webbrowser

# ---------- Helpers ----------
def open_link(url):
    if url != "#":
        webbrowser.open(url)

# ---------- Root ----------
root = tk.Tk()
root.title("Quoffice 2025")
root.geometry("1100x800")
root.configure(bg="#f5f7fb")

ACCENT = "#0078D4"
CARD_BG = "#ffffff"

# ---------- Scrollable Container ----------
container = tk.Frame(root, bg="#f5f7fb")
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container, bg="#f5f7fb", highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#f5f7fb")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Enable mouse wheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ---------- Navbar ----------
navbar = tk.Frame(scrollable_frame, bg="white", height=60)
navbar.pack(fill="x")

logo = tk.Label(
    navbar,
    text="Quoffice 2025",
    font=("Segoe UI", 14, "bold"),
    fg=ACCENT,
    bg="white"
)
logo.pack(side="left", padx=30)

nav_links = [
    ("Home", "#"),
    ("Templates", "https://masterd2012.github.io/Quoffice2025/templates/"),
    ("My Sites", "https://masterd2012.github.io/Quoffice2025/mysites/"),
    ("Help & About", "https://masterd2012.github.io/Quoffice2025/help/"),
    ("GitHub", "https://github.com/MasterD2012/Quoffice2025/")
]

for text, link in reversed(nav_links):
    btn = tk.Button(
        navbar,
        text=text,
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#444",
        bd=0,
        cursor="hand2",
        command=lambda l=link: open_link(l)
    )
    btn.pack(side="right", padx=10)

# ---------- Hero ----------
hero = tk.Frame(scrollable_frame, bg=ACCENT, height=220)
hero.pack(fill="x")

hero_title = tk.Label(
    hero,
    text="Welcome to Quoffice 2025",
    font=("Segoe UI", 28, "bold"),
    fg="white",
    bg=ACCENT
)
hero_title.pack(pady=(40, 10))

hero_text = tk.Label(
    hero,
    text="A modern, lightweight office suite — built for the web\n\n⚠️ This page is under construction ⚠️",
    font=("Segoe UI", 12),
    fg="white",
    bg=ACCENT,
    justify="center"
)
hero_text.pack()

# ---------- Section Helper ----------
def create_section(title, apps):
    section = tk.Frame(scrollable_frame, bg="#f5f7fb")
    section.pack(fill="x", pady=30)

    lbl = tk.Label(
        section,
        text=title,
        font=("Segoe UI", 18, "bold"),
        bg="#f5f7fb"
    )
    lbl.pack(anchor="w", padx=40, pady=10)

    grid = tk.Frame(section, bg="#f5f7fb")
    grid.pack(padx=40)

    for i, (icon, name, link) in enumerate(apps):
        card = tk.Frame(
            grid,
            bg=CARD_BG,
            width=200,
            height=140
        )
        card.grid(row=i // 4, column=i % 4, padx=15, pady=15)
        card.pack_propagate(False)

        icon_lbl = tk.Label(
            card,
            text=icon,
            font=("Segoe UI Emoji", 28),
            bg=CARD_BG
        )
        icon_lbl.pack(pady=(20, 5))

        btn = tk.Button(
            card,
            text=name,
            font=("Segoe UI", 12, "bold"),
            fg=ACCENT,
            bg=CARD_BG,
            bd=0,
            cursor="hand2",
            command=lambda l=link: open_link(l)
        )
        btn.pack()

# ---------- Sections ----------
create_section("Main Apps", [
    ("📝", "Type", "https://masterd2012.github.io/Quoffice2025/type/"),
    ("📊", "Slides", "https://masterd2012.github.io/Quoffice2025/slides/"),
    ("📈", "Sheets", "https://masterd2012.github.io/Quoffice2025/sheets/app/"),
    ("🗒️", "Notes", "https://masterd2012.github.io/Quoffice2025/notes/")
])

create_section("Other Apps", [
    ("📷", "Q Cam", "https://masterd2012.github.io/Quoffice2025/qcam/"),
    ("✅", "To Do", "https://masterd2012.github.io/Quoffice2025/todo/"),
    ("🖎🏻", "QBoard", "https://masterd2012.github.io/Quoffice2025/qboard/")
])

create_section("Other Websites", [
    ("🌐", "MasterD2012 Home", "https://masterd2012.github.io/")
])

# ---------- Footer ----------
footer = tk.Label(
    scrollable_frame,
    text="© 2025 Quoffice — Built by MasterD2012",
    font=("Segoe UI", 10),
    fg="#666",
    bg="#f5f7fb"
)
footer.pack(pady=20)

# ---------- Run ----------
root.mainloop()
