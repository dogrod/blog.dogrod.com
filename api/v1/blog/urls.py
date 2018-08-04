from django.conf.urls import url
from . import views

urlpatterns = [
    # Post list
    url(r'^posts$', views.PostListAPIView().as_view(), name='post_list'),
    # Post detail
    url(r'^posts/(?P<post_slug>[-\w]+)$',
        views.PostDetailAPIView.as_view(),
        name='post_detail'),
    # Like post
    url(r'^posts/(?P<post_slug>[-\w]+)/like',
        views.LikePostAPIView.as_view(),
        name='like_post'),
    # Tag list API
    url(r'^tags$', views.TagsView.as_view(), name='tag_list')
]
