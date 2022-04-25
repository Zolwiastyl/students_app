from datetime import datetime
from typing import List
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

    def add_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
            return self
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            raise e

    def get_json(self):
        return {"id": str(self.id), "name": self.name}

    @classmethod
    def get_all(self):
        return self.query.all()

    @classmethod
    def get_multiple_by_ids(self, ids_list: List[str]):
        return self.query.filter(self.id.in_(ids_list)).all()
