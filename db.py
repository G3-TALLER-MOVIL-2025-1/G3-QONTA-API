from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

# db = SQLAlchemy()
engine = create_engine("postgresql://g3qontaadmin:1sg2eSWE7q5l7gZmWiCZTYX1Z0RWX1Kd@dpg-d0otab6uk2gs7392ifa0-a.virginia-postgres.render.com/qontadb")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()
Base = declarative_base()
bcrypt = Bcrypt()
