from django.contrib import admin
from .models import Profile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'nick_name', 'bio', 'location', 'age')
    list_filter = ('location', 'age')


admin.site.register(Profile, UserProfileAdmin)
