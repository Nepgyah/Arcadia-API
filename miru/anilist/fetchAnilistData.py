import os
from pathlib import Path
import requests
import os
import json
BASE_DIR = Path(__file__).resolve().parent

def FetchAnilistData(anilist_id):
    anilist_api_url = os.environ.get('ANILIST_API')
    if anilist_api_url is None:
        print('ANILIST_API env key not found')
        return
    
    query = '''
    query Query($mediaId: Int) {
        Media(id: $mediaId) {
            description
            title {
                english
                native
                romaji
            }
        }
    }
    '''

    variables = {'mediaId': 182255}

    try:
        # print('Attempting to call anilist api')
        # response = requests.post(
        #     anilist_api_url,
        #     json={'query': query, 'variables': variables },
        #     timeout=20
        # )
        # if response.status_code != 200:
        #     print('Error from anilist api')
        
        with open(BASE_DIR / 'frieren.json', 'r', encoding='utf-8') as f:
            response = json.load(f)
        
        # data = response.json().get('data').get('Media')
        data = response.get('data').get('Media')
        return data

        
    except requests.Timeout:
        print('Error: Anilist API timed out')