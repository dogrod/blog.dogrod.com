from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import Post
from .serializers import PostSerializer, PostDetailSerializer
from .pagination import PostPagination

class PostListView(generics.ListAPIView):
  """
  View of /posts route
  return a list of Post
  """
  queryset = Post.published.all()
  serializer_class = PostSerializer
  pagination_class = PostPagination

  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

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

  def retrieve(self, request, pk = None):
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, pk = pk)
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)
# class CommentView(APIView):