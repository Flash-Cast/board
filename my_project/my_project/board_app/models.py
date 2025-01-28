from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField('user name', max_length=15,default="Unnamed")
    micropost = models.CharField('tweet', max_length=140, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    def __str__(self):
        return self.name

