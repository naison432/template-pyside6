"""
Componente principal del Sidebar.
Maneja la lógica de navegación, animación de colapso/expansión y layout de botones.
"""

import os

from dataclasses import dataclass
from typing import Literal

# 1. QtWidgets
from PySide6.QtWidgets import (  # pylint: disable=no-name-in-module, unused-import # noqa
    QFrame,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QScrollArea,
    QSizePolicy,
    QButtonGroup,
)

# 2. QtCore
from PySide6.QtCore import (  # pylint: disable=no-name-in-module, unused-import # noqa
    Qt,
    QVariantAnimation,
    QEasingCurve,
    QSize,
    Signal,
)

from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QPainter,
    QColor,
)


@dataclass
class MenuItemProp:
    """Estructura de datos para ítems del menú"""

    text: str  # Texto visible
    icon: str  # Nombre del archivo de icono
    page_class: QWidget  # instancia
    section: Literal["scroll", "fixed"] = (
        "scroll"  # valores opcionales: 'fixed' o 'scroll'
    )


# Helpers
def get_icon_path(filename: str) -> str:
    """Retorna la ruta absoluta al icono."""
    # Sidebar.py está en components/, así que subimos un nivel para llegar a la raíz
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "assets", "icons", filename)


class SidebarButton(QPushButton):
    """
    Clase base para botones del sidebar con estilos comunes
    """

    def __init__(self, icon_svg: str, text: str = ""):
        super().__init__()
        self.setObjectName("BtnSidebar")
        self.icon_path = get_icon_path(icon_svg)

        # Propiedades Visuales
        self.setIconSize(QSize(24, 24))
        self.setFixedHeight(48)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)  # Necesario para selección exclusiva en grupo

        if text:
            self.setText(text)

        # 2. Carga inicial
        self.setIcon(QIcon(self.icon_path))


class MenuButton(SidebarButton):
    """Botón de hamburguesa para colapsar/expandir el menú."""

    def __init__(self):
        super().__init__(icon_svg="menu_open.svg")
        self.setFixedWidth(44)
        self.setCheckable(False)  # El botón de menú no debe quedarse presionado


# ===============================
# SCROLL AREA
# ===============================


class SidebarContentWidget(QWidget):
    """
    Widget contenedor que va dentro del ScrollArea.
    Contiene la lista dinámica de opciones.
    """

    def __init__(self):
        super().__init__()

        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetLayout.setSpacing(0)
        self.widgetLayout.addStretch()


class SidebarScrollArea(QScrollArea):
    """
    Área de desplazamiento personalizada para la lista de opciones.
    """

    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar_ScrollArea")
        self.setWidgetResizable(
            True
        )  # CRÍTICO: Permite que el contenido se expanda al ancho del área

        self.widgetContent = SidebarContentWidget()
        self.setWidget(self.widgetContent)

        # ID para estilos específicos si es necesario
        self.widgetContent.setObjectName("ContentWidget")


class ConfigButton(SidebarButton):
    """Botón de configuración situado en la parte inferior."""

    def __init__(self):
        super().__init__("settings.svg", "Configuration")
        self.setCheckable(
            False
        )  # Configuración es un modal, no una opción de navegación


