from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, Date, Enum
from sqlalchemy.ext.hybrid import hybrid_property

class ProcurementNotice(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    estimated_value = Column(Float)
    submission_date = Column(Date)
    status = Column(Enum('approved', 'rejected', 'under_evaluation'), default='under_evaluation')
    evaluation_score = Column(Float)
    label_columns = ['Column1', 'Column2']  # Define the label_columns attribute


    @hybrid_property
    def status_label(self):
        return self.status.replace('_', ' ').title()



# from sqlalchemy import Column, String, Integer, Date
# from flask_appbuilder import Model

# class ProcurementNotice(Model):
#     id = Column(Integer, primary_key=True)
#     title = Column(String(100), nullable=False)
#     category = Column(String(50), nullable=False)
#     decision = Column(String(50), nullable=True)
#     date = Column(Date, nullable=False)

