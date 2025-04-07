from django.urls import path
from django.contrib.auth import views as auth_views
from board_app import views  # views 全体をインポート

print("board_app URLs loaded")  # デバッグ用（デプロイ時は削除）

app_name = 'board_app'  # 名前空間の設定（タプルにしない）

urlpatterns = [  
    path('', views.thread_list, name='thread_list'),  # スレッド一覧（トップページ）
    path('create/', views.create_thread, name='create_thread'),  # スレッド作成
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),  # スレッド詳細
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms_of_service, name='terms_of_service'),  # 利用規約
    
    # プロフィール関連
    path('profile/', views.profile, name='profile'),  
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # 投稿・スレッド管理
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),

    # 管理者用機能
    path('ban_user/<int:user_id>/', views.ban_user, name='ban_user'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  

    # 通報機能
    path('report/<int:post_id>/', views.report_post, name='report_post'),
]