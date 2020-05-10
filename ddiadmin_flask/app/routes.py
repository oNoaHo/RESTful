from app import app
from pymongo import MongoClient
from random import randint
from flask import request, jsonify
import string
import pprint
import json


@app.route('/')
@app.route('/index')
def index():
    adminrights = False
    record = ""
    recordtype = ""
    if 'record' in request.args:
        record = str(request.args['record'].lower())
    else:
        return "Error: No record field provided. Please specify an record."
    if 'type' in request.args:
        recordtype = str(request.args['type'].lower())
    else:
        return "Error: No type field provided. Please specify an type."
    print(record + " " + recordtype)
    client = MongoClient("mongodb://192.168.4.58:27017/")
    ddiadmindb = client.ddiadmin
    users = ddiadmindb.users
    ASingleReview = users.find_one({"id": 'w50cjm'})
    # pprint.pprint(ASingleReview)
    # user = json.loads(ASingleReview)
    # return "Hello, World!" + ASingleReview.firstname
    if "zones" in ASingleReview.keys():
        length = len(ASingleReview["zones"])
        print("length zones: " + str(length))
        for i in range(length):
            if ASingleReview["zones"][i]["name"] == record:
                if ASingleReview["zones"][i]["rights"][recordtype] == 1:
                    adminrights = True
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
                        print("RECORD: " +
                              str(ASingleReview["records"][i]["rights"][recordtype]))
    return '' + str(adminrights)
