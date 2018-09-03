"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^views/', include('blog.urls', namespace='post', app_name='post')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.api.urls', namespace='blog_api')),
    url(r'^account/', include('account.api.urls', namespace='user_api')),
    url(r'^api', include('api.urls', namespace='api'))
    # url(r'^api/account/', include('account.api.urls', namespace = 'account_api'))
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)
