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

    if "hola" in text:
        data = util.TextMessage("👋 ¡Hola! Soy tu asistente virtual de OFICOMP, listo para ayudarte con todo lo que tu oficina necesita. ¿En qué puedo asistirte hoy? Escribe 'Menú' para ver mis opciones o hazme una pregunta. ✨", number)
    elif "gracias" in text:
        data = util.TextMessage("¡De nada! En OFICOMP estamos para servirte. ¿Hay algo más en lo que pueda ayudarte?'. ", number)
    elif "format" in text:
        data = util.TextFormatMessage(number)
    elif "image" in text:
        data = util.ImageMessage(number)
    elif "list" in text:
        data = util.ListMessage(number)
    elif "button" in text:
            data = util.ButtonsnMessage(number)
    elif "ubicación" in text:
        data = util.LocationMessage(number)

    else:
        data = util.TextMessage("*¡Vaya!*No consigo entender a qué te refieres 😢 .\n\nAquí tienes algunos de los temas en los que puedo ayudarte:\n👉 *Hola*\n👉 *Gracias*",number)
   
    whatsappservice.SendMessageWhatsapp(data)

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