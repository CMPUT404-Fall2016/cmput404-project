import flask
from flask import Flask, request, render_template
import json
app = Flask(__name__, static_url_path='')
app.debug = True


@app.route('/login.html')
@app.route('/')
def login():
    return app.send_static_file('login.html')


@app.route('/index.html')
def start():
    return app.send_static_file('index.html')


@app.route('/profile.html')
def return ap.send_static_file('profile.html')

if __name__ == "__main__":
    app.run()
