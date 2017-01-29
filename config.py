from YamJam import yamjam
from collections import namedtuple


TELEGRAM_TOKEN = yamjam()['MCClosest']['TELEGRAM_TOKEN']
YANDEX_API_KEY = yamjam()['MCClosest']['YANDEX_API_KEY']

DB_NAME = 'MCClosest.db'
DB_SCHEME = {
    'Locations': {
        'lat' : 'REAL',
        'lon' : 'REAL',
        'name': 'TEXT',
    }
}

Station = namedtuple('Station', ['name', 'lon', 'lat'])