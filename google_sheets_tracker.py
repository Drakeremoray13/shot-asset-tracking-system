import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

def connect_google_sheets(creds_json, sheet_name):
    """Connect to Google Sheets using service account credentials"""
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def update_shot_status(sheet, shot_name, status, artist=None):
    """Update shot status in tracking sheet"""
    # Find the row with the shot name
    try:
        cell = sheet.find(shot_name)
        row = cell.row
        
        # Update status column (column 3)
        sheet.update_cell(row, 3, status)
        
        # Update timestamp (column 4)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sheet.update_cell(row, 4, timestamp)
        
        # Update artist if provided (column 5)
        if artist:
            sheet.update_cell(row, 5, artist)
        
        print(f'Shot {shot_name} updated to status: {status}')
        
    except Exception as e:
        print(f'Error updating shot {shot_name}: {str(e)}')

def get_all_shots_status(sheet):
    """Retrieve all shots and their current status"""
    records = sheet.get_all_records()
    return records

if __name__ == '__main__':
    # Example usage
    creds_json = 'credentials.json'  # Your Google service account credentials
    sheet_name = 'VFX Shot Tracking'
    
    # Connect to sheet
    sheet = connect_google_sheets(creds_json, sheet_name)
    
    # Update a shot status
    update_shot_status(sheet, 'Shot_001', 'Ready for Review', 'John Doe')
    
    # Get all shots
    all_shots = get_all_shots_status(sheet)
    print(f'Total shots tracked: {len(all_shots)}')
