from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from functools import wraps
import hashlib
import hmac
import json
from fb.utils.base64utils import base64_url_decode, base64_url_encode

def facebook_app_auth(view_func):
    """
    Decorator for doing all the Facebook Auth BS for FB Apps
    """
    @wraps(view_func)
    def decorator(request, *args, **kwargs):
        if request.method == "POST":
            signed_request = request.POST['signed_request']
            encoded_sig, payload = signed_request.split('.', 1)
            b64_sig = base64_url_decode(encoded_sig)
            b64_payload = base64_url_decode(payload)
            data = json.loads(b64_payload)
            if data['algorithm'].upper() == "HMAC-SHA256":
                expected_sig = hmac.new(settings.FACEBOOK_APP_SECRET, msg=payload, digestmod=hashlib.sha256).digest()
                if expected_sig == b64_sig:
                    if 'user_id' in data:
                        #CREATE OR UPDATE USER/AUTHENTICATE THEM WITHIN DJANGO
                        user, create = User.objects.get_or_create(id=str(data['user_id']), username=data['user_id'])
                        user.get_profile().refresh(data)
                        user = authenticate(username=user.username, facebook=True)
                        login(request, user)
                        request.method = "GET" #reset to GET, this was the first request from facebook, which is always post
                        return view_func(request, *args, **kwargs)
                    else:
                        data = urllib.urlencode({
                            'scope': 'email',
                            'client_id': settings.FACEBOOK_APP_ID,
                            'redirect_uri': settings.FACEBOOK_APPS_URI + settings.FACEBOOK_APP_NAMESPACE + request.get_full_path(),
                            'response_type': 'token',
                        })
                        encoded_url = settings.FACEBOOK_LOGIN_URI + '?' + data
                        return HttpResponse("<script>top.location.href='" + encoded_url + "'</script>")
                else:
                    return HttpResponse("Not from FBook")
            else:
                return HttpResponse("Bad Algo") 
        else:
            if request.user:
                user_profile = request.user.get_profile()
                if user_profile.access_token_expired():
                    data = urllib.urlencode({
                        'scope': 'email',
                        'client_id': settings.FACEBOOK_APP_ID,
                        'redirect_uri': settings.FACEBOOK_APPS_URI + settings.FACEBOOK_APP_NAMESPACE + request.get_full_path(),
                        'response_type': 'token',
                    })
                    encoded_url = settings.FACEBOOK_LOGIN_URI + '?' + data
                    return HttpResponse("<script>top.location.href='" + encoded_url + "'</script>")
                else:
                    return view_func(request, *args, **kwargs)
            else:
                data = urllib.urlencode({
                    'scope': 'email',
                    'client_id': settings.FACEBOOK_APP_ID,
                    'redirect_uri': settings.FACEBOOK_APPS_URI + settings.FACEBOOK_APP_NAMESPACE + request.get_full_path(),
                    'response_type': 'token',
                })
                encoded_url = settings.FACEBOOK_LOGIN_URI + '?' + data
                return HttpResponse("<script>top.location.href='" + encoded_url + "'</script>")
    return decorator
