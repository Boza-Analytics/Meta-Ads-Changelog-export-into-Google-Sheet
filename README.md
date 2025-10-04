# Meta (Facebook) Ad Activities to Google Sheets - Documentation

## Overview
This Python script fetches ad account activity logs from Meta's (Facebook) Marketing API and exports them to Google Sheets. It captures all account changes, modifications, and events within a specified timeframe for audit and tracking purposes.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Configuration](#configuration)
3. [Features](#features)
4. [Script Workflow](#script-workflow)
5. [Functions Reference](#functions-reference)
6. [Meta API Integration](#meta-api-integration)
7. [Google Sheets Integration](#google-sheets-integration)
8. [Data Fields](#data-fields)
9. [Error Handling](#error-handling)
10. [Usage Examples](#usage-examples)

---

## Requirements

### Python Packages
```bash
pip install requests gspread oauth2client
```

**Required Libraries:**
- `requests` - HTTP requests to Meta API
- `gspread` - Google Sheets API wrapper
- `oauth2client` - Google OAuth authentication
- `json` - JSON data handling
- `datetime` - Date/time operations

### API Access
- **Meta Business Account** with ad account access
- **Meta App** with Marketing API permissions
- **Access Token** with `ads_read` permission
- **Google Cloud Platform** service account with Sheets API enabled

---

## Configuration

### Meta API Credentials

```python
access_token = ''  # Your Meta access token
ad_account_id = ''  # Format: act_XXXXXXXXXX
meta_url = f"https://graph.facebook.com/v20.0/{ad_account_id}/activities"
```

**Getting Access Token:**
1. Go to Meta for Developers
2. Create or select your app
3. Navigate to Tools > Graph API Explorer
4. Generate token with `ads_read` permission
5. Copy the access token

**Ad Account ID Format:**
- Find in Meta Ads Manager URL
- Format: `act_1234567890123456`
- Include the `act_` prefix

### Google Sheets Credentials

```python
SERVICE_ACCOUNT_FILE = ''  # Path to JSON key file
SPREADSHEET_ID = ''  # From Google Sheets URL
SHEET_NAME = 'Sheet1'  # Target worksheet name
```

**Google Sheets ID Location:**
```
https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
```

---

## Features

### 1. Comprehensive Activity Tracking
- Captures all ad account changes
- Records user actions and modifications
- Tracks campaign, ad set, and ad changes
- Documents budget adjustments
- Logs status changes (pause/resume)

### 2. Pagination Support
- Automatically handles paginated responses
- Fetches all activities in date range
- No manual intervention required

### 3. Detailed Event Data
- Actor information (who made changes)
- Application details (where changes originated)
- Timestamps (when changes occurred)
- Object information (what was changed)
- Event type classification

### 4. Google Sheets Export
- Clears previous data
- Writes structured data with headers
- Single sheet update operation
- Ready for analysis and reporting

### 5. Debugging Output
- Prints request URLs
- Shows response status codes
- Displays API responses
- Helpful for troubleshooting

---

## Script Workflow

### Execution Flow

```
1. Define Time Range
   ↓
2. Call get_ad_activities()
   ├─ Build API request
   ├─ Fetch first page
   ├─ Loop through pagination
   └─ Collect all activities
   ↓
3. Call process_ad_activities()
   ├─ Create headers
   ├─ Extract activity fields
   └─ Format as 2D array
   ↓
4. Call write_to_google_sheets()
   ├─ Authenticate
   ├─ Clear existing data
   └─ Write new data
   ↓
5. Complete
```

---

## Functions Reference

### `get_ad_activities(start_time, end_time)`
Fetches ad activity logs from Meta API.

**Parameters:**
- `start_time` (datetime): Start of date range
- `end_time` (datetime): End of date range

**Returns:**
- `list`: Array of activity dictionaries

**Process:**
1. Converts datetime to ISO 8601 format
2. Builds API request with parameters
3. Handles pagination automatically
4. Collects all activities across pages
5. Returns complete activity list

**API Request Example:**
```python
params = {
    'access_token': 'YOUR_TOKEN',
    'since': '2024-06-08T00:00:00',
    'until': '2024-06-07T23:59:59',
    'fields': 'actor_id,actor_name,...'
}
```

**Pagination Handling:**
```python
while url:
    response = requests.get(url, params=params)
    data = response.json()
    all_activities.extend(data.get('data', []))
    url = data.get('paging', {}).get('next')  # Get next page URL
```

---

### `process_ad_activities(ad_activities)`
Converts raw API data to spreadsheet format.

**Parameters:**
- `ad_activities` (list): Raw activity data from API

**Returns:**
- `list`: 2D array ready for Google Sheets

**Process:**
1. Creates header row
2. Iterates through each activity
3. Extracts relevant fields
4. Builds data rows
5. Returns formatted array

**Output Structure:**
```python
[
    ['Actor ID', 'Actor Name', ...],  # Header row
    ['123456', 'John Doe', ...],      # Data row 1
    ['789012', 'Jane Smith', ...]     # Data row 2
]
```

---

### `write_to_google_sheets(data)`
Writes data to Google Sheets.

**Parameters:**
- `data` (list): 2D array of data to write

**Process:**
1. Authenticates with Google API
2. Opens target spreadsheet
3. Clears existing content
4. Writes new data starting at A1

**Authentication:**
```python
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE,
    scope
)
client = gspread.authorize(creds)
```

---

### `main(start_time, end_time)`
Main execution function.

**Parameters:**
- `start_time` (datetime): Report start date/time
- `end_time` (datetime): Report end date/time

**Workflow:**
1. Fetches ad activities
2. Processes data
3. Writes to Google Sheets

---

## Meta API Integration

### API Version
**Current:** v20.0
```python
meta_url = "https://graph.facebook.com/v20.0/{ad_account_id}/activities"
```

**Note:** Update version number as Meta releases new API versions.

### API Endpoint
**Activities Endpoint:**
```
GET /{ad-account-id}/activities
```

**Purpose:** Returns activity history for the ad account.

### Available Fields

```python
fields = [
    'actor_id',                    # User/app ID that performed action
    'actor_name',                  # Name of actor
    'application_id',              # App ID if action via app
    'application_name',            # App name
    'date_time_in_timezone',       # Localized timestamp
    'event_time',                  # Unix timestamp
    'event_type',                  # Type of event
    'extra_data',                  # Additional event data
    'object_id',                   # ID of modified object
    'object_name',                 # Name of modified object
    'object_type',                 # Type (campaign, ad set, ad)
    'translated_event_type'        # Human-readable event type
]
```

### Common Event Types

| Event Type | Description |
|------------|-------------|
| `create` | New object created |
| `update` | Object modified |
| `delete` | Object deleted |
| `pause` | Object paused |
| `resume` | Object resumed |
| `budget_change` | Budget modified |
| `bid_change` | Bid strategy changed |
| `status_change` | Status modified |

### Rate Limits

**Meta API Rate Limits:**
- **Standard:** 200 calls per hour per user
- **App-level:** Varies by app tier
- **Account-level:** Based on ad spend

**Best Practices:**
- Limit time ranges to reduce API calls
- Use pagination efficiently
- Cache results when possible
- Handle rate limit errors gracefully

---

## Google Sheets Integration

### Setup Steps

1. **Create Service Account:**
   - Go to Google Cloud Console
   - Enable Google Sheets API
   - Create service account
   - Download JSON key

2. **Share Spreadsheet:**
   - Open target Google Sheet
   - Click "Share"
   - Add service account email
   - Grant "Editor" access

3. **Configure Script:**
```python
SERVICE_ACCOUNT_FILE = 'path/to/service-account.json'
SPREADSHEET_ID = 'your_spreadsheet_id'
SHEET_NAME = 'Sheet1'
```

### Data Writing Method

**Clear and Replace:**
```python
sheet.clear()           # Remove all existing data
sheet.update('A1', data)  # Write from cell A1
```

**Alternative - Append:**
```python
# If you want to preserve existing data
sheet.append_rows(data, value_input_option='RAW')
```

---

## Data Fields

### Output Columns

| Column | Description | Example |
|--------|-------------|---------|
| **Actor ID** | User or app ID that made change | `1234567890` |
| **Actor Name** | Name of person/app | `John Doe` |
| **Application ID** | ID of app used (if applicable) | `9876543210` |
| **Application Name** | Name of application | `Meta Business Suite` |
| **Date/Time in Timezone** | Localized timestamp | `2024-06-08 14:30:45 PDT` |
| **Event Time** | Unix timestamp | `1686248445` |
| **Event Type** | Action performed | `update` |
| **Extra Data** | Additional JSON details | `{"old_value": "100", "new_value": "150"}` |
| **Object ID** | ID of changed object | `23848234234` |
| **Object Name** | Name of object | `Summer Sale Campaign` |
| **Object Type** | Type of object | `campaign` |
| **Translated Event Type** | Human-readable type | `Campaign Updated` |

---

## Error Handling

### API Errors

**Error Detection:**
```python
if response.status_code != 200:
    print(f"Error: {response.content.decode()}")
    response.raise_for_status()
```

**Common HTTP Errors:**

| Status Code | Meaning | Solution |
|-------------|---------|----------|
| `400` | Bad Request | Check parameters and date format |
| `401` | Unauthorized | Verify access token is valid |
| `403` | Forbidden | Check permissions on ad account |
| `404` | Not Found | Verify ad account ID is correct |
| `429` | Rate Limited | Implement retry with backoff |
| `500` | Server Error | Retry request after delay |

### Authentication Errors

**Invalid Token:**
```json
{
  "error": {
    "message": "Invalid OAuth access token",
    "type": "OAuthException",
    "code": 190
  }
}
```

**Solution:** Generate new access token from Meta for Developers.

### Google Sheets Errors

**Common Issues:**
- **Permission Denied:** Service account needs editor access
- **Spreadsheet Not Found:** Check SPREADSHEET_ID
- **Worksheet Not Found:** Verify SHEET_NAME exists
- **Quota Exceeded:** Check Google API quotas

---

## Usage Examples

### Example 1: Last 7 Days
```python
from datetime import datetime, timedelta

start_time = datetime.now() - timedelta(days=7)
end_time = datetime.now()

main(start_time, end_time)
```

### Example 2: Specific Date Range
```python
start_time = datetime(2024, 6, 1)   # June 1, 2024
end_time = datetime(2024, 6, 30)    # June 30, 2024

main(start_time, end_time)
```

### Example 3: Yesterday's Activities
```python
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.replace(hour=0, minute=0, second=0)
end_time = yesterday.replace(hour=23, minute=59, second=59)

main(start_time, end_time)
```

### Example 4: Current Month
```python
from datetime import datetime

now = datetime.now()
start_time = now.replace(day=1, hour=0, minute=0, second=0)
end_time = now

main(start_time, end_time)
```

---

## Important Notes

### ⚠️ Date Range Issue in Code

**Current Code:**
```python
start_time = datetime(2024, 6, 8)
end_time = datetime(2024, 6, 7)  # ERROR: End before start!
```

**This is incorrect!** End time should be after start time.

**Corrected:**
```python
start_time = datetime(2024, 6, 7)   # June 7
end_time = datetime(2024, 6, 8)     # June 8
```

### Time Zone Considerations

**ISO 8601 Format:**
```python
start_time.isoformat()
# Returns: '2024-06-08T00:00:00'
```

**With Timezone:**
```python
from datetime import timezone

start_time = datetime(2024, 6, 8, tzinfo=timezone.utc)
```

---

## Automation

### Schedule with Cron (Linux/Mac)

```bash
# Run daily at 1 AM
0 1 * * * /usr/bin/python3 /path/to/meta_activities.py
```

### Schedule with Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 1:00 AM
4. Action: Start a program
   - Program: `python.exe`
   - Arguments: `C:\path\to\meta_activities.py`

### Dynamic Date Range for Automation

```python
if __name__ == "__main__":
    # Yesterday's activities
    yesterday = datetime.now() - timedelta(days=1)
    start_time = yesterday.replace(hour=0, minute=0, second=0)
    end_time = yesterday.replace(hour=23, minute=59, second=59)
    
    main(start_time, end_time)
```

---

## Security Best Practices

### 1. Protect Access Tokens
```python
# Use environment variables
import os
access_token = os.getenv('META_ACCESS_TOKEN')
```

### 2. Secure Service Account Keys
- Store outside project directory
- Use restrictive file permissions (600)
- Never commit to version control
- Rotate periodically

### 3. Add to .gitignore
```
# Service account keys
*.json

# Environment files
.env
```

---

## Debugging

### Enable Verbose Output

The script already includes debugging output:
```python
print(f"Request URL: {response.url}")
print(f"Response Status Code: {response.status_code}")
print(f"Response Content: {response.content.decode()}")
```

### Test API Connection

```python
# Test basic API access
response = requests.get(
    f"https://graph.facebook.com/v20.0/me",
    params={'access_token': access_token}
)
print(response.json())
```

### Verify Ad Account Access

```python
# Check ad account permissions
response = requests.get(
    f"https://graph.facebook.com/v20.0/{ad_account_id}",
    params={
        'access_token': access_token,
        'fields': 'id,name,account_status'
    }
)
print(response.json())
```

---

## Troubleshooting

### No Activities Returned

**Possible Causes:**
1. No activities in date range
2. Incorrect date format
3. Permissions issue
4. Wrong ad account ID

**Solution:**
```python
# Add debug output
activities = get_ad_activities(start_time, end_time)
print(f"Total activities found: {len(activities)}")
```

### Google Sheets Not Updating

**Check:**
1. Service account has editor access
2. Sheet name matches exactly (case-sensitive)
3. Spreadsheet ID is correct
4. No API quota issues

---

## License

Proprietary - For use with Meta Marketing API integration only.

---

## Support

For issues:
1. Check debug output in console
2. Verify access token validity (they expire)
3. Confirm ad account ID format
4. Test Google Sheets connection separately
5. Review Meta API changelog for breaking changes
