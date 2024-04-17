from django.contrib import admin
from .models import *
# Register your models here.

class Profile_info(admin.ModelAdmin):
    list_display = ['user']
    list_display_links = ['user']

admin.site.register(Profile , Profile_info)