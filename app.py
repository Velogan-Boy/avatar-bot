from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
import requests
from credentials import bot_token, URL

app = Flask(__name__)
bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot, None, workers=0)

@app.route('/')
def hello():
    return 'Hello, this is your Telegram BOT!'

@app.route('/{}'.format(bot_token), methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return 'OK'

def start(update: Update, context: CallbackContext):
    update.message.reply_text(" Welcome to Avatar bot, the bot is using the service from https://ui-avatars.com to generate name avatars based on the name. Use /generate command with your name (eg. /generate raghul pranavesh )")

def generate_avatar(update: Update, context: CallbackContext):
    name = '+'.join(context.args)
    if name:
        avatar_url = "https://ui-avatars.com/api/?name={}&size=512".format(name.strip())
        update.message.reply_photo(photo=avatar_url)
    else:
        update.message.reply_text("Please enter a name to generate an avatar.")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('generate', generate_avatar))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
