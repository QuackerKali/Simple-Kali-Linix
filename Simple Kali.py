import os
import subprocess
import configparser
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, Toplevel, Text, BOTH, IntVar

APP_DIRS = [
    "/usr/share/applications",
    "/usr/share/applications/kali-menu",
    os.path.expanduser("~/.local/share/applications")
]


class KaliControlCenter(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Kali Control Center - Cyber Dashboard")
        self.geometry("1250x750")

        self.apps = []
        self.filtered_apps = []
        self.current_category = "ALL"

        self.search_var = StringVar()
        self.tor_var = IntVar(value=0)

        self.build_ui()
        self.load_apps()

    # ---------------- UI ----------------
    def build_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=8)

        ttk.Label(
            header,
            text="KALI CONTROL CENTER",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        search = ttk.Entry(header, textvariable=self.search_var, width=35)
        search.pack(side="right")
        search.bind("<KeyRelease>", lambda e: self.refresh_grid())

        ttk.Label(header, text="Search:").pack(side="right", padx=5)

        # ---------------- MAIN ----------------
        main = ttk.Frame(self)
        main.pack(fill=BOTH, expand=True)

        # ---------------- SIDEBAR ----------------
        sidebar = ttk.Frame(main, width=220, bootstyle="secondary")
        sidebar.pack(side="left", fill="y")

        ttk.Label(sidebar, text="CONTROLS", font=("Arial", 12, "bold")).pack(pady=10)

        # ===== TOR TOGGLE =====
        self.tor_label = ttk.Label(sidebar, text="🧅 TOR: OFF", bootstyle="danger")
        self.tor_label.pack(pady=5)

        ttk.Checkbutton(
            sidebar,
            text="Enable Tor Routing",
            variable=self.tor_var,
            bootstyle="success-round-toggle",
            command=self.toggle_tor
        ).pack(fill="x", padx=10, pady=5)

        ttk.Separator(sidebar).pack(fill="x", pady=10)

        # ===== CATEGORIES =====
        ttk.Label(sidebar, text="CATEGORIES", font=("Arial", 12, "bold")).pack(pady=5)

        categories = ["ALL", "RECON", "EXPLOIT", "WEB", "WIRELESS", "PASSWORD"]

        for cat in categories:
            ttk.Button(
                sidebar,
                text=cat,
                bootstyle="info-outline",
                command=lambda c=cat: self.set_category(c)
            ).pack(fill="x", padx=10, pady=4)

        # ---------------- SCROLL AREA ----------------
        container = ttk.Frame(main)
        container.pack(side="left", fill=BOTH, expand=True)

        self.canvas = ttk.Canvas(container)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.scroll_frame = ttk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill=BOTH, expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._scroll)

    # ---------------- TOR CONTROL ----------------
    def toggle_tor(self):
        if self.tor_var.get() == 1:
            cmd = ["pkexec", "systemctl", "start", "tor"]
            self.tor_label.config(text="🧅 TOR: ON", bootstyle="success")
        else:
            cmd = ["pkexec", "systemctl", "stop", "tor"]
            self.tor_label.config(text="🧅 TOR: OFF", bootstyle="danger")

        try:
            subprocess.Popen(cmd)
        except Exception as e:
            print("Tor toggle error:", e)

    # ---------------- SCROLL ----------------
    def _scroll(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------------- LOAD APPS ----------------
    def parse_desktop(self, path):
        config = configparser.ConfigParser()
        try:
            config.read(path)
            if "Desktop Entry" not in config:
                return None

            e = config["Desktop Entry"]

            return {
                "name": e.get("Name", "Unknown"),
                "exec": e.get("Exec", "").split("%")[0].strip(),
                "category": e.get("Categories", "Other"),
            }
        except:
            return None

    def load_apps(self):
        self.apps.clear()

        for d in APP_DIRS:
            if not os.path.exists(d):
                continue

            for f in os.listdir(d):
                if f.endswith(".desktop"):
                    app = self.parse_desktop(os.path.join(d, f))
                    if app:
                        self.apps.append(app)

        self.apps.sort(key=lambda x: x["name"].lower())
        self.refresh_grid()

    # ---------------- CATEGORY FILTER ----------------
    def set_category(self, cat):
        self.current_category = cat
        self.refresh_grid()

    def matches_category(self, app, cat):
        c = app["category"].lower()

        if cat == "ALL":
            return True
        if cat == "RECON":
            return "recon" in c or "scanner" in c
        if cat == "EXPLOIT":
            return "exploit" in c
        if cat == "WEB":
            return "web" in c
        if cat == "WIRELESS":
            return "wireless" in c
        if cat == "PASSWORD":
            return "password" in c or "crack" in c

        return True

    # ---------------- GRID ----------------
    def refresh_grid(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        q = self.search_var.get().lower()

        apps = [
            a for a in self.apps
            if q in a["name"].lower()
            and self.matches_category(a, self.current_category)
        ]

        cols = 3
        r = c = 0

        for app in apps:
            card = ttk.Frame(self.scroll_frame, padding=12, bootstyle="dark")
            card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")

            ttk.Label(
                card,
                text=app["name"],
                font=("Arial", 11, "bold"),
                wraplength=200
            ).pack(pady=5)

            ttk.Button(
                card,
                text="🚀 Launch",
                bootstyle=SUCCESS,
                command=lambda a=app: self.launch(a)
            ).pack(fill="x", pady=3)

            ttk.Button(
                card,
                text="ℹ Info",
                bootstyle=INFO,
                command=lambda a=app: self.info(a)
            ).pack(fill="x", pady=3)

            c += 1
            if c >= cols:
                c = 0
                r += 1

    # ---------------- ACTIONS ----------------
    def launch(self, app):
        try:
            subprocess.Popen(app["exec"], shell=True)
        except:
            pass

    def info(self, app):
        win = Toplevel(self)
        win.title(app["name"])
        win.geometry("500x300")

        text = Text(win, wrap="word")
        text.pack(fill=BOTH, expand=True)

        text.insert("1.0", f"""
TOOL: {app['name']}

CATEGORY: {app['category']}

EXEC: {app['exec']}
""")

        text.config(state="disabled")


if __name__ == "__main__":
    KaliControlCenter().mainloop()
