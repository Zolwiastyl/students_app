from .base import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class StudentSubjectAggregate(db.Model):
    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    student_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("student.id"), primary_key=True
    )

    subject_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("subject.id"), primary_key=True
    )

    # Relationships
    student = db.relationship(
        "Student", back_populates="favorite_subjects", lazy="joined"
    )
    subject = db.relationship("Subject", back_populates="students", lazy="joined")

    __tablename__ = "student_subject_aggregate"
