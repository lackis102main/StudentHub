import json
import os
import shutil
import datetime
import customtkinter as ctk
from tkinter import messagebox, filedialog


# ─────────────────────────────────────────────
# Embedded icon (base64) — no external file needed
# ─────────────────────────────────────────────
_ICON_B64 = """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"""

# ─────────────────────────────────────────────
# Internal data path  (%APPDATA%\StudentHub on Windows,
#                       ~/.local/share/StudentHub elsewhere)
# ─────────────────────────────────────────────
def _get_data_dir():
    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.join(os.path.expanduser("~"), ".local", "share")
    path = os.path.join(base, "StudentHub")
    os.makedirs(path, exist_ok=True)
    return path

DATA_DIR      = _get_data_dir()
FILE          = os.path.join(DATA_DIR, "tasks.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

# ─────────────────────────────────────────────
# Persistent settings  (theme + language)
# ─────────────────────────────────────────────
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"theme": "dark", "lang": "en"}
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"theme": "dark", "lang": "en"}

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ─────────────────────────────────────────────
# Color palettes
# ─────────────────────────────────────────────
ctk.set_default_color_theme("blue")

COLORS_DARK = {
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

COLORS_LIGHT = {
    "bg":           "#ffffff",
    "surface":      "#f1f5f9",
    "card":         "#e2e8f0",
    "card_hover":   "#cbd5e1",
    "border":       "#cbd5e1",
    "accent":       "#2563eb",
    "accent_dark":  "#1d4ed8",
    "accent_glow":  "#3b82f6",
    "success":      "#059669",
    "success_dark": "#047857",
    "danger":       "#dc2626",
    "warning":      "#d97706",
    "warning_dark": "#b45309",
    "text":         "#0f172a",
    "text_muted":   "#475569",
    "text_dim":     "#64748b",
    "badge_work":   "#7c3aed",
    "badge_study":  "#0891b2",
    "badge_other":  "#64748b",
    "done_bg":      "#dcfce7",
    "done_text":    "#166534",
    "notif_bg":     "#f8fafc",
    "notif_border": "#d97706",
    "notif_urgent": "#dc2626",
}

# COLORS is mutated in-place when the theme switches
COLORS = dict(COLORS_DARK)

FONTS = {
    "title":       ("Segoe UI", 26, "bold"),
    "subtitle":    ("Segoe UI", 11),
    "label":       ("Segoe UI", 12, "bold"),
    "body":        ("Segoe UI", 12),
    "small":       ("Segoe UI", 10),
    "badge":       ("Segoe UI", 9, "bold"),
    "mono":        ("Consolas", 11),
    "notif_title": ("Segoe UI", 11, "bold"),
    "notif_body":  ("Segoe UI", 10),
}

# ─────────────────────────────────────────────
# Translations
# ─────────────────────────────────────────────
STRINGS = {
    "en": {
        "app_title":          "StudentHub v0.4-beta",
        "subtitle":           "Your academic task dashboard",
        "new_task":           "New Task",
        "task_name":          "Task name",
        "task_type":          "Type  (exam / homework...)",
        "deadline":           "Deadline  YYYY-MM-DD",
        "add_btn":            "+  Add",
        "filter_label":       "Filter:",
        "all_btn":            "All",
        "type_hint":          "e.g. exam, homework...",
        "or_type":            "or type a type:",
        "tasks_header":       "Tasks",
        "shown":              "shown",
        "no_tasks":           "No tasks here yet -- add one above",
        "no_type_tasks":      "No \"{t}\" tasks found.",
        "done_btn":           "Done",
        "total":              "Total",
        "done_stat":          "Done",
        "pending":            "Pending",
        "missing_field":      "Missing Field",
        "task_required":      "Task name is required.",
        "notif_overdue":      "Overdue Task",
        "notif_today":        "Due Today!",
        "notif_tomorrow":     "Due Tomorrow",
        "notif_checked":      "Notifications",
        "notif_check_msg":    "Checked for upcoming deadlines.",
        "was_due":            "\"{t}\" was due on {d}",
        "due_today":          "\"{t}\" is due today.",
        "due_tomorrow":       "\"{t}\" is due tomorrow.",
        "overdue_suffix":     "{n}d overdue",
        "today_suffix":       "Today!",
        "tomorrow_suffix":    "Tomorrow",
        "no_deadline":        "No deadline",
        "backup_btn":         "Backup",
        "backup_title":       "Save Backup",
        "backup_success":     "Backup saved!",
        "backup_success_msg": "Tasks backed up to:\n{path}",
        "backup_none":        "No tasks to back up yet.",
        "backup_err":         "Backup failed:\n{err}",
        "restore_btn":        "Restore",
        "restore_title":      "Select a backup file",
        "restore_success":    "Restored!",
        "restore_success_msg":"Tasks restored from backup.",
        "restore_err":        "Restore failed:\n{err}",
        "restore_confirm":    "This will replace ALL current tasks with the backup. Continue?",
        "lang_label":         "Language:",
        "theme_label":        "Theme:",
        "theme_dark":         "Dark",
        "theme_light":        "Light",
    },
    "es": {
        "app_title":          "StudentHub v0.4-beta",
        "subtitle":           "Tu panel de tareas academicas",
        "new_task":           "Nueva Tarea",
        "task_name":          "Nombre de la tarea",
        "task_type":          "Tipo  (examen / tarea...)",
        "deadline":           "Fecha limite  YYYY-MM-DD",
        "add_btn":            "+  Anadir",
        "filter_label":       "Filtrar:",
        "all_btn":            "Todo",
        "type_hint":          "ej. examen, tarea...",
        "or_type":            "o escribe un tipo:",
        "tasks_header":       "Tareas",
        "shown":              "mostradas",
        "no_tasks":           "Aun no hay tareas -- anade una arriba",
        "no_type_tasks":      "No se encontraron tareas de \"{t}\".",
        "done_btn":           "Hecho",
        "total":              "Total",
        "done_stat":          "Hechas",
        "pending":            "Pendientes",
        "missing_field":      "Campo requerido",
        "task_required":      "El nombre de la tarea es obligatorio.",
        "notif_overdue":      "Tarea vencida",
        "notif_today":        "Vence hoy!",
        "notif_tomorrow":     "Vence manana",
        "notif_checked":      "Notificaciones",
        "notif_check_msg":    "Se comprobaron los plazos proximos.",
        "was_due":            "\"{t}\" vencio el {d}",
        "due_today":          "\"{t}\" vence hoy.",
        "due_tomorrow":       "\"{t}\" vence manana.",
        "overdue_suffix":     "{n}d de retraso",
        "today_suffix":       "Hoy!",
        "tomorrow_suffix":    "Manana",
        "no_deadline":        "Sin fecha limite",
        "backup_btn":         "Copia seg.",
        "backup_title":       "Guardar copia",
        "backup_success":     "Copia guardada!",
        "backup_success_msg": "Tareas guardadas en:\n{path}",
        "backup_none":        "Aun no hay tareas para respaldar.",
        "backup_err":         "Error al guardar:\n{err}",
        "restore_btn":        "Restaurar",
        "restore_title":      "Selecciona un archivo de copia",
        "restore_success":    "Restaurado!",
        "restore_success_msg":"Tareas restauradas desde la copia.",
        "restore_err":        "Error al restaurar:\n{err}",
        "restore_confirm":    "Esto reemplazara TODAS las tareas actuales con la copia. Continuar?",
        "lang_label":         "Idioma:",
        "theme_label":        "Tema:",
        "theme_dark":         "Oscuro",
        "theme_light":        "Claro",
    },
    "fr": {
        "app_title":          "StudentHub v0.4-beta",
        "subtitle":           "Votre tableau de bord academique",
        "new_task":           "Nouvelle tache",
        "task_name":          "Nom de la tache",
        "task_type":          "Type  (examen / devoir...)",
        "deadline":           "Echeance  YYYY-MM-DD",
        "add_btn":            "+  Ajouter",
        "filter_label":       "Filtrer:",
        "all_btn":            "Tout",
        "type_hint":          "ex. examen, devoir...",
        "or_type":            "ou tapez un type:",
        "tasks_header":       "Taches",
        "shown":              "affichees",
        "no_tasks":           "Aucune tache -- ajoutez-en une ci-dessus",
        "no_type_tasks":      "Aucune tache \"{t}\" trouvee.",
        "done_btn":           "Fait",
        "total":              "Total",
        "done_stat":          "Faites",
        "pending":            "En cours",
        "missing_field":      "Champ manquant",
        "task_required":      "Le nom de la tache est requis.",
        "notif_overdue":      "Tache en retard",
        "notif_today":        "A rendre aujourd'hui!",
        "notif_tomorrow":     "A rendre demain",
        "notif_checked":      "Notifications",
        "notif_check_msg":    "Verification des echeances effectuee.",
        "was_due":            "\"{t}\" etait du le {d}",
        "due_today":          "\"{t}\" est du aujourd'hui.",
        "due_tomorrow":       "\"{t}\" est du demain.",
        "overdue_suffix":     "{n}j de retard",
        "today_suffix":       "Aujourd'hui!",
        "tomorrow_suffix":    "Demain",
        "no_deadline":        "Pas d'echeance",
        "backup_btn":         "Sauvegarde",
        "backup_title":       "Enregistrer la sauvegarde",
        "backup_success":     "Sauvegarde enregistree!",
        "backup_success_msg": "Taches sauvegardees dans:\n{path}",
        "backup_none":        "Pas encore de taches a sauvegarder.",
        "backup_err":         "Echec de la sauvegarde:\n{err}",
        "restore_btn":        "Restaurer",
        "restore_title":      "Choisir un fichier de sauvegarde",
        "restore_success":    "Restaure!",
        "restore_success_msg":"Taches restaurees depuis la sauvegarde.",
        "restore_err":        "Echec de la restauration:\n{err}",
        "restore_confirm":    "Cela remplacera TOUTES les taches actuelles. Continuer?",
        "lang_label":         "Langue:",
        "theme_label":        "Theme:",
        "theme_dark":         "Sombre",
        "theme_light":        "Clair",
    },
    "de": {
        "app_title":          "StudentHub v0.4-beta",
        "subtitle":           "Dein akademisches Aufgaben-Dashboard",
        "new_task":           "Neue Aufgabe",
        "task_name":          "Aufgabenname",
        "task_type":          "Typ  (Pruefung / Hausaufgabe...)",
        "deadline":           "Frist  JJJJ-MM-TT",
        "add_btn":            "+  Hinzufuegen",
        "filter_label":       "Filter:",
        "all_btn":            "Alle",
        "type_hint":          "z.B. Pruefung, Hausaufgabe...",
        "or_type":            "oder Typ eingeben:",
        "tasks_header":       "Aufgaben",
        "shown":              "angezeigt",
        "no_tasks":           "Noch keine Aufgaben -- fuege eine oben hinzu",
        "no_type_tasks":      "Keine \"{t}\"-Aufgaben gefunden.",
        "done_btn":           "Erledigt",
        "total":              "Gesamt",
        "done_stat":          "Erledigt",
        "pending":            "Ausstehend",
        "missing_field":      "Fehlendes Feld",
        "task_required":      "Aufgabenname ist erforderlich.",
        "notif_overdue":      "Ueberfaellige Aufgabe",
        "notif_today":        "Heute faellig!",
        "notif_tomorrow":     "Morgen faellig",
        "notif_checked":      "Benachrichtigungen",
        "notif_check_msg":    "Anstehende Fristen geprueft.",
        "was_due":            "\"{t}\" war faellig am {d}",
        "due_today":          "\"{t}\" ist heute faellig.",
        "due_tomorrow":       "\"{t}\" ist morgen faellig.",
        "overdue_suffix":     "{n}T ueberfaellig",
        "today_suffix":       "Heute!",
        "tomorrow_suffix":    "Morgen",
        "no_deadline":        "Keine Frist",
        "backup_btn":         "Sicherung",
        "backup_title":       "Sicherung speichern",
        "backup_success":     "Sicherung gespeichert!",
        "backup_success_msg": "Aufgaben gesichert unter:\n{path}",
        "backup_none":        "Noch keine Aufgaben zum Sichern.",
        "backup_err":         "Sicherung fehlgeschlagen:\n{err}",
        "restore_btn":        "Wiederherstellen",
        "restore_title":      "Sicherungsdatei auswaehlen",
        "restore_success":    "Wiederhergestellt!",
        "restore_success_msg":"Aufgaben aus Sicherung wiederhergestellt.",
        "restore_err":        "Wiederherstellung fehlgeschlagen:\n{err}",
        "restore_confirm":    "Dies ersetzt ALLE aktuellen Aufgaben. Fortfahren?",
        "lang_label":         "Sprache:",
        "theme_label":        "Design:",
        "theme_dark":         "Dunkel",
        "theme_light":        "Hell",
    },
    "ja": {
        "app_title":          "StudentHub v0.4-beta",
        "subtitle":           "学業タスクダッシュボード",
        "new_task":           "新しいタスク",
        "task_name":          "タスク名",
        "task_type":          "種類 (試験 / 宿題...)",
        "deadline":           "期限  YYYY-MM-DD",
        "add_btn":            "+  追加",
        "filter_label":       "フィルター:",
        "all_btn":            "すべて",
        "type_hint":          "例: 試験、宿題...",
        "or_type":            "または種類を入力:",
        "tasks_header":       "タスク",
        "shown":              "表示中",
        "no_tasks":           "タスクがありません -- 上から追加してください",
        "no_type_tasks":      "「{t}」のタスクは見つかりませんでした。",
        "done_btn":           "完了",
        "total":              "合計",
        "done_stat":          "完了",
        "pending":            "未完了",
        "missing_field":      "入力必須",
        "task_required":      "タスク名は必須です。",
        "notif_overdue":      "期限超過",
        "notif_today":        "今日期限！",
        "notif_tomorrow":     "明日期限",
        "notif_checked":      "通知",
        "notif_check_msg":    "期限を確認しました。",
        "was_due":            "「{t}」の期限は {d} でした",
        "due_today":          "「{t}」は今日期限です。",
        "due_tomorrow":       "「{t}」は明日期限です。",
        "overdue_suffix":     "{n}日遅延",
        "today_suffix":       "今日！",
        "tomorrow_suffix":    "明日",
        "no_deadline":        "期限なし",
        "backup_btn":         "バックアップ",
        "backup_title":       "バックアップを保存",
        "backup_success":     "保存完了！",
        "backup_success_msg": "タスクを保存しました:\n{path}",
        "backup_none":        "まだバックアップするタスクがありません。",
        "backup_err":         "バックアップ失敗:\n{err}",
        "restore_btn":        "復元",
        "restore_title":      "バックアップファイルを選択",
        "restore_success":    "復元完了！",
        "restore_success_msg":"バックアップからタスクを復元しました。",
        "restore_err":        "復元失敗:\n{err}",
        "restore_confirm":    "現在のタスクがすべて上書きされます。続けますか？",
        "lang_label":         "言語:",
        "theme_label":        "テーマ:",
        "theme_dark":         "ダーク",
        "theme_light":        "ライト",
    },
}

LANG_OPTIONS = {
    "English":  "en",
    "Espanol":  "es",
    "Francais": "fr",
    "Deutsch":  "de",
    "Japanese": "ja",
}
LANG_KEYS = list(LANG_OPTIONS.keys())

# ─────────────────────────────────────────────
# File I/O
# ─────────────────────────────────────────────
def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

# ─────────────────────────────────────────────
# Toast Notification
# ─────────────────────────────────────────────
class ToastNotification(ctk.CTkToplevel):
    def __init__(self, parent, title, message, urgent=False, duration=5000):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=COLORS["bg"])

        border_color = COLORS["notif_urgent"] if urgent else COLORS["notif_border"]

        outer = ctk.CTkFrame(
            self, fg_color=COLORS["notif_bg"],
            corner_radius=12, border_width=2, border_color=border_color,
        )
        outer.pack(padx=2, pady=2)

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

        ctk.CTkButton(
            top_row, text="X", width=22, height=22,
            fg_color="transparent", hover_color=COLORS["card_hover"],
            text_color=COLORS["text_muted"], font=FONTS["small"],
            command=self.dismiss,
        ).pack(side="right")

        ctk.CTkLabel(
            outer, text=message,
            font=FONTS["notif_body"], text_color=COLORS["text_dim"],
            wraplength=260, justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 12))

        self.update_idletasks()
        w  = self.winfo_reqwidth()
        h  = self.winfo_reqheight()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"+{sw - w - 24}+{sh - h - 60}")

        self._job = self.after(duration, self.dismiss)

    def dismiss(self):
        try:
            self.after_cancel(self._job)
        except Exception:
            pass
        self.destroy()


