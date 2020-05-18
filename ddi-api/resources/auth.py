from flask import Response, request
from flask_jwt_extended import create_access_token
from database.models import apiuser
from flask_restful import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, InternalServerError


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            apiusers = apiuser(**body)
            apiusers.hash_password()
            apiusers.save()
            id = apiusers.id
            return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            apiusers = apiuser.objects.get(name=body.get('name'))
            authorized = apiusers.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(minutes=1)
            access_token = create_access_token(
                identity=str(apiusers.id), expires_delta=expires)
            return {'token': access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError
