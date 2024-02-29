from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, JobQueue, CallbackQueryHandler
import logging
from future.moves import configparser
import sys
sys.path.insert(0, 'telegram-handlers')
from commandHandlers import start, help, mywallets
from messageHandlers import message
from callbackQueryHandler import button_pressed
import db_manager
from txCheckScheduler import check_transactions

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    bot_token = config.get("TEL", "token")
    job_queue = JobQueue()
    application = ApplicationBuilder().token(bot_token).job_queue(job_queue).build()
    db_manager

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("mywallets", mywallets))
    application.add_handler(MessageHandler(filters.TEXT, message))
    application.add_handler(CallbackQueryHandler(button_pressed))
                            
    job_queue.run_repeating(check_transactions, interval=10, first=0)

    application.run_polling(1.0)

if __name__ == '__main__':
    main()