from zoom_video_migrator.jwt_token import generate_jwt_token
from datetime import datetime, timedelta
import json
import requests
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta


def get_previous_week_dates():
    """Collects the start and end dates for the previous week"""
    today = datetime.now().date() - timedelta(days=7)
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def collect_weekly_data(start_date=None, end_date=None):
    """Collects weekly recording data. If no date is specified, it collects the most recent weeks data. To specify a data enter it as a string in "YYYY-MM-DD" format"""
    if start_date is None or end_date is None:
        # Get the current week's start and end dates
        start_date, end_date = get_previous_week_dates()
    
    
    #get user ids for API call "/users/{user_id}/recordings"
    with open('./api_data/users/users.json') as f:
        users = json.load(f)


    #Collect all recording data, one user at a time
    for user in users['users']:

        user_first_name = user['first_name']
        user_last_name = user['last_name']
        user_id = user['id']
        print(f'Collecting recording results for user {user_first_name} {user_last_name} {user_id}')


        #Avoid sending API query with end date greater than today's date
        now = datetime.now()
        if datetime.strptime(end_date, '%Y-%m-%d') > now:
            break

        # API access
        base_url = "https://api.zoom.us/v2"
        token = generate_jwt_token()
        headers = {'Authorization': f'Bearer {token}'}
        url = base_url + f"/users/{user_id}/recordings"
        params = { "from": start_date,
                "to": end_date}

        response = requests.get(url, headers=headers, params = params)
        recordings_data = response.json()

        # Keep making API requests until all pages are collected
        next_token = recordings_data.get('next_page_token')
        while next_token:

            url = base_url + f"/users/{user_id}/recordings"
            params = { "from": start_date, "to": end_date, "next_page_token": next_token}
            response = requests.get(url, headers=headers, params=params)
            next_page_data = response.json()
            recordings_data['meetings'] += next_page_data['meetings']
            next_token = next_page_data.get('next_page_token')
            if next_token == recordings_data.get('next_page_token'):
                break
            recordings_data['next_page_token'] = next_token

        #print(f'Collecting recording results for user {user_first_name} {user_last_name} from {start} to {end}')

        #Store data
        directory = f'api_data/weekly_recordings/{user_first_name} {user_last_name} {user_id}'
        filename = f'api_data/weekly_recordings/{user_first_name} {user_last_name} {user_id}/{start_date} to {end_date}.json'

        if not os.path.exists(directory):
            os.makedirs(directory)


        with open(filename, 'w') as f:
            json.dump(recordings_data, f)

    print(f"DATA COLLECTION COMPLETE AT {datetime.now()}")



def main():
    collect_weekly_data()

if __name__ == "__main__":
    main()