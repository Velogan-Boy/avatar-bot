from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from credentials import bot_token, URL

app = Flask(__name__)

TOKEN = bot_token

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

@app.route('/')
def index():
    return 'Hello, this is your Telegram bot!'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_data = request.get_json()
    update = Update.de_json(json_data, updater.bot)
    dispatcher.process_update(update)
    return '', 200

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Please enter your name to get a cool avatar.")

def generate_avatar(update: Update, context: CallbackContext) -> None:
    name = ' '.join(context.args)
    if not name:
        update.message.reply_text("Please enter a name.")
        return

    avatar_url = f'http://avatars.adorable.io/{len(name)}bits/{name}.png'
    update.message.reply_photo(photo=avatar_url, caption=f"Here's a cool avatar for {name}!")

if __name__ == '__main__':
    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("generateavatar", generate_avatar, pass_args=True))

    # Start the Flask web application
    app.run(host="0.0.0.0", port=8080)
    
    # Start the Updater
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C
    updater.idle()
