from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from taggit.models import Tag
from ..models import Post
from .serializers import PostSerializer, PostDetailSerializer, TagSerializer
from .pagination import PostPagination

class PostListView(generics.ListAPIView):
  """
  View of /posts route
  return a list of Post
  """
  queryset = Post.published.all()
  serializer_class = PostSerializer
  pagination_class = PostPagination
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

  def list(self, request, tag_slug = None):
    queryset = self.filter_queryset(self.get_queryset())
    tag = None

    if tag_slug:
      tag = get_object_or_404(Tag, slug = tag_slug)
      queryset = queryset.filter(tags__in = [tag])
    
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)

    return Response({
      'results': serializer.data
    })

class PostDetailView(generics.RetrieveAPIView):
  """
  View of /post/:id
  return detail of specific post
  """
  queryset = Post.published.all()
  serializer_class = PostDetailSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  

  def retrieve(self, request, pk = None):
    queryset = Post.published.all()
    post = get_object_or_404(queryset, pk = pk)
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)
# class CommentView(APIView):

class TagsView(APIView):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  
  
  # def perform_create(self, serializer):
  #   instance = serializer.save()
  #   if 'tags' in self.request.DATA:
  #       instance.tags.set(*self.request.DATA['tags'])

  def get(self, request, format=None):
    queryset = Tag.objects.all()
    serializer = TagSerializer(queryset, many=True)

    return Response({
      'tags': serializer.data
    })
