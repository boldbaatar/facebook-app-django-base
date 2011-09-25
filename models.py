from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from fb.facebook_api import Facebook
import time

class UserProfile(models.Model):
    """
    UserProfile is an extension of the User model to store data pertaining to Facebook
    """
    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=500, null=True, blank=True)
    picture_url = models.URLField(verify_exists=False)
    access_token = models.CharField(max_length=200, null=True, blank=True)
    expires = models.IntegerField(null=True, blank=True)

    def refresh(self, data):
        """
        Refresh all user data from data and also with making a facebook
        api call.
        """
        if 'oauth_token' in data:
            self.access_token = data['oauth_token']
        if 'expires' in data:
            self.expires = data['expires']
        facebook = Facebook(user_id=self.user.id, access_token=self.access_token)
        facebook_data = facebook.api('/me', {'fields': 'name, email, picture, first_name, last_name, name'})
        self.user.first_name = facebook_data['first_name']
        self.user.last_name = facebook_data['last_name']
        self.display_name = facebook_data['name']
        self.picture_url = facebook_data['picture']
        self.user.save()
        self.save()

    def access_token_expired(self):
        """
        Determines if the access token is expired
        self.expires is a unix timestamp set by Facebook's API
        """
        if time.time() >= self.expires:
            return True
        else:
            return False 
    
#signal to ensure on each user creation there is also a UserProfile created with that user instance
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
