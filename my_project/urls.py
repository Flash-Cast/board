from django.contrib import admin
from django.urls import path, include   # Add


urlpatterns = [
    path('board_app/', include('board_app.urls')),   # Add
    path('admin/', admin.site.urls),
]
