from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from django.utils import dateformat

# Create your models here.
class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='author')
    user_output = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кому', related_name='user_output')
    message = models.CharField(max_length=300, verbose_name='Сообщение')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

class PostModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    formatted_date = dateformat.format(datetime.now(), settings.DATE_FORMAT)

    class Meta:
        ordering = ('-date_created',)

    def comment_count(self):
        return self.comment_set.all().count()

    def comments(self):
        return self.comment_set.all()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content


