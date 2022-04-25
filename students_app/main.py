from flask_migrate import Migrate
from flask import Flask, request
from flask_restx import Resource, Api, fields, reqparse

from marshmallow import Schema, fields

from enum import Enum

import os
import json
from dotenv import find_dotenv, load_dotenv

from .models import Student, db

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
            "id",
            type=str,
            help="student id should be provided",
            required=True,
            location="path",
        )
    return students_post_arg_parse


students_post_arg_parse = get_parser(True)
students_put_arg_parse = get_parser(False)


class Gender(Enum):
    male = "male"
    female = "female"

    def __str__(self) -> str:
        return self.value


# students_post_arg_parse.add_argument(
#     "gender",
#     type=Gender,
#     help="email should be string",
#     required=True,
#     location="json",
# )


class StudentSchema(Schema):
    firstName = fields.Str()
    lastName = fields.Str()


parser = reqparse.RequestParser()
parser.add_argument("var1", type=str, help="variable 1")
parser.add_argument("var2", type=str, help="variable 2")


@api.route("/hello/<string:id>")
class HelloWorldParameter(Resource):
    @api.doc(parser=parser)
    def get(self, id):
        parser = reqparse.RequestParser()
        print("aa")
        parser.add_argument("rate", type=int, help="Rate cannot be converted")
        parser.add_argument("name")
        args = parser.parse_args()
        print(args)


@api.route("/students")
class Students_endpoint(Resource):
    def get(self):
        print(os.environ.get("DATABASE_URI"))

        students_to_return = [x.get_json() for x in Student.query.all()]

        return students_to_return


@api.route("/student/<string:id>")
class Student_endpoint(Resource):
    def get(self, id):
        pass

    # @api.expect(student_model)
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

    @api.doc(parser=students_put_arg_parse)
    def patch(self):
        print("trying to parse")
        args = students_put_arg_parse.parse_args()
        print(args)
        student = Student.get_by_id(args.id)

        print(student)
        student_to_return = student.get_json()
        print(student_to_return)

        print("\n aa \n")
        # print(request.form[0])

        return student_to_return
