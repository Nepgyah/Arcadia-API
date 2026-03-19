from miru.models.misc import AnimeCompany

def SyncAnimeCompanies(anime_obj, data):

    # Anilist puts producers and studios under a single studio schema
    companies = data.get('studios').get('edges')

    if companies == []:
        return
    
    studio_list = []
    producer_list = []

    for company in companies:
        is_studio = company.get('node').get('isAnimationStudio')

        anime_company_instance, _created = AnimeCompany.objects.get_or_create(
            name = company.get('node').get('name')
        )

        if is_studio:
            studio_list.append(anime_company_instance)
        else:
            producer_list.append(anime_company_instance)
        
    anime_obj.studio.set(studio_list)
    anime_obj.producer.set(producer_list)
    
    return