import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://g3qontaadmin:1sg2eSWE7q5l7gZmWiCZTYX1Z0RWX1Kd@dpg-d0otab6uk2gs7392ifa0-a.virginia-postgres.render.com/qontadb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
