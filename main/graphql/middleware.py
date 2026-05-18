import logging
from strawberry.django.views import GraphQLView
from django.utils.functional import SimpleLazyObject

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, ExpiredTokenError
from users.repositories import UserRepository
from authorization.exceptions import AuthorizationError
from main.exceptions import ArcadiaException

logger = logging.getLogger(__name__)

authenticator = JWTAuthentication()

class JWTGraphQLView(GraphQLView):

    def get_context(self, request, response):
        context = super().get_context(request, response)

        request.user = getattr(request, 'user', None)

        auth_header = request.headers.get('Authorization', None)

        if auth_header:
            try:
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    raise AuthorizationError("Invalid authorization header")

                validated_token = authenticator.get_validated_token(parts[1])
                user_id = validated_token.get('user_id')

            except ExpiredTokenError as e:
                raise AuthorizationError('The access token has expired', code='auth_error_access_expired') from e
            except InvalidToken as e:
                logger.warning(e)
                raise AuthorizationError() from e
            except Exception as e:
                logger.exception(e)
                raise ArcadiaException('An unexpected error occured reading the auth header') from e
            if user_id:
                context.user_id = user_id
                context.user = SimpleLazyObject(lambda: UserRepository.get_user_by_id(user_id))
            else:
                context.user_id = None

        return context
