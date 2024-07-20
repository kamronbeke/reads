from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from books.models import BookReview
from users.models import CustomUser


def landing_page(request):
    # return HttpResponse(f"Django ishlayapti{request.META['HTTP_USER_AGENT']}")

    return render(request, template_name='landingpage.html')

def homeview(request):
    all_users = CustomUser.objects.all()
    req_user = list(filter(lambda user: request.user.is_following(user), [user for user in all_users]))
    comments = BookReview.objects.filter(user__in=req_user)


    page_size = request.GET.get('page_size', 2)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, page_size)
    page_obj = paginator.get_page(page)
    context = {
        'comments': comments,
        'page_obj': page_obj,
    }

    return render(request, template_name='home.html', context=context)
