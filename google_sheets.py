import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Defer sheet initialization to function call
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    try:
        sheet = client.open("ZoneAI_Data").worksheet("Sheet1")
    except gspread.exceptions.SpreadsheetNotFound:
        print("[ERROR] Spreadsheet 'ZoneAI_Data' not found. Creating a new one.")
        sheet = client.create("ZoneAI_Data").sheet1
    return sheet

def append_to_sheet(data):
    try:
        sheet = get_sheet()
        zone_id = data.get("zone_id", "")
        # Always append a new row to preserve all entries
        sheet.append_row([
            zone_id,
            data.get("timeframe", ""),
            data.get("event", ""),
            data.get("price", ""),
            data.get("bounce_pts", ""),
            data.get("direction", ""),
            data.get("parent_structure", ""),
            datetime.utcnow().isoformat()
        ])
        print(f"[INFO] Sheet appended for zone_id: {zone_id}")
    except Exception as e:
        print(f"[ERROR] Failed to update sheet: {e}")