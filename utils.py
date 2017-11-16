from wit import Wit

def wit_response(message_text):
        access_token = "MAG6GZ3NXCSL54FOUIGYANWPCHNPO5WM"
        client = Wit(access_token=access_token)
        resp = client.message(message_text)
        entity = None
        value = None
        try:
                entity = list(resp['entities'])[0]
                value = resp['entities'][entity][0]['value']
        except:
                pass
        return (entity,value)

#print(wit_response("I want books"))
