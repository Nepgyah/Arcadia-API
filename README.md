# Arcadia API
Introducing the Arcadia API. This is the backend repository dedicated to assisting fans in the world of anime, manga, games and more.

<br><br>
Visit Arcadia: https://arcadia-platform.vercel.app

## Latest Release - Alpha v2.0 - 4/xx/2026
- **General**
    - Add middleware to utilize jwt tokens for GraphQL authentication

- **Miru v0.4**
    - **Models**
        - Add anilist statistics
        - Add myanimelist statistics
    - **GraphQL**
        - Adjust mutations to anime entry lists
    - **Other**
        - Add script to update anilist and mal ratings
        - Add custom exceptions for app
        - Update unit layered unit tests

- **Users v0.1**
    - **Model**
        - Add local arcadia user
    - **Graphql**
        - Add arcadia user detail query
    - **Rest**
        - Add admin login endpoint
    - **Other**
        - Add layering and unit testing

## Why I started Arcadia
Advid fans of anime, manga, games and more would have to multiple web apps to maintain their hobbies. For example using AniList to track Anime, MyAnimeList to track Manga, Spotify to handle music, etc. Arcadia aims to solve this issue by combining all the sites into one multi app solution, unified by a single login/account. This would remove having to manage different accounts, having multiple tabs open while also having the opporitunity to connect different datasets into one. 

One the other hand, as a early career web developer, I have become fascinated on how these solutions are designed and implemented. Arcadia gives me that opporitunity to hone in on my web dev skills and explore new technologies in a sandbox enviornemnt. Using the context of anime and games allows me to add a fun twist in learning as well.

## Tech
Languages: Python
Frameworks: Django, Django Rest Framework, Graphene
Authentication: JWT
Database: Postgresql

## Features
As Arcadia is planned to be a multi app platform, here are the apps and their inspirationed counterparts

**Miru** - Anime info, tracking and watching (MyAnimeList + Crunchyroll)<br>
**Yomu** - Manga, LN, etc tracking and reading (Mangadex)<br>
**Asobu** - Game info, tracking and mod community (Steam + Nexus mods)<br>
**Kiku** - Music and playlist (Spotify)<br>
**Iku** - Event tracker (Google Events? lol)

## How to install - Onboarding
1. Download the Arcadia api repository
2. Install [Python](https://www.python.org/downloads/)
3. Install [Django](https://www.djangoproject.com)
```
pip install django
```

4. Create a a virtual enviornment
```
python -m venv .venv
```

5. Install the dependecies for Arcadia
```
pip install -r requirements.txt
```

6. Insert proper key values for the .env file

## ENV Key Values
```
DJANGO_SECRET= Your django secret key

DB_NAME= Name of the database
DB_USER= Your db user username
DB_PASSWORD= Your db user password
DB_HOST= Domain of your db
DB_PORT= Port number (default 5432)

CLIENT_ID= Name for the arcadia app (used for communication with the d2x client)
CLIENT_SECRET= Security password for the arcadia app (used for communication with the d2x client)

COOKIE_SAME_SITE="None"
COOKIE_SECURE="True"

D2X_URL= URL to the d2x website

```

## Database / Sample Data
Inside the repo is a db_dump.json file holding sample data to showcase arcadia. If you every with to download the api for yourself and wish to skip manually entering some sample data. There is a db_dump.json file to jump start the database.<br>
Run the following command to utilize the data<br>
'''
python -Xutf8 manage.py loaddata db_dump.json
'''

To run a dump for your db and to handle japanese letters and such run<br>
'''
python -Xutf8 manage.py dumpdata --natural-foreign --natural-primary -e admin.logentry -e auth -e contenttypes -e sessions --indent 4 -o db_dump.json
'''

## Others

### D2X
You may come across the phrase 'D2X' or 'Team Double Dragon'. This is a reference to a inside joke with my friends about a fake organization for our esports teams. This grew as the catalyst for the world building of Arcadia - A D2X Product. I also have plans to attach this D2X brand to susequent projects to help with this 'world building' such as D2X games when working on personal project video games and such.

### Accounts
Users do *not* directly create a Arcadia account, they instead create a *d2x* account. There are multiple reasons for this:

1: I plan to have multiple projects that will deal with a user having a account, having a single/already built source will hopefully speed up the production<br>
2: I was always curious on how auth processes like google worked so I would like to try my hand at creating/mimicking it for myself<br>
