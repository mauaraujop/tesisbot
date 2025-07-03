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

        if response.status_code == 200:
            return True
        
        return False
    except Exception as exception:
        print(exception)
        return False
        