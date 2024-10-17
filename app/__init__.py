from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

from . import views



# import logging

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_appbuilder import AppBuilder
# """
#  Logging configuration
# """

# logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
# logging.getLogger().setLevel(logging.DEBUG)


# # Initialize Flask app
# app = Flask(__name__)
# # ... other configurations ...
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0987@localhost/RFPs'  # Update with your actual database URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress the deprecation warning

# # Initialize SQLAlchemy
# db = SQLAlchemy(app)

# # Initialize AppBuilder with the session
# appbuilder = AppBuilder(app, db.session)  # Ensure this line is present



# """
# from sqlalchemy.engine import Engine
# from sqlalchemy import event

# #Only include this for SQLLite constraints
# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     # Will force sqllite contraint foreign keys
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()
# """

# from . import views
