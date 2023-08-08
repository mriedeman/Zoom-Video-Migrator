from zoom_video_migrator.jwt_token import generate_jwt_token
import json
import requests
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta


def legacy_dates():
    start_date_str = "2021-01-01" #first zoom recording was 2021-01-03
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    now = datetime.now()

    date_ranges = []
    while start_date < now:
        # Get the first day of the current month
        start_of_month = datetime(start_date.year, start_date.month, 1)

        #Get the last day of the current month
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        date_ranges.append((start_of_month.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d')))

        start_date = end_of_month + timedelta(days=1)

    #print("Created a tupled list of FROM and TO parameters for the Zoom API Query")
    return date_ranges




def collect_legacy_data():
    #get user ids for API call "/users/{user_id}/recordings"
    with open('./api_data/users/users.json') as f:
        users = json.load(f)


    #Collect all recording data, one user at a time
    for user in users['users']:
        user_first_name = user['first_name']
        user_last_name = user['last_name']
        user_id = user['id']
        print(f'Collecting recording results for user {user_first_name} {user_last_name} {user_id}')
        
        for start, end in legacy_dates():

            #Avoid sending API query with end date greater than today's date
            now = datetime.now()
            if datetime.strptime(end, '%Y-%m-%d') > now:
                break
            
            # API access
            base_url = "https://api.zoom.us/v2"
            token = generate_jwt_token()
            headers = {'Authorization': f'Bearer {token}'}
            url = base_url + f"/users/{user_id}/recordings"
            params = { "from": start,
                    "to": end}
            
            response = requests.get(url, headers=headers, params = params)
            recordings_data = response.json()
            
            # Keep making API requests until all pages are collected
            next_token = recordings_data.get('next_page_token')
            while next_token:
                
                url = base_url + f"/users/{user_id}/recordings"
                params = { "from": start, "to": end, "next_page_token": next_token}
                response = requests.get(url, headers=headers, params=params)
                next_page_data = response.json()
                recordings_data['meetings'] += next_page_data['meetings']
                next_token = next_page_data.get('next_page_token')
                if next_token == recordings_data.get('next_page_token'):
                    break
                recordings_data['next_page_token'] = next_token
                
            #print(f'Collecting recording results for user {user_first_name} {user_last_name} from {start} to {end}')

            #Store data
            directory = f'api_data/legacy_recordings_data/{user_first_name} {user_last_name} {user_id}'
            filename = f'api_data/legacy_recordings_data/{user_first_name} {user_last_name} {user_id}/{start} to {end}.json'

            if not os.path.exists(directory):
                os.makedirs(directory)

            
            with open(filename, 'w') as f:
                json.dump(recordings_data, f)

    print(f"DATA COLLECTION COMPLETE AT {datetime.now()}")



def main():
    collect_legacy_data()
    
if __name__ == '__main__':
    main()