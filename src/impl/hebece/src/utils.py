import base64
import json
import uuid
from datetime import datetime, timedelta

def encodebase64(data):
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def decodebase64(data):
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")

def get_tenant_from_jwt(token):
    try:
        # Split the JWT into parts
        header, payload, signature = token.split('.')

        # Decode the payload from Base64
        # Add padding 
        payload += '=' * (-len(payload) % 4)
        decoded_payload = base64.urlsafe_b64decode(payload).decode('utf-8')

        # Parse the payload as JSON
        payload_json = json.loads(decoded_payload)

        # Return the tenant
        return payload_json.get('tenant')
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        print(f"Error decoding JWT: {e}")
        return None

def getCurrentTimestamp():
    now = datetime.now()
    Timestamp = int(now.timestamp())

    return Timestamp

def getRandomIdentifier():
    ruuid = str(uuid.uuid4())

    return ruuid

def get_current_week():
    # Get today's date
    today = datetime.today()
    # Calculate the start of the week (Monday)
    start_of_week = today - timedelta(days=today.weekday())
    # Calculate the end of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)

    # Return the dates as formatted strings
    return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')