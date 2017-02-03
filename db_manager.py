import sqlite3
from math import sin, cos, sqrt, atan2, radians

from config import Place


EARTH_RADIUS = 6373.0

# TODO: migrate to SQLAlchemy

def geo_dist(point1, point2) -> float:
    '''takes 2 tuples, returns haversine distance.'''
    lon1, lat1 = map(radians, point1)
    lon2, lat2 = map(radians, point2)

    dlon = lon1 - lon2
    dlat = lat1 - lat2

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = EARTH_RADIUS * c

    return distance


class DBManager:

    def __init__(self, db_name):
        self._db_name = db_name
        # TODO: check if database exists
        self.connection = sqlite3.connect(self._db_name)
        self.cursor = self.connection.cursor()

    def __del__(self, **kwargs):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()

    def create_tables(self, scheme):
        '''Creates tables from the dictionary scheme.'''
        request = '''CREATE TABLE IF NOT EXISTS '''

        for table_name, columns in scheme.items():
            request += table_name + ' ('
            for col_name, col_type in columns.items():
                request += col_name + ' ' + col_type + ','
        request = request[:-1] + ')'

        self.cursor.execute(request)

    def insert_into(self, table, data):
        ''' Insert tuple representing row in the table.

            takes table name and array of tuples 
            (one tuple) = one row
            records values from tuples to rows
            NOTE: len(tuple) MUST be equal to the number 
                  of columns in the table
        '''
        query_base = 'INSERT INTO %s ' % table
        for row in data:
            values = 'VALUES ('
            values += '?, '*len(row)
            values = values[:-2] + ');'

            query = query_base + values

            self.cursor.execute(query, row)

        self.connection.commit()

        return None

    def find_closest(self, lon, lat):
        ''' Finds the closest station to given coordinates.

            returns (PlaceName, lon, lat)
        '''

        min_dist = 1000000
        closest_station = None

        self.cursor.execute('SELECT * FROM Locations')
        stations = self.cursor.fetchall()
        
        for station in stations:
            dist = geo_dist((lon, lat), (station[1], station[2]))
            if dist < min_dist:
                min_dist = dist
                closest_station = station

        return Place(closest_station[0], # name
                       closest_station[1], # longtitude
                       closest_station[2]  # latitude
                       )
