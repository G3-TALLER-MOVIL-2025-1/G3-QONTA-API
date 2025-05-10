from db import db
from datetime import datetime

class AuditMixin:
    CREATED = db.Column(db.DateTime, default=datetime.utcnow)
    CREATOR = db.Column(db.Integer)
    CAHNGED = db.Column(db.DateTime)
    CHANGER = db.Column(db.Integer)
    ISDELETED = db.Column(db.Boolean, default=False)

class User(db.Model, AuditMixin):
    __tablename__ = 'USERS'
    USERSID = db.Column(db.Integer, primary_key=True)
    EMAIL = db.Column(db.String(255), unique=True, nullable=False)
    PASSWORDHASH = db.Column(db.Text, nullable=False)
    NAME = db.Column(db.String(100), nullable=False)
    LASTNAME = db.Column(db.String(100), nullable=False)

class Category(db.Model, AuditMixin):
    __tablename__ = 'CATEGORIES'
    CATEGORIESID = db.Column(db.Integer, primary_key=True)
    USERID = db.Column(db.Integer, db.ForeignKey('USERS.USERSID'), nullable=False)
    CATEGORYNAME = db.Column(db.String(100), nullable=False)
    ICON = db.Column(db.String(100))

class Expense(db.Model, AuditMixin):
    __tablename__ = 'EXPENSESID'
    EXPENSESID = db.Column(db.Integer, primary_key=True)
    USERID = db.Column(db.Integer, db.ForeignKey('USERS.USERSID'), nullable=False)
    CATEGORYID = db.Column(db.Integer, db.ForeignKey('CATEGORIES.CATEGORIESID'))
    AMOUNT = db.Column(db.Numeric(10, 2), nullable=False)
    DESCRIPTION = db.Column(db.Text)
