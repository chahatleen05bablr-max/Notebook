"""
PocketHub — File Pockets + Smart Notification System
A complete Python/Tkinter desktop application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
import shutil
import time
import threading
import uuid
import datetime
from pathlib import Path

# ─── Theme / Palette ──────────────────────────────────────────────────────────
BG       = "#0B0D14"
SURFACE  = "#131620"
CARD     = "#181B28"
HOVER    = "#1C2030"
BORDER   = "#252A40"
TEXT     = "#E8EAF6"
MUTED    = "#6B72A8"
SUBTLE   = "#9BA3D4"

SUCCESS  = "#22C55E"; SUCCESS_BG = "#0A1F12"
ERROR    = "#EF4444"; ERROR_BG   = "#1F0A0A"
WARNING  = "#F59E0B"; WARNING_BG = "#1F180A"
INFO     = "#6366F1"; INFO_BG    = "#0E0F20"
BIRTHDAY = "#EC4899"; BDAY_BG    = "#1F0A16"
ACCENT   = "#6366F1"
PURPLE   = "#8B5CF6"
TEAL     = "#14B8A6"
ORANGE   = "#F97316"

TYPE_CFG = {
    "success":  {"color": SUCCESS,  "bg": SUCCESS_BG,  "icon": "✓",  "label": "Success"},
    "error":    {"color": ERROR,    "bg": ERROR_BG,    "icon": "✕",  "label": "Error"},
    "warning":  {"color": WARNING,  "bg": WARNING_BG,  "icon": "⚠",  "label": "Warning"},
    "info":     {"color": INFO,     "bg": INFO_BG,     "icon": "ℹ",  "label": "Info"},
    "birthday": {"color": BIRTHDAY, "bg": BDAY_BG,     "icon": "🎂", "label": "Birthday"},
    "reminder": {"color": WARNING,  "bg": WARNING_BG,  "icon": "🔔", "label": "Reminder"},
    "exam":     {"color": ERROR,    "bg": ERROR_BG,    "icon": "📝", "label": "Exam"},
    "deadline": {"color": WARNING,  "bg": WARNING_BG,  "icon": "⏰", "label": "Deadline"},
}

FILE_ICONS = {
    "pdf": "📄", "doc": "📝", "docx": "📝", "txt": "📃",
    "png": "🖼", "jpg": "🖼", "jpeg": "🖼", "gif": "🖼",
    "mp4": "🎬", "mp3": "🎵", "zip": "📦",
    "xlsx": "📊", "xls": "📊", "ppt": "📊", "pptx": "📊", "csv": "📊",
}

DEFAULT_FOLDERS = [
    {"id": "assignments", "name": "Assignments", "icon": "📚", "color": WARNING,  "desc": "Homework, projects & submissions"},
    {"id": "credentials", "name": "Credentials", "icon": "🔐", "color": SUCCESS,  "desc": "Passwords, logins & access keys"},
    {"id": "notes",       "name": "Study Notes", "icon": "📓", "color": INFO,     "desc": "Lectures, summaries & flashcards"},
    {"id": "exams",       "name": "Exam Prep",   "icon": "🎯", "color": ERROR,    "desc": "Mock tests, question banks & scores"},
]

DEMO_NOTIFS = [
    {"type": "success",  "title": "Note Saved Successfully",    "body": "Study notes for Chapter 7 saved."},
    {"type": "success",  "title": "Assignment Submitted",       "body": "Physics assignment submitted at 11:45 PM."},
    {"type": "success",  "title": "Password Added",             "body": "Credential for 'College Portal' saved."},
    {"type": "error",    "title": "Invalid Login Credentials",  "body": "Check your username and password."},
    {"type": "error",    "title": "Failed to Save Data",        "body": "Network timeout. Changes not saved."},
    {"type": "warning",  "title": "Assignment Due Tomorrow",    "body": "Maths Assignment 3 due at 11:59 PM."},
    {"type": "warning",  "title": "Exam in 2 Days",             "body": "Physics Unit Test — Thursday 9 AM."},
    {"type": "info",     "title": "New Update Available",       "body": "v2.4.1 — improved timetable sync."},
    {"type": "info",     "title": "Timetable Updated",          "body": "Wednesday's lab moved to Room 204."},
    {"type": "birthday", "title": "Today is Priya's Birthday 🎂","body": "Don't forget to wish her!"},
    {"type": "reminder", "title": "Good Morning! ☀️",           "body": "3 classes today. First at 9:00 AM."},
    {"type": "deadline", "title": "Deadline in 4 Hours ⏰",     "body": "Network Security — submit before 6 PM."},
    {"type": "reminder", "title": "AFCAT Study Session 📚",    "body": "Study session at 6 PM tonight."},
    {"type": "exam",     "title": "Exam Starting Soon 📝",      "body": "AFCAT mock test in 30 minutes!"},
]


# ─── Utilities ────────────────────────────────────────────────────────────────
def now_str():
    return datetime.datetime.now().strftime("%b %d, %I:%M %p")

def fmt_size(b):
    if b < 1024:     return f"{b} B"
    elif b < 1048576:return f"{b/1024:.1f} KB"
    else:            return f"{b/1048576:.1f} MB"

def file_icon(name):
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return FILE_ICONS.get(ext, "📎")

def make_id():
    return str(uuid.uuid4())[:8]


# ─── Scrollable Frame helper ──────────────────────────────────────────────────
class ScrollFrame(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=kw.get("bg", BG))
        self.canvas = tk.Canvas(self, bg=kw.get("bg", BG), bd=0, highlightthickness=0)
        self.vsb    = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner  = tk.Frame(self.canvas, bg=kw.get("bg", BG))
        self._win   = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._on_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self.canvas.itemconfig(self._win, width=e.width)

    def _on_mousewheel(self, e):
        self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")


# ─── Toast Notification (overlay window) ─────────────────────────────────────
class ToastManager:
    """Manages a stack of floating toast windows."""
    def __init__(self, root):
        self.root   = root
        self.toasts = []   # list of (window, y_pos)

    def show(self, title, body, ntype="info"):
        cfg = TYPE_CFG.get(ntype, TYPE_CFG["info"])
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.configure(bg=SURFACE)

        W, H = 340, 80
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        # stack from bottom-right
        idx = len(self.toasts)
        x = sw - W - 16
        y = sh - 60 - (H + 10) * (idx + 1)
        win.geometry(f"{W}x{H}+{x}+{y}")

        # Border frame
        outer = tk.Frame(win, bg=cfg["color"], padx=2, pady=2)
        outer.pack(fill="both", expand=True)
        inner = tk.Frame(outer, bg=SURFACE)
        inner.pack(fill="both", expand=True)

        # Icon
        icon_lbl = tk.Label(inner, text=cfg["icon"], font=("Segoe UI Emoji", 18),
                            bg=cfg["bg"], fg=cfg["color"], width=3)
        icon_lbl.pack(side="left", padx=(6, 0), pady=6)

        # Text
        txt = tk.Frame(inner, bg=SURFACE)
        txt.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        tk.Label(txt, text=title, font=("Segoe UI", 10, "bold"),
                 bg=SURFACE, fg=TEXT, anchor="w").pack(fill="x")
        tk.Label(txt, text=body, font=("Segoe UI", 8),
                 bg=SURFACE, fg=MUTED, anchor="w", wraplength=220).pack(fill="x")

        # Time
        tk.Label(inner, text=datetime.datetime.now().strftime("%I:%M %p"),
                 font=("Segoe UI", 7), bg=SURFACE, fg=MUTED).pack(side="right", padx=6, pady=6, anchor="ne")

        # Progress bar (simulated)
        bar_canvas = tk.Canvas(win, height=3, bg=SURFACE, highlightthickness=0)
        bar_canvas.place(relx=0, rely=1, relwidth=1, anchor="sw")
        bar_id = bar_canvas.create_rectangle(0, 0, W, 3, fill=cfg["color"], outline="")

        self.toasts.append(win)

        # Close button
        def close():
            try:
                win.destroy()
                if win in self.toasts:
                    self.toasts.remove(win)
                    self._restack()
            except Exception:
                pass

        win.bind("<Button-1>", lambda e: close())

        # Auto-dismiss after 4.5s + shrink bar
        steps = 90
        delay = int(4500 / steps)

        def animate_bar(step=0):
            if step >= steps:
                close(); return
            try:
                ratio = 1 - step / steps
                bar_canvas.coords(bar_id, 0, 0, W * ratio, 3)
                win.after(delay, animate_bar, step + 1)
            except Exception:
                pass

        animate_bar()

    def _restack(self):
        sh = self.root.winfo_screenheight()
        sw = self.root.winfo_screenwidth()
        W, H = 340, 80
        for i, w in enumerate(self.toasts):
            try:
                y = sh - 60 - (H + 10) * (i + 1)
                x = sw - W - 16
                w.geometry(f"+{x}+{y}")
            except Exception:
                pass


# ─── Modal Dialog Helpers ─────────────────────────────────────────────────────
class CenteredDialog(tk.Toplevel):
    def __init__(self, parent, title, width=420, height=320):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=SURFACE)
        self.resizable(False, False)
        self.grab_set()
        # Center
        parent.update_idletasks()
        px = parent.winfo_x() + parent.winfo_width() // 2 - width // 2
        py = parent.winfo_y() + parent.winfo_height() // 2 - height // 2
        self.geometry(f"{width}x{height}+{px}+{py}")


class RenameDialog(CenteredDialog):
    def __init__(self, parent, current_name, prompt="Rename:"):
        super().__init__(parent, "Rename", 380, 160)
        self.result = None

        tk.Label(self, text=prompt, font=("Segoe UI", 11, "bold"),
                 bg=SURFACE, fg=TEXT).pack(pady=(22, 8))

        self.entry = tk.Entry(self, font=("Segoe UI", 11), bg=CARD, fg=TEXT,
                              insertbackground=TEXT, relief="flat",
                              highlightthickness=1, highlightcolor=ACCENT,
                              highlightbackground=BORDER, width=32)
        self.entry.pack(padx=24)
        self.entry.insert(0, current_name)
        self.entry.select_range(0, "end")
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self._save())
        self.entry.bind("<Escape>", lambda e: self.destroy())

        btn_row = tk.Frame(self, bg=SURFACE)
        btn_row.pack(pady=18)
        tk.Button(btn_row, text="Cancel", font=("Segoe UI", 9), bg=CARD, fg=MUTED,
                  relief="flat", padx=16, pady=6, cursor="hand2",
                  command=self.destroy).pack(side="left", padx=6)
        tk.Button(btn_row, text="Save", font=("Segoe UI", 9, "bold"), bg=ACCENT, fg="#fff",
                  relief="flat", padx=16, pady=6, cursor="hand2",
                  command=self._save).pack(side="left", padx=6)

    def _save(self):
        val = self.entry.get().strip()
        if val:
            self.result = val
            self.destroy()

    @classmethod
    def ask(cls, parent, current_name, prompt="Rename:"):
        dlg = cls(parent, current_name, prompt)
        parent.wait_window(dlg)
        return dlg.result


class NewFolderDialog(CenteredDialog):
    ICONS   = ["📁","📂","📚","🗂","🔐","📝","🎯","📓","🗄","💼","🧪","🏆","🎮","🔬","📊"]
    COLORS  = [ACCENT, SUCCESS, ERROR, WARNING, BIRTHDAY, TEAL, ORANGE, PURPLE]

    def __init__(self, parent):
        super().__init__(parent, "New Folder", 440, 370)
        self.result = None
        self._icon  = tk.StringVar(value="📁")
        self._color = tk.StringVar(value=ACCENT)

        tk.Label(self, text="New Folder", font=("Segoe UI", 13, "bold"),
                 bg=SURFACE, fg=TEXT).pack(pady=(18, 12))

        # Name
        self.entry = tk.Entry(self, font=("Segoe UI", 11), bg=CARD, fg=TEXT,
                              insertbackground=TEXT, relief="flat",
                              highlightthickness=1, highlightcolor=ACCENT,
                              highlightbackground=BORDER, width=34)
        self.entry.pack(padx=24, pady=(0, 10))
        self.entry.insert(0, "")
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self._save())

        # Icons row
        tk.Label(self, text="ICON", font=("Segoe UI", 8, "bold"),
                 bg=SURFACE, fg=MUTED).pack(anchor="w", padx=26)
        icon_row = tk.Frame(self, bg=SURFACE)
        icon_row.pack(fill="x", padx=24, pady=(4, 10))
        for ic in self.ICONS:
            b = tk.Button(icon_row, text=ic, font=("Segoe UI Emoji", 14),
                          bg=CARD, fg=TEXT, relief="flat", padx=4, pady=2,
                          cursor="hand2",
                          command=lambda i=ic: self._icon.set(i))
            b.pack(side="left", padx=2)

        # Colors row
        tk.Label(self, text="COLOR", font=("Segoe UI", 8, "bold"),
                 bg=SURFACE, fg=MUTED).pack(anchor="w", padx=26)
        col_row = tk.Frame(self, bg=SURFACE)
        col_row.pack(fill="x", padx=24, pady=(4, 14))
        for col in self.COLORS:
            b = tk.Button(col_row, bg=col, activebackground=col,
                          width=2, height=1, relief="flat", cursor="hand2",
                          command=lambda c=col: self._color.set(c))
            b.pack(side="left", padx=4)

        btn_row = tk.Frame(self, bg=SURFACE)
        btn_row.pack()
        tk.Button(btn_row, text="Cancel", font=("Segoe UI", 9), bg=CARD, fg=MUTED,
                  relief="flat", padx=16, pady=6, cursor="hand2",
                  command=self.destroy).pack(side="left", padx=6)
        tk.Button(btn_row, text="Create Folder", font=("Segoe UI", 9, "bold"),
                  bg=ACCENT, fg="#fff", relief="flat", padx=16, pady=6,
                  cursor="hand2", command=self._save).pack(side="left", padx=6)

    def _save(self):
        name = self.entry.get().strip()
        if not name:
            self.entry.config(highlightbackground=ERROR)
            return
        self.result = {"id": make_id(), "name": name,
                       "icon": self._icon.get(), "color": self._color.get(), "desc": ""}
        self.destroy()

    @classmethod
    def ask(cls, parent):
        dlg = cls(parent)
        parent.wait_window(dlg)
        return dlg.result


# ─── Folder Pockets Tab ───────────────────────────────────────────────────────
class FolderPocketsTab(tk.Frame):
    def __init__(self, parent, toast_mgr, app):
        super().__init__(parent, bg=BG)
        self.toast_mgr = toast_mgr
        self.app       = app
        self.folders   = list(DEFAULT_FOLDERS)
        self.files     = []          # [{id, name, src_path, size, folder_id, added_at}]
        self._open_fid = None        # currently open folder id
        self._sort     = "date"

        self._build_toolbar()
        self._scroll = ScrollFrame(self, bg=BG)
        self._scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self._render()

    # ── Toolbar ──
    def _build_toolbar(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=16, pady=12)

        tk.Label(bar, text="🔍", bg=BG, fg=MUTED, font=("Segoe UI Emoji", 12)).pack(side="left", padx=(0, 4))
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._render())
        se = tk.Entry(bar, textvariable=self._search_var, font=("Segoe UI", 10),
                      bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                      highlightthickness=1, highlightcolor=ACCENT,
                      highlightbackground=BORDER, width=36)
        se.pack(side="left", ipady=5, padx=(0, 10))

        tk.Button(bar, text="+ New Folder", font=("Segoe UI", 9, "bold"),
                  bg=ACCENT, fg="#fff", relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self._new_folder).pack(side="left")

        self._back_btn = tk.Button(bar, text="← Folders", font=("Segoe UI", 9),
                                   bg=CARD, fg=MUTED, relief="flat", padx=12, pady=5,
                                   cursor="hand2", command=self._go_back)
        # Shown only when inside a folder

        self._upload_btn = tk.Button(bar, text="📤 Upload Files", font=("Segoe UI", 9, "bold"),
                                     bg=CARD, fg=TEXT, relief="flat", padx=12, pady=5,
                                     cursor="hand2", command=self._upload_files)

    def _go_back(self):
        self._open_fid = None
        self._back_btn.pack_forget()
        self._upload_btn.pack_forget()
        self._render()

    # ── Main render ──
    def _render(self):
        for w in self._scroll.inner.winfo_children():
            w.destroy()

        query = self._search_var.get().strip().lower()

        if query:
            self._render_search(query)
        elif self._open_fid:
            self._render_folder_view()
        else:
            self._render_folder_grid()

    def _render_folder_grid(self):
        self._back_btn.pack_forget()
        self._upload_btn.pack_forget()
        inner = self._scroll.inner

        summary = tk.Label(inner,
                           text=f"{len(self.folders)} folders  ·  {len(self.files)} files total",
                           font=("Segoe UI", 8), bg=BG, fg=MUTED)
        summary.pack(anchor="w", pady=(6, 10))

        grid = tk.Frame(inner, bg=BG)
        grid.pack(fill="x")

        COLS = 4
        for i, folder in enumerate(self.folders):
            fc = len([f for f in self.files if f["folder_id"] == folder["id"]])
            card = self._make_folder_card(grid, folder, fc)
            card.grid(row=i // COLS, column=i % COLS, padx=8, pady=8, sticky="nsew")

        for c in range(COLS):
            grid.columnconfigure(c, weight=1)

    def _make_folder_card(self, parent, folder, file_count):
        frm = tk.Frame(parent, bg=CARD, cursor="hand2",
                       highlightthickness=1, highlightbackground=BORDER)
        frm.bind("<Enter>", lambda e: frm.config(highlightbackground=folder["color"]))
        frm.bind("<Leave>", lambda e: frm.config(highlightbackground=BORDER))
        frm.bind("<Button-1>", lambda e: self._open_folder(folder["id"]))

        tk.Label(frm, text=folder["icon"], font=("Segoe UI Emoji", 26),
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=14, pady=(14, 4))
        tk.Label(frm, text=folder["name"], font=("Segoe UI", 11, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=14)
        if folder.get("desc"):
            tk.Label(frm, text=folder["desc"], font=("Segoe UI", 8),
                     bg=CARD, fg=MUTED, wraplength=150).pack(anchor="w", padx=14, pady=(2, 8))

        bottom = tk.Frame(frm, bg=CARD)
        bottom.pack(fill="x", padx=14, pady=(4, 10))
        tk.Label(bottom, text=f"{file_count} file{'s' if file_count != 1 else ''}",
                 font=("Segoe UI", 8, "bold"), bg=CARD,
                 fg=folder["color"]).pack(side="left")

        # Menu
        menu = tk.Menu(frm, tearoff=0, bg=SURFACE, fg=TEXT, activebackground=HOVER,
                       activeforeground=TEXT, bd=0)
        menu.add_command(label="✏  Rename",
                         command=lambda fid=folder["id"]: self._rename_folder(fid))
        menu.add_command(label="🗑  Delete",
                         command=lambda fid=folder["id"]: self._delete_folder(fid))

        def show_menu(e, m=menu):
            m.tk_popup(e.x_root, e.y_root)

        dots = tk.Label(frm, text="⋯", font=("Segoe UI", 14), bg=CARD, fg=MUTED, cursor="hand2")
        dots.place(relx=1, x=-12, y=10, anchor="ne")
        dots.bind("<Button-1>", show_menu)

        return frm

    def _open_folder(self, folder_id):
        self._open_fid = folder_id
        self._back_btn.pack(side="left", padx=(10, 0))
        self._upload_btn.pack(side="left", padx=(6, 0))
        self._render()

    def _render_folder_view(self):
        folder = next((f for f in self.folders if f["id"] == self._open_fid), None)
        if not folder:
            self._go_back(); return

        inner = self._scroll.inner

        # Breadcrumb label
        bc = tk.Label(inner, text=f"{folder['icon']} {folder['name']}",
                      font=("Segoe UI", 13, "bold"), bg=BG, fg=folder["color"])
        bc.pack(anchor="w", pady=(6, 12))

        # Drop zone
        dz = tk.Frame(inner, bg=CARD, height=90,
                      highlightthickness=2, highlightbackground=BORDER)
        dz.pack(fill="x", pady=(0, 14))
        dz.pack_propagate(False)
        dz_lbl = tk.Label(dz, text="📤  Click 'Upload Files' or drag & drop here",
                          font=("Segoe UI", 10), bg=CARD, fg=MUTED)
        dz_lbl.place(relx=0.5, rely=0.5, anchor="center")
        dz.bind("<Enter>", lambda e: dz.config(highlightbackground=folder["color"]))
        dz.bind("<Leave>", lambda e: dz.config(highlightbackground=BORDER))
        dz.bind("<Button-1>", lambda e: self._upload_files())

        # Sort bar
        ctrl = tk.Frame(inner, bg=BG)
        ctrl.pack(fill="x", pady=(0, 8))
        folder_files = [f for f in self.files if f["folder_id"] == self._open_fid]
        tk.Label(ctrl, text=f"{len(folder_files)} file{'s' if len(folder_files) != 1 else ''}",
                 font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(side="left")
        for s, lbl in [("date", "Date"), ("name", "Name")]:
            active = self._sort == s
            b = tk.Button(ctrl, text=lbl, font=("Segoe UI", 8, "bold"),
                          bg=ACCENT if active else CARD,
                          fg="#fff" if active else MUTED,
                          relief="flat", padx=8, pady=3, cursor="hand2",
                          command=lambda sv=s: self._set_sort(sv))
            b.pack(side="right", padx=3)

        # File grid
        if self._sort == "name":
            folder_files.sort(key=lambda f: f["name"].lower())
        else:
            folder_files.sort(key=lambda f: f["added_at"], reverse=True)

        if not folder_files:
            tk.Label(inner, text=f"{folder['icon']}\nThis folder is empty.\nUpload your first file above.",
                     font=("Segoe UI", 10), bg=BG, fg=MUTED, justify="center").pack(pady=30)
            return

        grid = tk.Frame(inner, bg=BG)
        grid.pack(fill="x")
        COLS = 5
        for i, f in enumerate(folder_files):
            card = self._make_file_card(grid, f, folder["color"])
            card.grid(row=i // COLS, column=i % COLS, padx=6, pady=6, sticky="nsew")
        for c in range(COLS):
            grid.columnconfigure(c, weight=1)

    def _set_sort(self, s):
        self._sort = s
        self._render()

    def _make_file_card(self, parent, file_data, folder_color):
        frm = tk.Frame(parent, bg=CARD, cursor="hand2",
                       highlightthickness=1, highlightbackground=BORDER, width=130)
        frm.pack_propagate(False)
        frm.bind("<Enter>", lambda e: frm.config(highlightbackground=folder_color))
        frm.bind("<Leave>", lambda e: frm.config(highlightbackground=BORDER))

        # Thumbnail area
        thumb = tk.Frame(frm, bg=HOVER, height=70)
        thumb.pack(fill="x")
        thumb.pack_propagate(False)
        tk.Label(thumb, text=file_icon(file_data["name"]),
                 font=("Segoe UI Emoji", 24), bg=HOVER).place(relx=0.5, rely=0.5, anchor="center")
        thumb.bind("<Button-1>", lambda e, fd=file_data: self._open_file(fd))

        # Name
        name_lbl = tk.Label(frm, text=file_data["name"], font=("Segoe UI", 8, "bold"),
                            bg=CARD, fg=TEXT, anchor="w",
                            width=16, cursor="hand2")
        name_lbl.pack(fill="x", padx=6, pady=(6, 1))
        name_lbl.bind("<Button-1>", lambda e, fd=file_data: self._open_file(fd))

        tk.Label(frm, text=fmt_size(file_data["size"]), font=("Segoe UI", 7),
                 bg=CARD, fg=MUTED, anchor="w").pack(fill="x", padx=6)

        btn_row = tk.Frame(frm, bg=CARD)
        btn_row.pack(fill="x", padx=5, pady=5)
        tk.Button(btn_row, text="✏", font=("Segoe UI", 9), bg=HOVER, fg=MUTED,
                  relief="flat", padx=4, pady=2, cursor="hand2",
                  command=lambda fd=file_data: self._rename_file(fd)).pack(side="left", padx=2)
        tk.Button(btn_row, text="✕", font=("Segoe UI", 9), bg=HOVER, fg=ERROR,
                  relief="flat", padx=4, pady=2, cursor="hand2",
                  command=lambda fd=file_data: self._delete_file(fd)).pack(side="left", padx=2)
        tk.Button(btn_row, text="⤤", font=("Segoe UI", 9), bg=HOVER, fg=SUBTLE,
                  relief="flat", padx=4, pady=2, cursor="hand2",
                  command=lambda fd=file_data: self._open_file(fd)).pack(side="left", padx=2)

        return frm

    def _render_search(self, query):
        inner = self._scroll.inner
        results = [f for f in self.files if query in f["name"].lower()]
        tk.Label(inner, text=f"{len(results)} result{'s' if len(results) != 1 else ''} for \"{query}\"",
                 font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(anchor="w", pady=(6, 10))
        if not results:
            tk.Label(inner, text="No files found.", font=("Segoe UI", 10),
                     bg=BG, fg=MUTED).pack(pady=20)
            return
        grid = tk.Frame(inner, bg=BG)
        grid.pack(fill="x")
        COLS = 5
        for i, f in enumerate(results):
            folder = next((fo for fo in self.folders if fo["id"] == f["folder_id"]), None)
            color  = folder["color"] if folder else ACCENT
            card = self._make_file_card(grid, f, color)
            card.grid(row=i // COLS, column=i % COLS, padx=6, pady=6, sticky="nsew")
        for c in range(COLS):
            grid.columnconfigure(c, weight=1)

    # ── Actions ──
    def _upload_files(self):
        if not self._open_fid:
            messagebox.showinfo("Open a Folder", "Please open a folder first, then upload files.")
            return
        paths = filedialog.askopenfilenames(title="Select files to upload")
        if not paths:
            return
        for p in paths:
            p = Path(p)
            entry = {
                "id":        make_id(),
                "name":      p.name,
                "src_path":  str(p),
                "size":      p.stat().st_size,
                "folder_id": self._open_fid,
                "added_at":  time.time(),
            }
            self.files.append(entry)
        folder = next((f for f in self.folders if f["id"] == self._open_fid), None)
        self.toast_mgr.show(f"{len(paths)} file{'s' if len(paths)>1 else ''} uploaded",
                            f"Added to {folder['name'] if folder else 'folder'}.", "success")
        self.app._add_notif({"type": "success",
                             "title": "Files Uploaded",
                             "body": f"{len(paths)} file(s) added to {folder['name'] if folder else 'folder'}."})
        self._render()

    def _rename_file(self, file_data):
        new_name = RenameDialog.ask(self, file_data["name"], "New file name:")
        if new_name:
            file_data["name"] = new_name
            self.toast_mgr.show("File Renamed", f"Renamed to \"{new_name}\"", "success")
            self._render()

    def _delete_file(self, file_data):
        if messagebox.askyesno("Delete File", f"Delete \"{file_data['name']}\"?"):
            self.files = [f for f in self.files if f["id"] != file_data["id"]]
            self.toast_mgr.show("File Deleted", file_data["name"], "info")
            self._render()

    def _open_file(self, file_data):
        p = file_data.get("src_path", "")
        if p and os.path.exists(p):
            os.startfile(p) if os.name == "nt" else os.system(f'xdg-open "{p}" &')
        else:
            messagebox.showinfo("File Preview", f"File: {file_data['name']}\nSize: {fmt_size(file_data['size'])}\n\nSource file path not available for preview.")

    def _new_folder(self):
        result = NewFolderDialog.ask(self)
        if result:
            self.folders.append(result)
            self.toast_mgr.show("Folder Created", f"\"{result['name']}\" is ready.", "success")
            self._render()

    def _rename_folder(self, folder_id):
        folder = next((f for f in self.folders if f["id"] == folder_id), None)
        if not folder: return
        new_name = RenameDialog.ask(self, folder["name"], "New folder name:")
        if new_name:
            folder["name"] = new_name
            self._render()

    def _delete_folder(self, folder_id):
        folder = next((f for f in self.folders if f["id"] == folder_id), None)
        if not folder: return
        fc = len([f for f in self.files if f["folder_id"] == folder_id])
        msg = f"Delete folder \"{folder['name']}\"?"
        if fc:
            msg += f"\nThis will also remove {fc} file record(s)."
        if messagebox.askyesno("Delete Folder", msg):
            self.folders = [f for f in self.folders if f["id"] != folder_id]
            self.files   = [f for f in self.files   if f["folder_id"] != folder_id]
            if self._open_fid == folder_id:
                self._go_back()
            else:
                self._render()


# ─── Notifications Tab ────────────────────────────────────────────────────────
class NotificationsTab(tk.Frame):
    def __init__(self, parent, toast_mgr, app):
        super().__init__(parent, bg=BG)
        self.toast_mgr = toast_mgr
        self.app = app
        self._build()

    def _build(self):
        # Left: trigger buttons  |  Right: history
        panes = tk.Frame(self, bg=BG)
        panes.pack(fill="both", expand=True, padx=16, pady=12)

        left = tk.Frame(panes, bg=BG, width=320)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        right_outer = tk.Frame(panes, bg=BG)
        right_outer.pack(side="left", fill="both", expand=True)

        self._build_triggers(left)
        self._build_history(right_outer)

    def _build_triggers(self, parent):
        scroll = ScrollFrame(parent, bg=BG)
        scroll.pack(fill="both", expand=True)
        inner = scroll.inner

        def section(title, color, items):
            hdr = tk.Frame(inner, bg=SURFACE,
                           highlightthickness=1, highlightbackground=BORDER)
            hdr.pack(fill="x", pady=(6, 0))
            tk.Label(hdr, text=title, font=("Segoe UI", 8, "bold"),
                     bg=SURFACE, fg=color, anchor="w").pack(fill="x", padx=12, pady=6)
            body = tk.Frame(inner, bg=BG)
            body.pack(fill="x", pady=(0, 6))
            for lbl, ntype, data in items:
                self._trig_btn(body, lbl, ntype, data)

        section("✓  SUCCESS", SUCCESS, [
            ("Note Saved Successfully", "success",
             {"title": "Note Saved Successfully", "body": "Study notes for Chapter 7 saved."}),
            ("Assignment Submitted", "success",
             {"title": "Assignment Submitted", "body": "Physics assignment submitted at 11:45 PM."}),
            ("Password Added", "success",
             {"title": "Password Added", "body": "Credential for 'College Portal' saved."}),
            ("Show as Modal ⊞", "success",
             {"title": "File Uploaded ✅", "body": "Document saved to Assignments folder.", "_modal": True}),
        ])
        section("✕  ERROR", ERROR, [
            ("Invalid Login Credentials", "error",
             {"title": "Invalid Login Credentials", "body": "Check your username and password."}),
            ("Failed to Save Data", "error",
             {"title": "Failed to Save", "body": "Network timeout. Changes not saved."}),
            ("Show as Modal ⊞", "error",
             {"title": "Login Failed", "body": "Invalid credentials. Reset your password.", "_modal": True}),
        ])
        section("⚠  WARNING", WARNING, [
            ("Assignment Due Tomorrow", "warning",
             {"title": "Assignment Due Tomorrow", "body": "Maths Assignment 3 due at 11:59 PM."}),
            ("Exam in 2 Days", "warning",
             {"title": "Exam in 2 Days", "body": "Physics Unit Test — Thursday 9 AM."}),
            ("Show as Modal ⊞", "warning",
             {"title": "Deadline in 2 Hours!", "body": "Submit your assignment before 6 PM.", "_modal": True}),
        ])
        section("ℹ  INFO", INFO, [
            ("New Update Available", "info",
             {"title": "New Update Available", "body": "v2.4.1 — improved timetable sync."}),
            ("Timetable Updated", "info",
             {"title": "Timetable Updated", "body": "Wednesday's lab moved to Room 204."}),
        ])
        section("🔔  REMINDERS", WARNING, [
            ("Good Morning! 3 Classes", "reminder",
             {"title": "Good Morning! ☀️", "body": "3 classes today. First at 9:00 AM."}),
            ("Deadline in 4 Hours", "deadline",
             {"title": "Deadline in 4 Hours ⏰", "body": "Network Security — submit before 6 PM."}),
            ("AFCAT Session at 6 PM", "reminder",
             {"title": "AFCAT Study Session 📚", "body": "Study session at 6 PM tonight."}),
            ("Log Your Mood", "reminder",
             {"title": "Log Your Mood 💭", "body": "You haven't logged your mood today."}),
        ])
        section("🎉  SPECIAL", BIRTHDAY, [
            ("Birthday — Priya 🎂", "birthday",
             {"title": "Today is Priya's Birthday 🎂", "body": "Don't forget to wish her!", "_modal": True}),
            ("Exam Alert — AFCAT", "exam",
             {"title": "Exam Starting Soon 📝", "body": "AFCAT mock test in 30 minutes!"}),
        ])
        section("⚡  QUICK FIRE", ACCENT, [
            ("Fire 5 Random Notifications", "info",
             {"_random5": True}),
        ])

    def _trig_btn(self, parent, label, ntype, data):
        cfg = TYPE_CFG.get(ntype, TYPE_CFG["info"])

        def fire(d=data):
            if d.get("_random5"):
                import random
                picks = random.sample(DEMO_NOTIFS, 5)
                for i, n in enumerate(picks):
                    self.after(i * 600, lambda nd=n: self.app._add_notif(nd, toast=True))
                return
            nd = {k: v for k, v in d.items() if not k.startswith("_")}
            nd["type"] = ntype
            modal = d.get("_modal", False)
            self.app._add_notif(nd, toast=True, modal=modal)

        frm = tk.Frame(parent, bg=BG)
        frm.pack(fill="x", padx=6, pady=2)

        def on_enter(e):
            btn.config(bg=cfg["bg"], fg=cfg["color"],
                       highlightbackground=cfg["color"])

        def on_leave(e):
            btn.config(bg=BG, fg=MUTED, highlightbackground=BORDER)

        btn = tk.Button(frm, text=f"{cfg['icon']}  {label}",
                        font=("Segoe UI", 9), bg=BG, fg=MUTED,
                        relief="flat", anchor="w", padx=10, pady=6,
                        cursor="hand2", highlightthickness=1,
                        highlightbackground=BORDER,
                        command=fire)
        btn.pack(fill="x")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _build_history(self, parent):
        hdr = tk.Frame(parent, bg=BG)
        hdr.pack(fill="x", pady=(0, 8))

        tk.Label(hdr, text="Notification History", font=("Segoe UI", 12, "bold"),
                 bg=BG, fg=TEXT).pack(side="left")

        tk.Button(hdr, text="Mark all read", font=("Segoe UI", 8, "bold"),
                  bg=BG, fg=ACCENT, relief="flat", cursor="hand2",
                  command=self.app._mark_all_read).pack(side="right", padx=4)
        tk.Button(hdr, text="Clear all", font=("Segoe UI", 8, "bold"),
                  bg=BG, fg=ERROR, relief="flat", cursor="hand2",
                  command=self.app._clear_all_notifs).pack(side="right", padx=4)

        self.history_scroll = ScrollFrame(parent, bg=BG)
        self.history_scroll.pack(fill="both", expand=True)
        self.history_inner = self.history_scroll.inner

    def refresh_history(self, notifs):
        for w in self.history_inner.winfo_children():
            w.destroy()

        if not notifs:
            tk.Label(self.history_inner, text="🎉  All caught up! No notifications.",
                     font=("Segoe UI", 10), bg=BG, fg=MUTED).pack(pady=30)
            return

        for n in notifs:
            self._history_item(self.history_inner, n)

    def _history_item(self, parent, n):
        cfg = TYPE_CFG.get(n["type"], TYPE_CFG["info"])
        frm = tk.Frame(parent, bg=CARD if not n["read"] else SURFACE,
                       highlightthickness=1, highlightbackground=BORDER)
        frm.pack(fill="x", pady=2)

        # Color strip
        strip = tk.Frame(frm, bg=cfg["color"], width=4)
        strip.pack(side="left", fill="y")

        # Icon
        tk.Label(frm, text=cfg["icon"], font=("Segoe UI Emoji", 14),
                 bg=cfg["bg"], fg=cfg["color"], width=3, pady=10).pack(side="left")

        # Text
        txt = tk.Frame(frm, bg=frm["bg"])
        txt.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        title_row = tk.Frame(txt, bg=frm["bg"])
        title_row.pack(fill="x")
        if not n["read"]:
            tk.Label(title_row, text="●", font=("Segoe UI", 8),
                     bg=frm["bg"], fg=cfg["color"]).pack(side="left")
        tk.Label(title_row, text=n["title"], font=("Segoe UI", 10, "bold"),
                 bg=frm["bg"], fg=TEXT).pack(side="left")

        tk.Label(txt, text=n["body"], font=("Segoe UI", 9),
                 bg=frm["bg"], fg=MUTED, anchor="w", wraplength=380).pack(fill="x")
        tk.Label(txt, text=n["time"], font=("Segoe UI", 7),
                 bg=frm["bg"], fg=MUTED, anchor="w").pack(fill="x")

        # Actions
        acts = tk.Frame(frm, bg=frm["bg"])
        acts.pack(side="right", padx=8)
        if not n["read"]:
            tk.Button(acts, text="✓", font=("Segoe UI", 8), bg=HOVER, fg=MUTED,
                      relief="flat", padx=4, pady=2, cursor="hand2",
                      command=lambda nid=n["id"]: self.app._mark_read(nid)).pack(pady=2)
        tk.Button(acts, text="✕", font=("Segoe UI", 8), bg=HOVER, fg=ERROR,
                  relief="flat", padx=4, pady=2, cursor="hand2",
                  command=lambda nid=n["id"]: self.app._delete_notif(nid)).pack(pady=2)


# ─── Modal Alert Window ───────────────────────────────────────────────────────
class ModalAlert(CenteredDialog):
    def __init__(self, parent, notif):
        cfg = TYPE_CFG.get(notif["type"], TYPE_CFG["info"])
        super().__init__(parent, cfg["label"], 400, 280)
        self.configure(bg=SURFACE)

        tk.Label(self, text=cfg["icon"], font=("Segoe UI Emoji", 36),
                 bg=cfg["bg"], fg=cfg["color"],
                 width=4, pady=12).pack(pady=(24, 8))
        tk.Label(self, text=cfg["label"].upper(), font=("Segoe UI", 8, "bold"),
                 bg=SURFACE, fg=cfg["color"], letterSpacing=2).pack()
        tk.Label(self, text=notif["title"], font=("Segoe UI", 13, "bold"),
                 bg=SURFACE, fg=TEXT).pack(pady=(6, 4))
        tk.Label(self, text=notif["body"], font=("Segoe UI", 10),
                 bg=SURFACE, fg=MUTED, wraplength=340).pack()
        tk.Button(self, text="Got it", font=("Segoe UI", 10, "bold"),
                  bg=cfg["color"], fg="#fff", relief="flat",
                  padx=28, pady=8, cursor="hand2",
                  command=self.destroy).pack(pady=20)


# ─── Main Application Window ──────────────────────────────────────────────────
class PocketHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PocketHub — Files · Folders · Notifications")
        self.configure(bg=BG)
        self.geometry("1100x720")
        self.minsize(900, 600)

        self._notifs = []
        self._stats  = {"total": 0, "success": 0, "error": 0, "warning": 0}

        self.toast_mgr = ToastManager(self)
        self._build_ui()

    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self, bg=SURFACE, height=58,
                       highlightthickness=1, highlightbackground=BORDER)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        # Logo
        logo_frm = tk.Frame(hdr, bg=SURFACE)
        logo_frm.pack(side="left", padx=16, pady=8)
        tk.Label(logo_frm, text="🗂", font=("Segoe UI Emoji", 18),
                 bg=ACCENT, padx=6, pady=4).pack(side="left")
        t = tk.Frame(logo_frm, bg=SURFACE)
        t.pack(side="left", padx=8)
        tk.Label(t, text="PocketHub", font=("Segoe UI", 13, "bold"),
                 bg=SURFACE, fg=TEXT).pack(anchor="w")
        tk.Label(t, text="Files · Folders · Notifications", font=("Segoe UI", 7),
                 bg=SURFACE, fg=MUTED).pack(anchor="w")

        # Tab buttons
        self._tab_var = tk.StringVar(value="folders")
        tab_frm = tk.Frame(hdr, bg=CARD,
                           highlightthickness=1, highlightbackground=BORDER)
        tab_frm.pack(side="left", padx=20, pady=10)
        for tid, tlbl in [("folders", "📁  File Pockets"), ("notifications", "🔔  Notifications")]:
            b = tk.Button(tab_frm, text=tlbl, font=("Segoe UI", 9, "bold"),
                          relief="flat", padx=14, pady=6, cursor="hand2",
                          command=lambda t=tid: self._switch_tab(t))
            b.pack(side="left", padx=2, pady=2)
            b.config(bg=ACCENT if tid == "folders" else CARD,
                     fg="#fff" if tid == "folders" else MUTED)
            setattr(self, f"_tab_btn_{tid}", b)

        # Stats bar (right)
        stats_frm = tk.Frame(hdr, bg=SURFACE)
        stats_frm.pack(side="right", padx=16)
        self._stat_labels = {}
        for key, icon, color in [("total","📊",ACCENT),("success","✓",SUCCESS),
                                  ("error","✕",ERROR),("warning","⚠",WARNING)]:
            sf = tk.Frame(stats_frm, bg=SURFACE)
            sf.pack(side="left", padx=8, pady=4)
            tk.Label(sf, text=icon, font=("Segoe UI Emoji", 9), bg=SURFACE, fg=color).pack(side="left")
            lbl = tk.Label(sf, text="0", font=("Segoe UI", 11, "bold"), bg=SURFACE, fg=color)
            lbl.pack(side="left", padx=2)
            self._stat_labels[key] = lbl

        # Bell
        self._bell_btn = tk.Button(hdr, text="🔔", font=("Segoe UI Emoji", 14),
                                   bg=SURFACE, fg=TEXT, relief="flat",
                                   padx=8, pady=4, cursor="hand2",
                                   command=self._toggle_bell_panel)
        self._bell_btn.pack(side="right", padx=4, pady=8)
        self._unread_badge = tk.Label(hdr, text="", font=("Segoe UI", 7, "bold"),
                                      bg=ERROR, fg="#fff",
                                      padx=4, pady=1)

        # ── Content area ──
        self._content = tk.Frame(self, bg=BG)
        self._content.pack(fill="both", expand=True)

        self._folders_tab = FolderPocketsTab(self._content, self.toast_mgr, self)
        self._notifs_tab  = NotificationsTab(self._content, self.toast_mgr, self)

        self._current_tab = "folders"
        self._folders_tab.pack(fill="both", expand=True)

        # Bell panel (hidden by default)
        self._bell_panel_visible = False
        self._bell_panel = self._create_bell_panel()

    def _switch_tab(self, tab_id):
        if tab_id == self._current_tab:
            return
        self._current_tab = tab_id
        for tid in ["folders", "notifications"]:
            btn = getattr(self, f"_tab_btn_{tid}")
            btn.config(bg=ACCENT if tid == tab_id else CARD,
                       fg="#fff" if tid == tab_id else MUTED)
        self._folders_tab.pack_forget()
        self._notifs_tab.pack_forget()
        if tab_id == "folders":
            self._folders_tab.pack(fill="both", expand=True)
        else:
            self._notifs_tab.pack(fill="both", expand=True)
            self._notifs_tab.refresh_history(self._notifs)

    def _create_bell_panel(self):
        panel = tk.Toplevel(self)
        panel.withdraw()
        panel.overrideredirect(True)
        panel.attributes("-topmost", True)
        panel.configure(bg=SURFACE)
        panel.resizable(False, False)

        hdr = tk.Frame(panel, bg=SURFACE)
        hdr.pack(fill="x", padx=12, pady=(12, 6))
        tk.Label(hdr, text="Notifications", font=("Segoe UI", 11, "bold"),
                 bg=SURFACE, fg=TEXT).pack(side="left")
        tk.Button(hdr, text="✕", font=("Segoe UI", 9), bg=SURFACE, fg=MUTED,
                  relief="flat", cursor="hand2",
                  command=self._toggle_bell_panel).pack(side="right")

        action_row = tk.Frame(panel, bg=SURFACE)
        action_row.pack(fill="x", padx=12, pady=(0, 6))
        tk.Button(action_row, text="Mark all read", font=("Segoe UI", 8, "bold"),
                  bg=SURFACE, fg=ACCENT, relief="flat", cursor="hand2",
                  command=self._mark_all_read).pack(side="left")
        tk.Button(action_row, text="Clear all", font=("Segoe UI", 8, "bold"),
                  bg=SURFACE, fg=ERROR, relief="flat", cursor="hand2",
                  command=self._clear_all_notifs).pack(side="right")

        sep = tk.Frame(panel, bg=BORDER, height=1)
        sep.pack(fill="x")

        self._bell_scroll = ScrollFrame(panel, bg=SURFACE)
        self._bell_scroll.pack(fill="both", expand=True)
        panel.geometry("320x480")

        # Close when clicking outside
        panel.bind("<FocusOut>", lambda e: None)
        return panel

    def _toggle_bell_panel(self):
        if self._bell_panel_visible:
            self._bell_panel.withdraw()
            self._bell_panel_visible = False
        else:
            self._refresh_bell_panel()
            bx = self._bell_btn.winfo_rootx()
            by = self._bell_btn.winfo_rooty() + self._bell_btn.winfo_height() + 4
            self._bell_panel.geometry(f"320x480+{bx - 270}+{by}")
            self._bell_panel.deiconify()
            self._bell_panel.lift()
            self._bell_panel_visible = True

    def _refresh_bell_panel(self):
        for w in self._bell_scroll.inner.winfo_children():
            w.destroy()
        if not self._notifs:
            tk.Label(self._bell_scroll.inner, text="🎉 All caught up!",
                     font=("Segoe UI", 10), bg=SURFACE, fg=MUTED).pack(pady=20)
            return
        for n in self._notifs[:20]:
            self._bell_item(self._bell_scroll.inner, n)

    def _bell_item(self, parent, n):
        cfg = TYPE_CFG.get(n["type"], TYPE_CFG["info"])
        frm = tk.Frame(parent, bg=CARD if not n["read"] else SURFACE,
                       highlightthickness=1, highlightbackground=BORDER)
        frm.pack(fill="x", pady=1, padx=4)
        tk.Label(frm, text=cfg["icon"], font=("Segoe UI Emoji", 12),
                 bg=cfg["bg"], fg=cfg["color"], width=3, pady=8).pack(side="left")
        txt = tk.Frame(frm, bg=frm["bg"])
        txt.pack(side="left", fill="both", expand=True, padx=8, pady=6)
        row = tk.Frame(txt, bg=frm["bg"])
        row.pack(fill="x")
        if not n["read"]:
            tk.Label(row, text="●", font=("Segoe UI", 7),
                     bg=frm["bg"], fg=cfg["color"]).pack(side="left")
        tk.Label(row, text=n["title"], font=("Segoe UI", 9, "bold"),
                 bg=frm["bg"], fg=TEXT).pack(side="left")
        tk.Label(txt, text=n["body"], font=("Segoe UI", 8),
                 bg=frm["bg"], fg=MUTED, anchor="w", wraplength=200).pack(fill="x")
        acts = tk.Frame(frm, bg=frm["bg"])
        acts.pack(side="right", padx=4)
        if not n["read"]:
            tk.Button(acts, text="✓", font=("Segoe UI", 7), bg=HOVER, fg=MUTED,
                      relief="flat", padx=3, cursor="hand2",
                      command=lambda nid=n["id"]: self._mark_read(nid)).pack(pady=1)
        tk.Button(acts, text="✕", font=("Segoe UI", 7), bg=HOVER, fg=ERROR,
                  relief="flat", padx=3, cursor="hand2",
                  command=lambda nid=n["id"]: self._delete_notif(nid)).pack(pady=1)

    # ── Notification management ──
    def _add_notif(self, data, toast=True, modal=False):
        n = {**data, "id": make_id(), "read": False, "time": now_str()}
        self._notifs.insert(0, n)
        self._stats["total"] += 1
        if n["type"] == "success":  self._stats["success"] += 1
        if n["type"] == "error":    self._stats["error"]   += 1
        if n["type"] in ("warning", "deadline", "exam"): self._stats["warning"] += 1
        self._update_stats_ui()
        if toast:
            self.toast_mgr.show(n["title"], n["body"], n["type"])
        if modal:
            ModalAlert(self, n)
        if self._bell_panel_visible:
            self._refresh_bell_panel()
        if self._current_tab == "notifications":
            self._notifs_tab.refresh_history(self._notifs)

    def _mark_read(self, nid):
        for n in self._notifs:
            if n["id"] == nid:
                n["read"] = True
        self._update_stats_ui()
        if self._bell_panel_visible: self._refresh_bell_panel()
        if self._current_tab == "notifications": self._notifs_tab.refresh_history(self._notifs)

    def _mark_all_read(self):
        for n in self._notifs:
            n["read"] = True
        self._update_stats_ui()
        if self._bell_panel_visible: self._refresh_bell_panel()
        if self._current_tab == "notifications": self._notifs_tab.refresh_history(self._notifs)

    def _delete_notif(self, nid):
        self._notifs = [n for n in self._notifs if n["id"] != nid]
        if self._bell_panel_visible: self._refresh_bell_panel()
        if self._current_tab == "notifications": self._notifs_tab.refresh_history(self._notifs)

    def _clear_all_notifs(self):
        self._notifs.clear()
        self._stats = {"total": 0, "success": 0, "error": 0, "warning": 0}
        self._update_stats_ui()
        if self._bell_panel_visible: self._refresh_bell_panel()
        if self._current_tab == "notifications": self._notifs_tab.refresh_history(self._notifs)

    def _update_stats_ui(self):
        unread = sum(1 for n in self._notifs if not n["read"])
        for key, lbl in self._stat_labels.items():
            lbl.config(text=str(self._stats[key]))
        # Badge
        if unread > 0:
            self._unread_badge.config(text=str(unread) if unread < 100 else "99+")
            # Position badge near bell
            self._unread_badge.place(in_=self._bell_btn, relx=0.75, rely=0, anchor="nw")
            self._unread_badge.lift()
        else:
            self._unread_badge.place_forget()


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = PocketHubApp()
    app.mainloop()
