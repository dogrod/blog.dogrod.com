from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
  object_list = Post.published.all()
  paginator = Paginator(object_list, 3) # 3 posts in each page

  page = request.GET.get('page')

  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer deliver the first page
    # such as undefined or character
    posts = paginator.page(1)
  except EmptyPage:
    # If page is out of range deliver last page of results
    posts = paginator.page(paginator.num_pages)

  return render(request, 'post/list.html', {
    'page': page,
    'posts': posts
  })

def post_detail(request, year, month, day, slug):
  post = get_object_or_404(Post, slug=slug, status='published', publish_at__year=year, publish_at__month=month, publish_at__day=day)
  return render(request, 'post/detail.html', {
    'post': post,
  })

class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 3
  template_name = 'post/list.html'
