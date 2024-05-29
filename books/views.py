from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator

from books.models import Book



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
        book = Book.objects.get(pk=book_id)

        context = {'book': book}
        return render(request, 'books/detail.html', context)

