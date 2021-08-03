import psycopg2

def connect_db():
    ''' Connect to Database
    Notes:
        This method connects the program to the database.
    '''
    db = psycopg2.connect(dbname="weather_api",
                          user="postgres",
                          password="",
                          host="localhost",
                          port="5433")
    return db


def create_db(sql):
    ''' Create/Drop Database
    Args:
        sql : String
    Notes:
        This method is created or dropped
        the database by the user command.
    '''
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()


def query_db(sql):
    ''' Database query
    Args:
        sql : String
    Notes:
        Method Used to perform a database query.
    '''
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    regis = []
    for rec in recset:
        regis.append(rec)
    con.close()
    return regis


def insert_db(sql):
    ''' Insert a Character
    Args:
        sql: String
    Notes:
        This method inserts a character by name.
    '''
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        con.rollback()
        cur.close()
        return 1
    cur.close()


if __name__ == '__main__':

    sql = 'DROP TABLE IF EXISTS public.characters;'

    create_db(sql)

    sql = '''
        CREATE TABLE IF NOT EXISTS public.characters
        (
            id SERIAL PRIMARY KEY,
            name VARCHAR(20)
        );
    '''