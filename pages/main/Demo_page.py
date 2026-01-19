import logging
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QProgressBar,
)
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QFont

# Importamos el servicio
from services.genai_service import GenAIService

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)


class ChatWorker(QThread):
    """
    Worker thread to handle API calls asynchronously.
    """

    response_received = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, chat_session, text):
        super().__init__()
        self.chat_session = chat_session
        self.text = text

    def run(self):
        try:
            # Enviar mensaje usando la sesión de chat (mantiene historial)
            response = self.chat_session.send_message(self.text)
            self.response_received.emit(response.text)
        except Exception as e:
            self.error_occurred.emit(str(e))


class DemoPage(QWidget):
    def __init__(self):
        super().__init__()

        # --- Configuración del Servicio ---
        try:
            self.service = GenAIService()
            self.chat_session = self.service.chat_session()
            self.service_ready = True
        except Exception as e:
            self.service_ready = False
            logging.error(f"Error initializing GenAI: {e}")

        # --- UI Setup ---
        self.setup_ui()

        if not self.service_ready:
            self.append_system_message(
                "Error: No se pudo conectar con el servicio de IA (verifica tu API Key)."
            )
        else:
            self.append_system_message("¡Hola! Soy Gemini. ¿En qué puedo ayudarte hoy?")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título
        title = QLabel("Chat con Gemini AI")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        # Área de Historial del Chat
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet(
            """
            QTextEdit {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
        """
        )
        layout.addWidget(self.chat_history)

        # Barra de progreso (indeterminado)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminado
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Área de Entrada
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe tu mensaje aquí...")
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                padding: 8px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #1e1e1e;
                color: white;
            }
        """
        )
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Enviar")
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #555;
            }
        """
        )
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(input_layout)

    def send_message(self):
        if not self.service_ready:
            return

        text = self.input_field.text().strip()
        if not text:
            return

        # UI Updates
        self.append_user_message(text)
        self.input_field.clear()
        self.input_field.setDisabled(True)
        self.send_btn.setDisabled(True)
        self.progress_bar.show()

        # Start Worker
        self.worker = ChatWorker(self.chat_session, text)
        self.worker.response_received.connect(self.on_response_received)
        self.worker.error_occurred.connect(self.on_error_occurred)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    @Slot(str)
    def on_response_received(self, response_text):
        self.append_ai_message(response_text)

    @Slot(str)
    def on_error_occurred(self, error_text):
        self.append_system_message(f"Error: {error_text}")

    @Slot()
    def on_worker_finished(self):
        self.input_field.setDisabled(False)
        self.send_btn.setDisabled(False)
        self.input_field.setFocus()
        self.progress_bar.hide()

    def append_user_message(self, text):
        formatted = f"""
        <div style="margin-bottom: 10px; text-align: right;">
            <span style="background-color: #0078d4; color: white; padding: 5px 10px; border-radius: 10px;">
                <b>Tú:</b> {text}
            </span>
        </div>
        """
        self.chat_history.append(formatted)

    def append_ai_message(self, text):
        # Convert markdown-like breaks to html if needed, but simple text works
        text = text.replace("\n", "<br>")
        formatted = f"""
        <div style="margin-bottom: 15px; text-align: left;">
            <span style="background-color: #3d3d3d; color: #e0e0e0; padding: 5px 10px; border-radius: 10px;">
                <b>Gemini:</b> {text}
            </span>
        </div>
        """
        self.chat_history.append(formatted)

    def append_system_message(self, text):
        formatted = f"""
        <div style="margin-bottom: 10px; text-align: center; color: #888;">
            <i>{text}</i>
        </div>
        """
        self.chat_history.append(formatted)
