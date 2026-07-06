# Arcadia API
Introducing the Arcadia API. This is the backend repository dedicated to assisting fans in the world of anime, manga, games and more.

Visit Arcadia: https://arcadia-platform.vercel.app

## Latest Release - Alpha v3.1 - xx/xx/2026
- **General**
    - Create main arcadia library for standardization
    - Reorganize version changes for each app
    
- **Apps Updated**
    - Arcadia Library *NEW**
    - Miru

See overall [changelog](./CHANGELOG.md)

## The Problem
Advid fans of anime, manga and games use online resources such as anilist, myanimelist and steam to help track and maintain their hobby activities. But with the current services, it requires having and maintaining multiple accounts to in order to manage those hobbies. Also datawise, there can be overlaps where characters can appear in a game, manga and video game but there is no connection to them.

## The solution
With Arcadia, a user can manage their anime, manga, games and more in a single place with a single login and switching between the apps is simple with a few clicks. Data is no longer disconnected as the database is designed to connect the different medias together via concepts such as similar franchises, voice actors or characters.

## AI Usage Disclaimer
Though there is a big rise in the use of artificial intelligence in the development world, the use of AI in project arcadia will be limited for the following reason.

Utilzing tools such as gemini or claude to generate the majority of the Arcadia codebase contradicts the reason I began this project. As a aspiring developer in this industry, I want to be able to say '*I* built Arcadia'. Though the solutions are not going to be perfect in terms of efficiency and scalability, it does bring about joy knowing the solution is 'mine' to begin with. AI can help and improve afterwards but I would like to pride myself in laying down the foundation for Arcadia's solutions. It does seem that AI is here to stay (though its the desired capacity is debated) but I believe there are some growing pains I need to expereince as a solo developer on this project in order to grow. In the end, I aim to have AI as a 'assistance' rather than a 'reliance'.

That being said there are some parts I utilize AI for:
- Refining some snippets of code that i have written first
- Obscure bugs
- Research/Lookup for general practice and foundation of concepts (Architecture, Formatting, Etc)
- Writing unit tests for the repository and service layers to reduce time on this part of development allowing for more time on more major aspects (features, refactoring, etc)

## Other Notes
As a early career web developer, I have become fascinated on how these solutions (steam, MAL, anilist, spotify, etc) are designed and implemented. Arcadia gives me that opporitunity to hone in on my web dev skills and explore new technologies in a sandbox enviornemnt. Using the context of anime and games allows me to add a fun twist in learning as well.

## Tech
Languages: Python
Frameworks: Django, Django Rest Framework, Graphene
Authentication: JWT
Database: Postgresql

## Features
As Arcadia is planned to be a multi app platform, here are the apps and their inspirationed counterparts

[Miru](miru/readme.md) - Anime info, tracking and watching (MyAnimeList + Crunchyroll)<br>
**Yomu** - Manga, LN, etc tracking and reading (Mangadex)<br>
[Asobu](asobu/readme.md) - Game info, tracking and mod community (Steam + Nexus mods)<br>
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

DB_NAME = Name of the database
DB_USER = Your db user username
DB_PASSWORD = Your db user password
DB_HOST = Domain of your db
DB_PORT = Port number (default 5432)

CLIENT_ID = Name for the arcadia app (used for communication with the d2x client)
CLIENT_SECRET = Security password for the arcadia app (used for communication with the d2x client)

COOKIE_SAME_SITE="None"
COOKIE_SECURE="True"

BG_CDN_BASE = Base url for the cdn service

D2X_URL = URL to the d2x website

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
