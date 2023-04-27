# The blurring project

## Make the backend work

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
You can test using postman importing the "owkin_technical_test.postman_collection.json" file or running the
frontend part. You can use the input-lenna-bee-voiture.json file for input 
(that will also give you an idea of what the file looks like)

## The input file 
You can use the input-lenna-bee-voiture.json as an example 
(it is quite big so that we have time to see the loading bar). It is made of a list of image containing 
for each a name and the data that are associated and a list of filter.

The filter is made of name and params. The python pillow library has been used in this project. The name 
should be one (any)  of the class that is contained in the ImageFilter file of the library. 
The params associated should be either null (if the class doesn't need any attribute to be initiated) 
or should correspond to the class creation attribute (with the same name and type).

## Some remarks on the project

### Image storing
As it was ask (or at least that is what I understood) to put the image in the JSON (I didn't know that it was possible to do it), I have put every image in text format 
and return huge JSON file. If it had'nt been asked to do so, I would have separate the images from the rest (as the 
JSON with this kind of size are killing my computer very often when manipulating theim) by using S3 or a dedicated DB 
for example.

### DB 
The chosen DB is SQL lite but on PROD, postgreSQL would be my choice. 
I have made just one table for being faster but I would probably separate the json part from the run.
Whether by making two different table or by putting the JSON on S3. The idea behind it is that there won't be 
other performance problem than the JSON files so that if we need to change, it won't be mandatory to change everything.

I have also used SQL Alchemy because I thought (I never used it before) that it was cool to use entity mapping
(it's like hibernate).
In the end the use of SQL Alchemy in addition of Process is really painful as the entity don't automatically update when 
concurrent processes change the DB. I have manage to deal with it but I would be worried about the kind of hack I used
 if it was production code (If there will always be one and only one table, I would probably remove SQL Alchemy)

### Process 
As there was a loading bar asked, I needed to launch concurrent process. I used the Process option of python 
(after trying async and threaded function...). I have made a piece of code before to make sure that no more 
than 5 project are running at the same time (otherwise, it wait for one to finish). It's some kind of security if
a lot of user are calling the blurring function at the same time but I don't know if it works.

On an ideal world, I would have use an AWS batch job for each process to let AWS handle the complexity 
of being thread safe.

### Thinks that are still TODO
-> Batch job instead of process for thread safe (AWS batch or it's kubernete equivalent)
-> A clean Swagger
-> Clean JSON validation (with nice to read exception that makes it possible for the user to correct)
-> The result of the blurring process (containing the images) is returned in String as it is saved in SqL Lite (it should be an entity)
-> Only PNG file (no other file type) are allowed
-> do a correct logging mechanism
-> no time for perfect tox


### Fun fact
After playing with my application quite a lot to build the front end part, My DB is about 5Gb! 
It's clearly not possible to use this storage architecture on a long term perspective