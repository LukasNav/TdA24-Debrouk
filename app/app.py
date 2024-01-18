import os
import json

from flask import Flask, render_template, url_for, jsonify
from . import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)




def getData():
    file=open("data.json","r")
    data=file.read()
    data=json.loads(data)
    return data



# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/lecturer')
def card():  # put application's code here
    return render_template('card.html',data=getData())
    # return os.getcwd()

@app.route('/api', methods=['GET'])
def handle_method():
    # if request.method == 'GET':
    #     return 'This is a GET request.'
    data = {'secret': 'The cake is a lie'}
    return jsonify(data)



if __name__ == '__main__':
    app.run()
