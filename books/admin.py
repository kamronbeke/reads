from django.contrib import admin

from .models import BookModel, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn']
    search_fields = ['title', 'isbn']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'email', 'bio']

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['stars', 'book', 'users']
    list_filter = ['users', 'stars']

class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['book','author']
    list_filter = ['author']


admin.site.register(BookModel, BookAdmin),
admin.site.register(Author),
admin.site.register(BookAuthor),
admin.site.register(BookReview),