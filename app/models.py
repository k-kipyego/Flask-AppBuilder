from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, Date, Enum, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from app import db

class structured_scraped_data(Model):
    __tablename__ = 'structured_scraped_data'
     
    id = db.Column(db.Integer, primary_key=True)
    website_name = db.Column(db.String(255))
    website_url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)
    deadline = db.Column(db.DateTime)
    reference_number = db.Column(db.String(50))
    category = db.Column(db.String(100))
    location = db.Column(db.String(100))
    language = db.Column(db.String(50))
    contact = db.Column(db.String(100))
    budget = db.Column(db.String(100))
    type = db.Column(db.String(50))
    original_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)

    @hybrid_property
    def status_label(self):
        return self.category.replace('_', ' ').title()
