from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User

class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = User.objects.get(id=validated_token['user_id'])

        return (user, validated_token)