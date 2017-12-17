from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import Post
from .serializers import PostSerializer, PostDetailSerializer

class PostListView(generics.ListAPIView):
  queryset = Post.published.all()
  serializer_class = PostSerializer

class PostDetailView(generics.RetrieveAPIView):
  queryset = Post.published.all()
  serializer_class = PostDetailSerializer

# class CommentView(APIView):