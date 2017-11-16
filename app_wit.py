import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN="EAAHLxMxj2OoBAC4gJIsp8fbtFKR3ICG3SRoV7UUZAq5cW8IsvA5TIlZBbTpLhe34cxGfxcgxT84gxsY324ZA12Yph3WF9Uaon51ZB0dLbqZAAc7q7K5wZAkPFGZCZCUlf5tcrSZBmYw7ZBp4LzCZAAZB5VCHcuh0Gi725kbKfJ61uGlw6AZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    #Webhook verification
    #print("HELLO****************************")
    if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")=="hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200

@app.route('/', methods=['POST'])
def webhook():
    #print("HI****************************")
    data = request.get_json()
    print("data")
    log(data)
    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id=messaging_event['sender']['id']
                recipient_id=messaging_event['recipient']['id']
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text= messaging_event['message']['text']
                    else:
                        messaging_text='no text'
                    response = None
                    entity, value = wit_response(messaging_text)
                    if entity == 'books':
                        response = "Ok. I will show you {} books.".format(str(value))
                    elif entity == "greetings":
                        response = "Hello, how can I help you?"
                    elif entity == "intent":
                        response = "Which subject books do you want?"
                    else:
                        response = "Sorry, I din't get you."
                    bot.send_text_message(sender_id,response)
    return "ok", 200

def log(message):
	print(message)
	sys.stdout.flush()

if __name__=='__main__':
	app.run(debug=True, port=4000)
