from django.urls import path
from . import views

urlpatterns = [
    # Maps to the fetch_and_store_data function in views.py
    path('fetch-data/', views.fetch_and_store_data, name='fetch_data'),
    
    # Maps to the display_data function in views.py
    path('display-data/', views.display_data, name='display_data'),
]
