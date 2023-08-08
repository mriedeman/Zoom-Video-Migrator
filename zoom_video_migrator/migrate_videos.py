from zoom_video_migrator.jwt_token import generate_jwt_token
from datetime import datetime, timedelta
import io
import os
import requests
import json
import os
import jwt
from datetime import datetime, timedelta
from zoomus import ZoomClient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from dotenv import load_dotenv

def upload_video_to_google_drive(download_url, filename):
    """Uploads a single video to Google Drive given the download_url and filename"""

    # Load environment variables from .env file
    load_dotenv()

    # Google Drive API credentials
    if 'GOOGLE_AUTH_FILE' not in os.environ:
        raise ValueError('GOOGLE_AUTH_FILE environment variable not set')
    google_api_credentials = os.environ.get('GOOGLE_AUTH_FILE')
    creds = service_account.Credentials.from_service_account_file(google_api_credentials)

    if 'GOOGLE_PARENT_FOLDER_ID' not in os.environ:
        raise ValueError('GOOGLE_PARENT_FOLDER_ID environment variable not set')
    parent_folder_id = os.environ.get('GOOGLE_PARENT_FOLDER_ID')

    drive_service = build('drive', 'v3', credentials=creds)

    # Upload video file to Google Drive
    file_metadata = {'name': filename, 'parents': [parent_folder_id]}
    file = None
    try:
        token = generate_jwt_token()
        response = requests.get(download_url + "?access_token=" + token, stream=True)
        with io.BytesIO() as video_bytes:
            # Download video data in chunks and write to BytesIO object
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    video_bytes.write(chunk)
            video_bytes.seek(0)

            # Create a MediaIoBaseUpload object using the video_bytes
            media = MediaIoBaseUpload(video_bytes, mimetype='video/mp4', chunksize=1024 * 1024, resumable=True)

            # Upload video file to Google Drive
            file_metadata = {'name': filename, 'parents': [parent_folder_id]}
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
    except HttpError as error:
        print(f'An error occurred: {error}')
    
    print(f"{filename} uploaded successfully to Google Drive with a File ID of: {file.get('id')}.")

def migrate_videos_to_google_drive(json_file, first_name, last_name, user_id):
    """Migrates All The Videos in a Single JSON File to Google Drive"""

    with open(json_file) as f:
        data = json.load(f)

    for meeting in data['meetings']:
        for recording in meeting['recording_files']:
            if recording['file_type'] == "MP4":

                download_url = recording['download_url']
                date_string = recording['recording_start']
                dt_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
                timestamp_string = dt_object.strftime('%Y-%m-%d_%H-%M-%S')
                filename = f"{first_name} {last_name} {user_id} {timestamp_string}"

                upload_video_to_google_drive(download_url, filename)