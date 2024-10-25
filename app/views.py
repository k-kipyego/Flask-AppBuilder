from flask import render_template, redirect, url_for
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.charts.views import ChartView
from flask_appbuilder.models.group import aggregate_count
from . import appbuilder, db
from .models import structured_scraped_data

class ProcurementDashboard(BaseView):
    route_base = "/procurement"

    @expose('/')
    @has_access
    def list(self):
        data = db.session.query(structured_scraped_data).all()
        return self.render_template('procurement_dashboard.html', data=data)
    
    @expose('/update_status/<int:notice_id>/<string:new_status>', methods=['POST'])
    @has_access
    def update_status(self, notice_id, new_status):
        notice = db.session.query(structured_scraped_data).get(notice_id)
        if notice:
            notice.category = new_status
            db.session.commit()
        return redirect(url_for('ProcurementDashboard.list'))

class ProcurementChartView(ChartView):
    datamodel = SQLAInterface(structured_scraped_data)
    chart_title = "Procurement Notices by Category"
    label_columns = {'category': 'Category'}
    group_by_columns = ['category']

    definitions = [
        {
            "group": "category",
            "series": [(aggregate_count, "category")]
        }
    ]

appbuilder.add_view(ProcurementDashboard, "Dashboard", icon="fa-dashboard", category="Procurement")
appbuilder.add_view(ProcurementChartView, "Procurement Chart", icon="fa-bar-chart", category="Procurement")
