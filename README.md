# Library Assessment

## 1. Clone
The repository is dockerized, so you should first clone the repository and then `cd` into the project directory.

## 2. Project Structure
The Project directory looks something like this;

```
|-
|- library/         # Django Project Configs
|- library_api/     # Django App for REST APIs
|- manage.py        # For Executing Django Project
|- .env             # You need to place this file
|- Dockerfile
|- docker-compose.yml
|- Pipfile
|- Pipfile.lock
|- README.md
```
Sample `.env` file is as under
```
DEBUG=True

DB_HOST=db  # so that it uses docker service
DB_PORT=5432
DB_USER=postgres
DB_PASS=testUser123
DB_NAME=library
```

## 3. Pre-Requirement
Since the project uses **Docker** therefore, it is essential that your system has Docker installed and configured on it to proceed further.

## 4. Executing the Project
While in the project directory execute the following command from shell. 
```
docker-compose up --build -d
```
The server should be accessible at;
http://localhost:8000

## 5. Migrations and Seed (One Time Only)
Once, the docker containers are up, and if it is the first time the project has been executed them you need to perform some extra steps.
1. Make Migrations
```
docker-compose exec backend pipenv run python manage.py makemigrations
```
2. Migrate the Changes to Database
```
docker-compose exec backend pipenv run python manage.py migrate
```
3. Seed with dummy data
```
docker-compose exec backend pipenv run python manage.py seed
```
## 6. Resources & API Endpoints
Following resources and api endpoints are available to be consumed. 
1.  **Authors**
```
GET:    http:localhost:8000/api/authors/
POST:   http:localhost:8000/api/authors/
GET:    http:localhost:8000/api/authors/<id>/
PATCH:  http:localhost:8000/api/authors/<id>/
DELETE: http:localhost:8000/api/authors/<id>/
```

2.  **Books**
```
GET:    http:localhost:8000/api/books/
POST:   http:localhost:8000/api/books/
GET:    http:localhost:8000/api/books/<id>/
PATCH:  http:localhost:8000/api/books/<id>/
DELETE: http:localhost:8000/api/books/<id>/
```

3.  **Users**
All Endpoints are protected except for the `register` endpoint. `/favorites/add/` and `/favorites/remove/` also provide the user with a list of 5 recommended book titles whenever they are called. 
```
POST:   http:localhost:8000/api/users/register/
POST:   http:localhost:8000/api/users/login/
POST:   http:localhost:8000/api/users/token/refresh/
GET:    http:localhost:8000/api/users/favorites/
POST:   http:localhost:8000/api/users/favorites/add/<book_id>/
PATCH:  http:localhost:8000/api/users/favorites/remove/<book_id+>/
