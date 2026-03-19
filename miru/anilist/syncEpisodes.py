from miru.models.relations import AnimeEpisode

def SyncEpisodes(anime_obj, data):
    """
        Configures episode data for an anime
    """
    episodes_data = data.get('streamingEpisodes')
    if episodes_data == []:
        return
    
    episode_objects = []

    for index, episode in enumerate(episodes_data):
        ep_title = episode.get('title')
        formatted_title = ep_title.split('-')[1].strip()

        temp_episode = AnimeEpisode(
            anime = anime_obj,
            number = index + 1,
            title = formatted_title,
            cover_img_url = episode.get('thumbnail')
        )
        episode_objects.append(temp_episode)

    #TODO: BULK SAVE EPISODES
    AnimeEpisode.objects.bulk_create(episode_objects)
    print(episode_objects)