class Sidebar(QFrame):
    # Señal para navegación (envía la instancia de la página o una KEY para lazy loading)
    action_navigate = Signal(object)
    # Señal para abrir configuración
    action_config = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebarContainer")

        # Propiedades de ancho
        self.minWidth = 60
        self.maxWidth = 200
        self.setFixedWidth(200)

        self.isAnimating = False

        # Layout principal
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setObjectName("sidebar_content")
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

        # 1. Botón Menú (Colapso)
        self.btnMenu = MenuButton()
        self.btnMenu.clicked.connect(self.handleCollapse)
        self.mainLayout.addWidget(self.btnMenu)

        # Grupo de botones para selección exclusiva
        self.btnGroup = QButtonGroup(self)
        self.btnGroup.setExclusive(True)

        # Contenedor para botones fijos
        self.fixedLayout = QVBoxLayout()
        self.fixedLayout.setSpacing(10)
        self.mainLayout.addLayout(self.fixedLayout)

        # --------------------------------------------------

        # 3. Área de Scroll (Lista de opciones dinámica)
        self.scrollArea = SidebarScrollArea()
        self.mainLayout.addWidget(self.scrollArea, 1)  # stretch priority 1

        # 4. Spacer Widget
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.spacer.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.mainLayout.addWidget(self.spacer)
        self.spacer.hide()

        # 5. Botón Configuración
        self.btnConfig = ConfigButton()
        self.btnConfig.clicked.connect(self.action_config.emit)  # Conectar señal
        self.mainLayout.addWidget(self.btnConfig)

    def add_menu_item(self, item: MenuItemProp):
        """
        Agrega un botón al menú (Fixed o Scroll) y conecta la navegación.
        """
        # 1. Crear botón
        btn = SidebarButton(item.icon, item.text)
        # GUARDAR REFERENCIA PARA PROGRAMMATIC SELECTION
        btn._page_instance = item.page_class
        self.btnGroup.addButton(btn)
        
        # Selección visual por defecto (si es el primero)
        if len(self.btnGroup.buttons()) == 1:
            btn.setChecked(True)

        # 2. Agregar al layout correspondiente
        if item.section == "fixed":
            self.fixedLayout.addWidget(btn)
        else:
            # Para scroll, acceder al layout interno
            scroll_layout = self.scrollArea.widgetContent.widgetLayout
            # Insertar antes del stretch (que está al final)
            # count() - 1 asumiendo que el último es el spacer/stretch
            # Si no hay stretch, addWidget funciona igual.
            # Verificamos si ya hay items para insertar antes del stretch
            count = scroll_layout.count()
            if count > 0:
                # Insertar en penúltima posición (antes del stretch)
                scroll_layout.insertWidget(count - 1, btn)
            else:
                scroll_layout.addWidget(btn)

        # 3. Conexión de señal
        # Emitimos la instancia de la página directamente
        btn.clicked.connect(lambda: self.action_navigate.emit(item.page_class))

    def select_by_page_instance(self, page_instance):
        """
        Busca el botón asociado a esta instancia y lo marca como checked.
        """
        for btn in self.btnGroup.buttons():
            if getattr(btn, "_page_instance", None) == page_instance:
                btn.setChecked(True)
                return



    def handleCollapse(self):
        """
        Maneja la animación de colapso y expansión del sidebar.
        Usa QVariantAnimation para modificar setFixedWidth directamente,
        asegurando que el layout se fuerce a adaptar.
        """
        if self.isAnimating:
            return

        self.isAnimating = True
        currentWidth = self.width()

        # 1. Antes de animar: Asegurar que NO haya scroll horizontal
        # Esto evita que aparezca la barra fea mientras se encoge
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Determinar Ancho Objetivo
        if currentWidth > 64:
            # COLAPSANDO
            targetWidth = 64
            self.scrollArea.hide()
            self.spacer.show()
            self.btnMenu.setIcon(QIcon(get_icon_path("menu.svg")))
        else:
            # EXPANDIENDO
            targetWidth = 200
            # Preparamos UI para expandir
            self.spacer.hide()
            self.scrollArea.show()
            self.btnMenu.setIcon(QIcon(get_icon_path("menu_open.svg")))
            # Opcional: Si quisieras scroll horizontal al expandir, lo activas aquí.
            # Pero para un sidebar limpio, mejor dejarlo off siempre o AsNeeded.
            # self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Configurar QVariantAnimation
        self.animation = QVariantAnimation()
        self.animation.setStartValue(currentWidth)
        self.animation.setEndValue(targetWidth)
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        # Conectar el cambio de valor al resize
        self.animation.valueChanged.connect(self.setFixedWidth)

        # Cleanup al finalizar
        def onFinished():
            self.isAnimating = False
            self.setFixedWidth(targetWidth)  # Asegurar valor final

        self.animation.finished.connect(onFinished)
        self.animation.start()
