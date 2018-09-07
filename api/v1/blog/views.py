from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, views, status, viewsets
from rest_framework.response import Response

from taggit.models import Tag
from blog.models import Post, ActionSummary, Like, Comment
from .serializers import PostListSerializer, PostSerializer, TagSerializer, ActionSummarySerializer, LikeSerializer, CommentSerializer
from .forms import CommentForm


class TagsView(views.APIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, format=None):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)

        return Response({'tags': serializer.data})


class PostViewSet(viewsets.ModelViewSet):
    """
    View set of Post
    """
    queryset = Post.published.all()
    serializer_class = PostSerializer
    list_serializer_class = PostListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'list':
            if hasattr(self, 'list_serializer_class'):
                return self.list_serializer_class

        return super(PostViewSet, self).get_serializer_class()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        tag = None
        tag_in_query = request.query_params.get('tag')

        # If there's 'tag' in request query, filter post list before response.
        if tag_in_query:
            tag = get_object_or_404(Tag, id=tag_in_query)
            queryset = queryset.filter(tags__in=[tag])

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = serializer.data

            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, post_id):
        queryset = Post.published.all()
        post = get_object_or_404(queryset, id=post_id)

        action_summary, created = ActionSummary.objects.get_or_create(post=post)
        post_serializer = PostSerializer(post)
        action_summary_serializer = ActionSummarySerializer(action_summary)

        res = {}
        res.update(post_serializer.data)
        res.update(action_summary_serializer.data)

        return Response(res)


class PostBasedAPIVIew(views.APIView):
    """
    Basic API View of post to provide some method based on Post
    """
    def get_post(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404

    def get_summary(self, post):
        objects, created = ActionSummary.objects.get_or_create(post=post)
        return objects


class LikePostAPIView(PostBasedAPIVIew):
    """
    Like post view
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request, post_id):
        post = self.get_post(post_id)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, _request, post_id):
        post = self.get_post(post_id)

        queryset = Comment.objects.filter(post=post, approved=True)
        serializer = CommentSerializer(queryset, many=True)

        return Response({'list': serializer.data})

    def post(self, request, post_id):
        post = self.get_post(post_id)

        form = CommentForm(request.data or None)

        if not form.is_valid():
            return Response({
                'success': False,
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
