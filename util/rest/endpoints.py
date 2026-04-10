import json
from enum import Enum
from django.middleware.csrf import get_token
from django.db import connection

import rest_framework.status as HttpStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class ObtainCSRFToken(APIView):

    def get(self, request):
        csrf_token = get_token(request)
        return Response(
            status=200,
            data={
                'message': 'CSRF token generated',
                'token': csrf_token
            }
        )

class Health(Enum):
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'

class Status(Enum):
    UP = 'up'
    DOWN = 'down'

@api_view(['GET'])
def health_check(request):
    results = {
        'status': Health.HEALTHY.value,
        'checks': {}
    }

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        results['checks']['db'] = Status.UP.value

    except Exception:
        results['status'] = 'unhealthy'
        results['checks']['db'] = Status.DOWN.value

    if results['status'] != Health.HEALTHY.value:
        return Response(
            status=HttpStatus.HTTP_503_SERVICE_UNAVAILABLE,
            data=results
        )

    return Response(
        status=HttpStatus.HTTP_200_OK,
        data=results
    )

