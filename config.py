class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///mydatabase.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  # Not for production, but okay for this app