# ─────────────────────────────────────────────
# Settings Window
# ─────────────────────────────────────────────
class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self._app = parent
        self.title("Settings")
        self.geometry("360x430")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])
        self.attributes("-topmost", True)

        # Center over parent
        self.update_idletasks()
        px = parent.winfo_x() + parent.winfo_width()  // 2 - 180
        py = parent.winfo_y() + parent.winfo_height() // 2 - 170
        self.geometry(f"+{px}+{py}")

        self._build()

    def _build(self):
        app = self._app

        ctk.CTkLabel(
            self, text="Settings",
            font=FONTS["label"], text_color=COLORS["text"]
        ).pack(anchor="w", padx=24, pady=(22, 0))

        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]
        ).pack(fill="x", padx=24, pady=14)

        # ── Language card ─────────────────────
        lang_card = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=10, border_width=1, border_color=COLORS["border"]
        )
        lang_card.pack(fill="x", padx=24, pady=(0, 10))

        lang_inner = ctk.CTkFrame(lang_card, fg_color="transparent")
        lang_inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            lang_inner, text=app._("lang_label"),
            font=FONTS["body"], text_color=COLORS["text"]
        ).pack(side="left")

        current_display = next(
            k for k, v in LANG_OPTIONS.items() if v == app._lang)

        menu = ctk.CTkOptionMenu(
            lang_inner,
            values=LANG_KEYS,
            command=self._on_lang_change,
            width=130, height=30,
            fg_color=COLORS["card"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_dark"],
            dropdown_fg_color=COLORS["surface"],
            dropdown_hover_color=COLORS["card_hover"],
            text_color=COLORS["text"],
            font=FONTS["small"],
            dynamic_resizing=False,
        )
        menu.set(current_display)
        menu.pack(side="right")

        # ── Backup card ───────────────────────
        backup_card = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=10, border_width=1, border_color=COLORS["border"]
        )
        backup_card.pack(fill="x", padx=24, pady=(0, 10))

        backup_inner = ctk.CTkFrame(backup_card, fg_color="transparent")
        backup_inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            backup_inner, text=app._("backup_btn"),
            font=FONTS["body"], text_color=COLORS["text"]
        ).pack(side="left")

        ctk.CTkButton(
            backup_inner,
            text="Export .json",
            width=120, height=30,
            corner_radius=8,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            text_color=COLORS["text"],
            font=FONTS["small"],
            command=app._backup,
        ).pack(side="right")

        # ── Restore card ──────────────────────
        restore_card = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=10, border_width=1, border_color=COLORS["border"]
        )
        restore_card.pack(fill="x", padx=24, pady=(0, 10))

        restore_inner = ctk.CTkFrame(restore_card, fg_color="transparent")
        restore_inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            restore_inner, text=app._("restore_btn"),
            font=FONTS["body"], text_color=COLORS["text"]
        ).pack(side="left")

        ctk.CTkButton(
            restore_inner,
            text="Import .json",
            width=120, height=30,
            corner_radius=8,
            fg_color=COLORS["card"],
            hover_color=COLORS["success_dark"],
            text_color=COLORS["text"],
            font=FONTS["small"],
            command=lambda: [app._restore(), self.destroy()],
        ).pack(side="right")

        # ── Theme card ────────────────────────
        theme_card = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=10, border_width=1, border_color=COLORS["border"]
        )
        theme_card.pack(fill="x", padx=24, pady=(0, 10))

        theme_inner = ctk.CTkFrame(theme_card, fg_color="transparent")
        theme_inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            theme_inner, text=app._("theme_label"),
            font=FONTS["body"], text_color=COLORS["text"]
        ).pack(side="left")

        btn_frame = ctk.CTkFrame(theme_inner, fg_color="transparent")
        btn_frame.pack(side="right")

        is_dark = app._theme == "dark"

        dark_btn = ctk.CTkButton(
            btn_frame,
            text=app._("theme_dark"),
            width=72, height=30,
            corner_radius=8,
            fg_color=COLORS["accent"] if is_dark else COLORS["card"],
            hover_color=COLORS["accent_dark"],
            text_color=COLORS["text"],
            font=FONTS["small"],
            command=lambda: [app._set_theme("dark"), self.destroy()],
        )
        dark_btn.pack(side="left", padx=(0, 4))

        light_btn = ctk.CTkButton(
            btn_frame,
            text=app._("theme_light"),
            width=72, height=30,
            corner_radius=8,
            fg_color=COLORS["accent"] if not is_dark else COLORS["card"],
            hover_color=COLORS["accent_dark"],
            text_color=COLORS["text"],
            font=FONTS["small"],
            command=lambda: [app._set_theme("light"), self.destroy()],
        )
        light_btn.pack(side="left")

    def _on_lang_change(self, display_name):
        self._app._set_language(display_name)
        self.destroy()


