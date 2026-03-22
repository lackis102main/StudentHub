import json
import os
import datetime
import customtkinter as ctk
from tkinter import messagebox

FILE = "tasks.json"

# ─────────────────────────────────────────────
# Theme
# ─────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "bg":           "#0a0f1e",
    "surface":      "#111827",
    "card":         "#1a2236",
    "card_hover":   "#1f2d45",
    "border":       "#1e3a5f",
    "accent":       "#3b82f6",
    "accent_dark":  "#1d4ed8",
    "accent_glow":  "#60a5fa",
    "success":      "#10b981",
    "success_dark": "#059669",
    "danger":       "#ef4444",
    "warning":      "#f59e0b",
    "warning_dark": "#b45309",
    "text":         "#f1f5f9",
    "text_muted":   "#64748b",
    "text_dim":     "#94a3b8",
    "badge_work":   "#7c3aed",
    "badge_study":  "#0891b2",
    "badge_other":  "#475569",
    "done_bg":      "#052e16",
    "done_text":    "#6ee7b7",
    "notif_bg":     "#1e2d45",
    "notif_border": "#f59e0b",
    "notif_urgent": "#ef4444",
}

FONTS = {
    "title":    ("Segoe UI", 26, "bold"),
    "subtitle": ("Segoe UI", 11),
    "label":    ("Segoe UI", 12, "bold"),
    "body":     ("Segoe UI", 12),
    "small":    ("Segoe UI", 10),
    "badge":    ("Segoe UI", 9, "bold"),
    "mono":     ("Consolas", 11),
    "notif_title": ("Segoe UI", 11, "bold"),
    "notif_body":  ("Segoe UI", 10),
}

# ─────────────────────────────────────────────
# File I/O
# ─────────────────────────────────────────────
def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# ─────────────────────────────────────────────
# Toast Notification Window
# ─────────────────────────────────────────────
class ToastNotification(ctk.CTkToplevel):
    """A small pop-up toast that appears in the bottom-right and auto-dismisses."""

    def __init__(self, parent, title, message, urgent=False, duration=5000):
        super().__init__(parent)
        self.overrideredirect(True)          # no title bar
        self.attributes("-topmost", True)
        self.configure(fg_color=COLORS["bg"])

        border_color = COLORS["notif_urgent"] if urgent else COLORS["notif_border"]

        outer = ctk.CTkFrame(
            self,
            fg_color=COLORS["notif_bg"],
            corner_radius=12,
            border_width=2,
            border_color=border_color,
        )
        outer.pack(padx=2, pady=2)

        # Icon + title row
        top_row = ctk.CTkFrame(outer, fg_color="transparent")
        top_row.pack(fill="x", padx=14, pady=(12, 4))

        icon = "🔴" if urgent else "🔔"
        ctk.CTkLabel(
            top_row, text=icon,
            font=("Segoe UI", 14), text_color=border_color,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            top_row, text=title,
            font=FONTS["notif_title"], text_color=COLORS["text"],
        ).pack(side="left")

        # Close button
        ctk.CTkButton(
            top_row, text="✕", width=22, height=22,
            fg_color="transparent", hover_color=COLORS["card_hover"],
            text_color=COLORS["text_muted"], font=FONTS["small"],
            command=self.dismiss,
        ).pack(side="right")

        # Message
        ctk.CTkLabel(
            outer, text=message,
            font=FONTS["notif_body"], text_color=COLORS["text_dim"],
            wraplength=260, justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 12))

        # Position: bottom-right of screen
        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = sw - w - 24
        y = sh - h - 60
        self.geometry(f"+{x}+{y}")

        # Auto-dismiss
        self._job = self.after(duration, self.dismiss)

    def dismiss(self):
        try:
            self.after_cancel(self._job)
        except Exception:
            pass
        self.destroy()


