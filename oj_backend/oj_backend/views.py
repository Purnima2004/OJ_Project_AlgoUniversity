from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Online Judge Home Page!")
