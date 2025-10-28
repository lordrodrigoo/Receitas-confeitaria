from django.shortcuts import render

# Create your views here.

app_name = 'recipes'


def home(request):
    return render(request, 'recipes/pages/home.html')