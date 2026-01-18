import sys
from dataclasses import dataclass
from typing import Dict, Type

# 3rd Party
from PySide6.QtWidgets import QApplication, QWidget

# Local
from main_ui import Interface
from styles.themes import ThemeManager, ThemeType

# Importar páginas del Sidebar
from pages.Home_page import HomePage

# =============================================================================
# 1. CONFIGURACIÓN DECLARATIVA (MENU DEFINITIONS)
# =============================================================================


@dataclass
class MenuItemProp:
    """Estructura de datos para ítems del menú"""

    key: str  # ID único para el registro interno
    text: str  # Texto visible
    icon: str  # Nombre del archivo de icono
    page_class: Type[QWidget]  # Clase a instanciar (NO instancia)
    section: str = "scroll"  # 'fixed' o 'scroll'


# Configuración del Menú Principal
MAIN_MENU_CONFIG = [
    # Sección Fija
    MenuItemProp(
        key="home", text="Home", icon="home.svg", page_class=HomePage, section="fixed"
    ),
]

# Configuración del Menú de Configuración
# key: ID único, text: Nombre en lista, page_class: Clase
CONFIG_MENU_CONFIG = [
    {"key": "general", "text": "General", "page_class": QWidget},  # Placeholder
]


# =============================================================================
# 2. CONTROLADOR PRINCIPAL (PUPPET MASTER)
# =============================================================================


class Ventana(Interface):
    def __init__(self):
        super().__init__()
        # REGISTROS DE INSTANCIAS (Centralized Registry)
        self.pages: Dict[str, QWidget] = {}
        self.config_pages: Dict[str, QWidget] = {}

        # 1. Inicialización en orden
        self._inicializar_paginas()
        self._construir_menu()
        self._conectar_logica_negocio()

    def _inicializar_paginas(self):
        """
        LAZY LOADING: Solo instanciamos la página HOME al inicio.
        Las demás se instancian bajo demanda en _on_navigate.
        """
        # 1. Buscar configuración de Home
        home_config = next(
            (item for item in MAIN_MENU_CONFIG if item.key == "home"), None
        )

        if home_config:
            # Instanciar Home inmediatamente
            print("🚀 Iniciando Home Page...")
            instance = home_config.page_class()
            self.pages["home"] = instance
            self.register_page(instance)

        # B. Páginas de Configuración (Placeholder o carga inicial mínima)
        # Para config, quizás queramos cargar todo o también lazy.
        # Por simplicidad, cargamos todo lo de config por ahora (son pocas)
        for conf in CONFIG_MENU_CONFIG:
            key = conf["key"]
            instance = conf["page_class"]()
            self.config_pages[key] = instance
            self.config_window.add_config_page(conf["text"], instance)

    def _construir_menu(self):
        """
        Genera el menú pasando KEYs (strings) en lugar de instancias.
        """
        fixed_items = []
        scroll_items = []

        # Helper class temporal para pasar datos al Sidebar
        @dataclass
        class SidebarItem:
            text: str
            icon: str
            route: str  # Ahora es str (la key)

        for item in MAIN_MENU_CONFIG:
            # En lugar de pasar la instancia, pasamos item.key
            sidebar_obj = SidebarItem(text=item.text, icon=item.icon, route=item.key)

            if item.section == "fixed":
                fixed_items.append(sidebar_obj)
            else:
                scroll_items.append(sidebar_obj)

        self.set_menu_options(fixed_items, scroll_items)

    def _conectar_logica_negocio(self):
        """
        ORQUESTACIÓN CENTRALIZADA (Signals & Slots)
        """
        print(">> Conectando lógica del sistema...")

        # 1. Interceptar Navegación del Sidebar (Lazy Loading Handler)
        self.sidebar.action_navigate.connect(self._on_navigate)

    def _on_navigate(self, route_key: str):
        """
        Manejador de Navegación con Lazy Loading.
        Recibe la 'key' de la página deseada.
        """
        print(f"🔄 Navegando a: {route_key}")

        # 1. Verificar si ya existe
        if route_key in self.pages:
            page = self.pages[route_key]
            self.Canvas.set_current_page(page)
            return

        # 2. Si no existe, buscar en configuración e instanciar
        # (Esto simula el "Lazy Load")
        config_item = next(
            (item for item in MAIN_MENU_CONFIG if item.key == route_key), None
        )

        if config_item:
            print(f"⏳ Instanciando módulo por primera vez: {config_item.text}...")
            # Instanciar
            new_instance = config_item.page_class()

            # Registrar
            self.pages[route_key] = new_instance
            self.register_page(new_instance)

            # Mostrar
            self.Canvas.set_current_page(new_instance)

            # 3. CONEXIONES DINÁMICAS (Late Binding)
            # Si el módulo recién creado requiere conexiones, las hacemos aquí.
            self._conectar_modulo_dinamico(route_key, new_instance)

        else:
            print(f"⚠️ Error: Ruta '{route_key}' no encontrada en configuración.")

    def _conectar_modulo_dinamico(self, key: str, instance: QWidget):
        """
        Realiza conexiones específicas para módulos que se cargan tarde.
        """
        # Aquí puedes agregar lógica para conectar señales de nuevos módulos
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    initial_theme = ThemeType.DARK
    theme_manager = ThemeManager(initial_theme)
    theme_manager.apply_theme(initial_theme)

    windows = Ventana()
    windows.show()
    sys.exit(app.exec())
