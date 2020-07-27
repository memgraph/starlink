from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. This is where the Starlink simulator will be.")