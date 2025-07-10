from flask import Flask, request
import util
import whatsappservice

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
    except:
        return "", 400
    
@app.route('/whatsapp', methods=['POST'])
def ReceivedMessage():
    try:
        body = request.get_json()
        entry = (body["entry"])[0]
        changes = (entry["changes"])[0]
        value = changes["value"]
        message = (value["messages"])[0]
        number = message["from"]
        
        text = util.GetTextUser(message)
        ProcessMessage(text, number)
        print(text)

        return "EVENT_RECEIVED"
    except:
        return "EVENT_RECEIVED"
    
def ProcessMessage(text, number):
    text = text.lower()
    listData = []
    
    if "hola" in text or "opcion" in text:
        data = util.TextMessage("👋 ¡Hola! Soy tu asistente virtual de OFICOMP, listo para ayudarte con todo lo que tu oficina necesita. ¿En qué puedo asistirte hoy? Escribe 'Menú' para ver mis opciones o hazme una pregunta. ✨", number)
        dataMenu = util.ListMessage(number)
    
        listData.append(data)
        listData.append(dataMenu)
    elif "contáctanos" in text:
        data = util.TextMessage("👋 ¿Alguna duda referente al procesamiento del pago?", number)
    elif "gracias" in text:
        data = util.TextMessage("¡A su Orden! En A.C OFICOMP estamos para servirte. ¿Hay algo más en lo que pueda ayudarte?'. ", number)
        listData.append(data)
    elif "format" in text:
        data = util.TextFormatMessage(number)
        listData.append(data)
    elif "image" in text:
        data = util.ImageMessage(number)
        listData.append(data)
    elif "audio" in text: 
        data = util.AudioMessage(number) 
        listData.append(data)
    elif "comprar" in text:
        data = util.TextMessage("Para realizar una compra com ", number)
    elif "list" in text:
        data = util.ListMessage(number)
        listData.append(data)
    elif "button" in text:
            data = util.ButtonsnMessage(number)
            listData.append(data)
    elif "ubicación" in text:
        data = util.LocationMessage(number)
        listData.append(data)
    elif "regresar" in text:
        data = util.TextMessage("¿Qué quieres conocer sobre nuestras categorías de productos?\nElige una opción 👇:\n\nAquí tienes nuestras categorías de productos:\n\n1️⃣ Accesorios\n2️⃣ Almohadillas\n3️⃣ Archivadores\n4️⃣ Blocks\n5️⃣ Bolígrafos\n6️⃣ Borradores\n7️⃣ Cajas Chicas\n8️⃣ Carpetas\n9️⃣ Carteleras\n🔟 Chinches\n1️⃣1️⃣ Cintas\n1️⃣2️⃣ Clips\n1️⃣3️⃣ Compases\n1️⃣4️⃣ Correctores\n1️⃣5️⃣ Creyones\n1️⃣6️⃣ Cuchillas\n1️⃣7️⃣ Sobres\n1️⃣8️⃣ Engrapadoras\n1️⃣9️⃣ Tirros\n2️⃣0️⃣ Fichas", number)
        listData.append(data)
    elif "principal" in text:
        data = util.TextMessage("¿Tienes alguna duda?, puedes seleccionar la opción de contacto", number)
        dataMenu = util.ListMessage(number)
