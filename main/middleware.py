from users.models import ArcadiaUser
from rest_framework_simplejwt.authentication import JWTAuthentication

auth = JWTAuthentication()

class GrapheneAuthMiddleware(object):

    def resolve(self, next, root, info, **args):
        raw_token = info.context.COOKIES.get('access_token', None)

        if raw_token:
            print('Raw token')
            validated_token = auth.get_validated_token(raw_token)
            user_id = validated_token.get('user_id')
            if user_id:
                info.context.user_id = user_id

        return next(root, info, **args)