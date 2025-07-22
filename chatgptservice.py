import openai
import os

def GetResponse(text):
    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        result = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text}
            ],
            n=1,
            max_tokens=500
        )
        
        response = result.choices[0].message.content
        return response
    
    except openai.APIError as e:
        print(f"Error de la API de OpenAI: {e}")
        return "Lo siento, hubo un problema con la API de OpenAI."
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return "Lo siento, ocurrió un error inesperado."
