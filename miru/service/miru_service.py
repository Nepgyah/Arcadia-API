from miru.repository.miru_repository import MiruRepository
from miru.models import Anime
from django.core.paginator import Paginator

class MiruService:
    ''' Service layer to apply business logic to Miru '''

    @staticmethod
    def get_anime_by_id(id):
        return MiruRepository.get_anime_by_id(id)
    
    @staticmethod
    def get_characters_by_anime(id):
        return MiruRepository.get_characters_by_anime(id)
    
    @staticmethod
    def get_anime_by_category(category, count):
        if count == None:
            count = 5
        return MiruRepository.get_anime_by_category(category, count)
    
    @staticmethod
    def search_anime(filters, sort, pagination):
        queryset = Anime.objects.all()

        if filters:
            if filters['type'] != -1:
                queryset = queryset.filter(type=filters['type'])
            if filters['status'] != -1:
                queryset = queryset.filter(status=filters['status'])
            if filters['title'] != '':
                #TODO: Add functionality to query multiple languages
                queryset = queryset.filter(title__icontains=filters['title'])

        if sort:
            direction = '' if sort['direction'] == 'asc' else '-'
            if sort['category'] != "":
                queryset = queryset.order_by(f'{direction}{sort['category']}')

        paginator = Paginator(queryset, per_page=pagination['per_page'])
        results = paginator.get_page(pagination['current_page']).object_list
        page_count = paginator.num_pages
        total = paginator.count

        return results, page_count, pagination['current_page'], total
    
