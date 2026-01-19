from google import genai
import os
from dotenv import load_dotenv

class GenAIService:
    """
    Servicio wrapper para interactuar con Google Generative AI (Gemini) usando el SDK google-genai (v1.0+).
    """

    def __init__(self, api_key: str = None):
        """
        Inicializa el servicio.
        Si no se pasa api_key, intenta cargarla desde variables de entorno (GOOGLE_API_KEY).
        """
        load_dotenv()

        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print(
                "⚠️ Advertencia: No se encontró GOOGLE_API_KEY en variables de entorno."
            )
            self.client = None
        else:
            # Inicializar cliente con el nuevo SDK
            self.client = genai.Client(api_key=self.api_key)

        # Modelo recomendado y actual (Flash es más rápido para chat)
        self.model_name = "gemini-2.0-flash-exp"

    def generate_text(self, prompt: str) -> str:
        """
        Genera texto basado en un prompt simple.
        """
        if not self.client:
            return "Error: API Key no configurada."

        try:
            # API nuevo SDK: client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generando contenido: {str(e)}"

    def chat_session(self):
        """
        Inicia una sesión de chat (con historia).
        """
        if not self.client:
            raise ValueError("API Key no configurada")
        
        # API nuevo SDK: client.chats.create
        return self.client.chats.create(model=self.model_name)
