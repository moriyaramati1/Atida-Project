# Army Project:

In this project, I created two SQL tables:
Members table for conducting patient records with their personal properties.
Covid table with the id of those patients and information about their vaccination and isolation.

The table's common key is id, you can see the following structure:


<p align="left">
     <img src= Hospital\static\images\7.png width="500">
</p>


Building a UI with: HTML,CSS,JS.
For the server-side implementation,I use Flask framework (python).
Flask will enable me to build an API that handles the communication between the front-end interface and the back-end database.

##The Client Side:

The home page - contains 6 option buttons, each leads to the right html.

<p align="left">
     <img src= Hospital\static\images\1.png width="500">
</p>

New client page - which enable to fill form with patients details and add a picture of the patient.
<p align="left">
   <img src= Hospital\static\images\2.png >
</p>


New covid record page - which enables to fill form with patients details only if this person exists in patient's table.

<p align="left">
     <img src= Hospital\static\images\4.png >
</p>


When submitting the forms and the information passes successfully it will lead to the following page:

<p align="left">
    <img src= Hospital\static\images\3.png >
 </p>

In case of any error in the system, we get an Error page with a description of the error that Required.
For example, if the patient already exists its returns the following page:

<p align="left">
    <img src= Hospital\static\images\5.png width="500">
</p>

Activate Patients page - contains a barplot that represents the number of patients on each day in the last month:
<p align="left">
    <img src= Hospital\static\images\8.png width="500">
 </p>


The Covid data and Members' data we can get as this page:
<p align="left">
     <img src= Hospital\static\images\9.png width="500">
</p>

The number of people that didn't do vaccinated we can get as this page:

<p align="left">
      <img src= Hospital\static\images\10.png width="500">
</p>


## Docker-compose

I created docker-compose file, with two services:
- application container that runs my flask app,
- A database container for running Postgres SQL.

### For setting up the following commands should be executed.

(cd Hospital)
docker-compose up --build
and we can access our application from the following address http://127.0.0.1:5000.


## Project Files and Directories:
  The first assignment is under twitter-assignment Folder.

  The Second assignment is under Hospital Folder.
    Hospital Folder:

        Static Folder:
            contains CSS,JS for client side:
            images: with all project images.

        templates folder:
            Home_page.html  - home page.
            covid_data.html - page with members data.
            members_data.html - page with members data.
            new_client.html - form page for new patients.
            new_covid.html - form page for new covid record.
            not_vaccinated.html - page that represent the number of not vaccinated patients.
            fail.html - for errors with description.
            success.html - for success

        app.py - the flask app and the APIs.
        DB.py - builds the DB class and its functionality.
        requirements.txt - all the packages for this project.
        Dockerfile and docker-compose - as explained above.

        For part 2 on this assignment - there is Part2.docx file with answers.


