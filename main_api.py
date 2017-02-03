#!/usr/bin/env python3
import requests
import logging
import json
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler
                          )

import config
from parser import get_coordinates, scrap_stations_names

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_schedule(code):
    ''' Returns schedule for the station by given code. '''
    r = requests.get(config.YA_API_STATION, params = {
            'apikey': config.YA_API_KEY,
            'code'  : code,
            'format': 'json',
            'lang'  : 'ru'        
        })

    return r



def text(bot, update):
    ''' Finds closest station from geo object represented by string. '''
    list_of_places = get_coordinates([bot.message.text])

    nearest_station = find_nearest(list_of_places[0])

    # TODO: call location() with coordinates of nearest station

def find_nearest(place):
    ''' Find closest station from given longtitude, latutude.
    '''
    # get the nearest station with ya api
    print('wut')
    r = requests.get(config.YA_API_NEAREST + \
            '?apikey{0}'.format(config.YA_API_KEY) + \
            '&lat={0}'.format(place[1]) + \
            '&lon={0}'.format(place[0]) + \
            '&distance=10' + \
            '&transport_types=suburban' + \
            '&format=json'
            )

    print('yo')
    print(r.json())

    return r.json()


# TODO: solve following pronlem
#       function is redudant since i can add find_nearest as handler,
#       but i can't
#       other way is to call location() from text(), 
#       but that doesn't semm possible
# TODO: read why does this thing mute all the errors?
def location(bot, update):
    ''' Will call normal function instead of bot method'''
    user = update.message.from_user
    user_location = update.message.location

    r = requests.get(config.YA_API_NEAREST, params= {
                     'apikey'  : config.YA_API_KEY,
                     'lat'     : user_location['latitude'],
                     'lng'     : user_location['longitude'],
                     'distance': + 3,
                     'format'  : 'json',
                     'transport_types': 'train',
                     'station_type'   : 'станция',
                    })

    # print('Запрос, чтобы получить ближайшие станции:', r.url)
    print(r.json())
    for station in r.json()['stations']:

        # check if it's MCC station
        if station['title'] in scrap_stations_names():

            # TODO: get schedule to nearest MCC station
            # print(station)
            # schedule = get_schedule(station['code'])

            update.message.reply_text('Ближайшая станция к вам - '
                                      '{}'.format(station['title'])
                                      )

            break


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(config.TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, text))
    dp.add_handler(MessageHandler(Filters.location, location))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
