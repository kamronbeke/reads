from django.http import HttpResponse
from django.shortcuts import render


def landing_page(request):
    # return HttpResponse(f"Django ishlayapti{request.META['HTTP_USER_AGENT']}")

    return render(request, template_name='landingpage.html')