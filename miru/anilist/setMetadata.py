def setMetadata(anime_obj, data):
    """
    Configures title fields for the anime
    """
    print('Called set titles')
    print(data)
    anime_obj.title = data.get('title').get('english')
    anime_obj.title_ja = data.get('title').get('native')
    anime_obj.title_romaji = data.get('title').get('romaji')
    return