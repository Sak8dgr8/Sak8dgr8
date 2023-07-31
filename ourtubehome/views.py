from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    username = request.user.username
    context = {'username':username}
    return render(request, "index.html", context)

def loda(request):
    
    return render(request, "how-it-works.html", {'username':request.user.username})


