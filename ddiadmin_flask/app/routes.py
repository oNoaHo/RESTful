from app import app
from pymongo import MongoClient
from flask import request, jsonify
from werkzeug.http import HTTP_STATUS_CODES
import string
import json


@app.route('/')
@app.route('/index')
def index():
    return "<h1>DDI Admin API</h1><p>This site is a prototype API for requesting user rights against DDI Admin</p>"


@app.route('/api/v1/users')
def rights():
    adminrights = False
    dnsobject = []
    record = ""
    recordtype = ""
    if 'record' in request.args:
        record = str(request.args['record'].lower())
    else:
        status_code = 404
    # return "Error: No record field provided. Please specify an record."
        response = jsonify({'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
                            'message': 'The requested object ' +
                            record + ' doesn\'t exists'})
        response.status_code = status_code
        return response
    if 'type' in request.args:
        recordtype = str(request.args['type'].lower())
    else:
        status_code = 404
        response = jsonify({'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
                            'message': 'The requested object ' +
                            recordtype + ' doesn\'t exists'})
        response.status_code = status_code
        return response
    print(record + " " + recordtype)
    client = MongoClient("mongodb://192.168.4.58:27017/")
    ddiadmindb = client.ddiadmin
    users = ddiadmindb.users
    ASingleReview = users.find_one({"id": 'w50cjm'})
    # user = json.loads(ASingleReview)
    # return "Hello, World!" + ASingleReview.firstname
    if "zones" in ASingleReview.keys():
        length = len(ASingleReview["zones"])
        print("length zones: " + str(length))
        for i in range(length):
            if ASingleReview["zones"][i]["name"] == record:
                if ASingleReview["zones"][i]["rights"][recordtype] == 1:
                    adminrights = True
                    dnsobject = ASingleReview["zones"][i]
                    print(
                        "ZONE: " + str(ASingleReview["zones"][i]["rights"][recordtype]))
    if adminrights == False:
        if "records" in ASingleReview.keys():
            length = len(ASingleReview["records"])
            print("length records: " + str(length))
            for i in range(length):
                if ASingleReview["records"][i]["name"] == record:
                    print("RECORD: " +
                          str(ASingleReview["records"][i]["name"]))
                    if ASingleReview["records"][i]["rights"][recordtype] == 1:
                        adminrights = True
                        dnsobject = ASingleReview["records"][i]
                        print("RECORD: " +
                              str(ASingleReview["records"][i]["rights"][recordtype]))
    return jsonify({'allowed': adminrights, 'object': dnsobject})
