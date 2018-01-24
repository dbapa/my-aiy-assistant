'''
import pprint
import sys
from apiclient.discovery import build

service = build('books', 'v1', developerKey=api_key)
request = service.volumes().list(source='public', q='android')
'''

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'People API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'people.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google People API.

    Creates a Google People API service object and outputs the name if
    available of 10 connections.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('people', 'v1', http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')

    print('List 10 connection names')
    results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1,
            personFields='names,emailAddresses,phoneNumbers').execute()
    connections = results.get('connections', [])
    name=''
    phoneNo= ''
    for person in connections:
        names = person.get('names', [])
        if len(names) > 0:
            name = names[0].get('displayName')
        print(person)
        phoneNos = person.get('phoneNumbers', [])

        if len(phoneNos) > 0:
            phoneNo = phoneNos[0].get('value')
        print ('Name:',name,' Ph:',phoneNo)


if __name__ == '__main__':
    main()