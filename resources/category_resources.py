from models import db
from flask import Blueprint
from models.category import Category
from models.user import User
from utilis import get_respose
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful.reqparse import RequestParser

category_create_parser = RequestParser()
category_create_parser.add_argument("title", type=str, required=True)
category_create_parser.add_argument("description", type=str, required=True)

category_update_parser = RequestParser()
category_update_parser.add_argument("title", type=str)
category_update_parser.add_argument("description", type=str)

category_bp = Blueprint("category", __name__, url_prefix="/api/category")
api = Api(category_bp)

class CategoryCreateResource(Resource):
    @jwt_required()
    def post(self):
        """ Category Create API
        Path - /api/category
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
                required: [title, description]
        responses:
            200:
                description: Return Access Token
        """

        username = get_jwt_identity()
        found_user = User.query.filter_by(username=username).first()
        if found_user.role == 'admin':
            data = category_create_parser.parse_args()

            new_data = Category (
            title = data['title'],
            description = data['description']
            )
            db.session.add(new_data)
            db.session.commit()
            return get_respose("Category yaratildi", None, 201)
        else:
            return get_respose("Category faqat admin yarata oladi", None, 404)
        
    @jwt_required()
    def get(self):
        """ Category List API
        Path - /api/category
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
        found_data = Category.query.all()
        
        return get_respose("topildi", [data.to_dict() for data in found_data], 201)
    
class CategoryDetailResource(Resource):
    @jwt_required()
    def delete(self, category_id):
        """ Category Delete API
        Path - /api/category/<category_id>
        Method - DELETE
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              reqiured: true
              description: Bearer token for authorization

            - name: category_id
              in: path
              type: integer
              required: true
              description: Enter Category ID
        responses:
            200:
                description: Return Access Token
        """
        username = get_jwt_identity()
        found_user = User.query.filter_by(username=username).first()
        if found_user.role == 'admin':
            found_data = Category.query.filter_by(id=category_id).first()
            db.session.delete(found_data)
            db.session.commit()
            return get_respose("Category o'chirildi", None, 201)
        else:
            return get_respose("Category faqat admin o'chiradi", None, 404)
 
    @jwt_required()
    def get(self, category_id):
        """ Category Get API
        Path - /api/category/<category_id>
        Method - GET
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              reqiured: true
              description: Bearer token for authorization
            
            - name: category_id
              in: path
              type: integer
              required: true
              description: Enter Category ID
        responses:
            200:
                description: Return Access Token
        """
        found_data = Category.query.filter_by(id=category_id).first()
        return get_respose("topildi", found_data.to_dict(), 200)
    
    @jwt_required()
    def patch(self, category_id):
        """ Category Update API
        Path - /api/category/<category_id>
        Method - PATCH
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              reqiured: true
              description: Bearer token for authorization

            - name: category_id
              in: path
              type: integer
              required: true
              description: Enter Category ID

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
        responses:
            200:
                description: Return Access Token
        """
        found_data = Category.query.filter_by(id=category_id).first()
        if not found_data:
            return get_respose("topilmadi", None, 404)
        
        username = get_jwt_identity()
        found_user = User.query.filter_by(username=username).first()

        if found_user.role == 'admin':
            data = category_update_parser.parse_args()

            found_data.title = data['title']
            found_data.description = data['description']
            db.session.commit()
            return get_respose("Category o'zgartirildi", None, 201)
        else:
            return get_respose("faqat admin o'zgartiradi", None, 404)


api.add_resource(CategoryCreateResource, "/")
api.add_resource(CategoryDetailResource,"/<category_id>")
