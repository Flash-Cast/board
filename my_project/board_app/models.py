from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField('スレッドタイトル', max_length=100)
    content = models.TextField(default="No content")
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField(default="No content")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)  # ゲスト投稿者名として使うならOK

    def __str__(self):
        return f"Post by {self.author if self.author else self.name} on {self.created_at}"

class Report(models.Model):
    reported_post = models.ForeignKey('Post', on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(default="No content")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by} on {self.created_at}"

class Notice(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField(default="No content")  
    created_at = models.DateTimeField(auto_now_add=True)  # 統一のため修正

    def __str__(self):
        return self.title
    
class UserNoticeStatus(models.Model):
    """ユーザーごとのお知らせの既読状態を管理するモデル"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        # userとnoticeの組み合わせで重複したデータが作られないようにする設定
        unique_together = ('user', 'notice')

    def __str__(self):
        return f"{self.user.username} - {self.notice.title} ({'既読' if self.is_read else '未読'})"


class Todo(models.Model):
    """サイト全体で共有するTodo（予定）を管理するモデル"""

    GRADE_CHOICES = [
        (1, '1年'),(2, '2年'),(3, '3年'),(4, '4年'),
    ]

    title = models.CharField(max_length=200, verbose_name="タスク名")
    due_date = models.DateField(verbose_name="締切日") 
    grade = models.IntegerField(choices=GRADE_CHOICES, verbose_name="学年")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    class Meta:
        ordering = ['due_date'] # 締切日が近い順に並べる

    def __str__(self):
        return self.title