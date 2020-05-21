class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UpdatingUserError(Exception):
    pass


class DeletingUserError(Exception):
    pass


class UserNotExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ExpiredSignatureError(Exception):
    pass


class WrongTokenError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UserAlreadyExistsError": {
        "message": "User with given name already exists",
        "status": 400
    },
    "UpdatingUserError": {
        "message": "Updating User added by other is forbidden",
        "status": 403
    },
    "DeletingUserError": {
        "message": "Deleting User added by other is forbidden",
        "status": 403
    },
    "UserNotExistsError": {
        "message": "User with given id doesn't exists",
        "status": 400
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
    "ExpiredSignatureError": {
        "message": "Session expired",
        "status": 401
    },
    "WrongTokenError": {
        "message": "Wrong token given. Please use valid access token",
        "status": 401
    }
}
