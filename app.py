from flask import Flask, jsonify
from flask_swagger import swagger
from flask_restx import Api
from models import db
from config import Config
from api import ContactApi

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app)
    swag = swagger(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(Config.swaggerui_blueprint, url_prefix=Config.SWAGGER_URL)
    
    # Swagger documentation
    @app.route('/swagger')
    def get_swagger():
        swag['info']['version'] = '0.1'
        swag['info']['title'] = 'Contacts API'
        return jsonify(swag)

    api.add_resource(ContactApi, '/api/contacts')


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
