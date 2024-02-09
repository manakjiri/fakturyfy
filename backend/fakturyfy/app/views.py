from django.shortcuts import render

def index(request, page="index"):
    # TODO add 404 to non-existing pages
    return render(request, "index.html")

