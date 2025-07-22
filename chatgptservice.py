import openai
import os

def GetResponse(text):
    try:
        # Configuración para OpenRouter.ai
        # La URL base de OpenRouter.ai
        openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        # Tu API Key de OpenRouter.ai
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        # El modelo a usar en OpenRouter.ai. Puedes cambiarlo por otros disponibles.
        # Por ejemplo: "mistralai/mistral-7b-instruct:free" o "google/gemini-pro"
        openrouter_model = os.environ.get("OPENROUTER_MODEL", "qwen/qwen3-235b-a22b-2507") 

        # Inicializa el cliente de OpenAI, pero apuntando a OpenRouter
        client = openai.OpenAI(
            base_url=openrouter_base_url,
            api_key=openrouter_api_key,
        )

        # Realiza la llamada a la API de chat completions
        result = client.chat.completions.create(
            model=openrouter_model,
            messages=[
                {"role": "user", "content": text}
            ],
            n=1,
            max_tokens=500
        )
        
        # Accede al contenido de la respuesta
        response = result.choices[0].message.content
        return response
    
    except openai.APIError as e:
        # Manejo de errores específicos de la API (ahora de OpenRouter)
        print(f"Error de la API de OpenRouter: {e}")
        return "Lo siento, hubo un problema con la API de OpenRouter."
    except Exception as e:
        # Otros errores inesperados
        print(f"Ocurrió un error inesperado: {e}")
        return "Lo siento, ocurrió un error inesperado."