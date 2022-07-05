from django.urls import path
from .views import client_table

urlpatterns = [
    path('table/<slug:slug>/', client_table, name='client_table'),
]
