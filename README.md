# Schedule Program

## About
This program will read all the events saved on a Google Calendar you have access to and send those events in an email to anyone you want.

## Access Instructions
* Only needs to be done once when setting up the program

1. Sign in to your gmail that contains the calendar you will use.

2. Navigate to [Google Console](https://console.cloud.google.com)

3. To the right of Google Cloud Platform, click New Project

4. Go through the steps to make a project.

5. Go to your project's dashboard.

6. Click the navigation menu in the top left corner.

7. Click APIs & Services --> Library.

8. Search for Calendar and click on Google Calendar API.

9. Click Enable.

10. Repeat steps 7 - 9 for the Gmail API.

11. Go back to the navigation menu in the top left corner.

12. Click APIs & Services --> Credentials.

13. Click Create Credentials at the top of the screen.

14. Click OAuth client ID.

15. You will now have to go through the steps to create an OAuth consent screen. In the Scopes section, add the following scopes: 
    * https://www.googleapis.com/auth/calendar.readonly
    * https://www.googleapis.com/auth/gmail.send

16. When you are done with that, click Create Credentials at the top of the screen.

17. Click OAuth client ID.

18. Go through the steps of making an OAuth client ID.

19. When you are done, navigate to the Credentials dashboard.

20. Under OAuth 2.0 Client IDs, you should see the ID you just made.

21. Under Actions, you should see a download button.

22. In the popup screen that appears, click Download JSON.

23. In your downloads, rename the file to client_secret_personal.json.

24. In this directory, make a ```secrets``` folder and move client_secret_personal.json to that directory.

25. You are good to move on to the next steps below.


## Local Change Instructions
* Only needs to be done once when setting up the program

1. In schedule.py, change line 4 to be the number of hours it would take to convert from your local time to UTC's timezone.

2. Visit the Google Calendar you want to use and navigate to its settings.

3. Click on Integrate Calendar and copy the Calendar ID in that section. If you want to use your primary calendar, the calendar ID is simply ```primary```

4. In example.csv, change example@group.calendar.google.com to the calendar ID you just copied.

5. Additionally, update example.csv to have the correct receiver emails. 
    * For more than 1 receiver email, put a space between the emails

6. Rename example.csv to secrets_personal.csv and move this file into the secrets folder

7. Make sure that Python3 is downloaded and up-to-date

8. Open Terminal (Mac) or Command Prompt (Windows)

9. Navigate to this directory using cd commands

10. Run the following command in Terminal/Cmd: ```pip install -r requirements.txt ```

## Option 1: Run the Program Yourself
1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to this directory using cd commands
3. Run the following command in Terminal/Cmd: ```python3 app.py```

## Option 2: Automate the Program to Run at a Certain Time
* Note: the following instructions are for a Mac but there are Windows instructions [here](https://medium.com/analytics-vidhya/effortlessly-automate-your-python-scripts-cd295697dff6)
1. Install and configure [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Copy the path of this directory 
3. Replace line 2 in ```script``` with this copied path
4. Open the Automator application
5. Open a new document and choose ```Application```
6. Search for ```Get Specified Finder Items``` and drag that action into the workflow
7. Click ```Add``` and choose the ```script``` file in this directory
8. Next, search for ```Open Finder Items``` and drag that under the ```Get Specified Finder Items``` action
9. Save the application as ```schedule_app.app``` in this directory
10. Open another document in Automator
11. Choose ```Calendar Alarm```
12. Search for ```Launch Application``` and drag that into the workflow
13. Next, click ```Other``` and choose the ```schedule_app.app``` application in this directory
14. This should open up the Calendar with a new event. Change the frequency of the event and the time you want it to run at.
15. The script will now run at those times assuming that Docker is always running


## Files/Folders
* .gitignore contains all the files that Github should not commit (it is important that you do not commit your client_secret_personal.json or secrets_personal.csv files)
* app.py is the application that verifies credentials and calls the other files' functions
* client_secret_personal.json contains your Google OAuth client secrets
* Dockerfile contains the commands for the Docker image
* emails.py handles working with the Gmail API and sending messages
* example.csv is an example CSV file for what secret.csv should look like
* pictures folder contains the pictures that will randomly be added to the daily emails
* README.md is this file you're reading right now
* requirements.txt contains all the requirements you will need for this program
* schedule_app.app is the application (if you choose to run it with automation)
* schedule.py handles working with the Google Calendar API and creating the body of the email
* script is the script that the application will run (if you choose to run it with automation)
* secrets folder contains secrets_personal.csv, client_secret_personal.json, and (after running the script once) gmail_personal.json and calendar_personal.json
* secrets_personal.csv contains receiver emails as well as your calendar's ID

## Sources
* [Gmail Send Example](https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
)
* [Stack Overflow](https://stackoverflow.com/)


