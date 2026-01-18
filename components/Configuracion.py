from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
    QListWidget, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt, QSize

class Configuracion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración")
        self.setMinimumSize(600, 400) 
        
        # Layout Principal Horizontal (Menú Izq | Contenido Der)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. PANEL IZQUIERDO (Categorías)
        self.list_menu = QListWidget()
        self.list_menu.setFixedWidth(150)
        # self.list_menu.addItems(...) -> Se agregan dinámicamente
        self.list_menu.setObjectName("ConfigSidebar")
        
        # Estilos visuales se definen en style.qss bajo #ConfigSidebar
        
        main_layout.addWidget(self.list_menu)

        # 2. PANEL DERECHO (Stack de Páginas)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: transparent;") # Usa el fondo de la ventana
        main_layout.addWidget(self.stack)
        
        # Lógica de Cambio
        self.list_menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        
        # Estilo Global del Widget (se define en style.qss por #ConfigWindow si se desea)
        self.setObjectName("ConfigWindow")

    def add_config_page(self, name: str, widget: QWidget):
        """
        Agrega una página de configuración dinámicamente.
        """
        # 1. Agregar al menú lateral
        self.list_menu.addItem(name)
        
        # 2. Agregar al stack de contenido
        self.stack.addWidget(widget)
        
        # Si es la primera página, seleccionarla por defecto
        if self.list_menu.count() == 1:
            self.list_menu.setCurrentRow(0)
