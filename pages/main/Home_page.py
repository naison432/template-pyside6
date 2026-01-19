from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Título de Bienvenida
        title_label = QLabel("Bienvenido al Template PySide6")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #ffffff;")  # Asegurar contraste

        # Subtítulo / Descripción
        subtitle_label = QLabel(
            "Esta es una plantilla base limpia lista para tu nuevo proyecto.\n"
            "Arquitectura 'Puppet Master' configurada y lista."
        )
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #a1a1aa;")

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
