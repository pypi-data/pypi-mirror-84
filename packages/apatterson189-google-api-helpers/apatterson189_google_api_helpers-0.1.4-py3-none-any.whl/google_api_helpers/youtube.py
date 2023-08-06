from . import auth
from googleapiclient.discovery import build


def _getService(scopes):
    creds = auth.getCreds(scopes)
    return build('youtube', 'v3', credentials=creds)


def getReadonlyService():
    return _getService(['https://www.googleapis.com/auth/spreadsheets.readonly'])


def getService():
    return _getService(['https://www.googleapis.com/auth/spreadsheets'])
