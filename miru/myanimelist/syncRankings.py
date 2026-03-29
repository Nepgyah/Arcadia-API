import logging
import requests
from bs4 import BeautifulSoup
def syncMALRankings(mal_id) -> int:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(
            f'https://myanimelist.net/anime/{mal_id}',
            headers=headers,
            timeout=10
        )

        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')

        score_element = soup.find("span", class_="numbers ranked").strong.text[1:]
        popularity_element = soup.find("span", class_="numbers popularity").strong.text[1:]

        if not score_element or not popularity_element:
            raise ValueError("Could not finding ranking elements, check MyAnimeList page to see if they updated their UI")
        

        rank_by_score = int(score_element)
        rank_by_popularity = int(popularity_element)

        print(f"ID: {mal_id} Score: {rank_by_score} Popularity: {rank_by_popularity}")
        return rank_by_score, rank_by_popularity
    
    except (requests.RequestException, ValueError, AttributeError) as e:
        raise Exception(f"External Data Error: {str(e)}")