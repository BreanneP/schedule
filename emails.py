import base64
import mimetypes
import os
from apiclient import errors, discovery
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_message(receiver, subject, msg_html, msg_plain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = receiver
    msg.attach(MIMEText(msg_plain, 'plain'))
    msg.attach(MIMEText(msg_html, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {'raw': raw}


def create_message_with_file(receiver, subject, msg_html, msg_plain, attachment_file):
    message = MIMEMultipart('mixed')
    message['to'] = receiver
    message['subject'] = subject

    messageA = MIMEMultipart('alternative')
    messageR = MIMEMultipart('related')

    messageR.attach(MIMEText(msg_html, 'html'))
    messageA.attach(MIMEText(msg_plain, 'plain'))
    messageA.attach(messageR)
    message.attach(messageA)

    content_type, encoding = mimetypes.guess_type(attachment_file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachment_file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(attachment_file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(attachment_file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    filename = os.path.basename(attachment_file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
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


def send_message(creds, receiver, subject, msg_html, msg_plain):
    service = discovery.build('gmail', 'v1', http=creds)
    message = create_message(receiver, subject, msg_html, msg_plain)
    result = send_message_internal(service, 'me', message, receiver)
    return result


def send_emails(creds, receivers, subject, msg_html, msg_plain):
    receivers = receivers.split(' ')
    for email in receivers:
        send_message(creds, email, subject, msg_html, msg_plain)
