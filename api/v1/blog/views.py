from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response

from taggit.models import Tag
from blog.models import Post
from .serializers import PostSerializer
from .pagination import PostPagination


class PostListView(generics.ListAPIView):
    """
    List API View of /posts
    """
    queryset = Post.published.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request, tag_slug=None):
        queryset = self.filter_queryset(self.get_queryset())
        tag = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags_in=[tag])

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
