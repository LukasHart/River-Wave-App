from flask_app import app
from flask_app.models import user_model,post_model
import datetime as dt
import requests
import math
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register')
def registration_page():
    return render_template('registration.html')

@app.route('/register', methods = ['POST'])
def register():
    
    if user_model.User.validate_registration(request.form):
        
        user_model.User.save({
            'user_name': request.form['user_name'],
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password':bcrypt.generate_password_hash(request.form['password'])
        })
        
        flash('Successfully Registered', 'registration')
    return redirect('/register')

@app.route('/login')
def login_form():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    
    user = user_model.User.get_by_email(request.form['email'])
    
    if user == None or bcrypt.check_password_hash(user.password, request.form['password']) == False:
        flash('Invalid Credentials', 'login')
        return redirect('/login')
    
    session['user_id'] = user.id
    session['user_name'] = user.user_name
    print(session['user_name'])
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "8848cc0b4d92bb8f7d915bc8a49906a6"
CITY = "Bend"

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

def kmh_to_mph(kmh):
    mph = kmh * .62
    return mph
    

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()

temp_kelvin = response['main']['temp']
temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
feels_like_kelvin = response['main']['feels_like']
feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
wind_speed_kmh = response['wind']['speed']
wind_speed_mph = kmh_to_mph(wind_speed_kmh)
humidity = response['main']['humidity']
info = response['weather'][0]['main']
description = response['weather'][0]['description']
timezone = response['timezone']
icon = response['weather'][0]['icon']
sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
print(wind_speed_kmh)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', posts = post_model.Post.get_users_posts(), temp_fahrenheit = math.floor(temp_fahrenheit), city = CITY, time = timezone, description = description, humidity = humidity,sunrise_time = sunrise_time,sunset_time = sunset_time, wind_speed_mph = math.floor(wind_speed_mph), feels_like_fahrenheit = math.floor(feels_like_fahrenheit))