################################################## INVENTARIO #################################################
    elif "inventario" in text:
        data = util.TextMessage("¿Qué quieres conocer sobre nuestras categorías de productos?\nElige una opción 👇:\n\nAquí tienes nuestras categorías de productos:\n\n1️⃣ Accesorios\n2️⃣ Almohadillas\n3️⃣ Archivadores\n4️⃣ Blocks\n5️⃣ Bolígrafos\n6️⃣ Borradores\n7️⃣ Cajas Chicas\n8️⃣ Carpetas\n9️⃣ Carteleras\n🔟 Chinches\n1️⃣1️⃣ Cintas\n1️⃣2️⃣ Clips\n1️⃣3️⃣ Compases\n1️⃣4️⃣ Correctores\n1️⃣5️⃣ Creyones\n1️⃣6️⃣ Cuchillas\n1️⃣7️⃣ Sobres\n1️⃣8️⃣ Engrapadoras\n1️⃣9️⃣ Tirros\n2️⃣0️⃣ Fichas", number)
        listData.append(data) 
    
    elif "1" in text: # Accesorios
        data = util.TextMessage("📦Pestaña Plástica Mayka p/carpeta Colgante", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "2" in text: # Almohadillas
        data = util.TextMessage("📦Almohadilla para Sello Mayka Nº 1\n📦Almohadilla Dactilar", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "3" in text: # Archivadores
        data = util.TextMessage("📦Archivador Lomo Ancho t/carta - Unidad\n📦Archivador Acordeón Plástico t/carta - Unidad\n📦Archivador Acordeón Plástico t/oficio - Unidad", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "4" in text: # Blocks
        data = util.TextMessage("📦Block de Cartulina de Construcción\n📦Block de Notas Nº 3\n📦Block de Papel Milimetrado\n📦Block de Papel Rotulado 20 H\n📦Block de Dibujo Espiral Caribe 6148D", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "5" in text: # Bolígrafos
        data = util.TextMessage("📦Bolígrafo Gel P/fina Printa Colores Surtidos\n📦Bolígrafo P/Fina Kores Negro, Azul y Rojo\n📦Bolígrafo P/media Kores Negro", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "6" in text: # Borradores
        data = util.TextMessage("📦Borra Nata 620 (E)\n📦Borrona Nata 601\n📦Porta Borra Tipo Lápiz\n📦Borra Nata 612", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "7" in text: # Cajas Chicas
        data = util.TextMessage("📦Caja Chica Pequeña\n📦Caja Chica Grande\n📦Caja Chica Mediana", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "8" in text: # Carpetas
        data = util.TextMessage("📦Carpeta Transparente t/carta\n📦Carpeta P/Forma Continua Data N° 2 91/2x11\n📦Carpeta de Fibra Especial 5 Divisiones\n📦Carpeta de Fibra 2da t/oficio", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "9" in text: # Carteleras
        data = util.TextMessage("📦Cartelera de Corcho 0.90x1.20\n📦Cartelera de Corcho 0.60x0.90\n📦Cartelera de Corcho 0.45x0.60", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "10" in text: # Chinches
        data = util.TextMessage("📦Alfiler P/mapa Barril x 50\n📦Chinche Colores Surtidos", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "11" in text: # Cintas
        data = util.TextMessage("📦Cinta Adhesiva Celoven 3472 3/4\"\n📦Cinta Adhesiva 3/4\"\n📦Cinta Doble Faz Transparente Celoven 3/4\" 45 Mtrs.\n📦Cinta Adhesiva Celoven 1236 1/2\"\n📦Cinta Adhesiva Celoven 3436 3/4\"", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "12" in text: # Clips
        data = util.TextMessage("📦Clips Mariposa Nº 3\n📦Clips Standard Fixo Nº 1\n📦Clips Standard Nº 1", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "13" in text: # Compases
        data = util.TextMessage("📦Compás de Precisión (E)\n📦Compás de Precisión Artesco Mod. 602\n📦Compás Escolar Artesco Mod. 101", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "14" in text: # Correctores
        data = util.TextMessage("📦Corrector tipo Lápiz Artesco\n📦Corrector Líquido Kores\n📦Corrector tipo Lápiz Kores\n📦Corrector Líquido Ofimak", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "15" in text: # Creyones
        data = util.TextMessage("📦Creyones de Madera Kores 12 Colores\n📦Creyones de Madera Kores 36 Colores\n📦Creyones de Madera Artesco Jumbo 12 Colores", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "16" in text: # Cuchillas
        data = util.TextMessage("📦Cuchilla Exacto Nº 11\n📦Repuesto P/cuchilla Pequeña x 10\n📦Cuchilla Pequeña\n📦Cuchilla Grande", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "17" in text: # Cuenta Fácil (Si tienes productos, ponlos aquí. De lo contrario, dejará solo los botones de volver.)
        data = util.TextMessage("📦Productos de Cuenta Fácil (Pendiente de definir)", number) # O vacío si no hay productos aún
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "18" in text: # Engrapadoras
        data = util.TextMessage("📦Engrapadora t/Alicate Printa Tiburon\n📦Engrapadora t/Alicate Ofimak Mini 26/6\n📦Engrapadora Semi Industrial Ofimak 200 Hojas", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "19" in text: # Escarchas (Si tienes productos, ponlos aquí. De lo contrario, dejará solo los botones de volver.)
        data = util.TextMessage("📦Productos de Escarchas (Pendiente de definir)", number) # O vacío si no hay productos aún
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    elif "20" in text: # Fichas
        data = util.TextMessage("📦Fichas Rayadas 5x8\n📦Fichas Rayadas 4x6", number)
        listData.append(data)
        dataBotonesVolver = util.RegresarMessage(number)
        listData.append(dataBotonesVolver)

    
    else:
        data = util.TextMessage("*¡Vaya!*No consigo entender a qué te refieres 😢 .\n\nAquí tienes algunos de los temas en los que puedo ayudarte:\n👉 *Hola*\n👉 *Gracias*",number)
        listData.append(data)
        
    for item in listData:
        whatsappservice.SendMessageWhatsapp(item)

def GenerateMessage(text, number):
    text = text.lower()
    if "format" in text:
        data = util.TextFormatMessage(number)
    if "image" in text:
        data = util.ImageMessage(number)
    if "audio" in text:
        data = util.AudioMessage(number)
    if "location" in text:
        data = util.LocationMessage(number)
    if "button" in text:
        data = util.ButtonsnMessage(number)
    if "list" in text:
        data = util.ListMessage(number)
    if "prueba" in text:
        data = util.PruebaMessage(number)
    else:
        # Si ninguna palabra clave anterior coincide, envía un mensaje por defecto
        data = util.TextMessage("Lo siento, no entendí tu mensaje. Intenta decir 'hola' o 'menu'.", number)

    whatsappservice.SendMessageWhatsapp(data)


if(__name__ == "__main__"):
    app.run(debug=True)