from rest_framework import serializers
from ..models import Post, Comment

# Define serializer for comment in post
class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ('id', 'name', 'body', 'create_at')

class StringListField(serializers.ListField): # get from http://www.django-rest-framework.org/api-guide/fields/#listfield
  child = serializers.CharField()

  def to_representation(self, data):
    return ' '.join(data.values_list('name', flat=True)) # you change the representation style here.

class PostSerializer(serializers.ModelSerializer):
  tags = StringListField()

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'author', 'publish_at', 'tags')

class PostDetailSerializer(serializers.ModelSerializer):
  tags = StringListField()
  comments = CommentSerializer(many = True)

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'author', 'publish_at', 'comments', 'tags')

