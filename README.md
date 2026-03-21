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
Arcadia holds the backend logic for all the apps on one django server. When dealing with data for the Arcadia apps, frontends can communicate via a single graphql endpoint. For actions dealing with authentication/accounts, frontends call specific endpoints created via Django Rest Framework. The main reason for integrating 2 different types of apis is for practice and application.

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

## Accounts
Users do *not* directly create a Arcadia account, they instead create a *d2x* account. There are multiple reasons for this:

1: I plan to have multiple projects that will deal with a user having a account, having a single/already built source will hopefully speed up the production<br>
2: I was always curious on how sso like google worked so I would like to try my hand at creating/mimicking it for myself<br>
3: Most of my projects revolve around my imaginary company 'D2X' so having a 'd2x' account helps with the imaginary world building<br>

## Future Plans
1: If the arcadia apps become collectively big, I plan to split them up into microservices which is already in place with django's app system<br>
2. Create other apps/use cases

## Database
Inside the repo is a db_dump.json file holding sample data to showcase arcadia
To run a dump for your db and to handle japanese letters and such run <br>
python -Xutf8 manage.py dumpdata --natural-foreign --natural-primary -e admin.logentry -e auth -e contenttypes -e sessions --indent 4 -o db_dump.json

To utilize the json <br>
python -Xutf8 manage.py loaddata db_dump.json