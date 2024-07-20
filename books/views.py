from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse

from users.models import CustomUser
from .forms import CommentForm, EditCommentForm, AddBookForm, AddAuthorForm
from .models import Book, BookReview, Author, BookAuthor
from django.views.generic import View, UpdateView, DeleteView
from django.core.paginator import Paginator
from books.models import Book
from django.shortcuts import render, redirect
from django.http import JsonResponse



class BookListView(View):
    def get(self, request):
        books = Book.objects.all()

        search_query = request.GET.get('q')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        context = {"page_obj": page_obj,}
        return render(request, 'books/list.html', context)

class BookDetailView(View):
    def get(self, request, book_id):
        forms = CommentForm()
        book = Book.objects.get(pk=book_id)
        comments = BookReview.objects.filter(book=book_id)
        print(comments)
        context = {'book': book,
                   'comments': comments,
                   'form': forms
                   }
        return render(request, 'books/detail.html', context=context)

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        user = request.user
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = BookReview.objects.create(
                user=user,
                book=book,
                comment=form.cleaned_data['comment'],
                stars = form.cleaned_data['stars']
            )
            comment.save()
            return redirect('books:detail', book.id)
        return render(request, 'books/detail.html', {'form':form})

class EditReviewView(View):
    def get(self, request, book_id, review_id):
        comment = get_object_or_404(BookReview, id=review_id)
        book = comment.book
        comments = BookReview.objects.filter(book=book).exclude(id=review_id)

        if comment.user != request.user:
            messages.error(request, "You do not have permission to edit this review.")
            return redirect(reverse('books:detail', kwargs={'book_id': book_id}))

        comment_form = CommentForm(instance=comment)
        return render(request, 'pages/update.html', {'form': comment_form, 'book': book, 'comments': comments})

    def post(self, request, book_id, review_id):
        comment = get_object_or_404(BookReview, id=review_id)

        # Check if the user is authorized to edit the comment
        if comment.user != request.user:
            messages.error(request, "You do not have permission to edit this review.")
            return redirect(reverse('books:detail', kwargs={'book_id': book_id}))

        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, "Review updated successfully.")
            return redirect(reverse('books:detail', kwargs={'book_id': book_id}))
        else:
            messages.error(request, "Please correct the error below.")

        return render(request, 'pages/update.html', {'form': comment_form})


class DeleteRewiewView(View):
    def get(self, request, book_id, review_id):
        review = BookReview.objects.filter(id=review_id)
        review.delete()
        return render(request, 'pages/delete.html',)
class AddBookView( View):
    def get(self, request):
        form = AddBookForm()
        return render(request, 'books/add_book.html', {'form': form})

    def post(self, request):
        book_form = AddBookForm(data = request.POST, files=request.FILES)
        if book_form.is_valid():
            book = book_form.save()
            book.save()
            return redirect('books:list')
        return render(request, 'books/add_book.html', {'form':book_form})




class AddBookAuthorView(View):
    def get(self, request):
        form = AddAuthorForm()

        return render(request, 'books/add_author.html', {'form':form})
    def post(self, request):
        form = AddAuthorForm(data = request.POST, files = request.FILES)
        if form.is_valid():
            author = form.save()
            author.save()
            return redirect('books:list')

        return render(request, 'books/add_author.html', {'form':form})

class BookAuthorDetailView(View):

    def get(self, request, author_id):
        author = Author.objects.get(id=author_id)
        book = BookAuthor.objects.filter(author=author)
        print(book)
        context = {
            'author': author,
            'books': book
        }
        return render(request, 'books/book_author_detail.html', context)