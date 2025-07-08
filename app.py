from flask import Flask, request
import util
import whatsappservice

# --- ALMACENAMIENTO DE ESTADOS (GLOBAL) ---
user_states = {}

app = Flask(__name__)
@app.route('/welcome', methods=['GET'])
def index():
    return "welcome developer"

@app.route('/whatsapp', methods=['GET'])
def VerifyToken():
    try:
        accessToken = "341894BASDASD"
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token is not None and challenge is not None and token == accessToken: # Cambié "is None" por "!=" y "is not None"
            return challenge
        else:
            return "", 400
    except Exception as e:
        print(f"Error en VerifyToken: {e}")
        return "", 400
    
@app.route('/whatsapp', methods=['POST'])
def ReceivedMessage():
    try:
        body = request.get_json()
        
        # Depuración: Imprime el cuerpo completo del webhook
        print("Cuerpo del Webhook recibido:", body)

        # Aquí asumimos la estructura del webhook de texto y extraemos directamente
        # Solo entramos si hay una entrada, un cambio, un valor y un mensaje de tipo 'text'.
        # Es menos robusto si WhatsApp cambia la estructura o envía otros tipos de mensajes.
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if messages and messages[0].get("type") == "text":
            message_payload = messages[0]
            number = message_payload["from"]
            text_body = util.GetTextUser(message_payload) # Asumo que GetTextUser maneja el payload completo
            
            ProcessTextMessageWithState(text_body, number) # Llamamos a la función que solo maneja texto con estados
            print(f"Texto procesado: {text_body}")
        else:
            # Si el mensaje no es de tipo 'text' o no tiene la estructura esperada,
            # aún así debes devolver 200 OK para evitar reintentos.
            print("DEBUG: Mensaje recibido no es de tipo texto o no tiene la estructura esperada.")
        
        return "EVENT_RECEIVED" 
    except Exception as e:
        print(f"Error en ReceivedMessage: {e}")
        # Si ocurre un error, aún debes devolver 200 OK para evitar reintentos de WhatsApp
        return "EVENT_RECEIVED" 
    
def ProcessTextMessageWithState(text, number):
    text_lower = text.lower() # Convertimos el texto a minúsculas una sola vez
    responses_to_send = [] # Lista para recolectar las respuestas
    
    # 1. Obtener el estado actual del usuario (o establecer un predeterminado)
    current_state = user_states.get(number, "main_menu") 
    print(f"DEBUG: Usuario {number} en estado: {current_state}, Texto: '{text}'")

    # --- LÓGICA DE PROCESAMIENTO BASADA EN EL ESTADO ACTUAL ---

    # Estado: Menú Principal
    if current_state == "main_menu":
        if "hola" in text_lower or "menu" in text_lower:
            responses_to_send.append(util.TextMessage("👋 ¡Hola! Soy tu asistente virtual de OFICOMP, listo para ayudarte con todo lo que tu oficina necesita. ¿En qué puedo asistirte hoy? Escribe 'Menú' para ver mis opciones o hazme una pregunta. ✨", number))
            responses_to_send.append(util.ListMessage(number)) # Aunque el usuario solo escriba texto, puedes enviarle una lista.
            # No cambiamos el estado, ya estamos en el menú principal
        elif "gracias" in text_lower:
            responses_to_send.append(util.TextMessage("¡De nada! En OFICOMP estamos para servirte. ¿Hay algo más en lo que pueda ayudarte?'. ", number))
        elif "format" in text_lower:
            responses_to_send.append(util.TextFormatMessage(number))
        elif "audio" in text_lower: 
            responses_to_send.append(util.AudioMessage(number))
        elif "image" in text_lower: 
            responses_to_send.append(util.ImageMessage(number))
        elif "list" in text_lower: # Si el usuario escribe "list" (para ver la lista principal)
            responses_to_send.append(util.ListMessage(number))
            # Aquí podrías considerar cambiar el estado si quieres que las respuestas a la lista sean contextuales
            # user_states[number] = "esperando_seleccion_lista_principal"
        elif "button" in text_lower: # Si el usuario escribe "button"
            responses_to_send.append(util.ButtonsnMessage(number))
        elif "ubicación" in text_lower:
            responses_to_send.append(util.LocationMessage(number))
        
        # Nueva lógica para ir a sub-menú de inventario
        elif "inventario" in text_lower or "productos" in text_lower:
            responses_to_send.append(util.TextMessage("Perfecto, estás en la sección de Inventario de Productos. ¿Qué tipo de producto buscas? Puedes escribir el nombre, por ejemplo: 'Engrapadoras', 'Archivadores'.", number))
            user_states[number] = "inventario_subcategorias" # ¡CAMBIAMOS EL ESTADO!

        else:
            responses_to_send.append(util.TextMessage("*¡Vaya!* No consigo entender a qué te refieres 😢 .\n\nAquí tienes algunos de los temas en los que puedo ayudarte:\n👉 *Hola*\n👉 *Gracias*", number))
            responses_to_send.append(util.ListMessage(number)) # Reenviar el menú principal para guiar

    # Estado: Dentro de "Inventario de Productos"
    elif current_state == "inventario_subcategorias":
        if "engrapadora" in text_lower:
            responses_to_send.append(util.TextMessage("¡Claro! Tenemos varios tipos de engrapadoras: [Tipos de engrapadoras]", number))
            # Si esto lleva a un nuevo sub-submenú, cambiarías el estado aquí.
            # user_states[number] = "tipos_engrapadoras"
        elif "archivador" in text_lower:
            responses_to_send.append(util.TextMessage("Aquí están los archivadores disponibles: [Tipos de archivadores]", number))
        elif "blocks" in text_lower:
            responses_to_send.append(util.TextMessage("Aquí están los blocks disponibles: [Tipos de blocks]", number))
        # Agrega más condiciones para el resto de tus productos de inventario aquí
        # ...
        elif "menu principal" in text_lower or "volver" in text_lower or "atras" in text_lower: 
            responses_to_send.append(util.TextMessage("Volviendo al menú principal.", number))
            responses_to_send.append(util.ListMessage(number)) # Reenviar el menú principal
            user_states[number] = "main_menu" # CAMBIA EL ESTADO DE VUELTA
        else:
            responses_to_send.append(util.TextMessage("Estoy en la sección de inventario. Por favor, especifica un producto (ej. 'Engrapadoras', 'Archivadores') o escribe 'menu principal' para volver.", number))
            # Podrías aquí incluso listar los productos de inventario disponibles para guiar.

    # Puedes añadir más estados si tu bot tiene más flujos de conversación basados solo en texto
    # elif current_state == "otro_flujo_texto":
    #    ...
    
    # 2. Enviar todas las respuestas recolectadas
    for item in responses_to_send:
        whatsappservice.SendMessageWhatsapp(item)

    # 3. Imprimir el estado final para depuración
    print(f"DEBUG: Nuevo estado para {number}: {user_states.get(number, 'main_menu')}")


# --- Bloque de ejecución principal de Flask ---
if __name__ == "__main__":
    app.run(debug=True)

