from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("No API Key found")
    exit()

client = genai.Client(api_key=api_key)

print("Listando modelos del nuevo SDK:")
try:
    # La paginación en el nuevo SDK puede ser distinta, intentamos listar
    # Nota: client.models.list() devuelve un iterador/generador
    for m in client.models.list():
        # Imprimimos nombre para saber cuál usar
        print(f"- {m.name} (DisplayName: {m.display_name})")
except Exception as e:
    print(f"Error listando modelos: {e}")
