from google_auth_oauthlib.flow import InstalledAppFlow

def ytmusic_oauth():
    try:
        scope = ['https://www.googleapis.com/auth/youtube']
        flow = InstalledAppFlow.from_client_secrets_file('ProjectLibrary/client_secret.json', scope)

        credentials = flow.run_local_server(port=52736, access_type='offline', prompt='consent')

        print('token is successfully retrieved')
        return credentials

    except:
        return None

# ytmusic_oauth()