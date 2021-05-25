from django.db import models
from django.conf import settings
from . import Post
from vote.models import VoteModel

class Comment(VoteModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(verbose_name='Content Comment', max_length=255, blank=True)
    def __str__(self):
        return self.content
    class Meta:
        db_table = "comment"