# Schedule Program

## About
This program will read all the events saved on a Google Calendar you have access to and send those events in an email to anyone you want (internal receivers). It will also send events listed on a Google Spreadsheet to other users (external and internal receivers).

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
    * https://www.googleapis.com/auth/spreadsheets
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
1. In email_contents.py and schedule.py, change local_to_utc to be the number of hours it would take to convert from your local time to UTC's timezone.
2. Visit the Google Calendar you want to use and navigate to its settings.
3. Click on Integrate Calendar and copy the Calendar ID in that section. If you want to use your primary calendar, the calendar ID is simply ```primary```
4. In example.csv, change example@group.calendar.google.com to the calendar ID you just copied.
5. Additionally, update example.csv to have the correct receiver emails (internal and external receivers)
    * For more than 1 receiver email, put a space between the emails
6. Find the file ID of the spreadsheet you will be using. [Here](https://www.swipetips.com/how-to-determine-the-file-id-of-a-content-in-google-drive/) are the instructions for finding the ID. Replace file_id_here with this ID
7. Rename example.csv to secrets_personal.csv and move this file into the secrets folder
8. Make sure that Python3 is downloaded and up-to-date
9. Open Terminal (Mac) or Command Prompt (Windows) and navigate to this directory using cd commands
10. Run the following command in Terminal/Cmd: ```pip install -r requirements.txt ```

## Set Up Credential Files
1. Run ```python3 creds.py```
2. You should see two new files added to the ```secrets``` directory
3. You are good to move on to the next steps below


## Set Up Daily Pictures
1. Make a ```pictures``` directory and move the pictures you want sent on a daily basis in this directory
2. Rename them to start at ```1.jpg```, then ```2.jpg```, and so one
    * Important note: Make sure they are named ```.jpg``` not ```.JPG```
3. Note: the pictures.csv file contains the dates each picture will be sent. For instance, if it's August 17 and I am sending a reminder for August 18, picture ```2.jpg``` will be sent on August 17
4. You are good to move on to the next steps below


## Set Up Automation
1. Make sure all the files in the ```secrets``` folder are accessible to everyone by running ```chmod 755 file_name``` on each file
2. In Terminal, navigate to this directory and run the following command: ```pip install --target . google-api-python-client```
3. Run this command as well: ```pip install --target . oauth2client```
4. Next, zip the contents of this directory by running this command: ```zip -r package.zip .```
5. Now, make an AWS account with the free tier
6. Navigate to the Lambda service on AWS
7. Create a new function
    * Choose ```Author from scratch```
    * You can pick your function name
    * Use ```Python 3.9``` for the Runtime
    * Use x86_64 architecture
8. In the code section of the Lambda function, you should see an ```Upload from``` button.
9. Click this button and choose ```.zip file```
10. Choose the ```package.zip``` file
    * Note: if your zip file is too large, you might have to upload it from S3 instead
11. In Runtime settings, change the handler from ```lambda_function.lambda_handler``` to ```app.run```
12. Next, navigate to the EventBridge service in AWS
13. Create a new Rule
    * Name the rule whatever you want
    * Choose ```Schedule``` for Rule Type
14. Choose the schedule you want the program to run on
15. For Target, choose AWS service
16. Search for ```Lambda function```
17. Choose the lambda function you just created
18. You can skip the tag section and create the rule
19. Next, navigate back to the Lambda function you created
20. In the function overview, you should see ```+Add Trigger```
21. For source, select ```Eventbridge (CloudWatch Events)```
22. Search existing rules and select the one you just created
23. In the lambda function, click on ```Configuration```
24. Then click on ```General Configuration``` and change the timeout to 30 seconds
25. Test out your changes in the Lambda function by making a test event in the Test tab


## Files/Folders
* .gitignore contains all the files that Github should not commit (it is important that you do not commit your client_secret_personal.json or secrets_personal.csv files)
* app.py is the application that verifies credentials and calls the other files' functions
* client_secret_personal.json contains your Google OAuth client secrets
* creds.py is the script to generate your scope-specific credentials
* email_contents.py handles obtaining the message, subject, and image to send to receivers
* emails.py handles working with the Gmail API and sending messages
* example.csv is an example CSV file for what secret.csv should look like
* pictures folder contains the pictures that will randomly be added to the daily emails
* pictures.csv contains the keys (dates) and values (picture) for when pictures will be sent
* README.md is this file you're reading right now
* requirements.txt contains all the requirements you will need for this program
* schedule.py handles working with the Google Calendar API and obtaining the internal events
* secrets folder contains secrets_personal.csv, client_secret_personal.json, and (after running the script once) gmail_personal.json and calendar_personal.json
* secrets_personal.csv contains receiver emails as well as your calendar's ID
* sheets.py handles working with the Google Sheets API and obtaining the external events

## Sources
* [Gmail Send Example](https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
)
* [Stack Overflow](https://stackoverflow.com/)
* [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-package-with-dependency)
