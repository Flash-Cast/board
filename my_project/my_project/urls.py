from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from board_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board_app/', include('board_app.urls', namespace='board_app')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # これにより、ログイン、ログアウトなどのURLが登録されます
    path('register/', views.register, name='register'),
    path('', views.thread_list, name='thread_list'),
    path('thread/', views.thread_list, name='thread_list'),
     path('terms_of_service/', views.terms_of_service, name='terms_of_service')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)