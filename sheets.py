from apiclient import discovery, errors
from apiclient.http import MediaFileUpload

class Sheets:
    def read_file(self, creds, file_id, sheet_range):
        try:
            service = discovery.build("sheets", "v4", http=creds)
            sheet = service.spreadsheets()
            file_content = sheet.values().get(spreadsheetId=file_id, range=sheet_range).execute()
            return file_content

        except errors.HttpError as error:
            print(f"Could not read the spreadsheet file: {error}")


    def get_external_events(self, creds, file_id, date):
        contents = self.read_file(creds, file_id, "A1:C30")['values']

        for row in contents:
            if date == row[0]:
                return f'<li><u>{row[1]}</u>: {row[2]}</li>'
