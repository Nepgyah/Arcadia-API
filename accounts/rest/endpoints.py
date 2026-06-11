from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.service import AccountsService

@api_view(['POST'])
def adminLoginView(request):
    try:
        tokens = AccountsService.authentication.login_as_admin(
            request.data.get('email', None),
            request.data.get('password', None)
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
    except Exception as e:
        return Response(
            status=500,
            data={
                "message": "An unexpected error occured while logging in"
            }
        )

@api_view(['POST'])
def refreshTokenView(request):
    tokens = AccountsService.authentication.refresh_token(request.data.get('refresh', None))

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