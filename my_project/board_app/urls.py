from django.urls import path
from board_app import views
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
]
