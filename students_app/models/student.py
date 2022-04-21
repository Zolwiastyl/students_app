from .base import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Student(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    favorite_subject = db.Column(db.String)
    total_spent_books = db.Column(db.Integer)
