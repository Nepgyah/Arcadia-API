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
    query Media($mediaId: Int) {
        Media(id: $mediaId) {
            title {
                english
                native
                romaji
            }
            description
            synonyms
            season
            seasonYear
            format
            status
            episodes
            hashtag
            bannerImage
            coverImage {
                large
            }
            genres

            startDate {
                day
                month
                year
            }
            endDate {
                day
                month
                year
            }
            streamingEpisodes {
                site
                thumbnail
                title
            }
            characters {
                edges {
                    role
                    node {
                        name {
                            first
                            full
                            last
                        }
                        image {
                            large
                        }
                    }
                    voiceActors {
                        name {
                            first
                            last
                        }
                        image {
                            large
                        }
                    }
                }
            }
        }
    }
    '''

    variables = {'mediaId': anilist_id}

    try:
        print(f"Attempting to call anilist api for media id: {anilist_id}")
        response = requests.post(
            anilist_api_url,
            json={'query': query, 'variables': variables },
            timeout=20
        )
        if response.status_code != 200:
            print('Error from anilist api')

        data = response.json().get('data').get('Media')
        return data

    except requests.Timeout:
        print('Error: Anilist API timed out')