from django.urls import path
from .views import EntityListView

urlpatterns = [
    path('entity', EntityListView.as_view(), name='entity-list'),
]