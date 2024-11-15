"""Upload a csv file to an existing tab of a Google Sheet."""

import csv
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1hR2JKrbmP4j_6p2dNADQlneVKwHKoVfaTWEXy-DdgdM"
TAB_NAME = "Raw Data"


def main():
    """Upload a csv file to an existing tab of a Google Sheet."""
    if len(sys.argv) != 2:
        print("Usage: python upload_csv_to_sheets.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # read the CSV file in:
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            data = [row for row in reader]

        # convert numeric fields to integers
        for row in data:
            for i, cell in enumerate(row):
                try:
                    row[i] = int(cell)
                except ValueError:
                    pass

        # Post the data to the Google Sheet
        sheet = service.spreadsheets()

        response = (
            sheet.values()
            .update(
                spreadsheetId=SPREADSHEET_ID,
                range=TAB_NAME,
                valueInputOption="USER_ENTERED",
                body={"values": data},
            )
            .execute()
        )

        print(f'{response.get("updatedCells")} cells updated.')
    except HttpError as err:
        print(err)



if __name__ == "__main__":
    main()
