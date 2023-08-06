import csv
import datetime
from schedule import Schedule
from sheets import Sheets

local_to_utc = 0

months = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
          5: 'May', 6: 'June', 7: 'July', 8: 'August',
          9: 'September', 10: 'October', 11: 'November', 12: 'December'}

days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
        4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


class EmailContents:
    def __init__(self, internal, cal_creds, sheet_creds, cal_id, file_id):
        self.internal = internal
        self.cal_creds = cal_creds
        self.sheet_creds = sheet_creds
        self.cal_id = cal_id
        self.file_id = file_id
        self.tomorrow = self.get_formatted_date(1)
        self.image = self.get_image()
        self.num_days = self.get_num_days()
        self.subject = self.get_subject()
        self.message = self.get_message()
        self.html = self.get_html()
    
    def get_formatted_date(self, num_days):
        date = datetime.datetime.utcnow() - datetime.timedelta(hours=local_to_utc)
        date = date + datetime.timedelta(days=num_days)
        month = date.month
        month = months[month]
        day_of_week = date.weekday()
        day_of_week = days[day_of_week]
        return f'{day_of_week}, {month} {date.day}'
    
    def get_image(self):
        tomorrow = self.tomorrow.split(',')[1].strip()
        my_csv = csv.reader(open('pictures.csv'))
        for row in my_csv:
            if row[0] == tomorrow:
                return f'pictures/{row[1]}.jpg'
    
    def get_num_days(self):
        if self.tomorrow.startswith('Monday'):
            return 7
        elif self.tomorrow.startswith('Saturday'):
            return 2
        else:
            return 1
    
    def get_subject(self):
        if self.internal and self.num_days == 7:
            return 'This Week'
        elif self.internal and self.num_days == 2:
            return 'This Weekend'
        elif self.internal and self.num_days == 1:
            return self.tomorrow
        else:
            return 'Caturday Picture :)'
    
    def get_html(self):
        return self.message.replace('\n', '<br>')
    
    def get_message(self):
        message = ''
        for day in range(1, self.num_days + 1):
            if self.internal:
                internal_events = Schedule().get_internal_events(self.cal_creds, self.cal_id, day)
            else:
                internal_events = None

            date = self.get_formatted_date(day)
            external_events = Sheets().get_external_events(self.sheet_creds, self.file_id, date)

            message += f'\n<b>{date}</b>\n'
            if external_events:
                message += f'<ul>{external_events}</ul>'
            if internal_events:
                message += f'<ul>{internal_events}</ul>'
            if not external_events and not internal_events:
                message += '<ul> No events today :) </ul>'

        return f"<font size='+1'>{message}</font>"
