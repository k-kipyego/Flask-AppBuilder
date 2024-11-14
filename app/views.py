import calendar
from typing import List
from flask import render_template, redirect,request
from flask.helpers import flash
from flask_appbuilder.models.sqla.interface import SQLAInterface as _SQLAInterface,log
from flask_appbuilder.widgets import ListThumbnail, ListWidget, \
    ListItem, ListBlock, ShowBlockWidget, ListLinkWidget
from flask_appbuilder.actions import action
from flask_appbuilder.models.group import aggregate_count, aggregate_avg, aggregate_sum
from flask_appbuilder.views import MasterDetailView, ModelView as _ModelView
from flask_appbuilder.baseviews import expose, BaseView
from flask_appbuilder.charts.views import DirectByChartView, GroupByChartView
from flask_babel import lazy_gettext as _
from werkzeug.exceptions import abort
from .models import StructuredScrapedData, WorldBankDataModel
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.charts.views import ChartView
from datetime import datetime, timedelta

import sys

from . import db, appbuilder
# from .models import ContactGroup, Gender, Contact, CountryStats, Country
import time,re
from flask_appbuilder import Model
from flask_appbuilder._compat import as_unicode
from sqlalchemy import distinct
from flask_appbuilder import ModelView


from sqlalchemy.exc import IntegrityError
from flask_appbuilder.const import LOGMSG_ERR_DBI_DEL_GENERIC, LOGMSG_WAR_DBI_DEL_INTEGRITY

class SQLAInterface(_SQLAInterface):
    def before_delete(self, items: List[Model]) -> bool:
        try:
            for item in items:
                # self._delete_files(item)
                # self.session.delete(item)
                item.deleted_time = time.time()
            self.session.commit()
            self.message = (as_unicode(self.delete_row_message), "success")
            return True
        except IntegrityError as e:
            self.message = (as_unicode(self.delete_integrity_error_message), "warning")
            log.warning(LOGMSG_WAR_DBI_DEL_INTEGRITY.format(str(e)))
            self.session.rollback()
            return False
        except Exception as e:
            self.message = (
                as_unicode(self.general_error_message + " " + str(sys.exc_info()[0])),
                "danger",
            )
            log.exception(LOGMSG_ERR_DBI_DEL_GENERIC.format(str(e)))
            self.session.rollback()
            return False    
    def delete_all(self, items: List[Model]) -> bool:
        try:
            for item in items:
                # self._delete_files(item)
                # self.session.delete(item)
                item.deleted_time = time.time()
            self.session.commit()
            self.message = (as_unicode(self.delete_row_message), "success")
            return True
        except IntegrityError as e:
            self.message = (as_unicode(self.delete_integrity_error_message), "warning")
            log.warning(LOGMSG_WAR_DBI_DEL_INTEGRITY.format(str(e)))
            self.session.rollback()
            return False
        except Exception as e:
            self.message = (
                as_unicode(self.general_error_message + " " + str(sys.exc_info()[0])),
                "danger",
            )
            log.exception(LOGMSG_ERR_DBI_DEL_GENERIC.format(str(e)))
            self.session.rollback()
            return False
    def delete(self, item: Model, raise_exception: bool = False) -> bool:
        try:
            # self._delete_files(item)
            # self.session.delete(item)
            item.deleted_time = time.time()
            self.session.commit()
            self.message = (as_unicode(self.delete_row_message), "success")
            return True
        except IntegrityError as e:
            self.message = (as_unicode(self.delete_integrity_error_message), "warning")
            log.warning(LOGMSG_WAR_DBI_DEL_INTEGRITY.format(str(e)))
            self.session.rollback()
            if raise_exception:
                raise e
            return False
        except Exception as e:
            self.message = (
                as_unicode(self.general_error_message + " " + str(sys.exc_info()[0])),
                "danger",
            )
            log.exception(LOGMSG_ERR_DBI_DEL_GENERIC.format(str(e)))
            self.session.rollback()
            if raise_exception:
                raise e
            return False


