from django.urls import path
from .views import client_table, client_menu, request_service

urlpatterns = [
    path('table/<slug:slug>/', client_table, name='client_table'),
    path('menu/<slug:slug>/', client_menu, name='client_menu'),
    path('request-service/<slug:slug>/', request_service,
         name='request_service')
]
