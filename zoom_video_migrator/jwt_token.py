from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta

def generate_jwt_token():
# Load environment variables from .env file
    load_dotenv()

    # Get API credentials from environment variables
    api_key = os.environ.get('ZOOM_API_KEY')
    if not api_key:
        raise ValueError('ZOOM_API_KEY environment variable not set')

    api_secret = os.environ.get('ZOOM_API_SECRET')
    if not api_secret:
        raise ValueError('ZOOM_API_KEY environment variable not set')

    payload = {
        'iss': api_key,
        'exp': datetime.utcnow() + timedelta(minutes=10)
    }

    token = jwt.encode(payload, api_secret)
    return token

