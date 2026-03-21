# Talent App docs

## Overview
This app manages people entities of Arcadia such as:
- Characters (Game, Anime, Manga)
- Voice actors for said characters
- Artists for music
- Important staff for companies (Lead producer, creator, etc)

## Models

### Artist
The artist model was deemed one of the more tricky data structures to work on with its many scenarios. For example:
- A artist could simply be a solo artist, with no relation to any other Arcadia media (Ex: Kendrick Lamar lol)
- A artist could also be working as a voice actor (Ex: Azusa Tadokoro)
- The artist could simply be a vocal rendition for a certain character (Ex: Anime Character Songs)

The scenario of the artist is then concluded by whether a foreign key is set or not for the voice_actor or character field

## API
The Talent app mainly utilizes graphql for its ability to specificly request what information the platform needs of an anime.