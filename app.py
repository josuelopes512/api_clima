from flask import Flask, render_template, request
from config import *
from models import Weather
import requests, os

app = Flask(__name__)

API_KEY=os.getenv('API_KEY')

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
    
    return render_template('index.html', city=city, weather=weather, description=description, minima=minima, maxima=maxima)


if __name__ == '__main__':
    app.run(debug=True)