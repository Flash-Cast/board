from django.contrib import admin
from .models import Thread, Post, Report

# スレッド管理
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')  # 一覧表示の項目
    search_fields = ('title', 'author__username')  # 検索機能

# 投稿管理
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'author', 'thread')
    search_fields = ('content', 'author__username')

# 管理画面に登録
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported_post', 'reported_by', 'created_at')  # 管理画面の表示項目

