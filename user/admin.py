from django.contrib import admin

# Register your models here.

from user.models import User, Log

admin.site.register(User)

admin.site.register(Log)
