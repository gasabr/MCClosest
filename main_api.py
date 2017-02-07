#!/usr/bin/env python3
import requests
import logging
import json     # debugging 
from datetime import datetime, timedelta, date
import time
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

# TODO: write a request API


def get_schedule(code):
    ''' Returns this day schedule for the station encoded by code attribute. '''
    schedule = []
    for page in schedule_pages(code):
        # TODO: would be nice to get rid of this string
        for p in page:
            schedule.append(p)

    return schedule


def request_schedule(code, page=1):
    ''' To follow the DRY principle in the schedule_pages function. '''
    response = requests.get(config.YA_API_STATION, params = {
                'apikey' : config.YA_API_KEY,
                'station': code,
                'date'   : datetime.strftime(datetime.now(), '%Y-%m-%d'),
                'format' : 'json',
                'lang'   : 'ru',
                'page'   : page,
        })

    return response.json()


def schedule_pages(code):
    ''' Generates pages of the schedule. '''
    page_n = 1
    page = request_schedule(code, page_n)

    while page_n <= page['pagination']['page_count']:
        yield page['schedule']

        page_n += 1
        page = request_schedule(code, page_n)


def parse_schedule(schedule):
    ''' Returns closest trains from given schedule. '''
    now = datetime.now()
    
    # find the first train after now
    # for s in schedule[:10]:
    #     dep_time = datetime.strftime(s['departure_time'])
    #     print(dep_time)

    return []


def text(bot, update):
    ''' Finds closest station from geo object represented by string. '''
    list_of_places = get_coordinates([bot.message.text])

    nearest_station = find_nearest(list_of_places[0])

    # TODO: call location() with coordinates of nearest station


def find_nearest(place):
    ''' Find closest station from given longtitude, latutude. '''
    r = requests.get(config.YA_API_NEAREST, params={
            'apikey'  : config.YA_API_KEY,
            'lat'     : place[1],
            'lon'     : place[0],
            'distance': 10,
            'format'  : 'json',
            'transport_types': 'suburban',
        })

    return r.json()


# TODO: solve following pronlem
#       function is redudant since i can add find_nearest as handler,
#       but i can't
#       other way is to call location() from text(), 
#       but that doesn't semm possible
# TODO: read why does this thing mute all the errors?
def location(bot, update):
    ''' Will call normal function instead of bot method. '''
    user = update.message.from_user
    user_location = update.message.location

    r = requests.get(config.YA_API_NEAREST, params= {
                     'apikey'  : config.YA_API_KEY,
                     'lat'     : user_location['latitude'],
                     'lng'     : user_location['longitude'],
                     'distance': 3,
                     'format'  : 'json',
                     'transport_types': 'train',
                     'station_type'   : 'станция',
                    })

    for station in r.json()['stations']:

        # check if it's MCC station
        # scrap stations every time is not the best solution
        if station['title'] in scrap_stations_names():
            print('oopps')
            schedule = get_schedule(station['code'])
            print(len(schedule))
            nearest  = parse_schedule(schedule)

            print('SСHEDULE for :')
            # print(json.dumps(schedule, indent=2, ensure_ascii=False), '\n\n')
            # print(json.dumps(nearest, indent=2, ensure_ascii=False))

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
