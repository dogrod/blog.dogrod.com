from django.contrib import admin
from .models import Media

# Register your models here.
class MediaAdmin(admin.ModelAdmin):
  list_display=('description', 'image', 'created')
  list_filter=('created',)
  search_fields=('description',)
  ordering=('created',)

admin.site.register(Media, MediaAdmin)