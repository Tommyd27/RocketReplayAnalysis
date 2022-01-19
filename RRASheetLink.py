import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetsLink:
    def __init__(self) -> None:
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('sheetsKey.json', self.scope)
        self.client = gspread.authorize(self.creds)

