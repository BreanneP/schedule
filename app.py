import csv
import httplib2
import mimetypes
import os
import subprocess
import oauth2client
from oauth2client import client, tools, file
from shutil import copyfile
from emails import send_emails
from schedule import get_html, get_message


def get_creds(cred_path):
    tmp_dir = '/tmp/secrets'
    token_path = os.path.join(tmp_dir, cred_path.split('/')[1])

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    subprocess.run(["chmod", "755", str(tmp_dir)])
    copyfile(cred_path, token_path)
    store = oauth2client.file.Storage(token_path)
    credentials = store.get()

    return credentials


def get_secrets():
    secrets = {}
    my_csv = csv.reader(open('secrets/secrets_personal.csv'))
    for row in my_csv:
        secrets[row[0]] = row[1]
    return secrets


def run(event, context):
    # get secrets
    secrets = get_secrets()

    # get calendar credentials
    creds = get_creds('secrets/calendar_personal.json')

    # get the message
    message, html, subject, image = get_message(creds, secrets['calendar'])
    subject_line = f'Events Scheduled for {subject}'
    
    # send the message
    creds = get_creds('secrets/gmail_personal.json')
    creds = creds.authorize(httplib2.Http())
    send_emails(creds, secrets['receivers'], subject_line, html, message, image)