from rest_framework import serializers
from ..models import Post

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'author', 'publish_at') # TODO: 'tags' is a TagglableManager