from .user import UsersApiMongo, UsersApiSQL
from .auth import SignupApi, LoginApi, TokenRefresh


def initialize_routes(api):
    api.add_resource(UsersApiMongo, '/api/v1/musers')
    api.add_resource(UsersApiSQL, '/api/v1/users')
    # api.add_resource(MovieApi, '/api/movies/<id>')

    api.add_resource(SignupApi, '/api/v1/auth/signup')
    api.add_resource(LoginApi, '/api/v1/auth/login')
    api.add_resource(TokenRefresh, '/api/v1/auth/tokenrefresh')
