from django.conf.urls import include, url
from .user import urls as user_urls
from .blog import urls as blog_urls

urlpatterns = [
    url(r'^blog/', include(blog_urls, namespace='blog')),
    url(r'^user/', include(user_urls, namespace='user'))
]
