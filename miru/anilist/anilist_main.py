import requests
import os
import json
from dotenv import load_dotenv
from miru.anilist.setMetadata import setMetadata
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

def FetchAnilistEntry(anime_obj) -> None:
    """
        Multi layered function to sync data obtained from the anilist api
    """

    # if anime_obj.anilist_id is None:
    #     print('no anilist id given')
    #     return

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
        setMetadata(anime_obj, data)

        
    except requests.Timeout:
        print('Error: Anilist API timed out')
        