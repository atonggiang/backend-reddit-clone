from django.db import models
from django.conf import settings

class Sub(models.Model):
    mods = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(verbose_name='Sub Name', max_length=255, unique=True, blank=False, null=False)
    description = models.CharField(verbose_name='Description', max_length=255, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "sub"