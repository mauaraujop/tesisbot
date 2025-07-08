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
        dataVolver = util.ReturnMessage(dataVolver)
        listData.append(data)
        listData.append(dataMenu)

    elif "gracias" in text:
        data = util.TextMessage("¡De nada! En OFICOMP estamos para servirte. ¿Hay algo más en lo que pueda ayudarte?'. ", number)
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
    elif "inventario" in text:
        data = util.TextMessage("¿Qué quieres conocer sobre nuestras categorías de productos?\nElige una opción 👇:\n\nAquí tienes nuestras categorías de productos:\n\n1️⃣ Accesorios\n2️⃣ Almohadillas\n3️⃣ Archivadores\n4️⃣ Blocks\n5️⃣ Bolígrafos\n6️⃣ Borradores\n7️⃣ Cajas Chicas\n8️⃣ Carpetas\n9️⃣ Carteleras\n🔟 Chinches\n1️⃣1️⃣ Cintas\n1️⃣2️⃣ Clips\n1️⃣3️⃣ Compases\n1️⃣4️⃣ Correctores\n1️⃣5️⃣ Creyones\n1️⃣6️⃣ Cuchillas\n1️⃣7️⃣ Cuenta Fácil\n1️⃣8️⃣ Engrapadoras\n1️⃣9️⃣ Escarchas\n2️⃣0️⃣ Fichas", number)
        listData.append(data) 
    elif "list" in text:
        data = util.ListMessage(number)
        listData.append(data)
    elif "archivadores" in text:
        data = util.TextMessage("⭐Archivador Lomo Ancho t/carta - Unidad\n⭐Archivador Acordeón Plástico t/carta - Unidad\n⭐Archivador Acordeón Plástico t/oficio - Unidad", number)
        dataVolver = util.ReturnMessage(dataVolver)
    elif "button" in text:
            data = util.ButtonsnMessage(number)
            listData.append(data)
    elif "ubicación" in text:
        data = util.LocationMessage(number)
        listData.append(data)

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