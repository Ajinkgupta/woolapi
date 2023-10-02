from django.urls import path
from . import views

urlpatterns = [
    path('data.json', views.scrape_data, name='scrape_data'),
]