# ─────────────────────────────────────────────
# App
# ─────────────────────────────────────────────
class StudentHub(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Load persisted settings before building UI
        _s = load_settings()
        self._lang  = _s.get("lang",  "en")
        self._theme = _s.get("theme", "dark")
        COLORS.update(COLORS_LIGHT if self._theme == "light" else COLORS_DARK)
        ctk.set_appearance_mode(self._theme)

        self.geometry("820x700")
        self.minsize(720, 560)
        self.configure(fg_color=COLORS["bg"])

        self._active_filter = None
        self._notified_ids  = set()

        self._build_ui()
        self.refresh_tasks()
        self._check_notifications()

        # Window icon (embedded, works with PyInstaller one-file)
        try:
            import base64, io
            from PIL import Image, ImageTk
            _ico = Image.open(io.BytesIO(base64.b64decode(_ICON_B64))).resize((32, 32), Image.LANCZOS)
            self._icon = ImageTk.PhotoImage(_ico)
            self.iconphoto(True, self._icon)
        except Exception:
            pass


    # ── Translation shorthand ─────────────────
    def _(self, key, **kw):
        s = STRINGS[self._lang].get(key, key)
        return s.format(**kw) if kw else s

    # ── Language switch ───────────────────────
    def _set_language(self, display_name):
        self._lang = LANG_OPTIONS[display_name]
        save_settings({"theme": self._theme, "lang": self._lang})
        self._rebuild_ui()

    # ── Theme switch ──────────────────────────
    def _set_theme(self, theme_name):
        self._theme = theme_name
        COLORS.update(COLORS_LIGHT if theme_name == "light" else COLORS_DARK)
        ctk.set_appearance_mode(theme_name)
        save_settings({"theme": self._theme, "lang": self._lang})
        self._rebuild_ui()

    def _rebuild_ui(self):
        for w in self.winfo_children():
            w.destroy()
        self.configure(fg_color=COLORS["bg"])
        self._active_filter = None
        self._build_ui()
        self.refresh_tasks()

    # ── Backup / Restore ─────────────────────
    def _backup(self):
        if not os.path.exists(FILE):
            messagebox.showwarning(
                self._("backup_btn"), self._("backup_none"))
            return
        now  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = filedialog.asksaveasfilename(
            title=self._("backup_title"),
            initialfile=f"studenthub_backup_{now}.json",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not dest:
            return
        try:
            shutil.copy2(FILE, dest)
            messagebox.showinfo(
                self._("backup_success"),
                self._("backup_success_msg", path=dest),
            )
        except Exception as e:
            messagebox.showerror("Error", self._("backup_err", err=str(e)))

    def _restore(self):
        confirmed = messagebox.askyesno(
            self._("restore_btn"),
            self._("restore_confirm"),
        )
        if not confirmed:
            return
        src = filedialog.askopenfilename(
            title=self._("restore_title"),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not src:
            return
        try:
            # Validate it's a proper tasks JSON before overwriting
            with open(src, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Not a valid tasks backup.")
            shutil.copy2(src, FILE)
            self.refresh_tasks()
            messagebox.showinfo(
                self._("restore_success"),
                self._("restore_success_msg"),
            )
        except Exception as e:
            messagebox.showerror("Error", self._("restore_err", err=str(e)))

    # ── Notification logic ─────────────────────
    def _check_notifications(self):
        tasks = load_tasks()
        today = datetime.date.today()

        for i, task in enumerate(tasks):
            if task["done"] or not task.get("deadline"):
                continue
            try:
                dl = datetime.date.fromisoformat(task["deadline"])
            except ValueError:
                continue

            days_left = (dl - today).days
            t = task["title"]
            d = task["deadline"]

            if days_left < 0:
                uid = f"overdue-{i}-{d}"
                if uid not in self._notified_ids:
                    self._notified_ids.add(uid)
                    self._show_toast(
                        self._("notif_overdue"),
                        self._("was_due", t=t, d=d),
                        urgent=True,
                    )
            elif days_left == 0:
                uid = f"today-{i}-{d}"
                if uid not in self._notified_ids:
                    self._notified_ids.add(uid)
                    self._show_toast(
                        self._("notif_today"),
                        self._("due_today", t=t),
                        urgent=True,
                    )
            elif days_left == 1:
                uid = f"tomorrow-{i}-{d}"
                if uid not in self._notified_ids:
                    self._notified_ids.add(uid)
                    self._show_toast(
                        self._("notif_tomorrow"),
                        self._("due_tomorrow", t=t),
                        urgent=False,
                    )

        self.after(60_000, self._check_notifications)

    def _show_toast(self, title, message, urgent=False):
        try:
            toast = ToastNotification(self, title, message, urgent=urgent)
            existing = [
                w for w in self.winfo_children()
                if isinstance(w, ToastNotification) and w.winfo_exists()
            ]
            if len(existing) > 1:
                toast.update_idletasks()
                h     = toast.winfo_reqheight()
                parts = toast.geometry().split("+")
                new_y = int(parts[2]) - (len(existing) - 1) * (h + 8)
                toast.geometry(f"+{parts[1]}+{new_y}")
        except Exception:
            pass

    def _manual_notify_check(self):
        self._notified_ids.clear()
        self._check_notifications()
        self._show_toast(
            self._("notif_checked"),
            self._("notif_check_msg"),
            urgent=False,
        )

    def _open_settings(self):
        # Prevent opening multiple settings windows
        for w in self.winfo_children():
            if isinstance(w, SettingsWindow) and w.winfo_exists():
                w.focus()
                return
        SettingsWindow(self)

    # ── Layout ────────────────────────────────
    def _build_ui(self):
        self.title(self._("app_title"))

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
            title_col, text=self._("subtitle"),
            font=FONTS["subtitle"], text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", anchor="e")

        # Settings + Bell buttons
        btn_row = ctk.CTkFrame(right, fg_color="transparent")
        btn_row.pack(anchor="e")

        ctk.CTkButton(
            btn_row,
            text="[S]",
            width=36, height=36,
            corner_radius=18,
            fg_color=COLORS["card"],
            hover_color=COLORS["card_hover"],
            text_color=COLORS["text_dim"],
            font=("Segoe UI", 14),
            command=self._open_settings,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btn_row,
            text="[B]",
            width=36, height=36,
            corner_radius=18,
            fg_color=COLORS["card"],
            hover_color=COLORS["card_hover"],
            text_color=COLORS["text_dim"],
            font=("Segoe UI", 14),
            command=self._manual_notify_check,
        ).pack(side="left")

        self.stats_label = ctk.CTkLabel(
            right, text="",
            font=FONTS["small"], text_color=COLORS["text_muted"]
        )
        self.stats_label.pack(anchor="e", pady=(8, 0))

        # ── Divider ───────────────────────────
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]
        ).pack(fill="x", padx=30, pady=18)

        # ── Add Task Card ─────────────────────
        add_card = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=14, border_width=1, border_color=COLORS["border"]
        )
        add_card.pack(fill="x", padx=30, pady=(0, 16))

        ctk.CTkLabel(
            add_card, text=self._("new_task"),
            font=FONTS["label"], text_color=COLORS["accent_glow"]
        ).pack(anchor="w", padx=20, pady=(16, 8))

        fields_row = ctk.CTkFrame(add_card, fg_color="transparent")
        fields_row.pack(fill="x", padx=20, pady=(0, 16))

        self.title_entry = self._styled_entry(
            fields_row, self._("task_name"), width=220)
        self.title_entry.pack(side="left", padx=(0, 8))

        self.type_entry = self._styled_entry(
            fields_row, self._("task_type"), width=180)
        self.type_entry.pack(side="left", padx=(0, 8))

        self.deadline_entry = self._styled_entry(
            fields_row, self._("deadline"), width=160)
        self.deadline_entry.pack(side="left", padx=(0, 8))

        self._make_btn(
            fields_row, self._("add_btn"), self._add_task,
            fg=COLORS["accent"], hover=COLORS["accent_dark"], width=110
        ).pack(side="left")

        # ── Filter Row ────────────────────────
        self._filter_row = ctk.CTkFrame(self, fg_color="transparent")
        self._filter_row.pack(fill="x", padx=30, pady=(0, 14))

        ctk.CTkLabel(
            self._filter_row, text=self._("filter_label"),
            font=FONTS["small"], text_color=COLORS["text_muted"]
        ).pack(side="left", padx=(0, 8))

        self._all_btn = ctk.CTkButton(
            self._filter_row,
            text=self._("all_btn"),
            width=52, height=28,
            corner_radius=20,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            text_color=COLORS["text"],
            font=FONTS["small"],
            command=self._reset_filter,
        )
        self._all_btn.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            self._filter_row, text=self._("or_type"),
            font=FONTS["small"], text_color=COLORS["text_muted"]
        ).pack(side="left", padx=(0, 6))

        self._filter_var = ctk.StringVar()
        self._filter_var.trace_add("write", self._on_filter_type)

        ctk.CTkEntry(
            self._filter_row,
            width=160, height=28,
            placeholder_text=self._("type_hint"),
            placeholder_text_color=COLORS["text_muted"],
            fg_color=COLORS["card"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text"],
            corner_radius=20,
            font=FONTS["small"],
            textvariable=self._filter_var,
        ).pack(side="left")

        # ── Task List Area ────────────────────
        list_frame = ctk.CTkFrame(
            self, fg_color=COLORS["surface"],
            corner_radius=14, border_width=1, border_color=COLORS["border"]
        )
        list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        list_header = ctk.CTkFrame(list_frame, fg_color="transparent")
        list_header.pack(fill="x", padx=18, pady=(14, 0))

        ctk.CTkLabel(
            list_header, text=self._("tasks_header"),
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
        typed = self._filter_var.get().strip().lower()
        if typed:
            self._active_filter = typed
            self._all_btn.configure(
                fg_color=COLORS["card"], text_color=COLORS["text_dim"])
        else:
            self._active_filter = None
            self._all_btn.configure(
                fg_color=COLORS["accent"], text_color=COLORS["text"])
        self._render_tasks()

    def _reset_filter(self):
        self._active_filter = None
        self._filter_var.set("")
        self._all_btn.configure(
            fg_color=COLORS["accent"], text_color=COLORS["text"])

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
        done       = task["done"]
        border_col = COLORS["success_dark"] if done else self._deadline_color(task)

        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["done_bg"] if done else COLORS["card"],
            corner_radius=10, border_width=1, border_color=border_col,
        )
        card.pack(fill="x", pady=4, padx=4)
        card.columnconfigure(1, weight=1)

        dot_color = COLORS["success"] if done else self._deadline_color(task)
        ctk.CTkFrame(
            card, width=10, height=10,
            corner_radius=5, fg_color=dot_color
        ).grid(row=0, column=0, padx=(14, 10), pady=16, sticky="ns")

        ctk.CTkLabel(
            card,
            text=("v  " if done else "") + task["title"],
            font=FONTS["body"],
            text_color=COLORS["done_text"] if done else COLORS["text"],
            anchor="w",
        ).grid(row=0, column=1, sticky="w", pady=10)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.grid(row=0, column=2, padx=10, sticky="e")

        badge_color = self._type_badge_color(task.get("type", "other"))
        ctk.CTkLabel(
            info,
            text=(task.get("type") or "other").upper(),
            font=FONTS["badge"], text_color="#ffffff",
            fg_color=badge_color, corner_radius=4,
            width=54, height=20,
        ).pack(side="left", padx=4)

        dl_text, dl_color = self._deadline_display(task)
        ctk.CTkLabel(
            info, text=dl_text,
            font=FONTS["mono"], text_color=dl_color,
        ).pack(side="left", padx=(6, 6))

        if not done:
            self._make_btn(
                info, self._("done_btn"),
                lambda i=idx: self._complete_task(i),
                fg=COLORS["success"], hover=COLORS["success_dark"],
                width=75, height=28
            ).pack(side="left", padx=2)

        self._make_btn(
            info, "X", lambda i=idx: self._delete_task(i),
            fg=COLORS["card_hover"], hover=COLORS["danger"],
            width=32, height=28
        ).pack(side="left", padx=(2, 10))

    def _deadline_color(self, task):
        if not task.get("deadline") or task["done"]:
            return COLORS["border"]
        try:
            days = (datetime.date.fromisoformat(task["deadline"])
                    - datetime.date.today()).days
            if days <= 0:  return COLORS["danger"]
            if days == 1:  return COLORS["warning"]
            return COLORS["accent"]
        except ValueError:
            return COLORS["border"]

    def _deadline_display(self, task):
        if not task.get("deadline"):
            return self._("no_deadline"), COLORS["text_muted"]
        try:
            days = (datetime.date.fromisoformat(task["deadline"])
                    - datetime.date.today()).days
            if days < 0:
                suffix = "  " + self._("overdue_suffix", n=-days)
                color  = COLORS["danger"]
            elif days == 0:
                suffix = "  " + self._("today_suffix")
                color  = COLORS["danger"]
            elif days == 1:
                suffix = "  " + self._("tomorrow_suffix")
                color  = COLORS["warning"]
            else:
                suffix = f"  ({days}d)"
                color  = COLORS["text_dim"]
            return f"[D] {task['deadline']}{suffix}", color
        except ValueError:
            return f"[D] {task['deadline']}", COLORS["text_dim"]

    def _type_badge_color(self, t):
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
            messagebox.showerror(
                self._("missing_field"), self._("task_required"))
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
        for widget in self.scroll.winfo_children():
            widget.destroy()

        tasks = load_tasks()
        tasks_indexed = sorted(
            enumerate(tasks), key=lambda x: x[1]["deadline"] or "9999")

        ft      = self._active_filter
        visible = [(i, t) for i, t in tasks_indexed
                   if not ft or t.get("type", "other").lower() == ft]

        if not visible:
            empty = (self._("no_type_tasks", t=ft)
                     if ft else self._("no_tasks"))
            ctk.CTkLabel(
                self.scroll, text=empty,
                font=FONTS["body"], text_color=COLORS["text_muted"],
            ).pack(pady=30)
        else:
            for idx, task in visible:
                self._build_task_card(self.scroll, idx, task)

        total      = len(tasks)
        done_count = sum(1 for t in tasks if t["done"])
        pending    = total - done_count

        self.count_label.configure(
            text=f"{len(visible)} {self._('shown')}")
        self.stats_label.configure(
            text=(f"{self._('total')}: {total}   "
                  f"{self._('done_stat')}: {done_count}   "
                  f"{self._('pending')}: {pending}"))

    def refresh_tasks(self):
        self._render_tasks()


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = StudentHub()
    app.mainloop()