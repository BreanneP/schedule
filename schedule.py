import datetime
from googleapiclient.discovery import build

local_to_utc = 0

months = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
          5: 'May', 6: 'June', 7: 'July', 8: 'August',
          9: 'September', 10: 'October', 11: 'November', 12: 'December'}

days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
        4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


def get_dates(num_days):
    t1 = datetime.time(hour = 0, minute = 0)
    t2 = datetime.time(hour = 23, minute = 59)
    today = datetime.datetime.utcnow() - datetime.timedelta(hours=local_to_utc)
    date = today.date() + datetime.timedelta(days=num_days)
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


def get_formatted_date(num_days):
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=local_to_utc)
    date = date + datetime.timedelta(days=num_days)
    month = date.month
    month = months[month]
    day_of_week = date.weekday()
    day_of_week = days[day_of_week]
    return f'{day_of_week}, {month} {date.day}'


def get_events(creds, cal_id, num_days):
    service = build('calendar', 'v3', credentials=creds)
    start, end = get_dates(num_days)
    events_result = service.events().list(calendarId=cal_id, timeMin=start, timeMax=end, maxResults=15, singleEvents=True, orderBy="startTime").execute()
    events = events_result.get('items', None)

    message = ''
    if not events:
        message = '<li>No events :)</li>'

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start = convert_time(start)
        end = convert_time(end)
        summary = event['summary']
        message += f'<li><u>{start} - {end}</u>: {summary}'

        description = event.get('description', None)
        if description:
            message += f' - {description}'

        if event.get('location', None):
            location = event['location']
            if location.startswith('http'):
                message += ' (Virtual)'
            else:
                message += f' ({location})'
        message += '</li>'

    return message


def get_html(message):
    return message.replace('\n', '<br>')


def get_message(creds, cal_id):
    message = ''
    tomorrow = get_formatted_date(1)

    if tomorrow.startswith('Monday'):
        num_days = 7
        subject = 'This Week'
    elif tomorrow.startswith('Saturday'):
        num_days = 2
        subject = 'This Weekend'
    else:
        num_days = 1
        subject = tomorrow

    for day in range(1, num_days + 1):
        message += f'<b>{get_formatted_date(day)}</b>\n'
        message += f'<ul>{get_events(creds, cal_id, day)}</ul>\n'

    message = f"<font size='+1'>{message}</font>"
    html = get_html(message)
    return message, html, subject