class ProcurementDashboard(BaseView):
    route_base = "/home"

    @expose('/')
    @has_access
    def list(self):
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 30))

        # Get the most recent created_at timestamp
        latest_timestamp = db.session.query(
            db.func.max(StructuredScrapedData.created_at)
        ).scalar()

        # Get all distinct created_at timestamps, ordered by timestamp
        timestamps = db.session.query(
            distinct(StructuredScrapedData.created_at)
        ).order_by(
            StructuredScrapedData.created_at.desc()
        ).all()

        # Get paginated data ordered by created_at desc
        query = db.session.query(StructuredScrapedData)
        
        # Order by created_at timestamp in descending order (newest first)
        query = query.order_by(StructuredScrapedData.created_at.desc())
        
        data = query.paginate(page=page, per_page=per_page, error_out=False)

        # Process items and mark new ones
        new_count = 0
        for item in data.items:
            # Mark items from the latest batch as new
            item.is_new = (item.created_at == latest_timestamp)
            if item.is_new:
                new_count += 1
            
            # Add time ago information
            if item.created_at:
                delta = datetime.now() - item.created_at
                if delta.days == 0:
                    if delta.seconds < 3600:
                        item.time_ago = f"{delta.seconds // 60} minutes ago"
                    else:
                        item.time_ago = f"{delta.seconds // 3600} hours ago"
                elif delta.days == 1:
                    item.time_ago = "Yesterday"
                else:
                    item.time_ago = f"{delta.days} days ago"
            else:
                item.time_ago = "Unknown"

        # Calculate pagination values
        min_pages = min(10, data.pages)
        max_pages = data.pages
        last_pages_start = max(11, max_pages - 2) if max_pages > 10 else None

        # Get total counts
        total_count = query.count()
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        today_count = query.filter(
            StructuredScrapedData.created_at >= today_start
        ).count()

        yesterday_start = today_start - timedelta(days=1)
        yesterday_count = query.filter(
            StructuredScrapedData.created_at.between(yesterday_start, today_start)
        ).count()

        return self.render_template(
            'procurement_dashboard.html',
            data=data,
            new_count=new_count,
            total_count=total_count,
            today_count=today_count,
            yesterday_count=yesterday_count,
            latest_timestamp=latest_timestamp,
            min_pages=min_pages,
            max_pages=max_pages,
            last_pages_start=last_pages_start,
            now=datetime.now()
        )

    def get_time_ago(self, timestamp):
        """Convert timestamp to 'time ago' format"""
        if not timestamp:
            return "Unknown"

        now = datetime.now()
        diff = now - timestamp

        if diff.days == 0:
            if diff.seconds < 60:
                return "Just now"
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        if diff.days == 1:
            return "Yesterday"
        if diff.days < 7:
            return f"{diff.days} days ago"
        if diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        if diff.days < 365:
            months = diff.days // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        years = diff.days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"
    
class WorldBankDashboard(BaseView):
    route_base = "/world_bank"

    @expose('/')
    @has_access
    def list(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 30))

        # Get all data
        query = db.session.query(WorldBankDataModel)
        
        # Calculate statistics
        total_count = query.count()
        
        # Calculate documents this month
        thirty_days_ago = datetime.now() - timedelta(days=30)
        month_count = query.filter(WorldBankDataModel.docdt >= thirty_days_ago).count()
        
        # Calculate recent documents (last 24 hours)
        one_day_ago = datetime.now() - timedelta(days=1)
        recent_count = query.filter(WorldBankDataModel.docdt >= one_day_ago).count()

        # Get paginated data
        world_bank_data = query.order_by(WorldBankDataModel.docdt.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        # Calculate pagination
        min_pages = min(10, world_bank_data.pages)
        max_pages = world_bank_data.pages
        last_pages_start = max(11, max_pages - 2) if max_pages > 10 else None

        return self.render_template(
            'world_bank_dashboard.html',
            world_bank_data=world_bank_data,
            total_count=total_count,
            month_count=month_count,
            recent_count=recent_count,
            min_pages=min_pages,
            max_pages=max_pages,
            last_pages_start=last_pages_start
        )

class ProcurementModelView(ModelView):
    datamodel = SQLAInterface(StructuredScrapedData)
    
    # Define which columns to show in the list view
    list_columns = ['title', 'reference_number', 'category', 'deadline', 'tender_link']
    
    # Define search columns
    search_columns = ['title', 'description', 'reference_number', 'category']
    
    # Define which columns to show in the show view
    show_columns = ['title', 'description', 'date_posted', 'deadline', 
                   'reference_number', 'category', 'location', 'language',
                   'contact', 'budget', 'type', 'website_name', 'tender_link']
    
    # Format the tender_link column as a clickable URL
    @property
    def show_template(self):
        return "appbuilder/general/model/show_cascade.html"
    
    def pre_update(self, item):
        """Ensure the tender_link is properly set before update"""
        if not item.direct_url and item.website_url:
            item.direct_url = item.website_url
    
    def pre_add(self, item):
        """Ensure the tender_link is properly set before adding"""
        if not item.direct_url and item.website_url:
            item.direct_url = item.website_url

# Add the new ModelView to FAB
appbuilder.add_view(
    ProcurementModelView, 
    "Procurement Notices", 
    icon="fa-file-text-o", 
    category="Procurement"
)

class ProcurementChartView(ChartView):
    datamodel = SQLAInterface(StructuredScrapedData)
    chart_title = "Procurement Notices by Category"
    label_columns = {'category': 'Category'}
    group_by_columns = ['category']

    definitions = [
        {
            "group": "category",
            "series": [(aggregate_count, "category")]
        }
    ]

# appbuilder.add_view(ProcurementDashboard, "Dashboard", icon="fa-dashboard", category="Procurement")
appbuilder.add_view(ProcurementChartView, "Procurement Chart", icon="fa-bar-chart", category="Procurement")
appbuilder.add_view(WorldBankDashboard, "World Bank Opportunities", icon="fa-globe", category="World Bank")  

# adjust security menu to the last.
from flask_appbuilder.menu import Menu


def adjust_menu(self):
    old_menu = self.menu
    new_menu = old_menu[1:]
    new_menu.append(old_menu[0])
    self.menu = new_menu


Menu.adjust_menu = adjust_menu
appbuilder.menu.adjust_menu()

# add active status of menu items.
from flask_appbuilder.menu import MenuItem
def is_active(self):
    
    if self.childs:
        for c in self.childs:
            if c.is_active():
                return True
    else:        
        if request.path == self.get_url():
            return True
        else :
            if self.baseview :
                if request.blueprint == self.baseview.blueprint.name:
                    return True

    return False


MenuItem.is_active = is_active    