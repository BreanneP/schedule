import datetime
from googleapiclient.discovery import build

date = datetime.date.today() + datetime.timedelta(days = 0)
local_to_utc = 0

months = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
          5: 'May', 6: 'June', 7: 'July', 8: 'August',
          9: 'September', 10: 'October', 11: 'November', 12: 'December'}

days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
        4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


def get_dates():
    t1 = datetime.time(hour = 0, minute = 0)
    t2 = datetime.time(hour = 23, minute = 59)
    start = datetime.datetime.combine(date, t1) + datetime.timedelta(hours=local_to_utc)
    end = datetime.datetime.combine(date, t2) + datetime.timedelta(hours=local_to_utc)
    start = start.isoformat() + 'Z'
    end = end.isoformat() + 'Z'
    return [start, end]


def convert_time(time):
    time = time.split('T')[1].split('-')[0]
    hour = int(time.split(':')[0])
    minutes = time.split(':')[1]
    time_of_day = 'AM' if hour < 12 else 'PM'
    hour = hour % 12
    hour = 12 if hour == 0 else hour
    time = f'{hour}:{minutes} {time_of_day}'
    return time


def get_subject():
    month = int(str(date).split('-')[1])
    month = months[month]
    day = int(str(date).split('-')[2])
    day_of_week = date.weekday()
    day_of_week = days[day_of_week]
    return f'{day_of_week} {month} {day}'


def get_events(creds, cal_id):
    service = build('calendar', 'v3', credentials=creds)
    start, end = get_dates()
    events_result = service.events().list(calendarId=cal_id, timeMin=start, timeMax=end, maxResults = 15, singleEvents = True, orderBy="startTime").execute()
    events = events_result.get('items', None)

    subject = get_subject()
    message = f'The following events are scheduled for {subject}:\n'
    if not events:
        message = f'No events for {subject} :)'

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start = convert_time(start)
        end = convert_time(end)
        summary = event['summary']
        message += f'{start} - {end}: {summary}\n'

    return message


def get_html(message):
    return message.replace('\n', '<br>')


def get_message(creds, cal_id):
    message = get_events(creds, cal_id)
    html = get_html(message)
    subject = get_subject()
    return message, html, subject
