import os
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


def get_icon_path(filename: str) -> str:
    # Reciclar lógica de ruta de iconos.
    # Podríamos mover esto a un utils.py pero por ahora lo duplicamos por simplicidad en el componente.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "assets", "icons", filename)


class Header(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        self.setObjectName("HeaderFrame")

        # Estilos visuales se definen en styles/style.qss usando #HeaderFrame

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)  # Margen izq/der
        layout.setSpacing(15)

        # 1. Izquierda: Título o Breadcrumb (Opcional, por ahora vacío o título dinámico)
        # Podríamos usar un StackedWidget aquí también para mostrar el título de la página activa
        self.page_title = QLabel("Dashboard")
        self.page_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #fff;")
        layout.addWidget(self.page_title)

        layout.addStretch()  # Espaciador para empujar lo demás a la derecha

        # 2. Centro/Derecha: Barra de Búsqueda
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar...")
        self.search_bar.setFixedWidth(250)
        # Icono de búsqueda (acción)
        # search_action = self.search_bar.addAction(QIcon(get_icon_path("search.svg")), QLineEdit.LeadingPosition)
        # QLineEdit.addAction es soportado en PySide6 recientes, probamos:
        try:
            self.search_bar.addAction(
                QIcon(get_icon_path("search.svg")), QLineEdit.LeadingPosition
            )
        except:
            pass  # Fallback si versión antigua

        layout.addWidget(self.search_bar)

        # 3. Iconos de Acción
        # Notificaciones
        btn_notif = QPushButton()
        btn_notif.setIcon(QIcon(get_icon_path("bell.svg")))
        btn_notif.setIconSize(QSize(20, 20))
        btn_notif.setFixedSize(32, 32)
        btn_notif.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_notif)

        # Ajustes (opcional)
        # btn_settings = QPushButton()
        # btn_settings.setIcon(QIcon(get_icon_path("settings.svg")))
        # btn_settings.setIconSize(QSize(20, 20))
        # btn_settings.setFixedSize(32, 32)
        # layout.addWidget(btn_settings)

        # Separador vertical pequeño
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFixedHeight(20)
        sep.setStyleSheet("color: rgba(255,255,255,0.2);")
        layout.addWidget(sep)

        # 4. Perfil de Usuario
        user_container = QWidget()
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(10)

        # Avatar (círculo)
        avatar = QLabel()
        avatar.setFixedSize(32, 32)
        avatar.setStyleSheet(
            """
            background-color: #3b82f6;
            border-radius: 16px;
            color: white;
            font-weight: bold;
        """
        )
        avatar.setText("JD")  # Initials
        avatar.setAlignment(Qt.AlignCenter)
        user_layout.addWidget(avatar)

        # Nombre
        lbl_name = QLabel("John Doe")
        lbl_name.setStyleSheet("color: #e5e5e5; font-size: 13px; font-weight: 500;")
        user_layout.addWidget(lbl_name)

        # Arrow icon (opcional)
        # lbl_arrow = QLabel("▼")
        # lbl_arrow.setStyleSheet("color: #aaa; font-size: 10px;")
        # user_layout.addWidget(lbl_arrow)

        layout.addWidget(user_container)
