# CITS3403-Project

1. A description of the purpose of the application, explaining its design and use.

The Job Matchmaker application is an app which serves as a job board for tradies. 
  - Users can sign up (if they are tradies they can register their acount as a tradie account)
  - Once signed up, regular users and tradie users alike can post requests for trade work that they need done, e.g requesting a plumber to unclog their pipes.
  - Signed in users can search all job requests that have been made, based on certain filters (i.e trade, location) and can order the results by criteria like date created, State, postcode, etc...
  - When a relevant job is found the user can view the job, if they are a tradie, and their trade matches the required trade they can make an offer to complete the job by specifying an estimated time to complete, and an appointment date.
  - When viewing a job a user can see all of the job information, aswell as the details of all offers made for that job
  - If the user is the owner of a request they can respond to offers made on their requests either accepting or rejecting.
  - Users can easily view all the job requests they have made by viewing their request history page
  - Tradies can easily view all of the offers they have made, and their acceptance/rejection status by viewing their offer history page

2. a table with with each row containing the i) UWA ID ii) name and iii) Github user name of the group members.

| UWA ID       | name              | Git-Hub Username |
|--------------|-------------------|------------------|
| 23213995     | Tyler Etherton    | T-Eth            |
| 23123894     | Jansen Chuah      | JC3009           |
| 23078885     | Leonard Yau       | Anyting0476      |
| 23457849     | Akshay Sundru     | akshaysundru     |




3. a brief summary of the architecture of the application.

The application is built using javascript, html, css, and flask. jinja, sqlalchemy and wtforms are used alongside flask to facilitate the core server functionality.
  - app/templates contains all of the jinja/html templates used to serve data from the application to end users
  - app/static contains the images, javascript scripts and css files used to make the website interactive on the front end, and visually appealing
  - app contains all of the python files that facilitate the backend functionality of the application.
  - models.py contains all of the database models used by the application for storing, retreiving and using persistent data
  - forms.py builds the classes for each of the types of forms used in the application
  - controllers.py contains functions used to control the logic of the application, these functions are used by view functions in routes.py to control the logical flow of serving data to users.


4. instructions for how to launch the application.
  - Create a virtual environment with all packages in the requirements.txt file installed
  - Ensure terminal is in CITS3403-Project/Website directory
  - Ensure that FLASK_APP environment variable is set to webserver.py
  - Ensure that TRADIE_SECRET_KEY environment variable is set to the secret key
  - execute flask run
  
5. instructions for how to run the tests for the application.
  - To run tests, make sure virtual environment has all packages in the requirements.txt file installed
  - For testing we need to run pytest in the terminal, this can be done by entering pytest into the terminal.
  - To ensure that pytest will run when entered, run export PYTHONPATH=.:$PYTHONPATH in the terminal.
  - This will run the tests as long as long as the terminal is set in the project directory.
