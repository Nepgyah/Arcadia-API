from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.service import AccountsService

@api_view(['POST'])
def adminLoginView(request):
    tokens = AccountsService.authentication.login_as_admin(
        request.POST.get('email', None),
        request.POST.get('password', None)
    )

    return Response(status=200, data={
        'detail': "account_admin_login_success",
        'message': "Login success",
        'data': {
            'access': {
                'value': tokens['access']['value'],
                'expiry': tokens['access']['expiry']
            },
            'refresh': {
                'value': tokens['refresh']['value'],
                'expiry': tokens['refresh']['expiry']
            }
        }
    })

@api_view(['POST'])
def refreshTokenView(request):
    tokens = AccountsService.authentication.refresh_token(request.POST.get('refresh', None))

    return Response(status=200, data={
        'detail': "account_token_refresh_success",
        'message': "Tokens refreshed",
        'data': {
            'access': {
                'value': tokens['access']['value'],
                'expiry': tokens['access']['expiry']
            },
            'refresh': {
                'value': tokens['refresh']['value'],
                'expiry': tokens['refresh']['expiry']
            }
        }
    })