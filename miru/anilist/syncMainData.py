import requests
import os
import json
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

def SyncMainData(anime_obj, data) -> None:
    """
    Configures title fields for the anime
    """
    
    anime_obj.title = data.get('title').get('english')
    anime_obj.title_ja = data.get('title').get('native')
    anime_obj.title_romaji = data.get('title').get('romaji')

    ani_season = data.get('season')

    if ani_season == "WINTER":
        season = 0
    elif ani_season == "SPRING":
        season = 1
    elif ani_season == "SUMMER":
        season = 2
    else:
        season = 3

    anime_obj.season = season
    anime_obj.season_year = data.get('seasonYear')

    ani_type = data.get('format')
    
    if ani_type == 'MOVIE':
        miru_type = 1
    elif ani_type == 'OVA':
        miru_type = 2
    elif ani_type in ('ONA', 'SPECIAL'):
        miru_type = 3
    else:
        miru_type = 0

    anime_obj.type = miru_type
    anime_obj.rating = 0

    anime_obj.episode_count = data.get('episodes')
    anime_obj.hashtag = data.get('hashtag')
    anime_obj.banner_img_url = data.get('bannerImage')
    anime_obj.cover_img_url = data.get('coverImage').get('large')

    formatted_start_date = f"{data.get('startDate').get('year')}-{data.get('startDate').get('month')}-{data.get('startDate').get('day')}"
    anime_obj.airing_start_date = formatted_start_date

    formatted_end_date = f"{data.get('endDate').get('year')}-{data.get('endDate').get('month')}-{data.get('endDate').get('day')}"
    anime_obj.airing_end_date = formatted_end_date
        