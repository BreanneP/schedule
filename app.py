import csv
import httplib2
import mimetypes
import oauth2client
import os
from emails import send_emails
from oauth2client import client, tools, file
from schedule import get_html, get_message


client_secret_file = 'client_secret.json'
application_name = 'Gmail API Python Send Email'
subject_line = 'Calendar Update for Tomorrow'


def get_creds(cred_file, scope):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    
    credential_path = os.path.join(credential_dir, cred_file)
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, scope)
        flow.user_agent = application_name
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials


def get_secrets():
    secrets = {}
    my_csv = csv.reader(open('secrets.csv'))
    for row in my_csv:
        secrets[row[0]] = row[1]
    return secrets


if __name__ == '__main__':
    print("Do you want to send an email with events for the week, tomorrow, or the weekend?")
    email_format = input("Either submit week, tomorrow, or weekend: ")

    # get secrets
    secrets = get_secrets()

    # get calendar credentials
    creds = get_creds('gmail-calendar.json', 'https://www.googleapis.com/auth/calendar.readonly')

    # get the message
    if email_format.lower() == 'week':
        message, html, subject = get_message(creds, secrets['calendar'], 7)
    elif email_format.lower() == 'weekend':
        message, html, subject = get_message(creds, secrets['calendar'], 2)
    else:
        message, html, subject = get_message(creds, secrets['calendar'], 1)
    subject_line = f"Events Scheduled for {subject}"
    
    # send the message
    creds = get_creds('gmail-python-email-send.json', 'https://www.googleapis.com/auth/gmail.send')
    creds = creds.authorize(httplib2.Http())
    send_emails(creds, secrets['receivers'], subject_line, html, message)
    