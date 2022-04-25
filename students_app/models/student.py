from psycopg2 import IntegrityError
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
        print("this is self \n")
        print(self)
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }

    @classmethod
    def get_by_id(self, id):
        print("id to look by %s", id)
        return self.query.filter_by(id=id).first()
