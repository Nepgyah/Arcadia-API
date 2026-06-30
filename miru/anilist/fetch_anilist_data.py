import os
import logging
from pathlib import Path
import requests

# Provides the name of the py module as a dotted path
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

def fetch_anilist_data(anilist_id):
    anilist_api_url = os.environ.get('ANILIST_API')

    if anilist_api_url is None:
        logger.critical('Anilist api url not found in .env file')
        return None
    
    query = '''
    query Media($mediaId: Int, $language: StaffLanguage) {
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
                    voiceActors(language: $language) {
                        name {
                            first
                            last
                        }
                        image {
                            large
                        }
                        languageV2
                    }
                }
            }
            studios {
                edges {
                    node {
                        isAnimationStudio
                        name
                    }
                }
            }
            rankings {
                format
                rank
                context
                type
                year
                allTime
                season
            }
        }
    }
    '''

    variables = {'mediaId': anilist_id, 'language': "JAPANESE"}

    try:
        response = requests.post(
            anilist_api_url,
            json={'query': query, 'variables': variables },
            timeout=20
        )
        if response.status_code != 200:
            logger.warning('Anilist api returned a non 200 code')

        data = response.json().get('data').get('Media')
        return data

    except requests.Timeout:
        return None