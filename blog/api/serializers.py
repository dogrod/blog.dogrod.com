from rest_framework import serializers
from ..models import Post, Comment

# Define serializer for comment in post
class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ('id', 'name', 'body', 'create_at')

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'author', 'publish_at') # TODO: 'tags' is a TagglableManager

class PostDetailSerializer(serializers.ModelSerializer):
  comments = CommentSerializer(many = True)

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'author', 'publish_at', 'comments') # TODO: 'tags' is a TagglableManager

