from threading import Thread
from chat import getTag, getReplyFromTag
from bot import MY_CHAT_ID, bot
from typing import Final
from telebot import types

#make a simple webserver to keep the bot alive
from flask import Flask, request, Response

from flask_cors import CORS

from mailer import sendEmail

import os
from dotenv import load_dotenv
load_dotenv()

import re

#listen to the port

app = Flask(__name__)

PORT: Final = 3000

client_url: Final = os.getenv('API_ACCESS_CLIENT_URL')

print(client_url)

cors: Final =  CORS(app, resources={r"/*": {"origins": client_url}})

#send cors headers for all routes.
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', client_url)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        # not allowed
        return Response("Not allowed", status=403)
    else:
        return Response("I'm alive", status=200)


def send_message(message):
    bot.send_message(MY_CHAT_ID, message)

# handle /contact route to send email
@app.route('/contact', methods=['POST'])
def contact():
    if (request.method == 'POST'):
        # get the payload from the request
        params = request.get_json()
        name = params['name']
        email = params['email']
        message = params['message']

        msg = f'New message from {name}\nEmail: {email}\nMessage: {message}'
        
        resp = Response("OK", status=200)
        # send the message to the bot
        send_message(msg)

        Thread(target=sendEmail, args=(email, 'Thanks for reaching out', f'Hello {name},\nThanks for messaging me. I\'ll reach you out whenever I get time. Have a nice day!', None, True)).start()
        #sendEmail(email, 'Thanks for reaching out', f'Hello {name},\nThanks for messaging me. I\'ll reach you out whenever I get time. Have a nice day!', auto_reply=True)
        # return cors headers for 'itsfuad.me' domain to allow cross origin requests
        print("Message relayed to bot from website")
        return resp
    else:
        response = Response("Not allowed", status=403)
        return response
    

def sendDocuments(file, title):
    if 'image' in file.content_type:
        bot.send_photo(MY_CHAT_ID, file)
    elif 'audio' in file.content_type:
        bot.send_audio(MY_CHAT_ID, file, title=title)
    elif 'video' in file.content_type:
        bot.send_video(MY_CHAT_ID, file)
    else:
        bot.send_document(MY_CHAT_ID, file, visible_file_name=title)
    print("Document sent to bot")

@app.route('/sendDoc', methods=['POST'])
def sendDoc():
    # check if has file
    files = request.files
    if not files:
        return Response("No file found", status=400)
    else:
        file = files['file']
        Thread(target=sendDocuments, args=(file, file.filename)).start()
        print("Document relayed to bot from website")
        return Response("OK", status=200)
    

# handle /visitor route
@app.route('/visitor', methods=['POST'])
def visitor():
    if (request.method == 'POST'):
        # get the payload from the request
        params = request.get_json()
        message = params['message']
        bot.send_message(MY_CHAT_ID, message)
        print(message)
        response = Response("OK", status=200)
        return response
    else:
        response = Response("Not allowed", status=403)
        return response
    

#handler for all other routes for 404
@app.errorhandler(404)
def not_found(e):
    return Response("There is nothing here", status=404)

    

def run_flask():
    from waitress import serve
    print(f'Server started on port {PORT}')
    serve(app, host='0.0.0.0', port=PORT)


# Make the bot listen to the messages
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == MY_CHAT_ID:
        bot.send_message(message.chat.id, "I'm here, Dear.🥰")
    else:
        # send inline keyboard button [Are you a human?, Yes, No]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Yes", callback_data='yes'), types.InlineKeyboardButton("No", callback_data='no'))
        bot.send_message(message.chat.id, "Are you a human?", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data in ["yes", "no"])
