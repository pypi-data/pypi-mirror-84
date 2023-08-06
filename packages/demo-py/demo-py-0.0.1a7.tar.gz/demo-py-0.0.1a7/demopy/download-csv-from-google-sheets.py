# This is based off of the following links ...
# -

# For it to work ... a service account must be created ... and the google sheet file must be shared with that service account as well

# Sample Usage:
# python test.py '/Users/oeid/Downloads/project-id-0905112707509830376-028dc8bad02b.json' '12lCPaKogTJx9d5GMZsG7VGI_eu-idFIPEZLoNpOHwyI''property-schema!A1:L100'


from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import sys

CRED_FILE = sys.argv[1]
SPREADSHEET_ID= sys.argv[2]
RANGE = sys.argv[3]


credentials = service_account.Credentials.from_service_account_file(
    '/Users/oeid/Downloads/project-id-0905112707509830376-028dc8bad02b.json')

scoped_credentials = credentials.with_scopes([
    'https://www.googleapis.com/auth/spreadsheets.readonly'
])

service = build('sheets', 'v4', credentials=scoped_credentials)

spreadsheets = service.spreadsheets()

# Gets Metadata on Spreadsheet
# result = spreadsheets.get(spreadsheetId=SPREADSHEET_ID, ranges=RANGE).execute()
# Gets values in Spreadsheet
result = spreadsheets.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
columns, values = result.get('values', [])[0], result.get('values', [])[1:]
# print(columns)
# print(values)
df = pd.DataFrame([v for v in values if v])
# If last column is all null ... its not included in data ...
if columns:
    df.columns = columns[:len(df.columns)]
print(df.to_csv(index=False), end="")
