from models import Weather


SQL_DELETA_WEATHER_ID = 'DELETE FROM weather_db WHERE id = %s;'
SQL_DELETA_WEATHER_CIDADE = 'DELETE FROM weather_db WHERE city = %s;'


SQL_WEATHER_BUSCA_POR_CIDADE = 'SELECT city, weather, description, minima, maxima from weather_db where city = %s;'
SQL_WEATHER_BUSCA_POR_ID = 'SELECT city, weather, description, minima, maxima from weather_db where id = %s;'
SQL_BUSCA_WEATHER = 'SELECT * FROM weather_db;'

SQL_ATUALIZA_WEATHER = 'UPDATE weather_db SET weather= %s description= %s minima= %s maxima= %s where city = %s;'

SQL_CRIA_WEATHER = 'INSERT INTO weather_db(city, weather, description, minima, maxima) VALUES (%s,%s,%s,%s,%s);'

SQL_CRIA_TABELA_WEATHER = """
        create table if not exists weather_db
        (
            id SERIAL PRIMARY KEY,
            city VARCHAR(200) UNIQUE not null,
            weather VARCHAR(200) not null,
            description VARCHAR(200) not null,
            minima VARCHAR(200) not null,
            maxima VARCHAR(200) not null
        );
    """


class WeatherDao:
    def __init__(self, db):
        self.__db = db
        cursor = self.__db.cursor()
        cursor.execute(SQL_CRIA_TABELA_WEATHER)

    def salvar(self, weather):
        cursor = self.__db.cursor()
        try:
            if (weather.id):
                cursor.execute(SQL_ATUALIZA_WEATHER, (
                            weather.weather, weather.description, weather.minima, weather.maxima, weather.city))
            else:
                cursor.execute(SQL_CRIA_WEATHER, (weather.city,
                            weather.weather, weather.description, weather.minima, weather.maxima))
                weather.id = cursor.lastrowid
            self.__db.commit()
        except Exception as e:
            raise e

        return weather

    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_WEATHER)
        weathers = tarnsforma_lista(cursor.fetchall())
        return weathers

    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_WEATHER_BUSCA_POR_ID, (id,))
        vect = cursor.fetchone()
        if vect:
            return Weather(vect[1], vect[2], vect[3], vect[4], vect[5], vect[0])
        else:
            return None

    def deletar_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_DELETA_WEATHER_ID, (id, ))
        self.__db.commit()

    def busca_por_cidade(self, city):
        cursor = self.__db.cursor()
        cursor.execute(SQL_WEATHER_BUSCA_POR_CIDADE, (city,))
        vect = cursor.fetchone()
        if vect:
            return Weather(vect[1], vect[2], vect[3], vect[4], vect[5], vect[0])
        else:
            return None

    def deletar_por_cidade(self, city):
        cursor = self.__db.cursor()
        cursor.execute(SQL_DELETA_WEATHER_CIDADE, (city, ))
        self.__db.commit()

def tarnsforma_lista(weather):
    def cria_vectors(vect):
        return Weather(vect[1], vect[2], vect[3], vect[4], vect[5], vect[0])
    return list(map(cria_vectors, weather))
