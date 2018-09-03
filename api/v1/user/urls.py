from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from .views import UserProfileView

urlpatterns = [
    url(r'^$', UserProfileView.as_view(), name='user_profile'),
    url(r'^\/login$', obtain_jwt_token, name='user_login'),
    url(r'^\/verify$', verify_jwt_token, name='user_verify'),
]
