from datetime import datetime, timezone
from app import db

class Employee(db.Model):
    """SQLAlchemy model for employee_details table."""
    __tablename__ = 'employee_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(20), nullable=False)
    occupation = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String(100), nullable=True)
    salary = db.Column(db.Numeric(12, 2), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    marital_status = db.Column(db.String(30), nullable=True)
    status = db.Column(db.String(20), nullable=True, default='active')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        """Convert model instance to a dictionary payload."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "occupation": self.occupation,
            "designation": self.designation,
            "salary": float(self.salary) if self.salary is not None else None,
            "city": self.city,
            "marital_status": self.marital_status,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
