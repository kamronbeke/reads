from django.contrib import admin
from django.shortcuts import render
from django.views import View

from users.models import Follow, CustomUser
from users.views import UserListView


# from users.views import UserListView


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to', 'created')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')

