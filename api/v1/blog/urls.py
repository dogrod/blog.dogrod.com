from django.conf.urls import url
from . import views
from .views import PostViewSet

post_list = PostViewSet.as_view({
    'get': 'list'
})

post_detail = PostViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    # Post list
    url(r'^\/posts$', post_list, name='post_list'),
    # Post detail
    url(r'^\/posts/(?P<post_id>[-\w]+)$',
        post_detail,
        name='post_detail'),
    # Like post
    url(r'^\/posts/(?P<post_id>[-\w]+)/like$',
        views.LikePostAPIView.as_view(),
        name='like_post'),
    url(r'^\/posts/(?P<post_id>[-\w]+)/comments$',
        views.CommentAPIView.as_view(),
        name='comment_post'),
    # Tag list API
    url(r'^\/tags$', views.TagsView.as_view(), name='tag_list')
]
