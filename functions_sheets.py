import os.path
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from decorators import *
from exceptions import *
import config

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = config.SPREADSHEET_ID

logger = logging.getLogger("Scraper.functions")

def get_valid_creds():
    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is created
        # automatically when the authorization flow completes for the first time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                is_docker = os.path.exists("/.dockerenv")
                if is_docker:
                    logger.info("Running in Docker. Starting OAuth local server on port 8080. Please ensure port 8080 is exposed/mapped.")
                    creds = flow.run_local_server(host="localhost", bind_addr="0.0.0.0", port=8080, open_browser=False)
                else:
                    creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds
    except:
        handleException("Couldn't get valid credits from token.")

def get_sheets_api(creds):
    try:
        service = build("sheets", "v4", credentials=creds)
        # Call the Sheets API
        return service.spreadsheets()
    except:
        handleException("Couldn't get Google Sheets API.")

@sheets_retry()
def get_sheet_values(sheets, address):
    return sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=address).execute().get("values")

@sheets_retry()
def update_sheet_values(sheets, address, values):
    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=address,
                          valueInputOption="USER_ENTERED", body={"values": values}).execute()

@sheets_retry()
def clear_sheet_values(sheets, address):
    sheets.values().clear(spreadsheetId=SPREADSHEET_ID, range=address).execute()    

@sheets_retry()
def append_sheet_values(sheets, address, values):
    sheets.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=address, # Can be any column, e.g., "Sheet1!A1"
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",  # Ensures it inserts new rows if needed
        body={"values": values}
    ).execute()

@sheets_retry()
def get_sheet_id(sheets, sheet_name):
    spreadsheet = sheets.get(spreadsheetId=SPREADSHEET_ID).execute()
    for sheet in spreadsheet["sheets"]:
        if sheet["properties"]["title"] == sheet_name:
            return sheet["properties"]["sheetId"]
    return None  # Returns None if the sheet name doesn't exist

@sheets_retry()
def add_rows(sheets, sheet_name, num_rows):
    sheet_id = get_sheet_id(sheets, sheet_name)
    requests = [
        {
            "appendDimension": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "length": num_rows
            }
        }
    ]
    body = {"requests": requests}
    sheets.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

@sheets_retry()
def remove_filter(sheets, sheet_name):
    sheet_id = get_sheet_id(sheets, sheet_name)
    requests = [
        {
            "clearBasicFilter": {
                "sheetId": sheet_id
            }
        }
    ]
    body = {"requests": requests}
    sheets.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

@sheets_retry()
def apply_filter(sheets, sheet_name, start_row, start_col, end_row):
    sheet_id = get_sheet_id(sheets, sheet_name)
    requests = [
        {
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": start_row,  # First row (header)
                        "endRowIndex": end_row,  # Last row with data
                        "startColumnIndex": start_col,  # First column (0-based)
                        #"endColumnIndex": end_col  # Last column +1
                    }
                }
            }
        }
    ]
    body = {"requests": requests}
    sheets.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

@sheets_retry()
def safe_insert_at_bottom(sheets, sheet_name, values):
    # Get the current sheet dimensions and data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID, 
        range=f"{sheet_name}!A:A"
    ).execute()
    
    current_rows = result.get('values', [])
    last_row_index = len(current_rows) # This tells us where the data ends
    
    # If the sheet is totally empty, we start at row 1. 
    # If you have headers, last_row_index + 1 is your first available empty row.
    target_row = last_row_index + 1
    
    # Update the values at the exact bottom
    address = f"{sheet_name}!A{target_row}"
    
    sheets.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=address,
        valueInputOption="USER_ENTERED",
        body={"values": values}
    ).execute()
