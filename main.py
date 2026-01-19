import sys

# 3rd Party
from PySide6.QtWidgets import QApplication, QWidget

# Local
from main_ui import Interface
from styles.themes import ThemeManager, ThemeType
from components.Sidebar import MenuItemProp

# Importar páginas (Nueva estructura)
from pages.main.Home_page import HomePage
from pages.main.Demo_page import DemoPage
from pages.config.General_config import GeneralConfigPage

# =============================================================================
# CONTROLADOR PRINCIPAL
# =============================================================================


class Ventana(Interface):
    def __init__(self):
        super().__init__()

        # 2. Registrar Páginas
        # Usamos la sintaxis directa: registramos y guardamos la referencia en una sola línea
        self.homePage = self.register_page(
            MenuItemProp("Home", "home.svg", HomePage(), "fixed")
        )

        # 'code.svg' no existía, cambiamos a 'html.svg' que sí existe
        self.demoPage = self.register_page(
            MenuItemProp("Demo", "html.svg", DemoPage(), "scroll")
        )

        self.navigate_to(self.demoPage)

        # 3. Registrar Configuración
        self.generalConfigPage = self.register_config(
            "General", GeneralConfigPage()
        )

        # Opcional: Probar navegación a config
        # self.navigate_to_config(self.generalConfigPage)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    initial_theme = ThemeType.GRAY
    theme_manager = ThemeManager(initial_theme)
    theme_manager.apply_theme(initial_theme)

    windows = Ventana()
    windows.show()
    sys.exit(app.exec())
