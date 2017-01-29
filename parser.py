#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sqlite3

from config import Station # namedtuple


STATION_LIST_URL = "http://mkmzd.ru/stations/"
YA_MAPS_URL = "https://geocode-maps.yandex.ru/1.x/?format=json&geocode="
SCHEDULE_URL_BASE = "https://rasp.yandex.ru/station/"
SCHEDULE_START_N = 9855157
SCHEDULE_URL_APPENDIX = "type=suburban&span=schedule"


def scrap_stations_names():
    # TODO: what is the right name for the function?
    # TODO: docstring for station_names()
    r = requests.get(STATION_LIST_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    stations = [] # list of 31 station names
    for l in soup.ol():
        try:
            stations.append(l.a.text)
        # TODO: where from this exception comes?
        except AttributeError as e:
            pass

    print("%d stations were parsed" % len(stations))

    return stations


def get_coordinates(places):
    # TODO: docstring for get_coordinates()
    places_info = []
    for p in places:
        request_place = 'Москва мцк ' + p # to make request more accurate
        r = requests.get(YA_MAPS_URL + request_place)
        objects = r.json()['response']['GeoObjectCollection']['featureMember']

        for o in objects:
            object_meta = o['GeoObject']['metaDataProperty']
            if object_meta['GeocoderMetaData']['kind'] == 'metro':
                lon, lat = map(float, o['GeoObject']['Point']['pos'].split(' '))
                places_info.append(Station(p, lon, lat))
                # as soon as we found metro -- break loop
                break

    return places_info


def main():
    print('Testing parser:')

    stations_list = scrap_stations_names()
    print('List of station contains %d titles' % len(stations_list))

    stations = get_coordinates(stations_list)
    print('%d couples (lon, lat) were received from Yandex Maps' % len(stations))
    
    if len(stations) == len(stations_list) == 31:
        print('\nAll stations were successfully scraped/parsed.')


if __name__ == "__main__":
    main()