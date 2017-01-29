#!/usr/bin/env python3
import requests
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler)

import config
from db_manager import DBManager

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

YA_MAPS_URL = "https://geocode-maps.yandex.ru/1.x/?format=json&"


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location

    dbm = DBManager(config.DB_NAME)

    closest_station = dbm.find_closest(user_location.longitude, 
                                       user_location.latitude)
    update.message.reply_text("Closest station to you is %s" % 
                              closest_station.name
                              )


def text(bot, update):
    address = "Москва, " + update.message.text
    r = requests.get(YA_MAPS_URL + "geocode=%s" % address)
    # TODO: what is logger and why do I need that?
    logger.info(r.json())


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # handler for text and location
    dp.add_handler(MessageHandler(Filters.text, text))
    dp.add_handler(MessageHandler(Filters.location, location))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
