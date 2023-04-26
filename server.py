from flask_app import app
from flask_app.controllers import user_routes,post_routes
from flask_app.models import user_model, post_model
from flask import render_template, redirect, session
import datetime as dt
import requests

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def index_home():
    return render_template('index.html')


@app.errorhandler(404)
def invalid_request(e):
    return ('Please go back and enter a valid URL')

if __name__ == "__main__":
    app.run(debug=True)