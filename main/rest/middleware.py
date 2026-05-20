import logging
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, ExpiredTokenError



logger = logging.getLogger(__name__)

class RESTAuthMiddleware(JWTAuthentication):

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)

        if auth_header:
            try:
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    raise Exception('Invalid access token')
                
                validated_token = self.get_validated_token(parts[1])
                user_id = validated_token.get('user_id')
                # user = SimpleLazyObject(lambda: UserRepository.get_user_by_id(user_id))
                return (None, validated_token)
            
            except Exception as e:
                print(e)
            # except ExpiredTokenError:
            #     raise AuthorizationError('The access token has expired', code='auth_error_access_expired')
            # except InvalidToken as e:
            #     logger.warning(e)
            #     raise AuthorizationError()
            # except Exception as e:
            #     logger.warning(f'Unexpected auth error: {e}')
            #     raise AuthorizationError()
        
        return (AnonymousUser, None)