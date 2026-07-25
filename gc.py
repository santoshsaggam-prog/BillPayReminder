from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "config" / "token.json"
CREDENTIALS_FILE = BASE_DIR / "config" / "credentials.json"


def get_calendar_service():
    """Authenticate with Google Calendar and return a service client."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    "credentials.json not found. Download it from Google Cloud Console "
                    "and place it in the same folder as this script."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with TOKEN_FILE.open("w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def list_events(days: int = 7):
    """Return events from the next N days in the user's primary calendar."""
    service = get_calendar_service()

    now = datetime.utcnow().replace(microsecond=0)
    time_min = now.isoformat() + "Z"
    time_max = (now + timedelta(days=days)).isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])
    return events


if __name__ == "__main__":
    for event in list_events(days=30):
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f"{start} :: {event.get('summary', 'No title')}")
