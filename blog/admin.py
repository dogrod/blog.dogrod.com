from django.contrib import admin
from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Post, Comment

# Register your models here.
class PostForm(forms.ModelForm):
  content = forms.CharField(widget = AdminPagedownWidget())

  class Meta:
    model = Post
    fields = '__all__'

class PostAdmin(admin.ModelAdmin):
  form = PostForm
  # config which item can show in the list
  list_display = ('title', 'slug', 'author', 'publish_at', 'status')
  # filter config
  list_filter = ('status', 'create_at', 'publish_at', 'author')
  # search config
  search_fields = ('title', 'content')
  # Set prepopulated_fields to a dictionary mapping field names to the fields it should prepopulate from
  # 改变 title 时 slug 将会跟随改变
  prepopulated_fields = {'slug': ('title',)}
  raw_id_fields = ('author',)
  # Set date_hierarchy to the name of a DateField or DateTimeField in your model, 
  # and the change list page will include a date-based drilldown navigation by that field.
  date_hierarchy = 'publish_at'
  ordering = ['status', 'publish_at']

class CommentAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'post', 'create_at', 'active')
  list_filter = ('active', 'create_at', 'update_at')
  search_fields = ('name', 'email', 'content')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
