from YamJam import yamjam
from collections import namedtuple


secrets = yamjam()['MCClosest']

TELEGRAM_TOKEN = secrets['TELEGRAM_TOKEN']
YA_API_KEY = secrets['YANDEX_API_KEY']

WEBHOOK_HOST = secrets['SERVER_DOMAIN']
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = secrets['SERVER_IP']

WEBHOOK_SSL_CERT = 'webhook_cert.pem' # path to cert file
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TELEGRAM_TOKEN)
WEBHOOK_URL = WEBHOOK_URL_BASE + WEBHOOK_URL_PATH

YA_API_NEAREST = 'https://api.rasp.yandex.net/v1.0/nearest_stations/'
YA_API_STATION = 'https://api.rasp.yandex.net/v1.0/schedule/'

Place = namedtuple('Place', ['name', 'lon', 'lat'])

reply_pattern = ('Ближайшие поезда на станции {station_name}:\n'
				 'Направление                    | Время\n'
				 '{direction1:22} | {time1}\n'
				 '{direction2:22} | {time2}\n'
				 )
