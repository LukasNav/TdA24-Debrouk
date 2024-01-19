import os
import json

from flask import Flask, render_template, url_for, jsonify, request
from . import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)




# def getData():
#     path="./app/data.json"
#     file=open(path,"r")
#     data=file.read()
#     data=json.loads(data)
#     return data




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
def lecturer():  # put application's code here
    return render_template('card.html',lecturers=db.get_lecturers())
    # return getData()


#api

@app.route('/lecturers', methods=['GET'])
def get_lecturers():

    # return db.get_lecturers()
    return jsonify(db.get_lecturers())


@app.route('/lecturers', methods=['POST'])
def post_lecturer():
    lecturer=request.get_json()
    return jsonify(db.post_lecturer(lecturer))

@app.route('/lecturers/<uuid>', methods=['GET'])
def get_lecturer(uuid):

    return jsonify(db.get_lecturer(uuid))
    # return

@app.route('/lecturers/<uuid>', methods=['PUT'])
def put_lecturer(uuid):
    change=request.get_json()
    return jsonify(db.put_lecturer(uuid,change))

@app.route('/lecturers/<uuid>', methods=['DELETE'])
def delete_lecturer(uuid):
    return jsonify(db.delete_lecturer(uuid))

if __name__ == '__main__':
    app.run()
