from zoomus import ZoomClient
import os
import json
from datetime import datetime
from dotenv import load_dotenv

def update_users():

    load_dotenv()
    api_key = os.environ.get('ZOOM_API_KEY')
    if not api_key:
        raise ValueError('ZOOM_API_KEY environment variable not set')

    api_secret = os.environ.get('ZOOM_API_SECRET')
    if not api_secret:
        raise ValueError('ZOOM_API_SECRET environment variable not set')

    zoom = ZoomClient(api_key=api_key, api_secret=api_secret)

    users_response = zoom.user.list().json()

    filename = 'api_data/users/users.json'
    with open(filename, 'w') as f:
        json.dump(users_response, f)

    print(f"Updated the {filename} to include any new users on {datetime.now()}")

def main():
    update_users()

if __name__ == '__main__':
    main()