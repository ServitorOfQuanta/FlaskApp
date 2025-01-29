from flask_swagger_ui import get_swaggerui_blueprint

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True # Not for production, but okay for this app
    # Swagger UI route
    SWAGGER_URL = '/swagger-ui'
    API_URL = '/swagger'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'My API'
        }
    )
