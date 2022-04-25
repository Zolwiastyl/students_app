# Students app

## Installing dependencies

This project uses [poetry](https://python-poetry.org/docs/cli/) for package management.

To install packages run:
`poetry install`

### installation troubleshooting

When you get error that you cannot compile `libpg-dev` [try this](https://stackoverflow.com/questions/71195823/poetry-python-how-to-install-psycopg2-with-postgres-running-from-docker)

## Running project

1. First in root directory of this project rename:
   `mv sample.env .env`
2. Then run:
   `docker-compopse up`
   To initialize postgres database.
3. Then:
   `FLASK_APP=students_app/main.py poetry run flask run`
   To run the server

## Using docs

Because it uses restX library you have swagger endpoint on `/`, use it wisely

## important

When you run patch on student you have to pass whole favorite subjects list.
Database state of favorite subjects will be updated to match data passed in `PATCH` request for updating student
