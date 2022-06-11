import base64
import mimetypes
from apiclient import errors, discovery
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_message(sender, to, subject, msg_html, msg_plain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msg_plain, 'plain'))
    msg.attach(MIMEText(msg_html, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {'raw': raw}


def send_message_internal(service, user_id, message, receiver):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(f'Successfully sent to {receiver}')
        return message
    except errors.HttpError as error:
        print(f'An error occurred: {error}')
        return 'Error'
    return 'OK'


def send_message(creds, sender, receiver, subject, msg_html, msg_plain):
    service = discovery.build('gmail', 'v1', http=creds)
    message = create_message(sender, receiver, subject, msg_html, msg_plain)
    result = send_message_internal(service, 'me', message, receiver)
    return result


def send_emails(creds, sender, receivers, subject, msg_html, msg_plain):
    receivers = receivers.split(' ')
    for email in receivers:
        send_message(creds, sender, email, subject, msg_html, msg_plain)
