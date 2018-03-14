from django.conf.urls import include, url
from .user import urls as user_urls

urlpatterns = [
    url(r'^user/', include(user_urls, namespace='user'))
]
