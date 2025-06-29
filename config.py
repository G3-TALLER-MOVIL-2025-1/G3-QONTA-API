import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://qonta_prod_bd_user:uN1n2qzNvIEFqlQCZYxOEESBXoaE35Qi@dpg-d1fvevnfte5s7381gqug-a.virginia-postgres.render.com/qonta_prod_bd")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
