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
    return render_template('card.html',lecturers=db.get_lecturers()),200
    # return getData()


#api

@app.route('/api/lecturers', methods=['GET'])
def get_lecturers():

    # return db.get_lecturers()
    return jsonify(db.get_lecturers()),200


@app.route('/api/lecturers', methods=['POST'])
def post_lecturer():
    lecturer=request.get_json()
    status=jsonify(db.post_lecturer(lecturer))
    if status !="ERROR":
        return status,200
    else:
        return status

@app.route('/api/lecturers/<uuid>', methods=['GET'])
def get_lecturer(uuid):
    lecturers=jsonify(db.get_lecturer(uuid))
    if lecturers != []:
        return lecturers,200
    else:
        return {"code": 404, "message": "Invalid uuid"},404


@app.route('/api/lecturers/<uuid>', methods=['PUT'])
def put_lecturer(uuid):
    change=request.get_json()
    return jsonify(db.put_lecturer(uuid,change)),200

@app.route('/api/lecturers/<uuid>', methods=['DELETE'])
def delete_lecturer(uuid):
    status=jsonify(db.delete_lecturer(uuid))
    if status == "OK":
        return status,204
    else:
        return {"code": 404, "message": "Invalid uuid"},404

if __name__ == '__main__':

    app.run()
