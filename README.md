# fit_app
## Description
This is a learning project, made using Flask. It's a simple RESTful fitness web application to track consumed calories and exercises with the following API endpoints:

|path|methods|description|
|----|-------|-----------|
|/users/|GET, POST| get list of all users; create a new user|
|/user/user_id| GET, PATCH, DELETE| get a user's info by id; update user's info; delete a user by id|
|/users/user_id/food_records/date|GET | get all the food records for the user on the specific date|
|/users/user_id/food_tracker| POST| add a food record for the user |
|/users/user_id/exercises_records/date| GET| get all the exercises records for the user on the specific date|
|/user/exercises_tracker | POST | add an exercise record for the user|
|/food/|GET, POST|get a list of all the food products; add a new food product|
|/food/food_id|GET, PATCH, DELETE|get info of a food product by id; update the info; remove a food product by id|
|/exercises/|GET, POST| get a list of all exercises; add a new exercise|
|/exercises/exercise_id|GET, PATCH, DELETE|get exercise info by id; update exercise info; delete exercise info by id|