# Zoom To Google Drive Video Migration

## Description
This Python package migrates Zoom video recordings from the Zoom cloud to Google Drive. It uses the Zoom API to retrieve a list of recordings within a specified date range, downloads the recordings to a local directory, and then uploads them to a Google Drive folder. The package includes functionality for batch processing a range of dates.


## Project Directory:

```
zoom/
├── api_data/
│   ├── legacy_recordings_data/
│   │   ├── Firstname1 Lastname1 Userid1/
│   │   │   ├── 2021-06-01 to 2021-06-07.json
│   │   │   ├── 2021-06-08 to 2021-06-14.json
│   │   │   ├── ...
│   │   ├── Firstname2 Lastname2 Userid2/
│   │   │   ├── ...
│   │   ├── ...
│   ├── users/
│   │   ├── users.json
|   ├── weekly_recordings/
│   │   ├── Firstname1 Lastname1 Userid1/
│   │   │   ├── 2021-06-01 to 2021-06-07.json
│   │   │   ├── 2021-06-08 to 2021-06-14.json
│   │   │   ├── ...
│   │   ├── Firstname2 Lastname2 Userid2/
│   │   │   ├── ...
├── zoom_video_migrator/
│   ├── __init__.py
│   ├── batch_job.py
│   ├── collect_legacy_data.py
│   ├── collect_weekly_data.py
│   ├── jwt_token.py
│   ├── migrate_videos.py
│   ├── update_users.py
│   └── ...
├── .env
├── requirements.txt
└── setup.py
```


## Installation
1. Clone the Git repository that contains the package to a local directory on your computer.

*Note: Virtual Environments*
- I used anaconda to create my virtual environment. The suggestion below can be used if you don't have anaconda installed.

2. Create a virtual environment 

```
python3 -m venv venv
```

3. Activate the virtual environment by running this command

```
source venv/bin/activate
```

4. Install the package's dependencies using pip by running the following command:
```
pip install -r requirements.txt
```

5. Set the necessary environment variables by creating a .env file in the root directory of the repository. The .env file should contain the following environment variables:
``` 
ZOOM_API_KEY=<your Zoom API key>
ZOOM_API_SECRET=<your Zoom API secret>
GOOGLE_AUTH_FILE=<path to your Google Drive API credentials JSON file>
GOOGLE_PARENT_FOLDER_ID=<the ID of the Google Drive folder where you want to upload the videos>
```

*Note: API Navigation*

- To obtain GOOGLE_AUTH_FILE one must create a Service account in Google Cloud Console and generate the json file.
- Before uploading files to the GOOGLE_PARENT_FOLDER be sure to share access to the folder with the email associated with the Google Clound Console Service Account.
- Create a JWT APP https://developers.zoom.us/docs/ to generate an API Key and Secret so that a JWT Token can be generated.


6. Create shell scripts to collect legacy data. The general data workflow is as follows:

    a.  Update the users data (run to include new users added to the system):

```
#!/bin/bash
source venv/bin/activate
cd zoom_video_migrator
python update_users.py 
```
b. Update the download_urls in the legacy data (they expire every 24 hours):
```
#!/bin/bash
source venv/bin/activate
cd zoom_video_migrator
python collect_legacy_data.py 
```

c. Run the batch_job function with a start date of "2022-01-01" and an end date of "2022-01-31" Note: Dates must be the first and last of the month and match the file names in the "legacy_recordings_data" folder:
```
#!/bin/bash
source venv/bin/activate
cd zoom_video_migrator
python batch_job.py --start-date 2022-01-01 --end-date 2022-01-31
```

7. Create shell scripts to collect new weekly recording data

*Note: Collecting the Latest Weekly Recording Data*

- Zoom Cloud Recording has been disabled for the past few months so there will be no weekly data until the service is enabled again.
    
    a.  Update the users data (run to include new users added to the system):

```
#!/bin/bash
source venv/bin/activate
cd zoom_video_migrator
python update_users.py 
```
b. Update the download_urls in the weekly data (they expire every 24 hours):
```
#!/bin/bash
source venv/bin/activate
cd zoom_video_migrator
python collect_weekly_data.py 
```

c. Run a batch job on the previous week's recording data. 

*Note: when no dates are included in the batch_job.py call, the previous weeks data are automatically searched through in the api_data/weekly_recordings folder*
```
#!/bin/bash
source venv/bin/activate
cd zoom_video_migrator
python batch_job.py 
```
## Alternate Setup
If running the commands directly instead of using a bash script:
- activate your python virtual environment
- install requirements ```pip install -r requirements.txt```
- navigate to the project directory ```/zoom``` and use these commands:

1. Update the Users data in api_data/users/users.json
```
python -m zoom_video_migrator.update_users
```

2. Update the Legacy data in api_data/legacy_recordings_data/{user}/
```
python -m zoom_video_migrator.collect_legacy_data
```

3. Update the weekly data in api_data/weekly_recordings/{user}/
```
python -m zoom_video_migrator.collect_weekly_data
```

4. Run a batch job for previous week's recording files
```
python -m zoom_video_migrator.batch_job
```

5. Run a batch job for specific date range. Date ranges must be 1 month and match the file name in api_data/legacy_recordings_data/
```
python -m zoom_video_migrator.batch_job --start-date "2021-06-01" --end-date "2021-06-30"
```


*Batch Jobs*

Batch Jobs were created to shorten the runtime of the data transfer script. The input parameter dates are associated with the file names in the legacy_recordings_data folder, therefore the start date should always be the first of the month e.g. "2021-01-01" and the end date should always be the last of the month e.g. "2021-1-31" in "YYYY-MM-DD" format wrapped in quotes.
