from .models import Entity
from django.views.generic.list import ListView
#from rest_framework.views import APIView
from django.shortcuts import render


class EntityListView(ListView):
    model = Entity
    

def index(request, page="index"):
    # TODO add 404 to non-existing pages
    return render(request, "index.html")

