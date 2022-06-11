# Schedule Program

## About
This program will read all the events saved on a Google Calendar you have access to and send those events in an email to anyone you want.

## Access Instructions
* Only needs to be done once when setting up the program

1. Sign in to your gmail that contains the calendar you will use.

2. Navigate to [Google Console](https://console.cloud.google.com/welcome?project=testing-352419)

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

23. In your downloads, rename the file to client_secret.json.

24. Move client_secret.json to this directory.

25. You are good to move on to the next steps below.


## Local Change Instructions
* Only needs to be done once when setting up the program

1. In schedule.py, change line 5 to be the number of hours it would take to convert from your local time to UTC's timezone.

2. Visit the Google Calendar you want to use and navigate to its settings.

3. Click on Integrate Calendar and copy the Calendar ID in that section

4. In example.csv, change example@group.calendar.google.com to the calendar ID you just copied.

5. Additionally, update example.csv to have the correct sender and receiver emails. 
    * For instance, suppose I want my sender email to be example5@gmail.com. Change the first line to sender,example5@gmail.com. 
    * For more than 1 receiver email, put a space between the emails

6. Rename example.csv to secrets.csv

7. Make sure that Python3 is downloaded and up-to-date

8. Open Terminal (Mac) or Command Prompt (Windows)

9. Navigate to this directory using cd commands

10. Run the following command in Terminal/Cmd: ```pip install -r requirements.txt ```

## Change the Date Instructions
Right now, this program will send an email with today's events. In order to change this, edit the number of days on line 4 in schedule.py. 
* For instance, if you want to send tomorrow's events, change days = 1 instead of days = 0

## How to Run the Program
1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to this directory using cd commands
3. Run the following command in Terminal/Cmd: ```python3 app.py```

## Files
* .gitignore contains all the files that Github should not commit (it is important that you do not commit your client_secret.json or secrets.csv files)
* app.py is the application that verifies credentials and calls the other files' functions
* client_secret.json contains your Google OAuth client secrets
* emails.py handles working with the Gmail API and sending messages
* example.csv is an example CSV file for what secret.csv should look like
* README.md is this file you're reading right now
* requirements.txt contains all the requirements you will need for this program
* schedule.py handles working with the Google Calendar API and creating the body of the email
* secrets.csv contains sender and receiver emails as well as your calendar's ID

## Sources
* [Gmail Send Example](https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
)
* [Stack Overflow](https://stackoverflow.com/)


