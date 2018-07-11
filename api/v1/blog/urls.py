from django.conf.urls import url
from . import views

urlpatterns = [
    # Post list
    url(r'^posts$', views.PostListView().as_view(), name='post_list'),
    # Post detail
    url(r'^posts/(?P<post_slug>[-\w]+)$',
        views.PostDetail.as_view(),
        name='post_detail'),
    # Like post
    url(r'^posts/(?P<post_slug>[-\w]+)/like',
        views.LikePost.as_view(),
        name='like_post'),
    # Tag list API
    url(r'^tags$', views.TagsView.as_view(), name='tag_list')
]
