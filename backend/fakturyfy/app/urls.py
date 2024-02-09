from django.urls import path
from fakturyfy.app import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'entity', views.EntityViewSet, basename='entity')

urlpatterns = [
    path('invoice/new', views.NewInvoice.as_view(), name='new_invoice'),
    path('invoice/list/<int:provider>/<int:client>', views.ListInvoices.as_view(), name='list_invoices')
] + router.urls