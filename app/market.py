from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # Create an instance of Flask class | __name__ is a special variable in Python that represents the name of the current module.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app) # Create an instance of SQLAlchemy class and bind it to the Flask app instance.


# SQLlite database will be created in the root directory of the project.
# The database file will be named market.db | Why? Because of the three slashes in the URI.
# The three slashes indicate a relative path.
# Four slashes would indicate an absolute path.
# For example: 'sqlite:////C:/path/to/database/market.db'

# The item table will be created in the market.db file. | The table will be created when the first query is made to the database.
# The table will have the following columns: id, name, price, barcode, description.
class Item(db.Model): # Inherit from db.Model
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(30), nullable=False, unique=True)#30 characters max, cannot be null, must be unique
    price = db.Column(db.Integer(), nullable=False) # Creating price column through the instance of db.Integer
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)

    def __repr__(self): # String representation of the object(for debugging & user-friendly printing.)
        return f'Item {self.name}'




# self refers to the instance of the class | current instance of the class.

# class User(db.Model): # Inherit from db.Model
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), nullable=False, unique=True)
#     email_address = db.Column(db.String(50), nullable=False, unique=True)
#     password_hash = db.Column(db.String(60), nullable=False)
#     budget = db.Column(db.Integer(), nullable=False, default=1000) # Default budget is 1000
#     items = db.relationship('Item', backref='owned_user', lazy=True) # One to many relationship

#     def __repr__(self): # String representation of the object(for debugging)
#         return f'User {self.username}'





with app.app_context():
    sword = Item.query.all()
    # Route decorator to define the route for the home page.
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('home.html')


    # items is the label to send data to html file.
    @app.route('/market')
    def market_page():
        # It's the same process, just modify the list on the funtion paramater section, or inside the function
        

        return render_template('market.html', items=sword)
            # items=sword is the data sent to html file.


# What is app.run()?# app.run() is a method of the Flask class that runs the application on a local development server.
# The host parameter specifies the hostname to listen on. '0.0.0.0' means that the server will be accessible from any IP address.
# The port parameter specifies the port number to listen on. 5000 is the default port for Flask.
# The debug parameter is set to True to enable debug mode.
# What is __name__ == '__main__'?# This condition is true if the script is run directly from the command line, and false if it is imported as a module.
if __name__ == '__main__':
    # local development server.
    app.run(host="0.0.0.0", port=5000, debug=True)


