import json
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from .serializers import GameListEntrySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from asobu.repository import AsobuRepository

@api_view(['GET'])
def export_list(request):
    if request.user == AnonymousUser:
        return Response(
            status=401,
            data={
                'detail': 'You must be logged in to export list',
                'message': 'Login required'
            }
        ) 
    
    user_game_list = AsobuRepository.get_game_list_by_user(request.user)
    
    list_data = {
        'playing': GameListEntrySerializer(user_game_list.filter(status=0), many=True).data,
        'completed': GameListEntrySerializer(user_game_list.filter(status=1), many=True).data,
        'planTo': GameListEntrySerializer(user_game_list.filter(status=2), many=True).data,
        'onHold': GameListEntrySerializer(user_game_list.filter(status=3), many=True).data,
        'replaying': GameListEntrySerializer(user_game_list.filter(status=4), many=True).data
    }

    return Response(
        status=200,
        data={
            'list': list_data,
            'detail': 'Game list data generated',
            'message': 'Successfully exported game list'
        }
    )
