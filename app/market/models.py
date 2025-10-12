# app/market/models.py
from . import db # Import the db instance from the current package(Object = db = SQLAlchemy()) 
# What the . mean
# The dot (.) in the import statement from . import db is a relative import in Python. It indicates that the db module is being imported from the current package or directory where the models.py file resides. In this case, it means that db is being imported from the same package as models.py, which is app/market.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False)    


    def __repr__(self):
        return f'Item {self.name}'