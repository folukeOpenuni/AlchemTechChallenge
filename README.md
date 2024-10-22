#Project Overview
This project is an event logging system built with Flask for the backend API and a React-based frontend. The system allows users to log and retrieve event data, which is stored in an SQLite database.

#Project Setup
Running in GitHub Codespaces
If you are using GitHub Codespaces, the environment is preconfigured, so no manual setup is required. Simply open the repository in Codespaces and follow the steps in the Running the Application section.

if running locally 
git clone --branch RestfulAPI https://github.com/folukeOpenuni/AlchemTechChallenge.git
the master branch is not working as expected, so do not clone the master branch 

##Backend Setup:
once the repository is cloned, run

##Install Python dependencies:

    pip install -r requirements.txt

##Set up the database: The project uses SQLite. Ensure you have SQLite installed, then run:
    python api/app.py  # This will auto-generate the SQLite database

