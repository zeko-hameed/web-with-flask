from app import db
from datetime import datetime


class listtable(db.Model):
    __tablename__ = 'dolist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    descrption = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

