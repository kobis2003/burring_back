# The blurring project

## Make the backend work
This part describe how to run the project

### Install the python library
You first need to install python3.10.

When done, run: `install pip3 .[test]` on a terminal in the project directory
It should install every library that are in the pyproject file.

### Create the SQL lite DB
In order to be able to use a progress bar, we need a DB. I chose sqlite DB
(so that it is easy to install for a demo).
run `python3 ./db/init_db.py` on a terminal in the project directory or use directly the run.sh 
of this project that will do it for you.
A file named blurring.db should have appeared in your project directory (that's the database).

### Run the tests
Now that the DB exists, you can run the command `pytest` to run the tests of the project.

### Run the python server
use the run.sh script of this project. The backend server should be up!
You can testing using postman importing the "owkin_technical_test.postman_collection.json" file






## DB part
### Initiate the project


### Remarks
In order to be able to use a progress bar, we need a DB. I chose sqlite DB 
(so that it is easy to install for a demo). On a go to prod project, I would have use a postgre sql DB and
add a docker-compose file for the local development 


### TODO
-> Batch instead of process for thread safe
-> Clean Swagger
-> Clean JSON validation (with nice to read exception that makes it possible for the user to correct)
-> Correct the strange SQLAlchemy refresh needed so that it really reads from the DB
-> The result is returned in String (it should be an entity)
-> The SQL Alchemy choice clearly deserved a discussion between dev before being done 
(like will there be just one table)
-> Only PNG file (no other file type)
-> do a correct logging mechanism
-> no time for perfect tox
