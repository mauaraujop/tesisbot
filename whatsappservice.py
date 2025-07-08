import requests 
import json

def SendMessageWhatsapp(data):
    try:
        print("1")
        token = "EAAeHBvAiNDEBOZCjoER7ClNrc5PZBjGelEDq2FSJxVbdRLU4D7IbC62a1li7V0UoZCEdLUJrjWMqrIKxiNZCqM9BSVQihzcoZAtLMtr1R7BEZBKUxrpgBduZB4rLx0NNQVqArZBRiZADwLdquUGP2QNrwaiRxtZBzggoioT4rwgvvttado8ZBc5eF3L1HDk0ZCaPaZAdz9AZDZD"
        print("2")
        api_url = "https://graph.facebook.com/v22.0/580401805166017/messages"
        
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        print("5")
        response = requests.post(api_url, data = json.dumps(data), headers = headers)

        # >>>>>>>>>>> ESTAS SON LAS LÍNEAS CLAVE QUE DEBES AÑADIR <<<<<<<<<<<
        if response.status_code == 200:
            print(f"DEBUG: Mensaje enviado con ÉXITO. Tipo de mensaje: {data.get('type', 'desconocido')}, Status: {response.status_code}")
            return True
        else:
            # Aquí es donde verás el error si WhatsApp rechaza el mensaje de botón
            print(f"DEBUG: ERROR al enviar mensaje. Status: {response.status_code}, Cuerpo de la respuesta: {response.text}")
            print(f"DEBUG: JSON del mensaje fallido: {json.dumps(data, indent=2)}") # Esto te mostrará el JSON exacto que enviaste
            return False
    except Exception as exception:
        print(f"DEBUG: EXCEPCIÓN al enviar mensaje: {exception}") # Cambiado para que muestre "DEBUG"
        return False
