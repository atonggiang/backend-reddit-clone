from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager

class ProfileManager(BaseUserManager):
    def create_profile(self, user, **kwargs):
        profile = self.model(user=user, **kwargs)
        profile.save(using=self.db) 
        return profile

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    email = models.EmailField(verbose_name='Email Address',max_length=254, blank=True)
    name = models.CharField(verbose_name='Your Name', max_length=254, blank=True)
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICE = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER_CHOICE,
        blank=True
    )
    age = models.PositiveSmallIntegerField(verbose_name='Age', blank=True, null=False)
    object = ProfileManager()
    def __str__(self):
        return self.user.username
    class Meta:
        db_table = "profile"