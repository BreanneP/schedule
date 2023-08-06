import datetime
from googleapiclient.discovery import build


class Schedule:
    def __init__(self):
        self.local_to_utc = 0

    def get_dates(self, num_days):
        t1 = datetime.time(hour = 0, minute = 0)
        t2 = datetime.time(hour = 23, minute = 59)
        today = datetime.datetime.utcnow() - datetime.timedelta(hours=self.local_to_utc)
        date = today.date() + datetime.timedelta(days=num_days)
        start = datetime.datetime.combine(date, t1) + datetime.timedelta(hours=self.local_to_utc)
        end = datetime.datetime.combine(date, t2) + datetime.timedelta(hours=self.local_to_utc)
        start = start.isoformat() + 'Z'
        end = end.isoformat() + 'Z'
        return [start, end]


    def convert_time(self, time):
        time = time.split('T')[1].split('-')[0]
        hour = int(time.split(':')[0])
        minutes = time.split(':')[1]
        time_of_day = 'AM' if hour < 12 else 'PM'
        hour = hour % 12
        hour = 12 if hour == 0 else hour
        time = f'{hour}:{minutes} {time_of_day}'
        return time


    def get_internal_events(self, creds, cal_id, num_days):
        service = build('calendar', 'v3', credentials=creds)
        start, end = self.get_dates(num_days)
        events_result = service.events().list(calendarId=cal_id, timeMin=start, timeMax=end, maxResults=15, singleEvents=True, orderBy="startTime").execute()
        events = events_result.get('items', None)

        message = ''

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            start = self.convert_time(start)
            end = self.convert_time(end)
            summary = event['summary']
            message += f'<li><u>{start} - {end}</u>: {summary}'

            if event.get('location', None):
                location = event['location']
                if location.startswith('http'):
                    message += ' (Virtual)'
                else:
                    message += f' ({location})'
            message += '</li>'

        return message
