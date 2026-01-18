from enum import Enum
from PySide6.QtWidgets import QApplication


class ThemeType(str, Enum):
    DARK = "DARK"
    GRAY = "GRAY"
    BLUE = "BLUE"
    LIGHT = "LIGHT"


THEME_PALETTES = {
    ThemeType.LIGHT: {
        # --- Layers ---
        "@bg_root": "#f9fafb",  # Gris muy claro (Gray 50) para el fondo
        "@bg_surface": "#ffffff",  # Blanco puro para Tarjetas/Sidebar
        "@bg_element": "#f3f4f6",  # Gris claro (Gray 100) para inputs
        "@bg_dim": "rgba(0, 0, 0, 0.05)",  # Overlay sutil para paneles internos
        # --- Text ---
        "@text_primary": "#111827",  # Negro casi puro (Gray 900)
        "@text_secondary": "#414245",  # Gris oscuro (Gray 600) para mejor lectura
        # --- Borders ---
        "@border_dim": "#e5e7eb",
        "@border_highlight": "#3b82f6",
        # --- Actions ---
        "@accent_primary": "#d6dde8",
        "@action_hover": "rgba(0, 0, 0, 0.05)",
        "@action_pressed": "rgba(0, 0, 0, 0.1)",
        "@action_selected": "rgba(59, 130, 246, 0.1)",
        # --- Misc ---
        "@scroll_thumb": "#9ca3af",
        # Iconos
        "@icon_color": "#111827",
    },
    ThemeType.DARK: {
        # --- Layers (Elevation) ---
        "@bg_root": "#121212",
        "@bg_surface": "#18181b",
        "@bg_element": "#27272a",
        "@bg_dim": "rgba(0, 0, 0, 0.2)",  # Overlay oscuro original
        # --- Text ---
        "@text_primary": "#e5e5e5",
        "@text_secondary": "#a1a1aa",
        # --- Borders ---
        "@border_dim": "#27272a",
        "@border_highlight": "#38bdf8",
        # --- Actions / Interactions ---
        "@accent_primary": "#38bdf8",
        "@action_hover": "rgba(255, 255, 255, 0.05)",
        "@action_pressed": "rgba(255, 255, 255, 0.1)",
        "@action_selected": "rgba(255, 255, 255, 0.1)",
        # --- Misc ---
        "@scroll_thumb": "#52525b",
        # Iconos
        "@icon_color": "#e5e5e5",
    },
    ThemeType.GRAY: {
        # --- Layers ---
        "@bg_root": "#27272a",
        "@bg_surface": "#18181b",
        "@bg_element": "#3f3f46",
        "@bg_dim": "rgba(0, 0, 0, 0.2)",
        # --- Text ---
        "@text_primary": "#a1a1aa",
        "@text_secondary": "#71717a",
        # --- Borders ---
        "@border_dim": "#3f3f46",
        "@border_highlight": "#ffffff",
        # --- Actions ---
        "@accent_primary": "#ffffff",
        "@action_hover": "rgba(255, 255, 255, 0.05)",
        "@action_pressed": "rgba(255, 255, 255, 0.1)",
        "@action_selected": "rgba(255, 255, 255, 0.1)",
        # --- Misc ---
        "@scroll_thumb": "#71717a",
        # Iconos
        "@icon_color": "#e5e5e5",
    },
    ThemeType.BLUE: {
        # --- Layers ---
        "@bg_root": "#0f172a",
        "@bg_surface": "#1e293b",
        "@bg_element": "#334155",
        "@bg_dim": "rgba(0, 0, 0, 0.2)",
        # --- Text ---
        "@text_primary": "#e2e8f0",
        "@text_secondary": "#94a3b8",
        # --- Borders ---
        "@border_dim": "#334155",
        "@border_highlight": "#38bdf8",
        # --- Actions ---
        "@accent_primary": "#38bdf8",
        "@action_hover": "rgba(56, 189, 248, 0.1)",
        "@action_pressed": "rgba(56, 189, 248, 0.2)",
        "@action_selected": "rgba(56, 189, 248, 0.15)",
        # --- Misc ---
        "@scroll_thumb": "#475569",
        # Iconos
        "@icon_color": "#e2e8f0",
    },
}


class ThemeManager:
    """
    Gestor de temas, carga las hojas de estilo qss.
    """

    def __init__(self, initial_theme: ThemeType):
        self._current_theme: ThemeType = initial_theme

        self._template_content: str = ""

        # Cargar plantilla inicial
        self._load_template()

    # -------------------------------------------------------------------------
    # GESTIÓN DE TEMAS
    # -------------------------------------------------------------------------
    def apply_theme(self, theme_type: ThemeType) -> None:
        """Aplica un tema específico a la aplicación."""
        # Asegurar que es Enum si viene como string
        if isinstance(theme_type, str):
            try:
                theme_type = ThemeType(theme_type)
            except ValueError:
                print(f"⚠️ Error: Tema '{theme_type}' no válido.")
                return

        if theme_type not in THEME_PALETTES:
            print(f"⚠️ Error: Tema '{theme_type}' no encontrado.")
            return

        self._current_theme = theme_type

        # 1. Preparar el QSS
        palette = THEME_PALETTES[theme_type]
        qss_content = self._process_template(palette)

        # 2. Aplicar a la aplicación ⭐
        app: QApplication = QApplication.instance()
        if app:
            app.setStyleSheet(qss_content)

    # -------------------------------------------------------------------------
    # MÉTODOS PRIVADOS (Auxiliares)
    # -------------------------------------------------------------------------
    def _load_template(self):
        """Carga la plantilla QSS en memoria."""
        try:
            with open("styles/style.qss", "r", encoding="utf-8") as f:
                self._template_content = f.read()
        except FileNotFoundError:
            print("No se encontró el archivo style.qss")

    def _process_template(self, palette: dict) -> str:
        """Reemplaza las variables en el string del QSS."""
        qss = self._template_content
        for key, value in palette.items():
            qss = qss.replace(key, value)
        return qss
