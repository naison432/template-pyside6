"""Interfaz principal de la app"""

from dataclasses import dataclass
from typing import Literal, List

# 1. QtWidgets
from PySide6.QtWidgets import (  # pylint: disable=no-name-in-module, unused-import # noqa
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from components.Sidebar import Sidebar, MenuItemProp
from components.Canvas import Canvas
from components.Header import Header
from components.Configuracion import Configuracion


class Interface(QMainWindow):
    def __init__(self):
        """
        Inicializa la ventana principal de la app.

        Métodos principales de navegación:
        - register_page(item): Registra una página en el Sidebar y el Canvas.
        - navigate_to(page): Navega programáticamente a una página específica.

        Métodos de configuración:
        - register_config(name, widget): Registra una página en la ventana de configuración.
        - navigate_to_config(widget): Abre la config y navega a la página.
        """
        super().__init__()
        self.setWindowTitle("mi app")
        self.resize(1200, 800)  # Un poco más grande para ver bien el dashboard

        # --- ESTRUCTURA BASE ---
        mainContainer = QWidget(self)
        mainContainer.setObjectName("mainContainer")
        self.setCentralWidget(mainContainer)

        # Layout principal horizontal: [ Sidebar | ContenidoDerecho ]
        self.layout_main = QHBoxLayout(mainContainer)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

        # ---------------------------------------------------------
        # 1. EL SIDEBAR (Izquierda)
        # ---------------------------------------------------------
        self.sidebar = Sidebar()
        self.layout_main.addWidget(self.sidebar)

        # ---------------------------------------------------------
        # 2. CONTENEDOR DERECHO (Header + Canvas)
        # ---------------------------------------------------------
        right_container = QWidget()
        right_content_layout = QVBoxLayout(right_container)
        right_content_layout.setContentsMargins(0, 0, 0, 0)
        right_content_layout.setSpacing(0)

        # A. Header
        self.header = Header()
        right_content_layout.addWidget(self.header)

        # B. Canvas (Páginas)
        self.Canvas = Canvas()
        right_content_layout.addWidget(self.Canvas)

        # Agregar el contenedor derecho al layout principal
        self.layout_main.addWidget(right_container)

        # 3. Conexión de Navegación Automática
        # Conexión directa: El Sidebar emite la instancia -> Canvas la muestra
        self.sidebar.action_navigate.connect(self.Canvas.set_current_page)

        # 4. Configuración
        self.config_window = Configuracion()
        self.sidebar.action_config.connect(self.show_config)

    def register_page(self, item: MenuItemProp) -> QWidget:
        """
        Registra una nueva página en el sistema de navegación de la aplicación.

        Este método realiza dos acciones principales:
        1. Crea un botón en el Sidebar utilizando las propiedades proporcionadas (texto, icono, sección).
        2. Agrega la instancia de la página al `QStackedWidget` del Canvas.

        Si es la primera página registrada, se establece automáticamente como la página visible.

        Args:
            item (MenuItemProp): Objeto que contiene la configuración de la página 
                                 (texto, icono, instancia de la página, sección).

        Returns:
            QWidget: La instancia de la página registrada. Útil para encadenar asignaciones.
        """
        # 1. Agregar botón al Sidebar
        self.sidebar.add_menu_item(item)

        # 2. Agregar página al Canvas
        self.Canvas.add_page(item.page_class)

        # Opcional: Establecer como actual si es la primera
        if self.Canvas.stack.count() == 1:
            self.Canvas.set_current_page(item.page_class)

        return item.page_class

    def navigate_to(self, page: QWidget):
        """
        Realiza la navegación programática a una página específica.

        Sincroniza el estado visual de la aplicación:
        1. Busca y selecciona el botón del Sidebar asociado a la instancia de la página.
        2. Cambia la página visible en el Canvas.

        Args:
            page (QWidget): La instancia de la página a la que se desea navegar.
                            Debe haber sido registrada previamente con `register_page`.
        """
        # 1. Sincronizar Sidebar
        self.sidebar.select_by_page_instance(page)
        
        # 2. Cambiar página
        self.Canvas.set_current_page(page)

    def register_config(self, name: str, widget: QWidget) -> QWidget:
        """
        Registra una página en la ventana de configuración.

        Args:
            name (str): Nombre visible en la lista lateral de configuración.
            widget (QWidget): Instancia de la página de configuración.

        Returns:
            QWidget: La misma instancia del widget, para encadenamiento.
        """
        self.config_window.add_config_page(name, widget)
        return widget

    def navigate_to_config(self, widget: QWidget):
        """
        Abre la ventana de configuración y navega a la página especificada.
        
        Args:
            widget (QWidget): La instancia de la página de configuración a mostrar.
        """
        # 1. Asegurar que la ventana es visible
        self.show_config()
        
        # 2. Buscar el índice del widget en el stack de config
        index = self.config_window.stack.indexOf(widget)
        
        if index >= 0:
            # 3. Seleccionar en la lista (esto dispara el cambio de página en el stack)
            self.config_window.list_menu.setCurrentRow(index)
        else:
            print(f"⚠️ Error: La página de configuración no fue encontrada en el stack.")

    def show_config(self):
        """Muestra la ventana de configuración o la trae al frente si ya existe."""
        if self.config_window.isVisible():
            # Si está minimizada, la restauramos
            if self.config_window.isMinimized():
                self.config_window.showNormal()
            
            self.config_window.raise_()
            self.config_window.activateWindow()
        else:
            self.config_window.show()

    def closeEvent(self, event):
        """Asegura que las ventanas hijas se cierren al cerrar la principal."""
        if self.config_window:
            self.config_window.close()
        super().closeEvent(event)
