from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt

class GeneralConfigPage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Configuración General")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Opciones de ejemplo
        self.check_updates = QCheckBox("Buscar actualizaciones automáticamente")
        self.check_updates.setChecked(True)
        layout.addWidget(self.check_updates)
        
        self.check_analytics = QCheckBox("Enviar datos de uso anónimos")
        layout.addWidget(self.check_analytics)
        
        layout.addStretch()
