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
  publish_at = models.DateTimeField(default = timezone.now)
  create_at = models.DateTimeField(auto_now_add = True)
  update_at = models.DateTimeField(auto_now = True)
  status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')

  class Meta:
    ordering = ('-publish_at',)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('post:post_detail',
      args=[
        self.publish_at.year,
        self.publish_at.strftime('%m'),
        self.publish_at.strftime('%d'),
        self.slug
      ]
    )

  def get_publish_date(self):
    return self.publish_at.date()

  objects = models.Manager() # default QS manager
  published = PublishedManager() # custom QS manager
