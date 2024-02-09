from django.urls import path
from .views import EntityViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'entity', EntityViewSet, basename='entity')

urlpatterns = [
    
] + router.urls