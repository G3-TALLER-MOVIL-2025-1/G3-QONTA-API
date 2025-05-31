import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://qonta_user:kmobuqJMYLAVZIG1257DFRIyZmodXbSY@dpg-d0oulhmmcj7s73djs5m0-a.oregon-postgres.render.com/qonta")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
