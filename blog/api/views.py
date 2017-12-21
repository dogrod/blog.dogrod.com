from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import Post
from .serializers import PostSerializer, PostDetailSerializer

class PostListView(generics.ListAPIView):
  queryset = Post.published.all()
  serializer_class = PostSerializer

  def list(self, request):
    queryset = self.get_queryset()
    serializer = PostSerializer(queryset, many = True)

    return Response({
      'posts': serializer.data
    })

class PostDetailView(generics.RetrieveAPIView):
  queryset = Post.published.all()
  serializer_class = PostDetailSerializer

  def retrieve(self, request, pk = None):
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, pk = pk)
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)
# class CommentView(APIView):