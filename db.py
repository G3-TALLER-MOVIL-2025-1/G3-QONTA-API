from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

# db = SQLAlchemy()
engine = create_engine("postgresql://postgres:admin@localhost:5432/qonta_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()
Base = declarative_base()
bcrypt = Bcrypt()
