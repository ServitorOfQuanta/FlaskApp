from flask import Flask, jsonify
from flask_swagger import swagger
from flask_restful import Api
from models import db
from config import Config
from api import ContactApi

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
swag = swagger(app)
db.init_app(app)
with app.app_context():
    db.create_all()

# Swagger documentation
@app.route('/swagger')
def get_swagger():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "My API"
    return jsonify(swag)

api.add_resource(ContactApi, '/contact')

app.register_blueprint(Config.swaggerui_blueprint, url_prefix=Config.SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
