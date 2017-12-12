from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Custom QuerySet manager
class PublishedManager(models.Manager):
  def get_queryset(self):
    return super(PublishedManager, self).get_queryset()\
                                        .filter(status='published')
# Create your models here.
class Post(models.Model):
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
  )

  title = models.CharField(max_length = 100)
  slug = models.SlugField(max_length = 100)
  author = models.ForeignKey(User, related_name = 'blog_posts')
  body = models.TextField()
  publish = models.DateTimeField(default = timezone.now)
  created = models.DateTimeField(auto_now_add = True)
  updated = models.DateTimeField(auto_now = True)
  status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')

  class Meta:
    ordering = ('-publish',)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('post:post_detail',
      args=[
        self.publish.year,
        self.publish.strftime('%m'),
        self.publish.strftime('%d'),
        self.slug
      ]
    )

  objects = models.Manager() # default QS manager
  published = PublishedManager() # custom QS manager
