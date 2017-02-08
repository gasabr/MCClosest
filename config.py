from YamJam import yamjam
from collections import namedtuple


TELEGRAM_TOKEN = yamjam()['MCClosest']['TELEGRAM_TOKEN']
YA_API_KEY = yamjam()['MCClosest']['YANDEX_API_KEY']

YA_API_NEAREST = 'https://api.rasp.yandex.net/v1.0/nearest_stations/'
YA_API_STATION = 'https://api.rasp.yandex.net/v1.0/schedule/'


DB_NAME = 'MCClosest.db'
DB_SCHEME = {
    'Locations': {
        'lat' : 'REAL',
        'lon' : 'REAL',
        'name': 'TEXT',
    }
}

Place = namedtuple('Place', ['name', 'lon', 'lat'])

reply_pattern = ('Ближайшие поезда на станции {station_name}:\n' 
				 'Направление                    | Время\n'
				 '{direction1:22} | {time1}\n'
				 '{direction2:22} | {time2}\n'
				 )
