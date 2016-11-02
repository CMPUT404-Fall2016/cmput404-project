import flask
from flask import Flask, request, render_template
import json
app = Flask(__name__, static_url_path='')
app.debug = True


@app.route('/login.html')
def login():
    return app.send_static_file('login.html')


@app.route('/index.html')
def start():
    return app.send_static_file('index.html')



if __name__ == "__main__":
    app.run()
