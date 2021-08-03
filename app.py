from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import kelvin_to_celsius, connect_db
from dao import WeatherDao
from models import Weather
import requests, os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

app = Flask(__name__)


# POSTGRES_CONFIG=os.getenv('POSTGRES_CONFIG')
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://{}'.format(POSTGRES_CONFIG)
# db=SQLAlchemy(app)

db = connect_db(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)



@app.route('/')
def index():
    '''show index

    args:
        name (string) \n
        id (int)


    notes:
        function to return a index
    '''


    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    city = request.form['cidade']
    URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, API_KEY)
    req = requests.request('GET', URL).json()
    if req['cod'] == '404' or not 'weather' in req:
        error = 'Cidade Inválida'
        not_found = True
        return render_template('index.html', error=error, not_found=not_found)
    weather = req['weather'][0]['main']
    description = req['weather'][0]['description']
    minima = round(kelvin_to_celsius(req['main']['temp_min']), 2)
    maxima = round(kelvin_to_celsius(req['main']['temp_max']), 2)

    

    wthr = Weather(city=city, weather=weather, description=description, minima=minima, maxima=maxima)
    wthr_dao = WeatherDao(db)
    wthr_dao.salvar(wthr)


    return render_template('index.html', city=city, weather=weather, description=description, minima=minima, maxima=maxima)


if __name__ == '__main__':
    app.run(debug=True)
