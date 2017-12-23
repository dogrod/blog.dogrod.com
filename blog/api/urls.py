from django.conf.urls import url
from . import views

urlpatterns = [
  # post list
  url(
    r'^posts',
    views.PostListView.as_view(),
    name = 'post_list'
  ),
  # post detail
  url(
    r'^post/(?P<pk>\d+)',
    views.PostDetailView.as_view(),
    name = 'post_detail'
  ),
  url(
    r'^tags',
    views.TagsView.as_view(),
    name = 'tag_list'
  ),
  url(
    r'^tag/(?P<tag_slug>[-\w]+)',
    views.PostListView.as_view(),
    name = 'post_list_as_tag'
  )
]