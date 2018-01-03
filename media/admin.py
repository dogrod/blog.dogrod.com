from django.contrib import admin
from .models import UpyunMedia


# Register your models here.
class UpyunMediaAdmin(admin.ModelAdmin):
    change_list_template = 'admin/media_list.html'
    search_fields = ('name', 'url')
    fields = ('name', 'url')
    list_display = ('name', 'url', 'create_at')
    actions_on_top = False


admin.site.register(UpyunMedia, UpyunMediaAdmin)
