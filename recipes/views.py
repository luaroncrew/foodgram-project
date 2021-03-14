from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'recipes/customPage.html', context={'message': 'тут что-то будет'})
