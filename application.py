"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import sys
from scraper import scraperAP
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text("Hi! Use /start to start the service \n" \
                                "Use /keywords to view keywords \n" \
                                "Use /add <keyword> to add keywords \n" \
                                "Use /delete to delete keywords \n" \
                                "Use /fetch to fetch news now")
    logger.info("/help Command triggered")

keywords = ['oneplus', 'xiaomi', 'google', 'android']

def newsflash(context):
    """Send the alarm message."""
    job = context.job
    """Run the scraper and dispatch results."""
    allposts = scraperAP(keywords)
    """Check if theres any news"""
    if allposts == []:
        context.bot.send_message(job.context, text='Sorry! No news updates today')
        logger.info("News retrieved -- No news today")
    else: 
        context.bot.send_message(job.context, text='Here\'s your cutomized daily news!')
        for post in allposts: 
            message = post['title']+'\n'+post['link']
            context.bot.send_message(job.context, text=message)
        logger.info("News retrieved and sent to user.")
    
def add_keyword(update, context):
    """Add a keyword to scraper"""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the new keyword to be added
        word = str(context.args[0]).lower()
        if word in keywords:
            update.message.reply_text('Sorry the word you entered is already a keyword!')
            return
        # add word to keywords
        keywords.append(word)
        update.message.reply_text('New keyword "'+word+'" added successfully!')
        logger.info(word + " -- keyword added")
    except(IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')
        logger.info("Invalid keyword added")

def display_keywords(update, context):
    """"Display keywords"""
    result = ', '.join(keywords)
    update.message.reply_text("Your keywords are currently: "+ result)
    logger.info("/keywords Command triggered")

def del_keywords(update,context):
    """Display keywords for deleting"""
    keyboard = []
    for word in keywords:
        temp = [InlineKeyboardButton(word, callback_data=word)]
        keyboard.append(temp)
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Select keyword to be deleted:', reply_markup=reply_markup)
    logger.info("/delete Command triggered")

def button(update, context):
    query = update.callback_query
    keywords.remove(query.data)
    query.edit_message_text(text="Deleted keyword: {}".format(query.data))
    logger.info(query.data + " -- keyword deleted")

from datetime import datetime, timedelta
from dateutil.parser import parse

def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # Add job to queue
        """Actual use"""
        job = context.job_queue.run_daily(newsflash,parse('1am').time(), context=chat_id)

        """Testing use"""
        #job = context.job_queue.run_repeating(newsflash,5,first=5,context=chat_id)
        context.chat_data['job'] = job

        update.message.reply_text('Daily news successfully set!')
        logger.info("/start Command triggered")

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /start')

def fetch_news(update, context):
    chat_id = update.message.chat_id
    job = context.job_queue.run_once(newsflash,1, context=chat_id)
    update.message.reply_text('Fetching your news!')
    logger.info("/fetch command triggered")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Run bot."""
    mode = os.getenv("MODE")
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN,use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", set_timer))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("add", add_keyword,
                                pass_args=True))
    dp.add_handler(CommandHandler("keywords", display_keywords))
    dp.add_handler(CommandHandler("delete", del_keywords))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("fetch", fetch_news))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    logger.info("Starting bot")
    
    # Set daily news on bot start
    j = updater.job_queue
    job_daily = j.run_daily(newsflash,parse('1am').time(), context = CHAT_ID)
    
    ### Test Code
    ## job_test = j.run_repeating(newsflash,10,first=0,context= CHAT_ID)

    logger.info("Job queue started.")
    if mode == "dev":
        updater.start_polling()
    elif mode == "prod":
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
        updater.idle()
        logger.info("Server started")
    else:
        logger.error("No MODE specified!")
        sys.exit(1)

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    


if __name__ == '__main__':
    main()