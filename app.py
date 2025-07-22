from flask import Flask, request
import util
import whatsappservice
import chatgptservice
import os # Importar os para acceder a variables de entorno

app = Flask(__name__)

# La ruta de bienvenida para verificar que el servidor está funcionando
@app.route('/welcome', methods=['GET'])
def index():
    return "welcome developer"

# Ruta para la verificación del token de WhatsApp (GET)
@app.route('/whatsapp', methods=['GET'])
def VerifyToken():
    try:
        # Es MUY recomendable que este token también sea una variable de entorno
        # Por ejemplo: accessToken = os.environ.get("VERIFY_TOKEN")
        accessToken = "341894BASDASD" # Tu token de verificación de WhatsApp
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token is not None and challenge is not None and token == accessToken:
            return challenge
        else:
            return "", 400
    except Exception as e: # Captura la excepción para depuración (CAMBIO: Añadido manejo de excepción)
        print(f"Error en VerifyToken: {e}") # (CAMBIO: Añadido print para depuración)
        return "", 400

# Ruta para recibir mensajes de WhatsApp (POST)
@app.route('/whatsapp', methods=['POST'])
def ReceivedMessage():
    try:
        body = request.get_json()
        
        # Imprime el cuerpo completo para depuración (opcional, puedes quitarlo después) (CAMBIO: Añadido print para depuración)
        print(f"Cuerpo del mensaje recibido: {body}")

        # Extrae la información del mensaje
        entry = (body["entry"])[0]
        changes = (entry["changes"])[0]
        value = changes["value"]
        
        # Asegúrate de que haya mensajes en el valor (CAMBIO: Añadida verificación de 'messages' en el payload)
        if "messages" not in value:
            print("No hay mensajes en el valor recibido.") # (CAMBIO: Añadido print para depuración)
            return "EVENT_RECEIVED" # Devuelve 200 OK para WhatsApp

        message = (value["messages"])[0]
        number = message["from"]
        
        # --- CAMBIO CLAVE: Manejo de diferentes tipos de mensajes ---
        text = "" # Inicializa text
        if message["type"] == "text":
            text = util.GetTextUser(message)
            print(f"DEBUG: Mensaje de texto recibido de {number}: '{text}'")
        elif message["type"] == "interactive":
            # Si es un mensaje interactivo, extrae el título de la opción seleccionada
            if "list_reply" in message["interactive"]:
                text = message["interactive"]["list_reply"]["title"]
                print(f"DEBUG: Opción de lista interactiva recibida de {number}: '{text}'")
            elif "button_reply" in message["interactive"]:
                text = message["interactive"]["button_reply"]["title"]
                print(f"DEBUG: Opción de botón interactivo recibida de {number}: '{text}'")
            else:
                print(f"DEBUG: Tipo de mensaje interactivo no reconocido: {message['interactive']['type']}")
                # Puedes enviar un mensaje de error o simplemente ignorarlo
                return "EVENT_RECEIVED"
        else:
            # Manejar otros tipos de mensajes (ej. imágenes, audios)
            print(f"DEBUG: Tipo de mensaje no soportado: {message['type']}")
            # Opcional: enviar un mensaje al usuario diciendo que no soportas ese tipo de mensaje
            data = util.TextMessage("Lo siento, solo puedo responder a mensajes de texto y opciones de menú por ahora.", number)
            whatsappservice.SendMessageWhatsapp(data)
            return "EVENT_RECEIVED" # No procesar más si el tipo no es texto/interactivo
        # --- FIN CAMBIO CLAVE ---

        # 1. Intentar procesar el mensaje con la lógica de palabras clave
        # La función ProcessMessage ahora devuelve True si maneja el mensaje, False si no.
        message_handled_by_keywords = ProcessMessage(text, number)

        # 2. Si las palabras clave no manejaron el mensaje, entonces llamar al modelo de lenguaje (Groq)
        if not message_handled_by_keywords:
            print(f"DEBUG: No se encontró palabra clave. Llamando al modelo de lenguaje para: {text}")
            responseLLM = chatgptservice.GetResponse(text)
            
            if responseLLM != "error":
                data = util.TextMessage(responseLLM, number)
            else:
                data = util.TextMessage("Lo siento, ocurrió un problema al obtener la respuesta del asistente. Por favor, inténtalo de nuevo más tarde.", number)
            
            whatsappservice.SendMessageWhatsapp(data)

        return "EVENT_RECEIVED"
    except Exception as e:
        # Captura cualquier excepción no manejada y la imprime para depuración
        print(f"Error general en ReceivedMessage: {e}")
        return "EVENT_RECEIVED" # Siempre devuelve 200 OK para WhatsApp, incluso en error

