import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup the Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the sheet with error handling
try:
    sheet = client.open("ZoneAI_Data").worksheet("Sheet1")
except gspread.exceptions.SpreadsheetNotFound:
    print("[ERROR] Spreadsheet 'ZoneAI_Data' not found. Creating a new one.")
    sheet = client.create("ZoneAI_Data").sheet1

def append_to_sheet(data):
    try:
        zone_id = data["zone_id"]
        all_records = sheet.get_all_records()
        found = False
        for i, record in enumerate(all_records, start=2):
            if str(record.get("zone_id")) == str(zone_id):
                found = True
                row = i
                sheet.update_cell(row, 2, data.get("timeframe", ""))
                sheet.update_cell(row, 3, data.get("event", ""))
                sheet.update_cell(row, 4, data.get("price", ""))
                sheet.update_cell(row, 5, data.get("bounce_pts", ""))
                sheet.update_cell(row, 6, data.get("direction", ""))
                sheet.update_cell(row, 7, data.get("parent_structure", ""))
                sheet.update_cell(row, 8, datetime.utcnow().isoformat())
                break
        if not found:
            sheet.append_row([
                data.get("zone_id", ""),
                data.get("timeframe", ""),
                data.get("event", ""),
                data.get("price", ""),
                data.get("bounce_pts", ""),
                data.get("direction", ""),
                data.get("parent_structure", ""),
                datetime.utcnow().isoformat()
            ])
        print(f"[INFO] Sheet updated for zone_id: {zone_id}")
    except Exception as e:
        print(f"[ERROR] Failed to update sheet: {e}")