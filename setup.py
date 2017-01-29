#!/usr/bin/env python3

from db_manager import DBManager
import config
import parser


if __name__ == '__main__':
    # create db and tables
    d = DBManager(config.DB_NAME)
    d.create_tables(config.DB_SCHEME)

    # parse information
    stations_list = parser.scrap_stations_names()
    stations      = parser.get_coordinates(stations_list)

    # dumb info into db
    d.insert_into(table='Locations', data=stations)
