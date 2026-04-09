import logging
from django.utils.functional import SimpleLazyObject

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, ExpiredTokenError
from authorization.exceptions import AuthorizationError

from users.repositories import UserRepository

logger = logging.getLogger(__name__)

authenticator = JWTAuthentication()

class GrapheneAuthMiddleware(object):

    def resolve(self, next, root, info, **args):
        auth_header = info.context.META.get('HTTP_AUTHORIZATION', None)

        if auth_header:
            try:
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    raise Exception('Invalid access token')
                
                validated_token = authenticator.get_validated_token(parts[1])
                user_id = validated_token.get('user_id')

            except ExpiredTokenError:
                raise AuthorizationError('The access token has expired', code='auth_error_access_expired')
            except InvalidToken as e:
                logger.warning(e)
                raise AuthorizationError()
            except Exception as e:
                logger.warning(f'Unexpected auth error: {e}')
                raise AuthorizationError()
            
            if user_id:
                info.context.user = SimpleLazyObject(lambda: UserRepository.get_user_by_id(user_id))

        return next(root, info, **args)