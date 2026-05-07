import logging
from django.utils.functional import SimpleLazyObject

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, ExpiredTokenError
from users.repositories import UserRepository
from authorization.exceptions import AuthorizationError
from .exceptions import ArcadiaException

logger = logging.getLogger(__name__)

authenticator = JWTAuthentication()

class GrapheneAuthMiddleware(object):

    def resolve(self, next, root, info, **args):
        try:
            auth_header = info.context.META.get('HTTP_AUTHORIZATION', None)

            if auth_header:
                try:
                    parts = auth_header.split()
                    if len(parts) != 2 or parts[0].lower() != 'bearer':
                        raise AuthorizationError('Invalid access token')
                    
                    validated_token = authenticator.get_validated_token(parts[1])
                    user_id = validated_token.get('user_id')

                except ExpiredTokenError as e:
                    raise AuthorizationError('The access token has expired', code='auth_error_access_expired') from e
                except InvalidToken as e:
                    logger.warning(e)
                    raise AuthorizationError() from e
                
                if user_id:
                    info.context.user = SimpleLazyObject(lambda: UserRepository.get_user_by_id(user_id))

            return next(root, info, **args)
        
        except ArcadiaException:
            # Contains errors from each app domain
            raise

        except AuthorizationError:
            raise

        except Exception as e:
            logger.exception(e)
            raise