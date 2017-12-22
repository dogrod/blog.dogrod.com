from rest_framework import serializers
from ..models import Post, Comment

# Define serializer for comment in post
class UserSerializer(serializers.Serializer):
  """
  Serializer of Django's default user
  """
  email = serializers.EmailField()
  username = serializers.CharField(max_length=100)

class CommentSerializer(serializers.ModelSerializer):
  """
  Serializer of comment in post
  """
  class Meta:
    model = Comment
    fields = ('id', 'name', 'body', 'create_at')

class StringListField(serializers.ListField):
  """
  Serializer of tag in post
  Get from http://www.django-rest-framework.org/api-guide/fields/#listfield
  """
  child = serializers.CharField()

  def to_representation(self, data):
    return ' '.join(data.values_list('name', flat=True)) # you change the representation style here.

class PostSerializer(serializers.ModelSerializer):
  """
  Serializer of Post in post list
  """
  tags = StringListField()
  author = UserSerializer()

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'author', 'publish_at', 'tags')

class PostDetailSerializer(serializers.ModelSerializer):
  """
  Serializer of Post in post detail
  """
  tags = StringListField()
  author = UserSerializer()  
  comments = CommentSerializer(many = True)

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'author', 'publish_at', 'comments', 'tags')

