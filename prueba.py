import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QLabel
)
from PySide6.QtCore import Qt


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selector estilizado - PySide6")
        self.resize(300, 150)

        layout = QVBoxLayout(self)

        label = QLabel("Seleccione una opción:")
        label.setAlignment(Qt.AlignLeft)

        selector = QComboBox()
        selector.addItems([
            "Opción 1",
            "Opción 2",
            "Opción 3",
            "Opción 4"
        ])

        selector.setStyleSheet("""
            QComboBox {
                background-color: #2c2c2c;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 6px 10px;
            }

            QComboBox:hover {
                border: 1px solid #1e90ff;
            }

            QComboBox::drop-down {
                border: none;
                width: 24px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #ffffff;
                margin-right: 6px;
            }

            QComboBox QAbstractItemView {
                background-color: #2c2c2c;
                color: #ffffff;
                selection-background-color: #1e90ff;
                border: 1px solid #555555;
            }
        """)

        layout.addWidget(label)
        layout.addWidget(selector)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
