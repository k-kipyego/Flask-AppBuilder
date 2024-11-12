import logging
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_sqlalchemy import BaseQuery
from sqlalchemy.engine import Engine
from sqlalchemy import event
from .indexview import FABView
from flask_softdeletes.query import SoftDeletedQuery

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app, query_class=type('Query', (SoftDeletedQuery, BaseQuery), {}))
appbuilder = AppBuilder(app, db.session, indexview=FABView)

# Replace the SQLite-specific pragma with a database-agnostic version
@event.listens_for(Engine, "connect")
def set_foreign_keys(dbapi_connection, connection_record):
    # Check if it's SQLite
    if 'sqlite' in str(dbapi_connection.__class__.__module__).lower():
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    # For PostgreSQL, foreign keys are enabled by default
    # You can add specific PostgreSQL configurations here if needed

from app import views, data
from app import api

@app.before_first_request
def initDB():
    db.create_all()