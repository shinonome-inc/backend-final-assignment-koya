from django.contrib import admin

from .models import Friendship, User

admin.site.register(User)
admin.site.register(Friendship)
