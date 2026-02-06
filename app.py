from flask import Flask
from flasgger import Swagger
from flask_restful import Api
from resources.user_resources import user_bp
from resources.elon_resouces import elon_bp
from resources.category_resources import category_bp
from models import db, migrate, bcrypt, jwt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = "DJEVCEDJVDVNKBA"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1111@127.0.0.1:5432/olx"
app.config['WTF_CSRF_ENABLED'] = False
app.config['WTF_CSRF_SECRET_KEY'] = "jkdbvkjvebjseg"

Swagger(app, template={
    "info": {
        "title": "OLX",
        "description": "API documentation for OLX",
        "version": "1.0.0"
    }
})

limiter = Limiter(get_remote_address, app=app, default_limits=['20 per minute'])

db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(elon_bp)
app.register_blueprint(category_bp)

if __name__ == "__main__":
    app.run(port=2222, debug=True)