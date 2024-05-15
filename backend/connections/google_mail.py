import json
from typing import Any, Dict, List, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Gmail:
    def __init__(self, credentials: dict, scope: list, token: list) -> None:
        self.credentials = credentials
        self.scopes = scope
        self.token = token

    def login(self):
        creds = None
        if self.token:
            creds = Credentials.from_authorized_user_info(
                self.token, self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    self.credentials, self.scopes
                )

                creds = flow.run_local_server(port=0)

            self.token = json.loads(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    # def fetch_emails(self):
    #     service.users().messages().list(userId="garg.arnav77@gmail.com", q="after:2024-03-29").execute()
