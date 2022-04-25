from datetime import datetime
from enum import Enum
from psycopg2 import IntegrityError

from students_app.models.student_subject_aggregate import StudentSubjectAggregate

from .subject import Subject
from .base import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import defer, relationship
from uuid import uuid4


# class Gender(Enum):
#     male = "MALE"
#     female = "FEMALE"


class Student(db.Model):
    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_spent_books = db.Column(db.Integer)

    # Relationships
    favorite_subjects = relationship(
        "StudentSubjectAggregate", back_populates="student", lazy="joined"
    )
    # meta
    __tablename__ = "student"

    def add_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
            return self
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            raise e

    @classmethod
    def get_students_list(self):
        return self.query.options(
            defer("favorite_subjects", "student.total_spent_books")
        ).all()

    def get_json(self):
        print("this is self \n")
        print(self)
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_date": str(self.created_date),
            "total_spend_books": self.total_spent_books,
            "favorite_subjects": [
                {"id": str(x.subject.id), "name": x.subject.name}
                for x in self.favorite_subjects
            ],
        }

    def get_list_json(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_date": str(self.created_date),
        }

    @classmethod
    def get_by_id(self, id):
        print("id to look by %s", id)
        return self.query.filter_by(id=id).first()

    def update(self, data_to_update):
        print("keys to update: ")
        if not data_to_update.first_name == None:
            self.first_name = data_to_update.first_name
        if not data_to_update.last_name == None:
            self.last_name = data_to_update.last_name
        if not data_to_update.email == None:
            self.email = data_to_update.email
        if not data_to_update.favorite_subjects == None:

            all_subjects = Subject.get_multiple_by_ids(data_to_update.favorite_subjects)
            print("subject found by ids:")
            print(all_subjects)
            for aggregate in all_subjects:
                print(aggregate)
                if not any(
                    x for x in self.favorite_subjects if aggregate.id == x.subject_id
                ):
                    print("subject is not yet in this list")
                    print(aggregate.id)
                    aggregate = StudentSubjectAggregate(
                        student_id=self.id, subject_id=aggregate.id
                    )
                    db.session.add(aggregate)
            print("favorite subjects")
            print(self.favorite_subjects)
            for aggregate in self.favorite_subjects:
                if not any(x for x in all_subjects if aggregate.subject_id == x.id):
                    print("subject should be removed:")
                    print(aggregate.subject.name)
                    StudentSubjectAggregate.query.filter_by(
                        student_id=self.id, subject_id=aggregate.subject_id
                    ).delete()
                    db.session.commit()
            print("here")
            print(self.favorite_subjects)

        if not data_to_update.total_spent_books == None:
            self.total_spent_books = data_to_update.total_spent_books

        db.session.add(self)
        try:
            db.session.commit()
            return self
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            raise e
