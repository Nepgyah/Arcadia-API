## App Version Tracker
| App        | Version |
| ---------- | ------- |
| Miru       | 0.3     |

## Alpha v1.0 - 3/19/2026
Dev note: After finalizing the base of miru and implementing a better way to input data through the help of Anilist API. The progress from this patch has been deemed big enough to jump from 0.6 to 1.0. Thank you to everyone involved through testing and suggestions - A.P

- **Miru**
    - **Models**
        - Add anilist model to handle rank data from anilist
    - **Admin**
        - Add admin page to ease the process of adding anime entries
    - **Other**
        - Add multi part script to fetch and format Anilist api data into the Arcadia DB schema

- **Talent**
    - **Models**
        - Adjusted several models to handle a image url

## Alpha v0.6 - 3/17/2026
- **General**
    - Add github actions for the following
        - Run unit tests on pr to main
        - Run python linter on pr to main
    - Improved code following pylinter suggestions

## Alpha v0.5 - 3/16/2026
- **Asobu**
    - **Models**
        - Add game model
        - Add relation models (characters, games, platforms)
    - **Graphql API**
        - Add queries for games, character by games and franchise by games

- **Talent**
    - **Service**
        - Improve querying efficiency

## Alpha v0.4 - 3/9/2026
- **General**
    - Add oauth journey via D2X Accounts

## Alpha v0.3 - 3/4/2026
- **Miru v0.3**
    - **Models**
        - Add AnimeEpisode
    - **API**
        - Add graphql query for anime episodes
        - Adjusted graphl query for fetching anime details

## Alpha v0.2 - 2/8/2026
- **Miru v0.2**
    - **Models**
        - Add AnimeListEntry
    - **API**
        - Adjust graphql Anime schema to allow voice actors and franchises
        - Add CRUD functionality to user anime lists
    - **Others**
        - Add several notes for some service layer methods
        - Improve folder structure to reflect layer architecture

- Create talent app to hold characters, voice actors and artists
- Create test case for user anime lists

## Alpha v0.1 - 2/24/2026
- **Miru v0.2**
    - **Models**
        - Add Studio
        - Add Season
        - Add Anime
        - Add AnimeCharacter
        - Add AnimeRelation
    - **API**
        - Add graphql with read queries for anime


- Initial setup from previous iterations of Arcadia concept testing