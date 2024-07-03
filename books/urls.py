
from django.urls import path
from django.views.generic import UpdateView, DeleteView

from books.views import BookListView, BookDetailView, AddReviewView, DeleteRewiewView, EditReviewView, AddBookView, \
    AddBookAuthorView

app_name = 'books'




urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:book_id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/add-review/', AddReviewView.as_view(), name='add-review'),
    path('add-book/', AddBookView.as_view(), name='add-book'),
    path('<int:book_id>/<int:review_id>/delete/', DeleteRewiewView.as_view(), name='delete_review'),
    path('add-author/', AddBookAuthorView.as_view(), name='add-author'),
    path('<int:book_id>/<int:review_id>/update/', EditReviewView.as_view(), name='edit_page'),


]