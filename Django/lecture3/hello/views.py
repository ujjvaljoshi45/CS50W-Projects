from pickletools import read_uint1
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def ujjval(request):
    return HttpResponse("Hello,Ujjval!")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name":name.capitalize()
    })