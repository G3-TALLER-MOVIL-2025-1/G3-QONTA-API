from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

# db = SQLAlchemy()
engine = create_engine("postgresql://qonta_prod_bd_user:uN1n2qzNvIEFqlQCZYxOEESBXoaE35Qi@dpg-d1fvevnfte5s7381gqug-a.virginia-postgres.render.com/qonta_prod_bd")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()
Base = declarative_base()
bcrypt = Bcrypt()
