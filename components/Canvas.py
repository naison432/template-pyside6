"""marco: QFrame ,  marco del sidebar"""

# 1. QtWidgets
from PySide6.QtWidgets import (  # pylint: disable=no-name-in-module, unused-import # noqa
    QFrame,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QScrollArea,
    QStackedWidget,
)

# 2. QtCore
from PySide6.QtCore import (  # pylint: disable=no-name-in-module, unused-import # noqa
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    Property,
    Signal,
    QSize,
)

from PySide6.QtGui import (  # pylint: disable=no-name-in-module, unused-import # noqa
    QIcon,
)

from pages.Home_page import HomePage


class Canvas(QFrame):
    """es el marco de trabajo y hereda de QFrame ."""

    def __init__(self):
        # 1. self:Canvas = QFrame:
        super().__init__()

        # propiedades:
        self.setObjectName("QCanvas")  # id para los estilos
        # El canvas crece automáticamente por defecto en un HBox si el otro es fijo,

        # 1. Crear el layout para el QFrame
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 2. Configurar Área de Scroll (Contenedor principal)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")

        # 3. StackedWidget (Pila de páginas)
        self.stack = QStackedWidget()  # Necesita importar QStackedWidget

        # 4. Asignar Stack al ScrollArea
        self.scroll_area.setWidget(self.stack)

        # 5. Agregar al layout
        layout.addWidget(self.scroll_area)

    def add_page(self, widget: QWidget):
        """Agrega una página a la pila."""
        self.stack.addWidget(widget)

    def set_current_page(self, widget: QWidget):
        """Cambia la página visible."""
        self.stack.setCurrentWidget(widget)
