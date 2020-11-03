from app import db
from datetime import datetime


class QueryLog(db.Model):
    """保存查询记录"""

    __tablename__ = "count_cet_queries"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zkzh = db.Column(db.String(16), nullable=False)  # 准考证号
    xm = db.Column(db.String(16))
    means = db.Column(db.Boolean, default=False)  # True为使用查询准考证，False为直接填写查询
    ip = db.Column(db.String(16), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())
