from flask import Response, request
from database.models import DDIUser, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, DDIUserAlreadyExistsError, InternalServerError, \
UpdatingDDIUserError, DeletingDDIUserError, DDIUserNotExistsError


class UsersApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        query = DDIUser.objects()
        users = DDIUser.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

