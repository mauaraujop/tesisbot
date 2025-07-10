def GetTextUser(message):
    text = ""
    typeMessage = message["type"]

    if typeMessage == "text":
        text = (message["text"])["body"]
    elif typeMessage == "interactive":
        interactiveObject = message["interactive"]
        typeInteractive = interactiveObject["type"]

        if typeInteractive == "button_reply":
            text = (interactiveObject["button_reply"])["title"]
        elif typeInteractive == "list_reply":
            text = (interactiveObject["list_reply"])["title"]
        else:
            print (" sin mensaje ")
    
    return text 

def TextMessage(text, number):
    data = {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": text
                }
            }
    return data

def TextFormatMessage(number):
    data ={
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "*Hola usuarioo* - _hola_ - "
            }
        }
    return data

def ImageMessage(number):
    data ={
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": "584247526123",
            "type": "image",
            "image": {
                "link": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/1920px-International_Pok%C3%A9mon_logo.svg.png"
            }
        }
    return data

def AudioMessage(number):
    data ={
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "audio",
            "audio": {
                "link": "https://biostoragecloud.blob.core.windows.net/resource-udemy-whatsapp-node/audio_whatsapp.mp3"
            }
        }
    return data

def LocationMessage(number):
    data ={
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "location",
            "location": {
                "latitude": "8.583761",
                "longitude": " -71.17011",
                "name": "Estado de Mérida",
                "address": "Urb. Santa Ana, Mérida 5101, Mérida"
            }
        }
    return data
def ButtonsnMessage(number):
    data ={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "header": {
                    "type": "image",
                     "image": {
                         "link": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/1920px-International_Pok%C3%A9mon_logo.svg.png" 
                         }
                     },
                    
                    "body": {
                        "text": "Holaa👽👽👽"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "001",
                                    "title": "Si"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "002",
                                    "title": "No"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "003",
                                    "title": "No se"
                                }
                            }
                        ]
                    }
                }
            }
    return data

def ListMessage(number):
    data ={
    "messaging_product": "whatsapp",
    "to": number,
    "type": "interactive",
    "interactive": {
        "type": "list",
        "body": {
            "text": "Para hacer tu búsqueda más eficiente, te presento nuestras opciones clave. ✨ ¿Qué necesitas hoy?"
        },
        "footer": {
            "text": "Seleccione una Opción"
        },
        "action": {
            "button": "Ver Opciones",
            "sections": [
                {
                    "title": "Inventario",
                    "rows": [
                        {
                            "id": "main-inventario",
                            "title": "Ver Inventario",
                            "description": " "
                        }
                    ]
                },
                {
                    "title": "👨Contáctanos 📞",
                    "rows": [
                        {
                            "id": "main-asesor",
                            "title": "Asesor",
                            "description": " "
                        },
                        {
                            "id": "main-ubicacion",
                            "title": "Ubicación",
                            "description": " "
                        }
                    ]
                }
            ]
        }
    }
}
    return data

def RegresarMessage(number):
    data ={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "button",                   
                    "body": {
                        "text": "💲¿Deseas realizar una compra?💲"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "001",
                                    "title": "Comprar 💵"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "002",
                                    "title": "👈Regresar"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "003",
                                    "title": "⏪ Menú Principal"
                                }
                            }
                        ]
                    }
                }
            }
    return data

