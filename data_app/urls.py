from django.urls import path
from . import views

urlpatterns = [
    # This path maps to the 'fetch_and_store_data' function
    path('fetch-data/', views.fetch_and_store_data, name='fetch_data'),
    # This new path maps to the 'display_data' function
    path('display-data/', views.display_data, name='display_data'),
]
