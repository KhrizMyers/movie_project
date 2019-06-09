from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def single(request):
    return render(request, 'single.html')


def horror(request):
    return render(request, 'horror.html')


def genres(request):
    return render(request, 'genres.html')


def list_view(request):
    return render(request, 'list.html')


def comedy(request):
    return render(request, 'comedy.html')
