# Asobu Docs

## Overview
This app manages all things related to games on the arcadia platform from displaying game details, handling a users game/library list and possibly handle mods and forums.

## Models
The asobu model is one of the most intricate models in Arcadia, though not as intricate as the Miru [anime model](/miru/models/anime.py). I made some decisions on how to properly handle relations between video games.

- The **Game** model contains a *prev_game* field, which handles games having multiple branching paths down the line.
- A seperate model: **DLC** was created to handle a game having multiple dlcs, this model also contains a choice field to handle different types of dlc (Story Expansions, Cosmetics, etc)
- The **GameRelation**, though not implements yet, plans to hold the outlying cases in which the relation cannot be deemed as a dlc or simply a prequel/sequel relationship (Re Release on a different market)

## API
The Asobu app mainly utilizes graphql for its ability to specificly request what information the platform needs of an anime.
