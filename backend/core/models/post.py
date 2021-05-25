from django.db import models
from django.conf import settings
from . import Sub
from vote.models import VoteModel

class Post(VoteModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=255, blank=False, null=False)
    content = models.CharField(verbose_name='Content Post', max_length=255, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = "post"
    def get_absolute_url(self):
        return "localhost:8000/p/%i/" % self.id
