import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, DateTime, Text
from flask_appbuilder.models.mixins import BaseMixin, FileColumn, ImageColumn
from flask_appbuilder import Model
from sqlalchemy.ext.hybrid import hybrid_property
from app import db
from sqlalchemy.orm import relationship



mindate = datetime.date(datetime.MINYEAR, 1, 1)

# from flask_appbuilder.models.mixins import AuditMixin as _AuditMixin

from flask_softdeletes.model import SoftDeletedMixin


# class AuditMixin(SoftDeletedMixin,_AuditMixin):
#     pass
class StructuredScrapedData(Model):
    __tablename__ = 'structured_scraped_data'
     
    id = Column(Integer, primary_key=True)
    website_name = Column(String(255))
    website_url = Column(String(500))
    title = Column(String(500))
    description = Column(Text)
    date_posted = Column(DateTime)
    deadline = Column(DateTime)
    reference_number = Column(String(100))
    category = Column(String(100))
    location = Column(String(100))
    language = Column(String(50))
    contact = Column(String(200))
    budget = Column(String(100))
    type = Column(String(50))
    original_id = Column(String(50))
    created_at = Column(DateTime)
    
    # Make direct_url optional
    try:
        direct_url = Column(String(500))
    except Exception:
        pass
    
    @hybrid_property
    def status_label(self):
        return self.category.replace('_', ' ').title() if self.category else 'Unknown'
    
    @hybrid_property
    def tender_url(self):
        """Return most specific URL available"""
        if hasattr(self, 'direct_url') and self.direct_url:
            return self.direct_url
        return self.website_url or '#'
    
    @hybrid_property
    def display_title(self):
        if self.title:
            return self.title
        elif self.description:
            return (self.description[:97] + '...') if len(self.description) > 100 else self.description
        return 'No title available'
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
