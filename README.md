<pre>
A base for Django powered Facebok Apps
</pre>
facebook-app-django-base will allow you to set up a Facebook Application easily with Django.

About
-------

The goal of this is to eliminate time reading through Facebook's [Canvas Tutorial](https://developers.facebook.com/docs/appsonfacebook/tutorial/), [Authorization](https://developers.facebook.com/docs/authentication/) and [Signed Requests](http://developers.facebook.com/docs/authentication/signed_request/) docs, and getting right to using the Graph API to build your Facebook app quickly and without headaches. A very good resource for learning how to write Facebook Apps with Python is the [Run With Friends Example App](http://developers.facebook.com/docs/authentication/signed_request/)

How To Use
----------

In the near future I'd love to have an install script and make this more robust. For the time being you'll have to copy this into the same directory as your other Django Apps.

Add the following to your `settings.py` file:

    FACEBOOK_APP_NAMESPACE = 'YOUR APP NAMESPACE'
    FACEBOOK_APP_ID = YOUR APP ID
    FACEBOOK_APP_SECRET = 'YOUR APP SECRET'
    FACEBOOK_APPS_URI = 'http://apps.facebook.com/'
    FACEBOOK_LOGIN_URI = 'http://www.facebook.com/dialog/oauth/'
    FACEBOOK_API_DOMAIN = 'graph'

Assuming you put the facebook-app-django-base code in a directory called `fb`, add the following to `settings.py`:

    AUTH_PROFILE_MODULE = 'fb.UserProfile'

And also in `settings.py` add:

    'fb.backends.FacebookAuthBackend'

to your AUTHENTICATION_BACKENDS tupple.

Now that your `settings.py` is setup, you can use the `facebook_app_auth` decorator to your django views.

In `views.py`:

    from fb.decorators import facebook_app_auth

    @facebook_app_auth
    def some_view(request):
        #your view code

How It Works
------------

The `facebook_app_auth` decorator checks if the request is a POST request with a POST var `signed_request`. If this exists it goes through all the exhausting authorization checks to ensure the request is from Facebook and once it does that, it creates or updates the User model with the information from Facebook and authenticates/logs in the user to the Django application with the custom FacebookAuthBackend backend which requires no password. 

Customizing
-----------

If you need more fields from Facebook for your UserProfile model, simply add them and set them in the `refresh()` method. `refresh()` is called during every successful Authorization, so it is an appropriate place to put Facebook API calls to obtain and set needed fields.
