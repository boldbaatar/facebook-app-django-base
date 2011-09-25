from django.contrib.auth.models import User

class FacebookAuthBackend(object):
    """
    Auth Backend for Facebook, requires no password
    ONLY use if you know a request is from facebook
    and the signed request is verified
    """
    def authenticate(self, username=None, password=None, facebook=False):
            try:
                user = User.objects.get(username=username)
                if user and facebook:
                    return user
            except User.DoesNotExist:
                return None
       
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
