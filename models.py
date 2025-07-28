from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# db를 함수로 받아서 사용
def init_models(db_instance):
    global db
    db = db_instance
    
    class User(UserMixin, db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        name = db.Column(db.String(100), nullable=False)
        phone = db.Column(db.String(20), nullable=False)
        employee_id = db.Column(db.String(20), nullable=False, unique=True)
        password_hash = db.Column(db.String(256), nullable=False)
        role = db.Column(db.String(20), nullable=False, default='input')  # input, download, admin
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        active_status = db.Column(db.Boolean, default=True)
        
        def __repr__(self):
            return f'<User {self.username}>'
        
        def has_permission(self, permission):
            """Check if user has specific permission"""
            permissions = {
                'input': ['input'],
                'download': ['input', 'download'],
                'admin': ['input', 'download', 'admin']
            }
            return permission in permissions.get(self.role, [])
    
    class Inspection(db.Model):
        __tablename__ = 'inspections'
        
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        equipment_type = db.Column(db.String(50), nullable=False)  # 보일러, 온수기
        equipment_id = db.Column(db.String(50), nullable=False)    # 장비 번호
        inspection_date = db.Column(db.DateTime, nullable=False)
        temperature = db.Column(db.Float)                          # 온도
        pressure = db.Column(db.Float)                            # 압력
        water_level = db.Column(db.Float)                         # 수위
        gas_consumption = db.Column(db.Float)                     # 가스 소비량
        efficiency = db.Column(db.Float)                          # 효율
        status = db.Column(db.String(20), default='normal')      # normal, warning, error
        notes = db.Column(db.Text)                               # 특이사항
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # 관계 설정
        user = db.relationship('User', backref='inspections')
        
        def __repr__(self):
            return f'<Inspection {self.equipment_id} by {self.user.name}>'
    
    return User, Inspection
