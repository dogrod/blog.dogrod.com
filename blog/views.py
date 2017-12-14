from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_detail(request, year, month, day, slug):
  post = get_object_or_404(Post, slug=slug, status='published', publish_at__year=year, publish_at__month=month, publish_at__day=day)
  
  # List of active comments for this post
  comments = post.comments.filter(active = True)

  if request.method == 'POST':
    # A comment was posted
    comment_form = CommentForm(data = request.POST)

    if comment_form.is_valid():
      # Create Comment object but don't save to database yet
      new_comment = comment_form.save(commit = False)
      # Assign the current post to the comment
      new_comment.post = post
      # Save the comment to the database
      new_comment.save()
  
  else:
    comment_form = CommentForm()

  return render(request, 'post/detail.html', {
    'post': post,
    'comments': comments,
    'comment_form': comment_form
  })

class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 3
  template_name = 'post/list.html'
