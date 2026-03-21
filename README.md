# Arcadia API
Introducing the Arcadia API. The backend service that helps users view and track anime, manga, games and music.
<br><br>
Visit Arcadia: https://arcadia-platform.vercel.app

## Latest Release - Alpha v1.1 - 3/20/2026
- **Asobu**
    - **Models**
        - Improve game relationship logic
    -**Graphql API**
        - Update schema to query game by id

## How it works
This repo holds the backend logic for all the apps on one django server. When dealing with data for the Arcadia apps, frontends can communicate via a single Graphql endpoint. For actions dealing with authentication/accounts, frontends call specific endpoints created via Django Rest Framework. The main reason for integrating 2 different types of apis is for practice and application.

## Why I started Arcadia
As an advid user of some of the apps that Arcadia tries to implement (MyAnimeList, AniList, Steam, Nexus Mods, Etc), I have wondered how the backend of these services could possibly be set up. And as a junior web developer, I wanted to work on something in my freetime that would function both as a way to reinforce what I have learned in the field so far as well as sorta learning 'playground' to try out new technologies and practices. So what better way to make the growth as a web developer fun than to work on a web platform based on my favorite hobbies: video games, anime and more.

## Features
As Arcadia is planned to be a multi app platform, here are the apps and their inspirationed counterparts

**Miru** - Anime info, tracking and watching (MyAnimeList + Crunchyroll)<br>
**Yomu** - Manga, LN, etc tracking and reading (Mangadex)<br>
**Asobu** - Game info, tracking and mod community (Steam + Nexus mods)<br>
**Kiku** - Music and playlist (Spotify)<br>
**Iku** - Event tracker (Google Events? lol)

## Tech
Languages: Python
Frameworks: Django, Django Rest Framework, Graphene
Authentication: JWT
Database: Postgresql

## How to install - Onboarding
1. Download the Arcadia api repository
2. Install [Python](https://www.python.org/downloads/)
3. Install [Django](https://www.djangoproject.com)
'''
pip install django
'''
4. Install the dependecies for Arcadia
'''
pip install -r requirements.txt
'''
5. Insert proper key values for the .env file

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

### Future Plans
1: If the arcadia apps become collectively big, I plan to split them up into microservices which is already in place with django's app system<br>
2. Create other apps/use cases
