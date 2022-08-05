import csv
import httplib2
import mimetypes
import oauth2client
import os
from emails import send_emails
from oauth2client import client, tools, file
from schedule import get_html, get_message

# TO DO LIST
# 1. Figure out why pictures repeat
# 2. Add more pictures to the pictures directory

client_secret_file = 'secrets/client_secret_personal.json'
application_name = 'Gmail API Python Send Email'
subject_line = 'Calendar Update for Tomorrow'


def get_creds(cred_path, scope):
    store = oauth2client.file.Storage(cred_path)
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, scope)
        flow.user_agent = application_name
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + cred_path)

    return credentials


def get_secrets():
    secrets = {}
    my_csv = csv.reader(open('secrets/secrets_personal.csv'))
    for row in my_csv:
        secrets[row[0]] = row[1]
    return secrets


if __name__ == '__main__':
    # get secrets
    secrets = get_secrets()

    # get calendar credentials
    creds = get_creds('secrets/calendar_personal.json', 'https://www.googleapis.com/auth/calendar.readonly')

    # get the message
    message, html, subject = get_message(creds, secrets['calendar'])
    subject_line = f'Events Scheduled for {subject}'
    
    # send the message
    creds = get_creds('secrets/gmail_personal.json', 'https://www.googleapis.com/auth/gmail.send')
    creds = creds.authorize(httplib2.Http())
    send_emails(creds, secrets['receivers'], subject_line, html, message)