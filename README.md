# Schedule Program

## About
This program will read all the events saved on a Google Calendar you have access to and send those events in an email to anyone you want.

## Access Instructions
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
1. In schedule.py, change line 4 to be the number of hours it would take to convert from your local time to UTC's timezone.
2. Visit the Google Calendar you want to use and navigate to its settings.
3. Click on Integrate Calendar and copy the Calendar ID in that section. If you want to use your primary calendar, the calendar ID is simply ```primary```
4. In example.csv, change example@group.calendar.google.com to the calendar ID you just copied.
5. Additionally, update example.csv to have the correct receiver emails
    * For more than 1 receiver email, put a space between the emails
6. Rename example.csv to secrets_personal.csv and move this file into the secrets folder
7. Make sure that Python3 is downloaded and up-to-date
8. Open Terminal (Mac) or Command Prompt (Windows) and navigate to this directory using cd commands
9. Run the following command in Terminal/Cmd: ```pip install -r requirements.txt ```
10. You are good to move on to the next steps below.


## Set Up Credential Files
1. Run ```python3 creds.py```
2. You should see two new files added to the ```secrets``` directory
3. You are good to move on to the next steps below


## Set Up Daily Pictures
1. Make a ```pictures``` directory and move the pictures you want sent on a daily basis in this directory
2. Rename them to start at ```1.jpg```, then ```2.jpg```, and so one
    * Important note: Make sure they are named ```.jpg``` not ```.JPG```
3. You are good to move on to the next steps below


## Set Up Automation
1. Make an AWS account with the free tier
2. Navigate to the Lambda service on AWS
3. Create a new function
    * Choose ```Author from scratch```
    * You can pick your function name
    * Use ```Python 3.9``` for the Runtime
    * Use x86_64 architecture
4. instructions here for zip folder

7. Next, navigate to the EventBridge service in AWS
8. Create a new Rule
    * Name the rule whatever you want
    * Choose ```Schedule``` for Rule Type
9. Choose the schedule you want the program to run on
10. For Target, choose AWS service
11. Search for ```Lambda function```
12. Choose the lambda function you just created
13. You can skip the tag section and create the rule
14. Next, navigate back to the Lambda function you created
15. In the function overview, you should see ```+Add Trigger```
16. For source, select ```Eventbridge (CloudWatch Events)```
17. Search existing rules and select the one you just created
18. In the lambda function, click on ```Configuration```
19. Then click on ```General Configuration``` and change the timeout to 30 seconds
20. You should see the schedule run at the time you set it for


## Files/Folders
* .gitignore contains all the files that Github should not commit (it is important that you do not commit your client_secret_personal.json or secrets_personal.csv files)
* app.py is the application that verifies credentials and calls the other files' functions
* client_secret_personal.json contains your Google OAuth client secrets
* creds.py is the script to generate your scope-specific credentials
* emails.py handles working with the Gmail API and sending messages
* example.csv is an example CSV file for what secret.csv should look like
* pictures folder contains the pictures that will randomly be added to the daily emails
* README.md is this file you're reading right now
* requirements.txt contains all the requirements you will need for this program
* schedule.py handles working with the Google Calendar API and creating the body of the email
* secrets folder contains secrets_personal.csv, client_secret_personal.json, and (after running the script once) gmail_personal.json and calendar_personal.json
* secrets_personal.csv contains receiver emails as well as your calendar's ID

## Sources
* [Gmail Send Example](https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
)
* [Stack Overflow](https://stackoverflow.com/)
* [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-package-with-dependency)
