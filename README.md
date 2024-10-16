# fit_app
## Description
This is a learning project, made with Flask, SQLAlchemy, Alembic, and Postgresql. It's a simple RESTful fitness web application with endpoints for managing user data, food nutrients, exercises, and tracking daily activities and calorie intake.

API endpoints:

|path|methods|description|
|----|-------|-----------|
|/users/login|POST| get an authentication token|
|/users|GET, POST| get list of all users; create a new user|
|/users/:user_id| GET, PATCH, DELETE| get a user's info by id; update user's info; delete a user by id|
|/users/:user_id/food_records/:date|GET | get all the food records for the user on the specific date|
|/users/:user_id/food_tracker| POST| add a food record for the user |
|/users/:user_id/exercises_records/:date| GET| get all the exercises records for the user on the specific date|
|/users/:user_id/exercises_tracker | POST | add an exercise record for the user|
|/food|GET, POST|get a list of all the food products; add a new food product|
|/food/:food_id|GET, PATCH, DELETE|get info of a food product by id; update the info; remove a food product by id|
|/exercises|GET, POST| get a list of all exercises; add a new exercise|
|/exercises/:exercise_id|GET, PATCH, DELETE|get exercise info by id; update exercise info; delete exercise info by id|

## Technologies
alembic  1.6.5  
Flask  2.2.2  
SQLAlchemy  1.4  
psycopg2-binary  2.9.5  
pyJWT

## Launch
The project requires running Postgres on port 5432. 
To launch it locally implement the following steps:
- Clone the repository
```
$ git clone https://github.com/nvp85/fit_app.git
```
- Create a database
```
$ psql -c 'CREATE DATABASE fit_app;'
```

- Create and activate a virtual environment, install requirements.txt
```
$ python -m venv venv
$ . Scripts/activate (for Windows)
$ python -m pip install --upgrade pip
$ pip install requirements.txt
```
- Migrate. To handle migrations the project uses Flask-Migrate and Alembic. To apply migrations from the my_app folder run : 
```
$ flask db upgrade
```

- Start the flask web server with debug mode on:
```
$export FLASK_DEBUG=1
$ flask run
```
# Examples

