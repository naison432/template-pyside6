"""Interfaz principal de la app"""

# 1. QtWidgets
from PySide6.QtWidgets import (  # pylint: disable=no-name-in-module, unused-import # noqa
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
    QStackedWidget,
    QButtonGroup,
)
from PySide6.QtGui import (  # pylint: disable=no-name-in-module, unused-import # noqa
    QIcon,
)

# 2. QtCore
from PySide6.QtCore import (  # pylint: disable=no-name-in-module, unused-import # noqa
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QSize,
)

from components.Sidebar import Sidebar
from components.Canvas import Canvas
from components.Header import Header
from components.Configuracion import Configuracion


class Interface(QMainWindow):
    def __init__(self):
        """
        Inicializa la ventana principal de la app
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
        # DEPRECATED for Lazy Loading: La conexión ahora la gestiona el Puppet Master (main.py)
        # self.sidebar.action_navigate.connect(self.Canvas.set_current_page)

        # 4. Configuración
        self.config_window = Configuracion()
        self.sidebar.action_config.connect(self.show_config)

    def register_page(self, widget: QWidget) -> QWidget:
        """
        Registra una página en el stack del Canvas.
        Retorna la misma instancia para facilitar asignación.
        Si es la primera página, se establece como visible por defecto.
        """
        self.Canvas.add_page(widget)

        # Opcional: Si es la única página, establecerla como actual
        if self.Canvas.stack.count() == 1:
            self.Canvas.set_current_page(widget)

        return widget

    def set_menu_options(self, fixed_items: list, scroll_items: list):
        """
        Configura las opciones del menú del Sidebar.
        Wrapper para no exponer self.sidebar directamente.
        """
        self.sidebar.setup_menu(fixed_items, scroll_items)

    def show_config(self):
        """Muestra la ventana de configuración o la trae al frente si ya existe."""
        if self.config_window.isVisible():
            self.config_window.raise_()
            self.config_window.activateWindow()
        else:
            self.config_window.show()

    def closeEvent(self, event):
        """Asegura que las ventanas hijas se cierren al cerrar la principal."""
        if self.config_window:
            self.config_window.close()
        super().closeEvent(event)