def callback_query(call):
    if call.message:
        if call.data == "yes":
            bot.send_message(call.message.chat.id, "Great!😍. But you're not Fuad, so I can't talk to you.🤭")
        elif call.data == "no":
            bot.send_message(call.message.chat.id, "Sorry, I'm not intersted to robots😴")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.chat.id == MY_CHAT_ID:
        tag = getTag(message.text)
        # print(message.content_type)
        if tag:
            if tag == 'sendEmail':
                reply = getReplyFromTag(tag)
                bot.send_message(message.chat.id, reply)
                sent_message = bot.send_message(message.chat.id, 'Who is the recipient?😐')
                # attach a listener to the next message
                bot.register_next_step_handler(sent_message, handleRecipent)
            else:
                bot.send_message(message.chat.id, getReplyFromTag(tag))
        else:
            bot.send_message(message.chat.id, 'Sorry, I did not understand that.😢')
    else:
        bot.send_message(message.chat.id, "Sorry, I'm not allowed to talk to strangers😴")



@bot.message_handler(content_types=['document', 'audio', 'photo', 'video', 'voice'])
def handleInputFiles(message):
    if message.chat.id == MY_CHAT_ID:
        print(message.content_type)
        bot.send_message(message.chat.id, 'You sent me a ' + message.content_type + ' file. But What will I do with it!🤔')
    else:
        bot.send_message(message.chat.id, "Sorry, I'm not allowed to talk to strangers😴")



def handleRecipent(message):
    recipient = message.text

    tag = getTag(message.text)
    
    if recipient.lower() == 'me' or recipient.lower() == 'myself' or recipient.lower() == 'ami':
        recipient = 'fuad.cs22@gmail.com'
    elif tag == 'cancelMail':
        bot.send_message(message.chat.id, getReplyFromTag(tag))
        return
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", recipient):
        bot.send_message(message.chat.id, 'Invalid recipient')
        return
    
    sent_message = bot.send_message(message.chat.id, "Okay, what's the subject?🤦🏻‍♀️")
    bot.register_next_step_handler(sent_message, handleSubject, recipient)



def handleSubject(message, recipient):
    subject = message.text

    tag = getTag(message.text)

    if tag == 'cancelMail':
        bot.send_message(message.chat.id, getReplyFromTag(tag))
        return
    
    sent_message = bot.send_message(message.chat.id, "Okay, what's the body?🙆🏻‍♀️")
    bot.register_next_step_handler(sent_message, handleBody, recipient, subject)



def handleBody(message, recipient, subject):
    body = message.text

    tag = getTag(message.text)

    if tag == 'cancelMail':
        bot.send_message(message.chat.id, getReplyFromTag(tag))
        return
    

    bot.send_message(message.chat.id, 'Do you want to add attachment?💁🏻‍♀️ (Yes/No)')
    bot.register_next_step_handler(message, handleFile, recipient, subject, body)



def handleFile(message, recipient, subject, body):
    affirmative = ['yes', 'y', 'yup', 'yeah', 'haan', 'ha', 'hmm', 'hmmmm', 'hmmm', 'hmmmmm', 'hm', 'ho', 'ji']
    negative = ['no', 'n', 'nope', 'nah', 'uhu', 'thak']
    if message.text.lower() in affirmative:
        sent_message = bot.send_message(message.chat.id, 'Send me the file🙆🏻‍♀️')
        bot.register_next_step_handler(sent_message, handleFileAttachment, recipient, subject, body)
    elif message.text.lower() in negative:
        bot.send_message(message.chat.id, 'Sending...')
        ok = sendEmail(recipient, subject, body)
        if ok:
            bot.send_message(message.chat.id, 'Email sent successfully🤭') 
        else:
            bot.send_message(message.chat.id, 'Something went wrong.😢')
    else:
        bot.send_message(message.chat.id, 'Sorry, I did not understand that.😢')



def handleFileAttachment(message, recipient, subject, body):
    file_info = ''
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
    elif message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
    bot.send_message(message.chat.id, 'Sending...')
    ok = sendEmail(recipient, subject, body, file_info)
    if ok:
        bot.send_message(message.chat.id, 'Email sent successfully🤭') 
    else:
        bot.send_message(message.chat.id, 'Something went wrong.😢')


bot_thread = Thread(target=bot.infinity_polling)

if __name__ == '__main__':
    print('Starting App...')
    try:
        #start bot and server in different threads
        bot_thread.start()
    except Exception as e:
        #stop server and bot
        print('Stopping App...')
        bot_thread.join()
    finally:
        print('App stopped')
        exit(0)