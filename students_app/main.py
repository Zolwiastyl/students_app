from flask import Flask, request
from flask_migrate import Migrate
from flask_restx import Resource, Api, fields, reqparse

from marshmallow import Schema, fields

import os
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
        "first_name": fields.String(attribute="firstName"),
        "address": fields.String,
    },
)

students_post_arg_parse = reqparse.RequestParser()
students_post_arg_parse.add_argument(
    "firstName",
    type=str,
    help="firstName should be string",
    required=True,
    # dest="file_name",
)
students_post_arg_parse.add_argument(
    "lastName",
    type=str,
    help="lastName should be string",
    required=True,
    # dest="last_name",
)


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
class Student_endpoint(Resource):
    def get(self):
        print(os.environ.get("DATABASE_URI"))

        print(Student.query.all())
        return {"dupa": 2137}

    def put(self):
        return "dupa"

    @api.expect(StudentSchema)
    def post(self):
        print("trying to parse")
        args = students_post_arg_parse.parse_args()
        print(args)

        print("\n aa \n")
        # print(request.form[0])

        return {"dupa": 2137}
