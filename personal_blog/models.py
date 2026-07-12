from datetime import datetime
from personal_blog import db


class Part(db.Model):
    __tablename__ = 'part'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    
    # علاقة اختيارية لتسهيل جلب المقالات التابعة لهذا القسم
    blogs = db.relationship('Blog', backref='part', lazy=True)


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    discription = db.Column(db.Text, nullable=True) # تم تعديله إلى Text ليتسع للوصف
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # وقت الإنشاء تلقائيًا
    
    # هنا نربط العمود بـ id الجدول الأول كمفتاح أجنبي
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
     
