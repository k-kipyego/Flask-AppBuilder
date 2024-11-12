import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import BaseMixin, FileColumn, ImageColumn
from flask_appbuilder import Model
from sqlalchemy.ext.hybrid import hybrid_property
from app import db


mindate = datetime.date(datetime.MINYEAR, 1, 1)

# from flask_appbuilder.models.mixins import AuditMixin as _AuditMixin

from flask_softdeletes.model import SoftDeletedMixin


# class AuditMixin(SoftDeletedMixin,_AuditMixin):
#     pass
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

# New model for World Bank data
class WorldBankDataModel(Model):
    __tablename__ = 'world_bank'
    
    id = db.Column(db.Integer, primary_key=True)
    docty = db.Column(db.String(100))  # Document Type
    docdt = db.Column(db.DateTime)      # Document Date
    display_title = db.Column(db.String(255))  # Display Title
    pdfurl = db.Column(db.String(255))  # PDF URL
class ContactGroup(SoftDeletedMixin,Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(SoftDeletedMixin,Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(SoftDeletedMixin,Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey('gender.id'), nullable=False)
    gender = relationship("Gender")

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)

#----------------------------------------------------------
#  Chart Views Example
#----------------------------------------------------------


class Country(SoftDeletedMixin,Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class CountryStats(SoftDeletedMixin,Model):
    id = Column(Integer, primary_key=True)
    stat_date = Column(Date, nullable=True)
    population = Column(Float)
    unemployed = Column(Float)
    college = Column(Float)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    country = relationship("Country")

    def __repr__(self):
        return "{0}:{1}:{2}:{3}".format(self.stat_date, self.country, self.population, self.college)

    def month_year(self):
        return datetime.datetime(self.stat_date.year, self.stat_date.month, 1)

    def year(self):
        return datetime.datetime(self.stat_date.year,1, 1)
