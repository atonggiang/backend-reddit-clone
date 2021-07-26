from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

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
    username = models.CharField(verbose_name='User Name', max_length=10000, default='Nguyen Van A', unique=True)
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
    email = models.EmailField(verbose_name='Email Address',max_length=10000, blank=True)
    name = models.CharField(verbose_name='Your Name', max_length=10000, blank=True)
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
    age = models.PositiveSmallIntegerField(verbose_name='Age', blank=True, null=True)
    media = models.TextField(verbose_name='Media', blank=True)
    objects = ProfileManager()
    def __str__(self):
        return self.user.username
    class Meta:
        db_table = "profile"

class Sub(models.Model):
    mods = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subs_mod')
    name = models.CharField(verbose_name='Sub Name', max_length=10000, unique=True, blank=False, null=False)
    description = models.CharField(verbose_name='Description', max_length=10000, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subs_join', blank=True, null=True)
    media = models.TextField(verbose_name='Media', blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "sub"
    def get_absolute_url(self):
        return "s/%s/" % self.name
    def info(self, user, posts):
        data = {
            "id":self.id,
            "sub_name":self.name, 
            "description":self.description,
            "media":self.media,
            "members": self.members.count(),
            "join_status":self.get_user_join_status(user),
            "url":self.get_absolute_url(),
            "posts": posts
        }
        return data
    def get_user_join_status(self, user):
        try:
            self.members.get(username=user.username)
            return 'joined'
        except:
            return 'not joined'

from vote.models import VoteModel
class Post(VoteModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=10000, blank=False, null=False)
    media = models.TextField(verbose_name='Media', blank=True)
    content = models.CharField(verbose_name='Content Post', max_length=10000, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = "post"
    def get_absolute_url(self):
        return "localhost:8000/p/%i/" % self.id
    def info(self, user, comments):
        data = {
            "id":self.id,
            "post_author":self.user.username,
            "title":self.title, 
            "media":self.media,
            "content":self.content,
            "vote_status":self.get_user_vote_status(user),
            "total_vote_count": self.votes.count(),
            "upvote_count": self.votes.count(0),
            "downvote_count": self.votes.count(1),
            "total_comment":self.comment_set.count(),
            "url":self.get_absolute_url(),
            "comments": comments,
        }
        return data
    def get_user_vote_status(self, user):
        if self.votes.exists(user.id):
                return 'up'
        else:
            if self.votes.exists(user.id, 1) == True:
                return 'down'
            return 'none'

from mptt.models import MPTTModel, TreeForeignKey
class Comment(MPTTModel,VoteModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(verbose_name='Content Comment', max_length=10000, blank=True)
    media = models.TextField(verbose_name='Media', blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    def __str__(self):
        return self.content
    class Meta:
        db_table = "comment"
    def get_absolute_url(self):
        return "c/%i/" % self.id
    def info(self, user):
        data = {
            "id":self.id,
            "comment_author": self.user.username,
            "media":self.media,
            "content": self.content,
            "status":self.get_user_vote_status(user),
            "total_vote_count": self.votes.count(),
            "upvote_count": self.votes.count(0),
            "downvote_count": self.votes.count(1),
            "url": self.get_absolute_url(),
            "children_comment":self.children_info(user)
            }
        if data["children_comment"] == []:
            data.pop('children_comment')
        return data
    def children_info(self, user):
        children = self.children.all()
        children_data = []
        for child in children:
            children_data.append(child.info(user))
        return children_data

    def get_user_vote_status(self, user):
        if self.votes.exists(user.id):
                return 'up'
        else:
            if self.votes.exists(user.id, 1) == True:
                return 'down'
            return 'none'