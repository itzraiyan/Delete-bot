from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to delete all bot messages in a channel
def delete_all(update: Update, context: CallbackContext) -> None:
    # Ensure the command is run in a channel where the bot has admin permissions
    if not update.effective_chat or update.effective_chat.type != "channel":
        update.message.reply_text("This command can only be used in a channel.")
        return

    chat_id = update.effective_chat.id
    try:
        # Fetch recent messages and delete them if the bot sent them
        for message_id in range(1, update.message.message_id):  # Iterating by message IDs
            try:
                context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception as e:
                logger.warning(f"Could not delete message {message_id}: {e}")

        update.message.reply_text("All deletable messages have been deleted.")
    except Exception as e:
        update.message.reply_text("An error occurred while deleting messages.")
        logger.error(e)

# Main function to run the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater("7526642009:AAHB4JSrLtFjQNLX5nDz28_RK1yQ1g8lHSc", use_context=True)

    # Command to delete all bot messages
    updater.dispatcher.add_handler(CommandHandler("delete_all", delete_all))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
