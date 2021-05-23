from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_superuser, **kwargs):
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, username=None, password=None, **kwargs):
        return self._create_user(username, password, False, False, **kwargs)
    def create_superuser(self, username, password, **kwargs):
        return self._create_user(username, password, True, True, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='User Name', max_length=255, default='Nguyen Van A', unique=True)
    USERNAME_FIELD = 'username'
    is_active = models.BooleanField(verbose_name='Is Active', default=True)
    is_staff = models.BooleanField(verbose_name='Is Staff', default=False)
    is_superuser = models.BooleanField(verbose_name='Is Superuser', default=False)
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.username
    class Meta:
        db_table = "user"