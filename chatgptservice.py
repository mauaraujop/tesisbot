import os
from groq import Groq # Importamos la clase Groq directamente

def GetResponse(text):
    try:
        # Tu API Key de Groq (la obtendrás de las variables de entorno)
        groq_api_key = os.environ.get("GROQ_API_KEY")
        
        # El modelo de Groq a usar (Mixtral 8x7b es muy popular por su velocidad)
        # Puedes ver otros modelos en console.groq.com/docs/models
        groq_model = os.environ.get("GROQ_MODEL", "llama3-8b-8192") 

        # Inicializa el cliente de Groq
        client = Groq(api_key=groq_api_key)

        # --- NUEVAS LÍNEAS PARA DEPURACIÓN ---
        print(f"DEBUG: Intentando conectar a Groq. Usando modelo: {groq_model}")
        if groq_api_key:
            print(f"DEBUG: API Key Groq (parcial): {groq_api_key[:5]}...") 
        else:
            print("DEBUG: API Key Groq no cargada (es None).")
        # --- FIN NUEVAS LÍNEAS PARA DEPURACIÓN ---

        # Realiza la llamada a la API de chat completions de Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model=groq_model,
            temperature=0.7, # Puedes ajustar la creatividad del modelo
            max_tokens=500,
            top_p=1,
            stop=None,
            stream=False, # No usaremos streaming por ahora
        )
        
        # Accede al contenido de la respuesta
        response = chat_completion.choices[0].message.content
        return response
    
    except Exception as e:
        # Groq no tiene un 'APIError' específico como OpenAI, así que capturamos Exception
        print(f"Ocurrió un error al conectar con Groq o procesar la respuesta: {e}")
        return "Lo siento, hubo un problema al procesar tu solicitud con Groq."