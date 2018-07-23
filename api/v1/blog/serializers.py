from django.utils import timezone
from rest_framework import serializers
from taggit.models import Tag
from blog.models import Post, Comment, Category, ActionSummary


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
        fields = ('id', 'name', 'content', 'create_at')


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer of category in post
    """

    class Meta:
        model = Category
        fields = ('title', 'slug')


class TagSerializerField(serializers.ListField):
    """
  Serializer of tag in post
  Get from http://www.django-rest-framework.org/api-guide/fields/#listfield
  """
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list('name', flat=True)


class TagSerializer(serializers.ModelSerializer):
    """
  Serializer of tag in list
  """

    # tags = TagSerializerField()

    class Meta:
        model = Tag
        fields = ('name', 'slug')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = super(TagSerializer, self).create(validated_data)
        instance.tags.set(*tags)
        return instance


class PostListSerializer(serializers.ModelSerializer):
    """
  Serializer of Post in post list
  """
    tags = TagSerializerField()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'slug', 'author', 'publish_at', 'tags')

    def to_representation(self, data):
        representation = super(PostListSerializer, self).to_representation(data)
        representation['content'] = data.get_summary()
        return representation


class PostSerializer(serializers.ModelSerializer):
    """
  Serializer of Post in post detail
  """
    tags = TagSerializerField()
    author = UserSerializer()
    comments = CommentSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'slug', 'author', 'publish_at',
                  'comments', 'tags', 'category')

    def to_representation(self, data):
        representation = super(PostSerializer, self).to_representation(data)
        # representation['content'] = data.get_content_as_markdown()
        representation['category'] = data.category.title
        return representation


class ActionSummarySerializer(serializers.ModelSerializer):
    """
    Serializer of ActionSummary
    """
    likes = serializers.SerializerMethodField('get_like_count')
    comments = serializers.SerializerMethodField('get_comment_count')

    class Meta:
        model = ActionSummary
        fields = ('likes', 'comments')

    def get_like_count(self, data):
        return data.like_count

    def get_comment_count(self, data):
        return data.comment_count

