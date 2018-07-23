from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response

from taggit.models import Tag
from blog.models import Post
from .serializers import PostListSerializer, PostSerializer, TagSerializer
from .pagination import PostPagination


class PostListView(generics.ListAPIView):
    """
    List API View of /posts
    """
    queryset = Post.published.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        tag = None
        tag_in_query = request.query_params.get('tag')

        # If there's 'tag' in request query, filter post list before response.
        if tag_in_query:
            tag = get_object_or_404(Tag, name=tag_in_query)
            queryset = queryset.filter(tags__in=[tag])

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = serializer.data

            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class PostDetailView(generics.RetrieveAPIView):
    """
    View of /post/:id
    return detail of specific post
    """
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def retrieve(self, request, post_slug=None):
        queryset = Post.published.all()
        post = get_object_or_404(queryset, slug=post_slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class TagsView(views.APIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, format=None):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)

        return Response({'tags': serializer.data})


class PostDetail(views.APIView):
    """
    Retrieve a post instance.
    """
    permission_classes = (permissions.AllowAny, )

    def get_object(self, post_slug):
        try:
            return Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_slug):
        post = self.get_object(post_slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_slug):
        content = request.data.get('content')

        post = self.get_object(post_slug)
        serializer = PostSerializer(post, data={'content': content}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
