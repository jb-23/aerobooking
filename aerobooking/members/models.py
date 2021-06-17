from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MemberManager(BaseUserManager):
    def create_user(self, username, password):
        user = Member.objects.create(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.save()
        return user


class Member(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    last_login = None
    USERNAME_FIELD = 'username'

    objects = MemberManager()
