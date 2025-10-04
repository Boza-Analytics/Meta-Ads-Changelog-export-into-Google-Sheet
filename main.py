import requests
import json
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Meta API credentials and endpoint
access_token = ''
ad_account_id = ''
meta_url = f"https://graph.facebook.com/v20.0/{ad_account_id}/activities"

# Google Sheets API credentials and spreadsheet details
SERVICE_ACCOUNT_FILE = ''
SPREADSHEET_ID = ''  # Update with your spreadsheet ID
SHEET_NAME = 'Sheet1'  # Update with your sheet name

def get_ad_activities(start_time, end_time):
    # Convert datetime to ISO 8601 format
    start_time_iso = start_time.isoformat()
    end_time_iso = end_time.isoformat()

    params = {
        'access_token': access_token,
        'since': start_time_iso,
        'until': end_time_iso,
        'fields': 'actor_id,actor_name,application_id,application_name,date_time_in_timezone,event_time,event_type,extra_data,object_id,object_name,object_type,translated_event_type'
    }

    all_activities = []
    url = meta_url

    while url:
        response = requests.get(url, params=params)
        
        # Print the URL and response for debugging
        print(f"Request URL: {response.url}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content.decode()}")

        if response.status_code != 200:
            print(f"Error: {response.content.decode()}")
            response.raise_for_status()
        
        data = response.json()
        all_activities.extend(data.get('data', []))
        url = data.get('paging', {}).get('next')

    return all_activities

def write_to_google_sheets(data):
    # Authenticate and create the service for Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
    client = gspread.authorize(creds)
    
    # Open the spreadsheet
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    
    # Clear existing data
    sheet.clear()
    
    # Write data to Google Sheets
    sheet.update('A1', data)

def process_ad_activities(ad_activities):
    data_to_write = []
    headers = ['Actor ID', 'Actor Name', 'Application ID', 'Application Name', 'Date/Time in Timezone', 'Event Time', 'Event Type', 'Extra Data', 'Object ID', 'Object Name', 'Object Type', 'Translated Event Type']
    data_to_write.append(headers)
    
    for activity in ad_activities:
        row = [
            activity.get('actor_id'),
            activity.get('actor_name'),
            activity.get('application_id'),
            activity.get('application_name'),
            activity.get('date_time_in_timezone'),
            activity.get('event_time'),
            activity.get('event_type'),
            activity.get('extra_data'),
            activity.get('object_id'),
            activity.get('object_name'),
            activity.get('object_type'),
            activity.get('translated_event_type')
        ]
        data_to_write.append(row)
    
    return data_to_write

def main(start_time, end_time):
    ad_activities = get_ad_activities(start_time, end_time)
    processed_data = process_ad_activities(ad_activities)
    write_to_google_sheets(processed_data)

if __name__ == "__main__":
    # Define the time frame for the ad activities
    start_time = datetime(2024, 6, 8)  # Replace with your desired start time
    end_time = datetime(2024, 6, 7)  # Replace with your desired end time
    
    main(start_time, end_time)
