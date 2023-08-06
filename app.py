import csv
import httplib2
import mimetypes
import os
import subprocess
import oauth2client
from oauth2client import client, tools, file
from shutil import copyfile
from emails import send_message
from email_contents import EmailContents


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

    # get credentials
    cal_creds = get_creds('secrets/calendar_personal.json')
    sheet_creds = get_creds('secrets/sheets_personal.json')
    sheet_creds = sheet_creds.authorize(httplib2.Http())
    gmail_creds = get_creds('secrets/gmail_personal.json')
    gmail_creds = gmail_creds.authorize(httplib2.Http())

    # send the schedule emails
    email = EmailContents(True, cal_creds, sheet_creds, secrets['calendar'], secrets['file_id'])
    for receiver in secrets['internal_receivers'].split(' '):
        send_message(gmail_creds, receiver, email.subject, email.html, email.message, email.image)

    # send the cat emails
    email = EmailContents(False, cal_creds, sheet_creds, secrets['calendar'], secrets['file_id'])
    for receiver in secrets['external_receivers'].split(' '):
        send_message(gmail_creds, receiver, email.subject, email.html, email.message, email.image)
