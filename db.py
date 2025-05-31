from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

# db = SQLAlchemy()
engine = create_engine("postgresql://dpg-d0otab6uk2gs7392ifa0-a.virginia-postgres.render.com:5432/qontadb")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()
Base = declarative_base()
bcrypt = Bcrypt()
