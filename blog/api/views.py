from rest_framework import generics
from ..models import Post
from .serializers import PostSerializer

class PostListView(generics.ListAPIView):
  queryset = Post.published.all()
  serializer_class = PostSerializer

class PostDetailView(generics.RetrieveAPIView):
  queryset = Post.published.all()
  serializer_class = PostSerializer