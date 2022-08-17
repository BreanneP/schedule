import httplib2
import oauth2client
from oauth2client import client, tools, file

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


creds = get_creds('secrets/calendar_personal.json', 'https://www.googleapis.com/auth/calendar.readonly')
creds = get_creds('secrets/gmail_personal.json', 'https://www.googleapis.com/auth/gmail.send')
creds = creds.authorize(httplib2.Http())
