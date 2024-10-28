from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from flask import Flask
import threading
import logging
import os

# Initialize environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Store your bot token as an environment variable
CHANNEL_ID = -1002390863629         # Channel ID for receiving commands

# Initialize Flask for keeping the bot alive on Render
app = Flask(__name__)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Route for Render to ping and keep the bot active
@app.route('/')
def home():
    return "Bot is running."

# /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! I'm here to help manage your channel.")

# /about command
def about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("This bot can delete all messages it has sent to the channel and responds to specific commands.")

# /delete_all command
def delete_all(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.id != CHANNEL_ID:
        update.message.reply_text("This command can only be used in the specified channel.")
        return

    chat_id = update.effective_chat.id
    try:
        # Iterate and delete bot messages within the channel
        for message_id in range(1, update.message.message_id):
            try:
                context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception as e:
                logger.warning(f"Could not delete message {message_id}: {e}")

        update.message.reply_text("All deletable messages have been deleted.")
    except Exception as e:
        update.message.reply_text("An error occurred while deleting messages.")
        logger.error(e)

# Main function to run the bot
def run_bot():
    updater = Updater(BOT_TOKEN, use_context=True)

    # Add handlers for /start, /about, and /delete_all
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("about", about))
    updater.dispatcher.add_handler(CommandHandler("delete_all", delete_all))

    # Start polling
    updater.start_polling()
    updater.idle()

# Run bot in a separate thread
threading.Thread(target=run_bot).start()

# Start Flask server to keep Render service active
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
