from models import db
from flask import Blueprint
from models.user import User
from utilis import get_respose
from models.category import Category
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful.reqparse import RequestParser
from models.elon import Elon

elon_create_parser = RequestParser()
elon_create_parser.add_argument("title", type=str, required=True)
elon_create_parser.add_argument("description", type=str, required=True)
elon_create_parser.add_argument("price", type=float, required=True)
elon_create_parser.add_argument("category_id", type=int, required=True)
elon_create_parser.add_argument("image_url", type=str, required=True)

elon_update_parser = RequestParser()
elon_update_parser.add_argument("title", type=str)
elon_update_parser.add_argument("description", type=str)
elon_update_parser.add_argument("price", type=float)
elon_update_parser.add_argument("category_id", type=int)
elon_update_parser.add_argument("image_url", type=str)

elon_bp = Blueprint("elon", __name__, url_prefix="/api/elon")
api = Api(elon_bp)

class ElonCreateResource(Resource):
    @jwt_required()
    def post(self):
        """Elon Create API
        Path - /api/elon
        Method - POST
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              reqiured: true
              description: Bearer token for authorization

            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    title: 
                        type: string
                    description:
                        type: string
                    price:
                        type: float
                    category_id:
                        type: int
                    image_url:
                        type: string
                required: [title, description, price, category_id, image_url]
        responses:
            200:
                description: Return Access Token
        """
        username = get_jwt_identity()
        found_user = User.query.filter_by(username=username).first()

        data = elon_create_parser.parse_args()
        category_id = data['category_id']
        found_category = Category.query.filter_by(id=category_id).first()

        if found_category:
            new_data =  Elon(
            user_id = found_user.id,
            title = data['title'],
            description = data['description'],
            category_id = found_category.id,
            price = data['price'],
            image_url = data['image_url']
            )
            db.session.add(new_data)
            db.session.commit()
            return get_respose("Yaratildi", None, 200)
        else: 
            return get_respose("xato kiritildi", None, 404)
        
    @jwt_required()
    def get(self):
        """ Elon List API
        Path - /api/elon
        Method - GET
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              reqiured: true
              description: Bearer token for authorization
        responses:
            200:
                description: Return Access Token
        """
        found_data = Elon.query.all()
        
        return get_respose("Elon List", [data.to_dict() for data in found_data], 200)

class ElonDetailResource(Resource):
    @jwt_required()
    def delete(self, elon_id):
        """ Elon Delete API
        Path - /api/elon/<elon_id>
        Method - DELETE
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              reqiured: true
              description: Bearer token for authorization

            - name: elon_id
              in: path
              type: integer
              required: true
              description: Enter Elon ID
        responses:
            200:
                description: Return Access Token
        """
        username = get_jwt_identity()
        found_user = User.query.filter_by(username=username).first()
        found_data = Elon.query.filter_by(user_id=found_user.id, id=elon_id).first()
        if found_data:   
            db.session.delete(found_data)
            db.session.commit()
            return get_respose("o'chirildi", None, 200)
        else:
            return get_respose("Topilmadi", None, 404)

    @jwt_required()
    def get(self, elon_id):
        """ Elon Get API
        Path - /api/elon/<elon_id>
        Method - GET
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              reqiured: true
              description: Bearer token for authorization
            
            - name: elon_id
              in: path
              type: integer
              required: true
              description: Enter Elon ID
        responses:
            200:
                description: Return Access Token
        """
        found_data = Elon.query.filter_by(id=elon_id).first()
        
        return get_respose("Elon Get", found_data.to_dict(), 200)
    
    @jwt_required()
    def patch(self, elon_id):
        """ Elon Update API
        Path - /api/elon/<elon_id>
        Method - PATCH
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              reqiured: true
              description: Bearer token for authorization

            - name: elon_id
              in: path
              type: integer
              required: true
              description: Enter Elon ID

            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    title: 
                        type: string
                    description:
                        type: string
                    price:
                        type: float
                    category_id:
                        type: int
                    image_url:
                        type: string
        responses:
            200:
                description: Return Access Token
        """
        username = get_jwt_identity()
        found_user = User.query.filter_by(username=username).first()
        found_data = Elon.query.filter_by(user_id=found_user.id, id=elon_id).first()
        if not found_data:
            return get_respose("Topilmadi", None, 404)
        
        data = elon_update_parser.parse_args()

        title = data['title']
        if title is not None:
            found_data.title = title

        description = data['description']
        if description is not None:
            found_data.description = description
        
        price = data['price']
        if price is not None:
            found_data.price = price
        
        category_id = data['category_id']
        if category_id is not None:
            found_data.category_id = category_id

        image_url = data['image_url']
        if image_url is not None:
            found_data.image_url = image_url
        
        db.session.commit()

        return get_respose("e'lon o'zgartirildi", None, 200)

api.add_resource(ElonCreateResource, "/")
api.add_resource(ElonDetailResource,"/<elon_id>")
