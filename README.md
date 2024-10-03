# Library Assessment

## Usage
The project uses `pipenv` therefore, be sure that you have pipenv installed your system or you can install it by using the following command.
```shell
pip install pipenv
```
Clone the repository, and `cd` into the root folder of the repository.
Run the following command.
```
pipenv install
```
All packages necessary to run the project shall be installed. 
Now we also need to place a .env file in the project root folder. Structure of the file shall be as follows.
```
DEBUG=True

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=********
DB_NAME=library
```
The project assumes uses PostgreSQL as a database to store the data. 
<br>
In the next step you need to make migrations, migrate and then seed the database with some initial data. For this run the following commands.
```
pipenv shell
python manage.py makemigrations
python manage.py migrate
python manage.py seed
```
Now, we can run the server.
```
python manage.py runserver
```
*Note: This will currently execute the server in development mode*


