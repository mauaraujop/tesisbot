import openai
import os

def GetResponse(text):
    try:
        openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        openrouter_model = os.environ.get("OPENROUTER_MODEL", "qwen/qwen3-235b-a22b-2507") 

        # --- NUEVAS LÍNEAS PARA DEPURACIÓN ---
        print(f"DEBUG: Intentando conectar a base_url: {openrouter_base_url}")
        print(f"DEBUG: Usando modelo: {openrouter_model}")
        # NO imprimas la API Key completa por seguridad, solo una parte si es necesario
        print(f"DEBUG: API Key (parcial): {openrouter_api_key[:5]}...") 
        # --- FIN NUEVAS LÍNEAS PARA DEPURACIÓN ---

        client = openai.OpenAI(
            base_url=openrouter_base_url,
            api_key=openrouter_api_key,
        )

        result = client.chat.completions.create(
            model=openrouter_model,
            messages=[
                {"role": "user", "content": text}
            ],
            n=1,
            max_tokens=500
        )

        response = result.choices[0].message.content
        return response

    except openai.APIError as e:
        print(f"Error de la API de OpenRouter: {e}")
        return "Lo siento, hubo un problema con la API de OpenRouter."
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return "Lo siento, ocurrió un error inesperado."
