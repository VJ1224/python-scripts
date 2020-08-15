from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build # noqa
from google_auth_oauthlib.flow import InstalledAppFlow # noqa
from google.auth.transport.requests import Request # noqa
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = os.getenv('SUBSCRIPTIONS_SHEET') # Sheet ID in environment variables
EMAIL_RANGE = 'Emails!B2:B' # Edit Range


def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=EMAIL_RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        file = open("emails.txt", "w") # Change filename
        for row in values:
            file.write(row[0]+"\n")
        print("File created")


if __name__ == '__main__':
    main()
