from .models import Entity
from django.views.generic.list import ListView
from rest_framework.views import APIView
from django.shortcuts import render
from .serializers import EntitySerializer
from rest_framework import permissions, viewsets


def index(request, page="index"):
    # TODO add 404 to non-existing pages
    return render(request, "index.html")

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [permissions.IsAuthenticated]

