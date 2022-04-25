from typing import List
from flask_migrate import Migrate
from flask import Flask, request
from flask_restx import Resource, Api, fields, reqparse

from marshmallow import Schema, fields

from enum import Enum

import os
import json
from dotenv import find_dotenv, load_dotenv

from .models import Student, db, StudentSubjectAggregate, Subject
from .models import *

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["RESTX_VALIDATE"] = True

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
with app.app_context():
    db.create_all()

student_model = api.model(
    "Student",
    {
        "first_name": fields.String,
        "last_name": fields.String,
    },
)


def get_parser(is_post: bool):

    students_post_arg_parse = reqparse.RequestParser()
    students_post_arg_parse.add_argument(
        "firstName",
        type=str,
        help="firstName should be string",
        required=is_post,
        dest="first_name",
        location="json",
    )
    students_post_arg_parse.add_argument(
        "lastName",
        type=str,
        help="lastName should be string",
        required=is_post,
        dest="last_name",
        location="json",
    )
    students_post_arg_parse.add_argument(
        "email",
        type=str,
        help="email should be string",
        required=is_post,
        location="json",
    )
    if not is_post:
        students_post_arg_parse.add_argument(
            "total_spent_books",
            type=int,
            help="total spent books should be int",
            required=False,
            location="json",
        )
        students_post_arg_parse.add_argument(
            "favorite_subjects",
            type=list,
            help="favorite_subject should be list of strings",
            required=False,
            location="json",
        )

    return students_post_arg_parse


students_post_arg_parse = get_parser(True)
students_patch_arg_parse = get_parser(False)


class Gender(Enum):
    male = "male"
    female = "female"

    def __str__(self) -> str:
        return self.value


@api.route("/student")
class Students_endpoint(Resource):
    def get(self):
        return [x.get_list_json() for x in Student.get_students_list()]

    @api.doc(parser=students_post_arg_parse)
    def post(self):
        print("trying to parse")
        args = students_post_arg_parse.parse_args()
        student = Student(**args)
        student_added = student.add_to_db()
        print(student_added)
        student_to_return = student_added.get_json()
        print(student_to_return)

        print("\n aa \n")
        # print(request.form[0])

        return student_to_return


@api.route("/student/<string:id>")
class Student_endpoint(Resource):
    def get(self, id):
        return Student.get_by_id(id).get_json()
        pass

    # @api.expect(student_model)

    @api.doc(parser=students_patch_arg_parse)
    def patch(self, id):
        print("trying to parse")
        args = students_patch_arg_parse.parse_args()
        print(args)
        student = Student.get_by_id(id)
        student.update(args).get_json()
        print(student)
        student_to_return = student.get_json()
        print(student_to_return)

        print("\n aa \n")
        # print(request.form[0])

        return student_to_return


subject_post_arg_parse = reqparse.RequestParser()
subject_post_arg_parse.add_argument(
    "name", type=str, help="name for subject", location="json"
)


@api.route("/subject")
class Subject_endpoint(Resource):
    def get(self):
        return [x.get_json() for x in Subject.get_all()]

    @api.doc(parser=subject_post_arg_parse)
    def post(self):
        args = subject_post_arg_parse.parse_args()
        subject = Subject(**args)
        subject_added = subject.add_to_db()
        return subject_added.get_json()