# Función para procesar mensajes basados en palabras clave
def ProcessMessage(text, number):
    text_lower = text.lower() # Convertir a minúsculas una vez
    listData = []
    handled = False # Bandera para indicar si el mensaje fue manejado por una palabra clave
    
    # --- NUEVAS LÍNEAS PARA DEPURACIÓN DE INVENTARIO ---
    print(f"DEBUG: Texto en ProcessMessage: '{text_lower}'")
    # --- FIN NUEVAS LÍNEAS PARA DEPURACIÓN ---

    # Lógica de palabras clave
    if "hola" in text_lower or "opcion" in text_lower or "menú" in text_lower:
        data = util.TextMessage("👋 ¡Hola! Soy tu asistente virtual de OFICOMP, listo para ayudarte con todo lo que tu oficina necesita. ¿En qué puedo asistirte hoy? Escribe 'Menú' para ver mis opciones o hazme una pregunta. ✨", number)
        dataMenu = util.ListMessage(number)
        listData.append(data)
        listData.append(dataMenu)
        handled = True
    elif "ver inventario" in text_lower or "inventario" in text_lower: # CAMBIO: Añadido "ver inventario" para la opción del menú
        print("DEBUG: Coincidencia con 'inventario' o 'ver inventario'. Preparando mensajes de categorías.")
        data = util.TextMessage("¿Qué quieres conocer sobre nuestras categorías de productos?\nElige una opción 👇:\n\nAquí tienes nuestras categorías de productos:\n\n1️⃣ Accesorios\n2️⃣ Almohadillas\n3️⃣ Archivadores\n4️⃣ Blocks\n5️⃣ Bolígrafos\n6️⃣ Borradores\n7️⃣ Cajas Chicas\n8️⃣ Carpetas\n9️⃣ Carteleras\n🔟 Chinches\n1️⃣1️⃣ Cintas\n1️⃣2️⃣ Clips\n1️⃣3️⃣ Compases\n1️⃣4️⃣ Correctores\n1️⃣5️⃣ Creyones\n1️⃣6️⃣ Cuchillas\n1️⃣7️⃣ Sobres\n1️⃣8️⃣ Engrapadoras\n1️⃣9️⃣ Tirros\n2️⃣0️⃣ Fichas", number)
        listData.append(data)
        handled = True
    elif "contáctanos" in text_lower: # CAMBIO: Añadido para la opción del menú
        data = util.TextMessage("¡Hola! 😊\n\nSi necesitas hablar directamente con uno de nuestros asesores para resolver dudas o recibir atención personalizada, haz clic en el siguiente enlace y tu mensaje se enviará automáticamente:\n\n📞 Chatea con un Asesor OFICOMP aquí:\nhttps://wa.me/584147171542?text=Hola%2C%20ten%C3%ADa%20una%20duda%20con%20respecto%20a%20algo\n\n¡Estamos listos para ayudarte!", number)
        listData.append(data)
        handled = True
    elif "asesor" in text_lower: # CAMBIO: Añadido para la opción del menú
        data = util.TextMessage("Para hablar con un asesor, por favor, utiliza el enlace de contacto:\n📞 Chatea con un Asesor OFICOMP aquí:\nhttps://wa.me/584147171542?text=Hola%2C%20ten%C3%ADa%20una%20duda%20con%20respecto%20a%20algo", number)
        listData.append(data)
        handled = True
    elif "ubicación" in text_lower: # CAMBIO: Añadido para la opción del menú
        data = util.LocationMessage(number)
        listData.append(data)
        handled = True
    elif "comprar" in text_lower:
        data = util.TextMessage("¡Perfecto! ✨ ¿Estás listo(a) para hacer tu compra? 💰\n\nIngresa a este enlace para hablar directamente con nuestro asesor de ventas y él te guiará en todo el proceso:\n\n🛒 Chatea con Ventas aquí:\nhttps://wa.me/584147171542?text=Me%20gustar%C3%ADa%20hacer%20una%20compra\n\n¡Esperamos tu mensaje!", number)
        listData.append(data)
        handled = True
    elif "gracias" in text_lower:
        data = util.TextMessage("¡A su Orden! En A.C OFICOMP estamos para servirte. ¿Hay algo más en lo que pueda ayudarte?'. ", number)
        listData.append(data)
        handled = True
    elif "format" in text_lower:
        data = util.TextFormatMessage(number)
        listData.append(data)
        handled = True
    elif "image" in text_lower:
        data = util.ImageMessage(number)
        listData.append(data)
        handled = True
    elif "audio" in text_lower:
        data = util.AudioMessage(number)
        listData.append(data)
        handled = True
    elif "list" in text_lower:
        data = util.ListMessage(number)
        listData.append(data)
        handled = True
    elif "button" in text_lower:
        data = util.ButtonsnMessage(number)
        listData.append(data)
        handled = True
    elif "regresar" in text_lower:
        data = util.TextMessage("¿Qué quieres conocer sobre nuestras categorías de productos?\nElige una opción 👇:\n\nAquí tienes nuestras categorías de productos:\n\n1️⃣ Accesorios\n2️⃣ Almohadillas\n3️⃣ Archivadores\n4️⃣ Blocks\n5️⃣ Bolígrafos\n6️⃣ Borradores\n7️⃣ Cajas Chicas\n8️⃣ Carpetas\n9️⃣ Carteleras\n🔟 Chinches\n1️⃣1️⃣ Cintas\n1️⃣2️⃣ Clips\n1️⃣3️⃣ Compases\n1️⃣4️⃣ Correctores\n1️⃣5️⃣ Creyones\n1️⃣6️⃣ Cuchillas\n1️⃣7️⃣ Sobres\n1️⃣8️⃣ Engrapadoras\n1️⃣9️⃣ Tirros\n2️⃣0️⃣ Fichas", number)
        listData.append(data)
        handled = True
    elif "principal" in text_lower:
        data = util.TextMessage("¿Tienes alguna duda?, puedes seleccionar la opción de contacto", number)
        dataMenu = util.ListMessage(number)
        listData.append(data)
        listData.append(dataMenu)
        handled = True
    ################################################## INVENTARIO #################################################
    # Las condiciones para los números de inventario (1 al 20) ya estaban bien.
    # Se ha añadido "ver inventario" a la condición principal de inventario.
    
    # Añadir todas las opciones de números de inventario
    elif "1" in text_lower: # Accesorios
        data = util.TextMessage("📦Pestaña Plástica Mayka p/carpeta Colgante", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "2" in text_lower: # Almohadillas
        data = util.TextMessage("📦Almohadilla para Sello Mayka Nº 1\n📦Almohadilla Dactilar", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "3" in text_lower: # Archivadores
        data = util.TextMessage("📦Archivador Lomo Ancho t/carta - Unidad\n📦Archivador Acordeón Plástico t/carta - Unidad\n📦Archivador Acordeón Plástico t/oficio - Unidad", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "4" in text_lower: # Blocks
        data = util.TextMessage("📦Block de Cartulina de Construcción\n📦Block de Notas Nº 3\n📦Block de Papel Milimetrado\n📦Block de Papel Rotulado 20 H\n📦Block de Dibujo Espiral Caribe 6148D", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "5" in text_lower: # Bolígrafos
        data = util.TextMessage("📦Bolígrafo Gel P/fina Printa Colores Surtidos\n📦Bolígrafo P/Fina Kores Negro, Azul y Rojo\n📦Bolígrafo P/media Kores Negro", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "6" in text_lower: # Borradores
        data = util.TextMessage("📦Borra Nata 620 (E)\n📦Borrona Nata 601\n📦Porta Borra Tipo Lápiz\n📦Borra Nata 612", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "7" in text_lower: # Cajas Chicas
        data = util.TextMessage("📦Caja Chica Pequeña\n📦Caja Chica Grande\n📦Caja Chica Mediana", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "8" in text_lower: # Carpetas
        data = util.TextMessage("📦Carpeta Transparente t/carta\n📦Carpeta P/Forma Continua Data N° 2 91/2x11\n📦Carpeta de Fibra Especial 5 Divisiones\n📦Carpeta de Fibra 2da t/oficio", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "9" in text_lower: # Carteleras
        data = util.TextMessage("📦Cartelera de Corcho 0.90x1.20\n📦Cartelera de Corcho 0.60x0.90\n📦Cartelera de Corcho 0.45x0.60", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "10" in text_lower: # Chinches
        data = util.TextMessage("📦Alfiler P/mapa Barril x 50\n📦Chinche Colores Surtidos", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "11" in text_lower: # Cintas
        data = util.TextMessage("📦Cinta Adhesiva Celoven 3472 3/4\"\n📦Cinta Adhesiva 3/4\"\n📦Cinta Doble Faz Transparente Celoven 3/4\" 45 Mtrs.\n📦Cinta Adhesiva Celoven 1236 1/2\"\n📦Cinta Adhesiva Celoven 3436 3/4\"", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "12" in text_lower: # Clips
        data = util.TextMessage("📦Clips Mariposa Nº 3\n📦Clips Standard Fixo Nº 1\n📦Clips Standard Nº 1", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "13" in text_lower: # Compases
        data = util.TextMessage("📦Compás de Precisión (E)\n📦Compás de Precisión Artesco Mod. 602\n📦Compás Escolar Artesco Mod. 101", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "14" in text_lower: # Correctores
        data = util.TextMessage("📦Corrector tipo Lápiz Artesco\n📦Corrector Líquido Kores\n📦Corrector tipo Lápiz Kores\n📦Corrector Líquido Ofimak", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "15" in text_lower: # Creyones
        data = util.TextMessage("📦Creyones de Madera Kores 12 Colores\n📦Creyones de Madera Kores 36 Colores\n📦Creyones de Madera Artesco Jumbo 12 Colores", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "16" in text_lower: # Cuchillas
        data = util.TextMessage("📦Cuchilla Exacto Nº 11\n📦Repuesto P/cuchilla Pequeña x 10\n📦Cuchilla Pequeña\n📦Cuchilla Grande", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "17" in text_lower: # Tirros (Originalmente "Sobres" en tu lista, pero el texto es de Tirros)
        data = util.TextMessage("📦Tirro Celoven 1240 1/2\"\n📦Tirro Celoven 3440 3/4\"\n📦Tirro Celoven 2140 2\"\n📦Tirro P/embalar Morropac Transparente x 90 Mts.\n📦Tirro Celoven 1140 1\"", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "18" in text_lower: # Engrapadoras
        data = util.TextMessage("📦Engrapadora t/Alicate Printa Tiburon\n📦Engrapadora t/Alicate Ofimak Mini 26/6\n📦Engrapadora Semi Industrial Ofimak 200 Hojas", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "19" in text_lower: # Sobres (Originalmente "Tirros" en tu lista, pero el texto es de Sobres)
        data = util.TextMessage("📦Sobres (Pendiente de definir)", number) 
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    elif "20" in text_lower: # Fichas
        data = util.TextMessage("📦Fichas Rayadas 5x8\n📦Fichas Rayadas 4x6", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)
        handled = True
    
    # Si ninguna palabra clave coincide, 'handled' permanece False.
    # NO se envía un mensaje de "no entiendo" desde aquí, para que el LLM pueda responder.

    # Envía los mensajes si la lógica de palabras clave los generó
    for item in listData:
        whatsappservice.SendMessageWhatsapp(item)

    return handled # Devuelve True si se manejó por palabra clave, False si no

if(__name__ == "__main__"):
    app.run(debug=True)