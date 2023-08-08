from zoom_video_migrator.collect_weekly_data import get_previous_week_dates
from zoom_video_migrator.migrate_videos import upload_video_to_google_drive, migrate_videos_to_google_drive
import os
import argparse

def batch_job(start_date=None, end_date=None):
    """Selectively Iterates Through The Recording Directory to Batch The Data Transfer"""
    
    if start_date is None or end_date is None:
        # Get the current week's start and end dates
        start_date, end_date = get_previous_week_dates()
        recording_directory = "./api_data/weekly_recordings"
    else:
        recording_directory = "./api_data/legacy_recordings_data"
    for user_folder in os.listdir(recording_directory):
        path = os.path.isdir(os.path.join(recording_directory, user_folder))
        if path:
                for file_name in os.listdir(os.path.join(recording_directory, user_folder)):
                    if file_name.startswith(start_date) and file_name.endswith(end_date + ".json"):
                            
                            file_path = os.path.join(recording_directory, user_folder, file_name)
                            first_name = user_folder.split(" ")[0]
                            last_name = user_folder.split(" ")[1]
                            user_id = user_folder.split(" ")[2]

                            print(file_path)
                            migrate_videos_to_google_drive(file_path, first_name, last_name, user_id)

    print(F"FINISHED BATCH JOB FOR '{start_date} to {end_date}.json' FILES")


def main():
    parser = argparse.ArgumentParser(description='Zoom video migration tool')
    parser.add_argument('--start-date', help='Start date of the date range (YYYY-MM-DD format)', required=False)
    parser.add_argument('--end-date', help='End date of the date range (YYYY-MM-DD format)', required=False)
    args = parser.parse_args()
    batch_job(args.start_date, args.end_date)

if __name__ == '__main__':
    main()