from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
            user = token.user
            if user.last_logout and token.created < user.last_logout:
                raise AuthenticationFailed('Invalid token')
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        return (user, token)
