from flask import Response, request, jsonify
from database.models import users, apiuser, groups
from pymongo import MongoClient
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, UserAlreadyExistsError, InternalServerError, \
    UpdatingUserError, DeletingUserError, UserNotExistsError, ExpiredSignatureError, WrongTokenError
from werkzeug.http import HTTP_STATUS_CODES
import json
import pprint


class UsersApiMongo(Resource):
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
            if len(user.zones) > 0:
                for i in range(len(user.zones)):
                    if user.zones[i]["name"] == record:
                        objectmessage = "object found"
                        if user.zones[i]["rights"][recordtype] == 1:
                            rightsmessage = "rights given"
                            adminrights = True
                            dnsobject = user["zones"][i]
            if adminrights == False:
                if len(user.records) > 0:
                    for i in range(len(user.records)):
                        if user.records[i]["name"] == record:
                            objectmessage = "object found"
                            if user.records[i]["rights"][recordtype] == 1:
                                rightsmessage = "rights given"
                                adminrights = True
                                dnsobject = user.records[i]
            if adminrights == False:
                if len(user.groups) > 0:
                    for i in range(len(user.groups)):
                        group = groups.objects.get(name=user.groups[i]["name"])
                        if len(group.zones) > 0:
                            for i in range(len(group.zones)):
                                if group.zones[i]["name"] == record:
                                    objectmessage = "object found"
                                    if group.zones[i]["rights"][recordtype] == 1:
                                        rightsmessage = "rights given"
                                        adminrights = True
                                        dnsobject = group.zones[i]
                        if adminrights == False:
                            if len(group.records) > 0:
                                for i in range(len(group.records)):
                                    if group.records[i]["name"] == record:
                                        objectmessage = "object found"
                                        if group.records[i]["rights"][recordtype] == 1:
                                            rightsmessage = "rights given"
                                            adminrights = True
                                            dnsobject = group["records"][i]
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


class UsersApiSQL(Resource):
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
            pass
        else:
            status_code = 400
            return Response({'status': 'error',
                             'error': HTTP_STATUS_CODES.get(status_code, 'Unknown or missing object'),
                             'message': 'missing UserID\n' + str(body)},
                            mimetype="application/json",
                            status=status_code)
        return jsonify({'status': 'ok',
                        'allowed': adminrights,
                        'object': dnsobject,
                        'message': objectmessage + " / " + rightsmessage})

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = apiuser.objects.get(id=user_id)
            ddiuser = users(**body, added_by=user)
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
