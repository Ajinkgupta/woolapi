from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scraping_app.urls')),  # Include your app's URL patterns here
]
