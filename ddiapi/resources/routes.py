from .ddi import UsersApi
from .auth import SignupApi, LoginApi

def initialize_routes(api):
    api.add_resource(UsersApi, '/api/users')
    #api.add_resource(UserApi, '/api/user/<id>')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
