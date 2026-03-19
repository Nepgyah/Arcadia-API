from base.models import Genre

def SyncGenres(data):
    genre_list = []
    genre_data = data.get('genres')

    if genre_data == []:
        return []
    
    for genre in genre_data:
        genre_instance, _created = Genre.objects.get_or_create(
            name=genre
        )
        genre_list.append(genre_instance)

    return genre_list