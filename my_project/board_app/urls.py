from django.urls import path
from board_app import views
from django.contrib.auth import views as auth_views
from board_app.views import ban_user
from .views import report_post
# URL のロードを確認
print("board_app URLs loaded")

app_name = 'board_app'  # 名前空間の設定

urlpatterns = [
    path('post/', views.read_post, name='read_post'),  # 投稿一覧
    path('post/create/', views.create_post, name='create_post'),  # 投稿作成
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),  # 投稿編集
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),  # 投稿削除
    path('create/', views.create_thread, name='create_thread'),  # スレッド作成
    path('', views.thread_list, name='thread_list'),  # スレッド一覧（トップページ）
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),  # スレッド詳細
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('ban_user/<int:user_id>/', ban_user, name='ban_user'),
    path('report/<int:post_id>/', views.report_post, name='report_post'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile, name='profile'),  # プロフィールページ
    path('profile/edit/', views.profile_edit, name='profile_edit'), 
]
