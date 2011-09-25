import json
import urllib, urllib2
from django.conf import settings

class FacebookApiError(Exception):
    def __init__(self, result):
        self.result = result

    def __str__(self):
        return self.__class__.__name__ + ': ' + json.dumps(self.result)


class Facebook(object):
    """
    Wraps the Facebook specific logic
    
    Example:
    facebook = Facebook(user_id=request.user.id, access_token=request.user.get_profile().access_token)
    me = facebook.api(path='/me', {u'fields': u'name,email,picture,friends'})
    friends = me[u'friends'][u'data']
    """
    def __init__(self, app_id=settings.FACEBOOK_APP_ID,
            app_secret=settings.FACEBOOK_APP_SECRET, user_id=None, access_token=None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user_id = user_id
        self.access_token = access_token

    def api(self, path, params=None, method=u'GET', domain=settings.FACEBOOK_API_DOMAIN):
        """Make API calls"""
        if not params:
            params = {}
        params[u'method'] = method
        if u'access_token' not in params and self.access_token:
            params[u'access_token'] = self.access_token
        req = urllib2.Request(
            url=u'https://' + domain + u'.facebook.com' + path,
            data=urllib.urlencode(params),
            headers={
                u'Content-Type': u'application/x-www-form-urlencoded'})
        result = json.loads(urllib2.urlopen(req).read())
        if isinstance(result, dict) and u'error' in result:
            raise FacebookApiError(result)
        return result
