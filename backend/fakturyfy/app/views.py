from .models import Entity
from django.views.generic.list import ListView
#from rest_framework.views import APIView


class EntityListView(ListView):
    model = Entity
    

