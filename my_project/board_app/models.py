from django.db import models


class Thread(models.Model):
    title = models.CharField('スレッドタイトル', max_length=100)
    content = models.TextField(default="No content") 
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    name = models.CharField('user name', max_length=15, default="Unnamed")
    micropost = models.CharField('tweet', max_length=140, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    thread = thread = models.ForeignKey('Thread', null=True, blank=True, related_name='posts', on_delete=models.CASCADE)
  
    def __str__(self):
        return self.name
