from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Entity

admin.site.register(Entity)