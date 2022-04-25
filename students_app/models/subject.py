from datetime import datetime
from psycopg2 import IntegrityError
from .base import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4


class Subject(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String, unique=True)

    # Relationships
    students = relationship(
        "StudentSubjectAggregate", back_populates="subject", lazy="joined"
    )
    # meta
    __tablename__ = "subject"
