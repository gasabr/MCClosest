import config
import sqlite3

def db_action(db_action):
    '''Decorator to open and close connection with db'''
    def action_wrapper(*args):
        # connect to db
        conn = sqlite3.connect(config.DB_NAME)
        c = conn.cursor()

        # call wrapped function
        db_action(*args)

        # commit changes and close connection
        c.close()
        conn.commit()
        conn.close()

    return action_wrapper


@db_action
def create_tables():
    '''scheme is a dict'''
    request = '''CREATE TABLE IF NOT EXISTS '''

    for table_name, columns in config.DB_SCHEME.items():
        request += table_name + ' ('
        for col_name, col_type in columns.items():
            request += col_name + ' ' + col_type + ','
    request += ')'

    print(request)

    c.execute(request)


def write_to(table, data):
    ''''''
    table_name = table.lower()
    if table_name == 'locations':
        _write_locations(data)
    elif table_name == 'schedule':
        # TODO: create func here
        print('not implemented')
        pass
    else:
        # TODO: proper exception 
        raise NameError('No table %s in db' % table_name)

    return None


    # @db_action
    # def _write_to_locations()