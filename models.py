from db import Base
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Numeric, Text

class AuditMixin:
    created = Column(DateTime, default=datetime.utcnow)
    creator = Column(Integer)
    cahnged = Column(DateTime)
    changer = Column(Integer)
    isdeleted = Column(Boolean, default=False)

class User(Base, AuditMixin):
    __tablename__ = 'users'
    usersid = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    passwordhash = Column(Text, nullable=False)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)

class Category(Base, AuditMixin):
    __tablename__ = 'categories'
    categoriesid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.usersid'), nullable=False)
    categoryname = Column(String(100), nullable=False)
    icon = Column(String(100))

class Expense(Base, AuditMixin):
    __tablename__ = 'expensesid'
    expensesid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.usersid'), nullable=False)
    categoryid = Column(Integer, ForeignKey('categories.categoriesid'))
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
