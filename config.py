import psycopg2, os

def connect_db(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT):
    ''' Connect to Database
    Notes:
        This method connects the program to the database.
    '''

    db = psycopg2.connect(dbname=(DB_NAME),
                          user=(DB_USER),
                          password=(DB_PASSWORD),
                          host=(DB_HOST),
                          port=(DB_PORT))
    return db


def kelvin_to_celsius(tmp):
    ''' Convert Kelvin to Celsius
    Notes:
        This method converts the kelvin value to celsius
    '''
    return tmp - 273.15
