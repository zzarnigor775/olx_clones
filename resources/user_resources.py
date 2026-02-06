from models import db
from flask import Blueprint
from models.user import User
from utilis import get_respose
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import create_access_token

auth_login_parser = RequestParser()
auth_login_parser.add_argument("username", type=str, required=True)
auth_login_parser.add_argument("password", type=str, required=True)

auth_register_parser = RequestParser()
auth_register_parser.add_argument("fullname", type=str, required=True)
auth_register_parser.add_argument("username", type=str, required=True)
auth_register_parser.add_argument("password", type=str, required=True)
auth_register_parser.add_argument("role", type=str, required=True)

user_bp = Blueprint("user", __name__, url_prefix="/api/user")
api = Api(user_bp)

class AuthLoginResource(Resource):
    def post(self):
        """Auth Login API
        Path - /api/user/login
        Method - POST
        ---
        consumes: application/json
        parameters:
            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    username: 
                        type: string
                    password:
                        type: string
                required: [username, password]
        responses:
            200:
                description: Return Access Token
        """
        data = auth_login_parser.parse_args()
        username = data['username']
        password = data['password']

        found_user = User.query.filter_by(username=username, password=password).first()
        if not found_user:
            return get_respose("o'tolmadingiz", None, 401)
        
        token = create_access_token(identity=found_user.username)
        result = {
            "token ": token,
            "user_id": found_user.id
        }
        return get_respose("ro'yhatdan o'tildi", result, 200)

class AuthRegisterResource(Resource):
    def post(self):
        """Auth Register API
        Path - /api/user/register
        Method - POST
        ---
        consumes: application/json
        parameters:
            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    fullname:
                        type: string
                    username: 
                        type: string
                    password:
                        type: string
                    role:
                        type: string
                required: [fullname, username, password, role]
        responses:
            200:
                description: Return Access Token
        """
        data = auth_register_parser.parse_args()

        fullname = data['fullname']
        username = data['username']
        password = data['password']
        role = data['role']

        new_user =  User(fullname, username, password, role)
        db.session.add(new_user)
        db.session.commit()
         
        return get_respose("ro'yhatga olindi", new_user.to_dict(), 201)
    
api.add_resource(AuthLoginResource, "/login")
api.add_resource(AuthRegisterResource, "/register")