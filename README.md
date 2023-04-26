# The blurring project

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
-> faire un system de logging correcte
-> shouldn't do all the picture at once as it's quite heavy to transfert. Maybe should have done the image treatment 
   one by one so that the user can start using the application with the first image and not wait for all the image 
   to be processed to be able to see the first one.