# ─────────────────────────────────────────────
# App
# ─────────────────────────────────────────────
class StudentHub(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StudentHub")
        self.geometry("780x680")
        self.minsize(700, 560)
        self.configure(fg_color=COLORS["bg"])

        self._active_filter = None   # None = All
        self._task_cards = []
        self._notified_ids = set()   # track already-shown notifications

        self._build_ui()
        self.refresh_tasks()

        # Start notification loop (checks every 60 s)
        self._check_notifications()

    # ── Notification logic ────────────────────
    def _check_notifications(self):
        """Called periodically; shows toasts for tasks due today or tomorrow."""
        tasks = load_tasks()
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        for i, task in enumerate(tasks):
            if task["done"] or not task.get("deadline"):
                continue

            try:
                dl = datetime.date.fromisoformat(task["deadline"])
            except ValueError:
                continue

            days_left = (dl - today).days

            if days_left < 0:
                # Overdue — always show (use index as id so it reappears on restart)
                uid = f"overdue-{i}-{task['deadline']}"
                if uid not in self._notified_ids:
                    self._notified_ids.add(uid)
                    self._show_toast(
                        "Overdue Task ⚠️",
                        f"\"{task['title']}\" was due on {task['deadline']}",
                        urgent=True,
                    )
            elif days_left == 0:
                uid = f"today-{i}-{task['deadline']}"
                if uid not in self._notified_ids:
                    self._notified_ids.add(uid)
                    self._show_toast(
                        "Due Today!",
                        f"\"{task['title']}\" is due today.",
                        urgent=True,
                    )
            elif days_left == 1:
                uid = f"tomorrow-{i}-{task['deadline']}"
                if uid not in self._notified_ids:
                    self._notified_ids.add(uid)
                    self._show_toast(
                        "Due Tomorrow",
                        f"\"{task['title']}\" is due tomorrow.",
                        urgent=False,
                    )

        # Repeat every 60 seconds
        self.after(60_000, self._check_notifications)

    def _show_toast(self, title, message, urgent=False):
        """Queue toasts with a small vertical offset so they stack."""
        try:
            toast = ToastNotification(self, title, message, urgent=urgent)
            # Stack multiple toasts: shift upward by prior toasts
            existing = [
                w for w in self.winfo_children()
                if isinstance(w, ToastNotification) and w.winfo_exists()
            ]
            if len(existing) > 1:
                toast.update_idletasks()
                h = toast.winfo_reqheight()
                x_str = toast.geometry().split("+")[1]
                y_str = toast.geometry().split("+")[2]
                new_y = int(y_str) - (len(existing) - 1) * (h + 8)
                toast.geometry(f"+{x_str}+{new_y}")
        except Exception:
            pass

    # ── Layout ────────────────────────────────
    def _build_ui(self):
        # ── Header ────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(28, 0))

        title_col = ctk.CTkFrame(header, fg_color="transparent")
        title_col.pack(side="left")

        ctk.CTkLabel(
            title_col, text="StudentHub",
            font=FONTS["title"], text_color=COLORS["text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_col, text="Your academic task dashboard",
            font=FONTS["subtitle"], text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        # Bell button (manual notification check)
        self._notif_btn = ctk.CTkButton(
            header,
            text="🔔",
            width=38, height=38,
            corner_radius=19,
            fg_color=COLORS["card"],
            hover_color=COLORS["card_hover"],
            font=("Segoe UI", 16),
            command=self._manual_notify_check,
        )
        self._notif_btn.pack(side="right", padx=(8, 0))

        self.stats_label = ctk.CTkLabel(
            header, text="",
            font=FONTS["small"], text_color=COLORS["text_muted"]
        )
        self.stats_label.pack(side="right", anchor="e")

        # ── Divider ───────────────────────────
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]
        ).pack(fill="x", padx=30, pady=18)

        # ── Add Task Card ─────────────────────
        add_card = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=14,
            border_width=1, border_color=COLORS["border"]
        )
        add_card.pack(fill="x", padx=30, pady=(0, 16))

        ctk.CTkLabel(
            add_card, text="New Task",
            font=FONTS["label"], text_color=COLORS["accent_glow"]
        ).pack(anchor="w", padx=20, pady=(16, 8))

        fields_row = ctk.CTkFrame(add_card, fg_color="transparent")
        fields_row.pack(fill="x", padx=20, pady=(0, 16))

        self.title_entry = self._styled_entry(fields_row, "Task name", width=240)
        self.title_entry.pack(side="left", padx=(0, 8))

        self.type_entry = self._styled_entry(fields_row, "Type  (exam / homework…)", width=180)
        self.type_entry.pack(side="left", padx=(0, 8))

        self.deadline_entry = self._styled_entry(fields_row, "Deadline  YYYY-MM-DD", width=160)
        self.deadline_entry.pack(side="left", padx=(0, 8))

        self._make_btn(
            fields_row, "＋  Add", self._add_task,
            fg=COLORS["accent"], hover=COLORS["accent_dark"], width=90
        ).pack(side="left")

        # ── Filter Row ────────────────────────
        self._filter_row = ctk.CTkFrame(self, fg_color="transparent")
        self._filter_row.pack(fill="x", padx=30, pady=(0, 14))

        ctk.CTkLabel(
            self._filter_row, text="Filter:",
            font=FONTS["small"], text_color=COLORS["text_muted"]
        ).pack(side="left", padx=(0, 8))

        # "All" pill button
        self._all_btn = ctk.CTkButton(
            self._filter_row,
            text="All",
            width=52, height=28,
            corner_radius=20,
            fg_color=COLORS["accent"],       # starts active
            hover_color=COLORS["accent_dark"],
            text_color=COLORS["text"],
            font=FONTS["small"],
            command=self._reset_filter,
        )
        self._all_btn.pack(side="left", padx=(0, 10))

        # Separator label
        ctk.CTkLabel(
            self._filter_row, text="or type a type:",
            font=FONTS["small"], text_color=COLORS["text_muted"]
        ).pack(side="left", padx=(0, 6))

        # Live-filter text entry
        self._filter_var = ctk.StringVar()
        self._filter_var.trace_add("write", self._on_filter_type)

        self._type_filter_entry = ctk.CTkEntry(
            self._filter_row,
            width=160, height=28,
            placeholder_text="e.g. exam, homework…",
            placeholder_text_color=COLORS["text_muted"],
            fg_color=COLORS["card"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text"],
            corner_radius=20,
            font=FONTS["small"],
            textvariable=self._filter_var,
        )
        self._type_filter_entry.pack(side="left")

        # Active-filter badge (hidden when filter is None)
        self._active_badge = ctk.CTkLabel(
            self._filter_row, text="",
            font=FONTS["badge"],
            fg_color=COLORS["accent_dark"],
            corner_radius=10,
            text_color=COLORS["text"],
            width=0, height=22,
        )
        # packed only when needed

        # ── Task List Area ────────────────────
        list_frame = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=14,
            border_width=1, border_color=COLORS["border"]
        )
        list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        list_header = ctk.CTkFrame(list_frame, fg_color="transparent")
        list_header.pack(fill="x", padx=18, pady=(14, 0))

        ctk.CTkLabel(
            list_header, text="Tasks",
            font=FONTS["label"], text_color=COLORS["text"]
        ).pack(side="left")

        self.count_label = ctk.CTkLabel(
            list_header, text="",
            font=FONTS["small"], text_color=COLORS["text_muted"]
        )
        self.count_label.pack(side="right")

        ctk.CTkFrame(list_frame, height=1, fg_color=COLORS["border"]
        ).pack(fill="x", padx=18, pady=10)

        self.scroll = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent"],
        )
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 12))

    # ── Filter callbacks ──────────────────────
    def _on_filter_type(self, *_):
        """Called on every keystroke in the type-filter entry."""
        typed = self._filter_var.get().strip().lower()
        if typed:
            self._active_filter = typed
            # Deactivate "All" button visually
            self._all_btn.configure(
                fg_color=COLORS["card"],
                text_color=COLORS["text_dim"],
            )
        else:
            self._active_filter = None
            self._all_btn.configure(
                fg_color=COLORS["accent"],
                text_color=COLORS["text"],
            )
        self._render_tasks()

    def _reset_filter(self):
        """All button pressed — clear filter and entry."""
        self._active_filter = None
        self._filter_var.set("")          # clears the entry (triggers _on_filter_type)
        self._all_btn.configure(
            fg_color=COLORS["accent"],
            text_color=COLORS["text"],
        )

    def _manual_notify_check(self):
        """Bell button: reset notified set and re-check so user can see them again."""
        self._notified_ids.clear()
        self._check_notifications()
        self._show_toast("Notifications", "Checked for upcoming deadlines.", urgent=False)

    # ── Widget helpers ─────────────────────────
    def _styled_entry(self, parent, placeholder, width=180):
        return ctk.CTkEntry(
            parent,
            width=width, height=36,
            placeholder_text=placeholder,
            placeholder_text_color=COLORS["text_muted"],
            fg_color=COLORS["card"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text"],
            corner_radius=8,
            font=FONTS["body"],
        )

    def _make_btn(self, parent, text, cmd, fg, hover, width=120, height=36):
        return ctk.CTkButton(
            parent, text=text, command=cmd,
            width=width, height=height,
            fg_color=fg, hover_color=hover,
            text_color=COLORS["text"],
            corner_radius=8, font=FONTS["body"],
        )

    # ── Task card ─────────────────────────────
    def _build_task_card(self, parent, idx, task):
        done = task["done"]
        card_bg  = COLORS["done_bg"] if done else COLORS["card"]

        # Deadline urgency colour for border
        border_col = COLORS["success_dark"] if done else self._deadline_color(task)

        card = ctk.CTkFrame(
            parent, fg_color=card_bg, corner_radius=10,
            border_width=1, border_color=border_col,
        )
        card.pack(fill="x", pady=4, padx=4)
        card.columnconfigure(1, weight=1)

        # Status dot
        dot_color = COLORS["success"] if done else self._deadline_color(task)
        ctk.CTkFrame(
            card, width=10, height=10,
            corner_radius=5, fg_color=dot_color
        ).grid(row=0, column=0, padx=(14, 10), pady=16, sticky="ns")

        # Title
        ctk.CTkLabel(
            card,
            text=("✓  " if done else "") + task["title"],
            font=FONTS["body"],
            text_color=COLORS["done_text"] if done else COLORS["text"],
            anchor="w",
        ).grid(row=0, column=1, sticky="w", pady=10)

        # Right-side info row
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.grid(row=0, column=2, padx=10, sticky="e")

        # Type badge (dynamic colour)
        badge_color = self._type_badge_color(task.get("type", "other"))
        ctk.CTkLabel(
            info,
            text=(task.get("type") or "other").upper(),
            font=FONTS["badge"], text_color="#ffffff",
            fg_color=badge_color, corner_radius=4,
            width=54, height=20,
        ).pack(side="left", padx=4)

        # Deadline with urgency label
        dl_text, dl_color = self._deadline_display(task)
        ctk.CTkLabel(
            info, text=dl_text,
            font=FONTS["mono"], text_color=dl_color,
        ).pack(side="left", padx=(6, 6))

        if not done:
            self._make_btn(
                info, "Done", lambda i=idx: self._complete_task(i),
                fg=COLORS["success"], hover=COLORS["success_dark"],
                width=62, height=28
            ).pack(side="left", padx=2)

        self._make_btn(
            info, "✕", lambda i=idx: self._delete_task(i),
            fg=COLORS["card_hover"], hover=COLORS["danger"],
            width=32, height=28
        ).pack(side="left", padx=(2, 10))

    def _deadline_color(self, task):
        """Returns a colour for the dot/border based on deadline proximity."""
        if not task.get("deadline") or task["done"]:
            return COLORS["border"]
        try:
            dl = datetime.date.fromisoformat(task["deadline"])
            days = (dl - datetime.date.today()).days
            if days < 0:   return COLORS["danger"]
            if days == 0:  return COLORS["danger"]
            if days == 1:  return COLORS["warning"]
            return COLORS["accent"]
        except ValueError:
            return COLORS["border"]

    def _deadline_display(self, task):
        """Returns (text, color) for deadline label."""
        if not task.get("deadline"):
            return "No deadline", COLORS["text_muted"]
        try:
            dl = datetime.date.fromisoformat(task["deadline"])
            days = (dl - datetime.date.today()).days
            if days < 0:
                suffix = f"  ⚠ {-days}d overdue"
                color  = COLORS["danger"]
            elif days == 0:
                suffix = "  🔴 Today!"
                color  = COLORS["danger"]
            elif days == 1:
                suffix = "  🟡 Tomorrow"
                color  = COLORS["warning"]
            else:
                suffix = f"  ({days}d)"
                color  = COLORS["text_dim"]
            return f"📅 {task['deadline']}{suffix}", color
        except ValueError:
            return f"📅 {task['deadline']}", COLORS["text_dim"]

    def _type_badge_color(self, t):
        """Consistent colour per type string (hash-based for custom types)."""
        palette = [
            "#7c3aed", "#0891b2", "#059669", "#d97706",
            "#db2777", "#6366f1", "#0f766e", "#b45309",
        ]
        return palette[hash(t or "other") % len(palette)]

    # ── Logic ──────────────────────────────────
    def _add_task(self):
        title     = self.title_entry.get().strip()
        task_type = self.type_entry.get().strip().lower()
        deadline  = self.deadline_entry.get().strip()

        if not title:
            messagebox.showerror("Missing Field", "Task name is required.")
            return

        tasks = load_tasks()
        tasks.append({
            "title":    title,
            "type":     task_type or "other",
            "deadline": deadline,
            "done":     False,
        })
        save_tasks(tasks)

        self.title_entry.delete(0, "end")
        self.type_entry.delete(0, "end")
        self.deadline_entry.delete(0, "end")

        # Reset notified IDs so new tasks can trigger notifications
        self._notified_ids.clear()
        self.refresh_tasks()
        self._check_notifications()

    def _complete_task(self, idx):
        tasks = load_tasks()
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = True
            save_tasks(tasks)
            self.refresh_tasks()

    def _delete_task(self, idx):
        tasks = load_tasks()
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
            save_tasks(tasks)
            self.refresh_tasks()

    def _render_tasks(self):
        """Redraw the task list based on _active_filter."""
        for widget in self.scroll.winfo_children():
            widget.destroy()

        tasks = load_tasks()
        tasks_indexed = sorted(enumerate(tasks), key=lambda x: x[1]["deadline"] or "9999")

        ft = self._active_filter
        visible = [(i, t) for i, t in tasks_indexed
                   if not ft or t.get("type", "other").lower() == ft]

        if not visible:
            empty_msg = (
                f"No \"{ft}\" tasks found." if ft
                else "No tasks here yet — add one above ↑"
            )
            ctk.CTkLabel(
                self.scroll, text=empty_msg,
                font=FONTS["body"], text_color=COLORS["text_muted"],
            ).pack(pady=30)
        else:
            for idx, task in visible:
                self._build_task_card(self.scroll, idx, task)

        total      = len(tasks)
        done_count = sum(1 for t in tasks if t["done"])
        pending    = total - done_count

        self.count_label.configure(text=f"{len(visible)} shown")
        self.stats_label.configure(
            text=f"Total: {total}   ·   Done: {done_count}   ·   Pending: {pending}"
        )

    def refresh_tasks(self):
        self._render_tasks()


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = StudentHub()
    app.mainloop()