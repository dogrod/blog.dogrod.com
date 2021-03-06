from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify as default_slugify
from unidecode import unidecode
from taggit.models import TaggedItemBase

import markdown


# Custom QuerySet manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='published')


class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey('Post')


class Category(models.Model):
    title = models.CharField(max_length=40, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def slugify(self, title, i=None):
        slug = default_slugify(unidecode(title))
        if i is not None:
            slug += '_%d' % i
        return slug


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, allow_unicode=True)
    author = models.ForeignKey(User, related_name='blog_posts')
    content = models.TextField()
    publish_at = models.DateTimeField(default=timezone.now)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager(through=TaggedPost, blank=True)
    category = models.ForeignKey(Category, related_name='posts', blank=True, null=True)
    cover_image = models.CharField(max_length=120, default='http://static.dogrod.com/media/i-am-root.png')

    class Meta:
        ordering = ('-publish_at', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify(self.title)

        super(Post, self).save(*args, **kwargs)

    def slugify(self, title, i=None):
        slug = default_slugify(unidecode(title))
        if i is not None:
            slug += '_%d' % i
        return slug

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    def get_summary(self):
        if len(self.content) > 40:
            return '{0}...'.format(self.content[:40])
        else:
            return self.content

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    def get_formatted_publish_time(self):
        return self.publish_at.strftime('%Y-%m-%dT%H:%M')

    def get_absolute_url(self):
        return reverse(
            'post:post_detail',
            args=[
                self.publish_at.year,
                self.publish_at.strftime('%m'),
                self.publish_at.strftime('%d'), self.slug
            ])

    def get_publish_date(self):
        return self.publish_at.date()

    objects = models.Manager()  # default QS manager
    published = PublishedManager()  # custom QS manager


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    author = models.ForeignKey(
        User, related_name='post_comments', blank=True, null=True)
    content = models.TextField(verbose_name=u'content')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True)
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child_comment',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-create_at', )

    def ban_comment(self):
        self.approved = False
        self.save()

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class Like(models.Model):
    """
    Record of like action
    """
    post = models.ForeignKey(Post, related_name='like')
    author = models.ForeignKey(
        User, related_name='post_like', blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)


class ActionSummary(models.Model):
    """
    Summary of likes & comments
    """
    post = models.ForeignKey(Post, related_name='likes')
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

