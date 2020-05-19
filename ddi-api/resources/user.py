from flask import Response, request, jsonify
from database.models import users, apiuser, groups
from pymongo import MongoClient
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, UserAlreadyExistsError, InternalServerError, \
    UpdatingUserError, DeletingUserError, UserNotExistsError
from werkzeug.http import HTTP_STATUS_CODES
import json
import pprint


class UsersApi(Resource):
    @jwt_required
    def get(self):
        adminrights = False
        dnsobject = []
        record = ""
        recordtype = ""
        objectmessage = "object not found"
        rightsmessage = "type not allowed"
        body = request.args
        if body.get('record'):
            record = str(body.get('record').lower())
        else:
            status_code = 400
            return Response({'status': 'error',
                             'error': HTTP_STATUS_CODES.get(status_code, 'Unknown or missing object'),
                             'message': 'The requested object ' +
                             record + ' doesn\'t exists\n' + str(body)},
                            mimetype="application/json",
                            status=status_code)
        if body.get('type'):
            recordtype = str(body.get('type').lower())
        else:
            status_code = 400
            return Response({'status': 'error',
                             'error': HTTP_STATUS_CODES.get(status_code, 'Unknown or missing object'),
                             'message': 'The requested object ' +
                             recordtype + ' doesn\'t exists\n' + str(body)},
                            mimetype="application/json",
                            status=status_code)
        if body.get('userid'):
            user = users.objects.get(userid=body.get('userid'))
            if user.zones:
                for i in range(len(user.zones)):
                    if user.zones[i]["name"] == record:
                        objectmessage = "object found"
                        if user.zones[i]["rights"][recordtype] == 1:
                            rightsmessage = "rights given"
                            adminrights = True
                            dnsobject = user["zones"][i]
                            print("ZONE: " + str(user.zones[i]["rights"][recordtype]))
            if adminrights == False:
                if user.records:
                    for i in range(len(user.records)):
                        if user.records[i]["name"] == record:
                            objectmessage = "object found"
                            if user.records[i]["rights"][recordtype] == 1:
                                rightsmessage = "rights given"
                                adminrights = True
                                dnsobject = user.records[i]
                                print("RECORD: " +
                                      str(user["records"][i]["rights"][recordtype]))
            if adminrights == False:
                if user.groups:
                    for i in range(len(user.groups)):
                        group = json.loads(groups.objects.get(
                            name=user.groups[i]["name"]).to_json())
                        if "zones" in group.keys():
                            length = len(group["zones"])
                            print("length gzones: " + str(length))
                            for i in range(length):
                                if group["zones"][i]["name"] == record:
                                    objectmessage = "object found"
                                    if group["zones"][i]["rights"][recordtype] == 1:
                                        rightsmessage = "rights given"
                                        adminrights = True
                                        dnsobject = group["zones"][i]
                                        print(
                                            "GZONE: " + str(group["zones"][i]["rights"][recordtype]))
                        if adminrights == False:
                            if "records" in group.keys():
                                length = len(group["records"])
                                print("length grecords: " + str(length))
                                for i in range(length):
                                    if group["records"][i]["name"] == record:
                                        objectmessage = "object found"
                                        print("GRECORD: " +
                                              str(group["records"][i]["name"]))
                                        if group["records"][i]["rights"][recordtype] == 1:
                                            rightsmessage = "rights given"
                                            adminrights = True
                                            dnsobject = group["records"][i]
                                            print("RECORD: " +
                                                  str(group["records"][i]["rights"][recordtype]))
            return jsonify({'status': 'ok',
                            'allowed': adminrights,
                            'object': dnsobject,
                            'message': objectmessage + " / " + rightsmessage})
        else:
            status_code = 400
            return Response({'status': 'error',
                             'error': HTTP_STATUS_CODES.get(status_code, 'Unknown or missing object'),
                             'message': 'missing UserID\n' + str(body)},
                            mimetype="application/json",
                            status=status_code)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            ddiuser = DDIuser(**body, added_by=user)
            ddiuser.save()
            user.update(push__movies=ddiuser)
            user.save()
            id = ddiuser.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise UserAlreadyExistsError
        except Exception as e:
            raise InternalServerError
