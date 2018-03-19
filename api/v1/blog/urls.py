from django.conf.urls import url
from . import views

urlpatterns = [
    # Post list
    url(r'^posts$', views.PostListView().as_view(), name='post_list'),
    # Post detail
    url(r'^posts/(?P<post_slug>[-\w]+)',
        views.PostDetailView.as_view(),
        name='post_detail'),
    # Tag list API
    url(r'^tags$', views.TagsView.as_view(), name='tag_list'),
    # Tag detail API, return a post list with tag
    url(r'^tag/(?P<tag_name>[-\w]+)',
        views.PostListView().as_view(),
        name='post_list_with_tag')
]
