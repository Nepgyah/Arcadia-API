from users.models import ArcadiaUser
from rest_framework_simplejwt.authentication import JWTAuthentication

auth = JWTAuthentication()

class GrapheneAuthMiddleware(object):

    def resolve(self, next, root, info, **args):
        raw_token = info.context.META.get('HTTP_AUTHORIZATION', None)
        
        if raw_token:
            access_token = raw_token.split()[1]
            validated_token = auth.get_validated_token(access_token)
            user_id = validated_token.get('user_id')
            if user_id:
                info.context.user_id = user_id

        return next(root, info, **args)