from django.contrib import admin
from .models import Thread, Post, Report, Notice, Category, Todo, UserNoticeStatus

# スレッド管理
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')  # 一覧表示の項目
    search_fields = ('title', 'author__username')  # 検索機能
    list_filter = ('created_at', 'author')  # フィルタ機能
    ordering = ('-created_at',)  # 最新のスレッドを上に表示
    readonly_fields = ('created_at',)  # 作成日時は変更不可

# 投稿管理
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'author', 'thread')
    list_display_links = ('created_at',)  # content 以外のフィールドをリンクにする
    search_fields = ('content', 'author__username')
    list_filter = ('created_at', 'author', 'thread')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    list_editable = ('content',)  


# お知らせ管理
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

# 通報管理
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported_post', 'reported_by', 'created_at')  
    list_filter = ('created_at', 'reported_by')  
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    # 一覧ページに表示する項目を指定
    list_display = ('title', 'due_date', 'grade')
    # 管理画面の右側に出てくる絞り込み（フィルタ）項目を指定
    list_filter = ('grade', 'due_date')
    # 検索ボックスで検索できる項目を指定
    search_fields = ('title',)

# 管理画面に登録
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Category)
admin.site.register(UserNoticeStatus)
