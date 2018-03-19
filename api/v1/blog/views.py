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

    def list(self, request, tag_name=None):
        queryset = self.filter_queryset(self.get_queryset())
        tag = None

        if tag_name:
            tag = get_object_or_404(Tag, name=tag_name)
            queryset = queryset.filter(tags__in=[tag])

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = serializer.data

            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
