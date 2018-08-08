from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response

from taggit.models import Tag
from blog.models import Post, ActionSummary, Like, Comment
from .serializers import PostListSerializer, PostSerializer, TagSerializer, ActionSummarySerializer, LikeSerializer, CommentSerializer
from .pagination import PostPagination
from .forms import CommentForm


class PostListAPIView(generics.ListAPIView):
    """
    List API View of /posts
    """
    queryset = Post.published.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        tag = None
        tag_in_query = request.query_params.get('tag')

        # If there's 'tag' in request query, filter post list before response.
        if tag_in_query:
            tag = get_object_or_404(Tag, name=tag_in_query)
            queryset = queryset.filter(tags__in=[tag])

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = serializer.data

            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class PostDetailView(generics.RetrieveAPIView):
    """
    View of /post/:id
    return detail of specific post
    """
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def retrieve(self, request, post_slug=None):
        queryset = Post.published.all()
        post = get_object_or_404(queryset, slug=post_slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class TagsView(views.APIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, format=None):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)

        return Response({'tags': serializer.data})


class PostBasedAPIVIew(views.APIView):
    """
    Basic API View of post to provide some method based on Post
    """
    def get_post(self, post_slug):
        try:
            return Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise Http404

    def get_summary(self, post):
        objects, created = ActionSummary.objects.get_or_create(post=post)
        return objects


class PostDetailAPIView(PostBasedAPIVIew):
    """
    Retrieve a post instance.
    """
    permission_classes = (permissions.AllowAny, )
    def get(self, _request, post_slug):
        post = self.get_post(post_slug)
        action_summary = self.get_summary(post)
        post_serializer = PostSerializer(post)
        action_summary_serializer = ActionSummarySerializer(action_summary)

        res = {}
        res.update(post_serializer.data)
        res.update(action_summary_serializer.data)

        return Response(res)

    def put(self, request, post_slug):
        content = request.data.get('content')

        post = self.get_object(post_slug)
        serializer = PostSerializer(post, data={'content': content}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikePostAPIView(PostBasedAPIVIew):
    """
    Like post view
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request, post_slug):
        post = self.get_post(post_slug)

        like = Like(post=post)
        # Save author if provide
        if request.user.is_authenticated:
            like.author = request.user
        like.save()

        increment = 1

        try:
            increment_in_request = request.data['increment']
            if isinstance(increment_in_request, int):
                increment = increment_in_request
            elif increment_in_request is not None and increment_in_request.isnumeric():
                increment = int(increment_in_request)
        except KeyError:
            # Key is not present
            pass

        summary = self.get_summary(post)
        summary.like_count = summary.like_count + increment
        summary.save()

        like_serializer = LikeSerializer(like)
        res = {
            'likes': summary.like_count,
            'detail': like_serializer.data
        }
        return Response(res)


class CommentAPIView(PostBasedAPIVIew):
    """
    Comment API VIew
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, post_slug):
        post = self.get_post(post_slug)

        form = CommentForm(request.POST or None)

        if not form.is_valid():
            return Response({
                'status': '-1',
                'reason': form.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        content_data = form.cleaned_data.get('content')

        comment = Comment(
            post=post,
            author=request.user,
            content=content_data,
        )
        comment.save()

        summary = self.get_summary(post)
        summary.comment_count = summary.comment_count + 1
        summary.save()

        comment_serializer = CommentSerializer(comment)
        res = {
            'comments': summary.comment_count,
            'detail': comment_serializer.data
        }
        return Response(res)
