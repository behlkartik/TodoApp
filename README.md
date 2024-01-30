# TodoApp
FastAPI app with JWT Authentication, API Docs, DB Migrations, Jinja Templating (Pending)

Requirements:
`python` - ^3.10. Can be installed using pyenv.
`pyenv`  - We are using this to install python 3.11.7. This can be useful to manage different python versions per different services
`poetry` - version 1.2.2

Local testing:
`cd ./TodoApp`
`poetry shell`
`poetry install`
`uvicorn main:app --reload` - runs the app with live reload

Database Migrations/Revisions (TodoApp/db_migrations/versions):
1. With MySQL connection string in TodoApp/database.py
    > Run mysql docker container: `docker run --rm --name todo-mysql-db -d -p 13306:3306 -v $HOME/TodoApp/mysqlconf/conf.d:/etc/mysql/conf.d -v $HOME/TodoApp/mysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root mysql/mysql-server`
2. With PostgresSQL connection string in TodoApp/database.py
   > Run postgres docker container: `docker run --rm --name todo-postgres-db -p 5433:5432 -v /Users/kart1813/personal/fastApiTest/TodoApp/pgdata/:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -d postgres`
3. With SQLlite connection string in TodoApp/database.py
   > No need of docker container as sqllite runs in ram

Upgrading database:
`cd ./TodoApp`
`alembic revision -m "<what change is made>"`
`alembic upgrade <revision>`

Downgrading database:
`cd ./TodoApp`
`alembic downgrade -1` or `alembic downgrade <revison>`

Access OpenAPI docs:
http://localhost:8000/docs