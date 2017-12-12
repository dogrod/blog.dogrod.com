from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
  # config which item can show in the list
  list_display = ('title', 'slug', 'author', 'publish', 'status')
  # filter config
  list_filter = ('status', 'created', 'publish', 'author')
  # search config
  search_fields = ('title', 'body')
  # Set prepopulated_fields to a dictionary mapping field names to the fields it should prepopulate from
  # 改变 title 时 slug 将会跟随改变
  prepopulated_fields = {'slug': ('title',)}
  raw_id_fields = ('author',)
  # Set date_hierarchy to the name of a DateField or DateTimeField in your model, 
  # and the change list page will include a date-based drilldown navigation by that field.
  date_hierarchy = 'publish'
  ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)