from flask import render_template, request, redirect, url_for
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.charts.views import ChartView
from flask_appbuilder.models.group import aggregate_count
from . import appbuilder, db
from .models import ProcurementNotice

class ProcurementDashboard(BaseView):
    route_base = "/procurement"

    @expose('/')
    @has_access
    def list(self):
        notices = db.session.query(ProcurementNotice).all()
        return self.render_template('procurement_dashboard.html', notices=notices)

    @expose('/update_status/<int:notice_id>/<string:new_status>', methods=['POST'])
    @has_access
    def update_status(self, notice_id, new_status):
        notice = db.session.query(ProcurementNotice).get(notice_id)
        if notice:
            notice.status = new_status
            db.session.commit()
        return redirect(url_for('ProcurementDashboard.list'))

class ProcurementChartView(ChartView):
    datamodel = SQLAInterface(ProcurementNotice)
    chart_title = "Procurement Notices by Status"
    label_columns = {'status': 'Status'}  # This must be a dictionary
    group_by_columns = ['status']  # Ensure 'status' is a valid column in your model

    definitions = [
        {
            "group": "status",
            "series": [(aggregate_count, "status")]
        }
    ]


appbuilder.add_view(ProcurementDashboard, "Dashboard", icon="fa-dashboard", category="Procurement")
appbuilder.add_view(ProcurementChartView, "Procurement Chart", icon="fa-bar-chart", category="Procurement")


# from flask_appbuilder.charts.views import GroupByChartView
# from flask_appbuilder.models.group import aggregate_count, aggregate_sum
# from flask_appbuilder.models.sqla.interface import SQLAInterface
# from .models import ProcurementNotice
# from flask_appbuilder import AppBuilder

# class ProcurementNoticeChartView(GroupByChartView):
#     datamodel = SQLAInterface(ProcurementNotice)
#     chart_title = 'Procurement Notices by Category'

#     # Group by 'category' and aggregate the number of notices in each category
#     group_by_columns = ['category']
#     aggregates = [aggregate_count]

# appbuilder = AppBuilder()

# appbuilder.add_view(ProcurementNoticeChartView, "Notices by Category", icon="fa-bar-chart", category="Dashboard")
