from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def post_list(request):
  posts = Post.published.all()
  return render(request, 'post/list.html', {'posts': posts})

def post_detail(request, year, month, day, slug):
  post = get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month, publish__day=day)
  return render(request, 'post/detail.html', {
    'post': post,
  })
