from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse("Hello, world. This is your first view in fakemoneyd.")
