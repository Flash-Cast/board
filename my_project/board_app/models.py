from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    title = models.CharField('スレッドタイトル', max_length=100)
    content = models.TextField(default="No content") 
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField(default="No content")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Post by {self.author} on {self.created_at}"
    
class Report(models.Model):
    reported_post = models.ForeignKey('Post', on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(default="No content")
    created_at = models.DateTimeField(auto_now_add=True)