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
                "body": "*Hola usuarioo*\n - _hola_ -\n hola otra vez "
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
            "text": "✅ I have these options"
        },
        "footer": {
            "text": "Select an option"
        },
        "action": {
            "button": "See options",
            "sections": [
                {
                    "title": "Buy and sell products",
                    "rows": [
                        {
                            "id": "main-buy",
                            "title": "Buy",
                            "description": "Buy the best product your home"
                        },
                        {
                            "id": "main-sell",
                            "title": "Sell",
                            "description": "Sell your products"
                        }
                    ]
                },
                {
                    "title": "📍center of attention",
                    "rows": [
                        {
                            "id": "main-agency",
                            "title": "Agency",
                            "description": "Your can visit our agency"
                        },
                        {
                            "id": "main-contact",
                            "title": "Contact center",
                            "description": "One of our agents will assist you"
                        }
                    ]
                }
            ]
        }
    }
}
def PruebaMessage(number):
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "prueba",
            "header": {
                "type": "image",
                "image": {
                    "link": "https://images.wikidexcdn.net/mwuploads/wikidex/9/94/latest/20230204063131/EP1229_Oshawott_de_Ash.png"  # Reemplaza con la URL de tu imagen
                }
            },
            "body": {
                "text": "¡Bienvenido a Oficomp Explora nuestros artículos de oficina y equipos de cómputo."
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "001",
                            "title": "Ver Productos"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "002",
                            "title": "Soporte Técnico"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "003",
                            "title": "Contáctanos"
                        }
                    }
                ]
            }
        }
    }
    return data

